"""Read-only name resolution probe of the role osism.validations.name_resolution.

The first argument is the command (sources, nameservers or lookup). The input
is one JSON object on stdin, the output one JSON object on stdout. Invalid
input prints one line to stderr and exits with 2. The probe uses the standard
library only and runs on Python 3.9 and later.
"""

import configparser
import glob
import ipaddress
import json
import random
import re
import socket
import struct
import sys
import time
import urllib.parse

ATTEMPTS = 2
FAMILIES = {"ipv4": socket.AF_INET, "ipv6": socket.AF_INET6, "any": socket.AF_UNSPEC}
RCODES = {
    0: "NOERROR",
    1: "FORMERR",
    2: "SERVFAIL",
    3: "NXDOMAIN",
    4: "NOTIMP",
    5: "REFUSED",
}
SCHEMES = ("http", "https", "ftp")
TRUE_VALUES = ("1", "yes", "true", "on")

APT_ONE_LINE_FILES = ["/etc/apt/sources.list"]
APT_ONE_LINE_GLOB = "/etc/apt/sources.list.d/*.list"
APT_DEB822_GLOB = "/etc/apt/sources.list.d/*.sources"
DNF_GLOB = "/etc/yum.repos.d/*.repo"


class InputError(Exception):
    pass


def one_line(exc):
    return " ".join(str(exc).split())


def seconds(value):
    return "%g" % value


def read_text(path, skipped):
    """Return the content of path, None for a missing file, and record any other error."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as exc:
        skipped.append("%s: %s" % (path, one_line(exc)))
        return None


def apt_one_line_uris(text):
    for line in text.splitlines():
        tokens = line.split("#", 1)[0].split()
        if not tokens or tokens[0] not in ("deb", "deb-src"):
            continue
        index = 1
        if index < len(tokens) and tokens[index].startswith("["):
            while index < len(tokens) and not tokens[index].endswith("]"):
                index += 1
            index += 1
        if index < len(tokens):
            yield tokens[index]


def deb822_stanzas(text):
    stanza, key = {}, None
    for line in text.splitlines() + [""]:
        if line.startswith("#"):
            continue
        if not line.strip():
            if stanza:
                yield stanza
            stanza, key = {}, None
        elif line[0] in " \t":
            if key is not None:
                stanza[key] += " " + line.strip()
        else:
            name, separator, value = line.partition(":")
            if separator:
                key = name.strip().lower()
                stanza[key] = value.strip()


def deb822_uris(text):
    for stanza in deb822_stanzas(text):
        if stanza.get("enabled", "yes").strip().lower() == "no":
            continue
        yield from stanza.get("uris", "").split()


def dnf_uris(path, skipped):
    parser = configparser.ConfigParser(interpolation=None, strict=False)
    try:
        with open(path, encoding="utf-8") as handle:
            parser.read_file(handle)
    except FileNotFoundError:
        return []
    except (OSError, UnicodeDecodeError, configparser.Error) as exc:
        skipped.append("%s: %s" % (path, one_line(exc)))
        return []
    uris = []
    for section in parser.sections():
        if (
            parser.get(section, "enabled", fallback="1").strip().lower()
            not in TRUE_VALUES
        ):
            continue
        uris.extend(re.split(r"[\s,]+", parser.get(section, "baseurl", fallback="")))
        uris.append(parser.get(section, "mirrorlist", fallback=""))
        uris.append(parser.get(section, "metalink", fallback=""))
    return [uri for uri in uris if uri]


def uri_host(uri, skipped):
    try:
        parts = urllib.parse.urlsplit(uri)
        host = parts.hostname
    except ValueError as exc:
        skipped.append("%s: %s" % (uri, one_line(exc)))
        return None
    if parts.scheme.split("+")[-1] not in SCHEMES or not host:
        return None
    if "$" in host:
        skipped.append("%s: hostname contains an unexpanded variable" % uri)
        return None
    return host.lower()


def cmd_sources(data):
    skipped = []
    uris = []
    for path in APT_ONE_LINE_FILES + sorted(glob.glob(APT_ONE_LINE_GLOB)):
        text = read_text(path, skipped)
        if text is not None:
            uris.extend(apt_one_line_uris(text))
    for path in sorted(glob.glob(APT_DEB822_GLOB)):
        text = read_text(path, skipped)
        if text is not None:
            uris.extend(deb822_uris(text))
    for path in sorted(glob.glob(DNF_GLOB)):
        uris.extend(dnf_uris(path, skipped))
    hosts = set()
    for uri in uris:
        host = uri_host(uri, skipped)
        if host:
            hosts.add(host)
    return {"hosts": sorted(hosts), "skipped": skipped}


def parse_nameserver(entry):
    """Split an entry in the DNS= syntax of resolved.conf(5) into address, port and interface."""
    value, _, interface = entry.split("#", 1)[0].partition("%")
    port = 53
    if value.startswith("["):
        host, separator, rest = value[1:].partition("]")
        if not separator or (rest and not rest.startswith(":")):
            raise ValueError(entry)
        if rest:
            port = int(rest[1:])
    elif value.count(":") == 1:
        host, _, port_text = value.partition(":")
        port = int(port_text)
    else:
        host = value
    if not 0 < port < 65536:
        raise ValueError(entry)
    return str(ipaddress.ip_address(host)), port, interface


def encode_name(name):
    labels = name.rstrip(".").split(".")
    if len(name.rstrip(".")) > 253:
        raise InputError("invalid query name: %s" % name)
    encoded = b""
    for label in labels:
        try:
            raw = label.encode("idna")
        except UnicodeError:
            raise InputError("invalid query name: %s" % name)
        if not raw or len(raw) > 63:
            raise InputError("invalid query name: %s" % name)
        encoded += bytes([len(raw)]) + raw
    return encoded + b"\x00"


def query_nameserver(address, port, interface, qname, timeout):
    family = socket.AF_INET6 if ":" in address else socket.AF_INET
    try:
        # NOTE: A link-local IPv6 address is only reachable through the
        # interface the entry names, so it becomes the scope of the socket.
        if family == socket.AF_INET6 and interface:
            target = (address, port, 0, socket.if_nametoindex(interface))
        else:
            target = (address, port)
        for _ in range(ATTEMPTS):
            query_id = random.getrandbits(16)
            packet = (
                struct.pack("!HHHHHH", query_id, 0x0100, 1, 0, 0, 0)
                + qname
                + struct.pack("!HH", 1, 1)
            )
            with socket.socket(family, socket.SOCK_DGRAM) as sock:
                sock.connect(target)
                sock.send(packet)
                deadline = time.monotonic() + timeout
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        break
                    sock.settimeout(remaining)
                    try:
                        reply = sock.recv(4096)
                    except socket.timeout:
                        break
                    if len(reply) < 12:
                        continue
                    reply_id, flags = struct.unpack("!HH", reply[:4])
                    if reply_id == query_id and flags & 0x8000:
                        code = flags & 0x000F
                        return RCODES.get(code, "RCODE%d" % code), None
    except OSError as exc:
        return None, one_line(exc)
    return None, "no answer after %d attempts of %s seconds" % (
        ATTEMPTS,
        seconds(timeout),
    )


def cmd_nameservers(data):
    servers = data.get("servers", [])
    timeout = float(data.get("timeout", 2))
    qname = encode_name(str(data.get("query", "")))
    results = []
    for entry in servers:
        result = {
            "entry": entry,
            "address": None,
            "port": None,
            "rcode": None,
            "error": None,
        }
        try:
            address, port, interface = parse_nameserver(str(entry))
        except ValueError:
            result["error"] = "invalid nameserver address"
        else:
            result["address"], result["port"] = address, port
            result["rcode"], result["error"] = query_nameserver(
                address, port, interface, qname, timeout
            )
        results.append(result)
    return {"servers": results}


def forward(name, family):
    try:
        infos = socket.getaddrinfo(name, None, FAMILIES[family], socket.SOCK_STREAM)
    except (OSError, UnicodeError) as exc:
        return [], one_line(exc)
    addresses = []
    for info in infos:
        if info[4][0] not in addresses:
            addresses.append(info[4][0])
    return addresses, None


def backward(address):
    try:
        return socket.gethostbyaddr(address)[0], None
    except (OSError, UnicodeError) as exc:
        return None, one_line(exc)


def cmd_lookup(data):
    lookups = data.get("lookups", [])
    addresses = data.get("reverse", [])
    deadline = float(data.get("deadline", 120))
    for item in lookups:
        if not isinstance(item, dict) or item.get("family") not in FAMILIES:
            raise InputError("invalid lookup: %s" % json.dumps(item))
    start = time.monotonic()
    late = "not checked: lookup deadline of %s seconds reached" % seconds(deadline)

    def in_time():
        return time.monotonic() - start < deadline

    forward_cache = {}
    forward_results = []
    for item in lookups:
        key = (str(item.get("name", "")), item["family"])
        if key not in forward_cache:
            forward_cache[key] = forward(*key) if in_time() else ([], late)
        found, error = forward_cache[key]
        forward_results.append(
            {"name": key[0], "family": key[1], "addresses": found, "error": error}
        )
    backward_cache = {}
    backward_results = []
    for address in addresses:
        address = str(address)
        if address not in backward_cache:
            backward_cache[address] = backward(address) if in_time() else (None, late)
        name, error = backward_cache[address]
        backward_results.append({"address": address, "name": name, "error": error})
    return {"lookups": forward_results, "reverse": backward_results}


COMMANDS = {
    "sources": cmd_sources,
    "nameservers": cmd_nameservers,
    "lookup": cmd_lookup,
}


def main(argv):
    try:
        if len(argv) < 2 or argv[1] not in COMMANDS:
            raise InputError(
                "usage: name_resolution_probe.py sources|nameservers|lookup < input.json"
            )
        try:
            data = json.load(sys.stdin)
        except ValueError as exc:
            raise InputError("invalid JSON on stdin: %s" % one_line(exc))
        if not isinstance(data, dict):
            raise InputError("the input on stdin must be a JSON object")
        result = COMMANDS[argv[1]](data)
    except InputError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2
    json.dump(result, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
