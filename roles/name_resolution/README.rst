This role validates that name resolution on a host works the way
osism.commons.resolvconf and osism.commons.hosts set it up, and that the names
the installation depends on resolve. Run it before a deployment or an upgrade.
The role only reads: it installs no package, writes no file and restarts no
service. The lookups run through a small Python script that uses the standard
library only, so no DNS tool has to be installed on the host.

The checks run in the order below and the role stops at the first failed
check. Every failure message starts with the label of the check and lists every
item of that check that fails, for example all nameservers that do not answer:

* ``resolved``: systemd-resolved is active and the resolver configuration lists
  only its stub resolver 127.0.0.53.
* ``nameservers``: each upstream nameserver answers a DNS query on its own,
  with the response code NOERROR, not only the stub resolver in front of them.
* ``hosts``: the name and the short name of every inventory host resolve to the
  IPv4 address osism.commons.hosts assigns to it. When DNS is the single source
  of truth for host names (``hosts_use_dns_as_single_source_of_truth``), DNS
  has to return the same addresses.
* ``reverse``: the address of every inventory host resolves back to its name.
  For a short inventory name, a returned FQDN with the same first label passes.
* ``additional-entries``: every entry of ``hosts_additional_entries`` resolves
  to its configured address.
* ``external``: the container registries and the package repositories the host
  uses resolve. When a proxy is configured, the proxy hosts are checked instead.
* ``endpoints``: the internal and external FQDN of the API endpoints resolve,
  the internal one to the internal VIP address.

A check that has nothing to check, or that is switched off, says so in a
message that starts with its label. Inventory hosts without an address, hosts
named by an IP address, and short names or addresses that several inventory
hosts share are not checked and are listed in such a message.

The selection of the inventory hosts and their addresses follows the template
of osism.commons.hosts that OSISM uses (``hosts_type: template``). It reads
``hosts_group_name``, ``hosts_ignore``, ``hosts_enable``, ``hosts_interface``,
``internal_interface`` and ``hosts_additional_entries`` from the inventory. The
addresses of other hosts come from their facts, so the facts of all hosts have
to be in the fact cache.

The defaults of the resolver settings read the inventory variables of
osism.commons.resolvconf (``enable_resolvconf``, ``resolvconf_file``,
``resolvconf_nameserver``, ``resolvconf_dns_over_tls``) and fall back to the
defaults of that role. The derived external names read the registry variables
of osism/defaults (``docker_registry_ansible``, ``docker_registry_kolla``,
``ceph_docker_registry``) and the proxy of osism.commons.proxy
(``proxy_proxies``, ``proxy_enable``). The endpoints read ``kolla_internal_fqdn``,
``kolla_internal_vip_address`` and ``kolla_external_fqdn``. These defaults have
to follow when one of these roles changes a default.

In an air-gapped installation the registry variables and the package sources
point at the local mirrors, and in a proxied installation the proxy hosts are
checked, so the derived external names need no configuration there. Set
``name_resolution_external_names`` to check other names.

**Role Variables**

.. zuul:rolevar:: name_resolution_check_resolved
   :default: {{ enable_resolvconf | default(true) }}

Run the ``resolved`` and ``nameservers`` checks only when this is true. When
osism.commons.resolvconf is not applied, systemd-resolved is not expected.

.. zuul:rolevar:: name_resolution_resolv_conf
   :default: {{ resolvconf_file | default('/etc/resolv.conf') }}

The resolver configuration that has to list only the stub resolver.

.. zuul:rolevar:: name_resolution_nameservers
   :default: {{ resolvconf_nameserver | default(['9.9.9.9', '149.112.112.112']) }}

The upstream nameservers, in the ``DNS=`` syntax of resolved.conf(5). Each one
has to answer a query for ``name_resolution_nameserver_query``. The fallback
follows ``resolvconf_nameserver_default`` and ``resolvconf_nameserver_extra``.

.. zuul:rolevar:: name_resolution_dns_over_tls
   :default: {{ resolvconf_dns_over_tls | default(false) }}

When DNS over TLS is enforced (true or yes), the ``nameservers`` check is
skipped, because a plain DNS query does not test that transport.

.. zuul:rolevar:: name_resolution_nameserver_query
   :default: the first external name, else the first endpoint FQDN

The name the upstream nameservers are asked for. In a proxied or air-gapped
installation the default is the proxy or the local mirror, a name the
nameservers of the installation know.

.. zuul:rolevar:: name_resolution_nameserver_timeout
   :default: 2

The timeout in seconds of each of the two attempts to query a nameserver.

.. zuul:rolevar:: name_resolution_external_names
   :default: derived

The names the ``external`` check resolves. When unset, the role derives them:
the proxy hosts when ``proxy_proxies`` is set, otherwise the registry hosts and
the hosts of the enabled apt or dnf package sources of the host. An empty list
switches the check off.

.. zuul:rolevar:: name_resolution_external_names_extra
   :default: []

Names the ``external`` check resolves in addition.

.. zuul:rolevar:: name_resolution_endpoints
   :default: {kolla_external_fqdn: '', kolla_internal_fqdn: kolla_internal_vip_address}

A dictionary from an FQDN to the address it has to resolve to. A name mapped to
an empty string only has to resolve. When both FQDNs are equal, the internal
entry wins. Names that are IP addresses, as in the defaults of osism/defaults,
are left out.

.. zuul:rolevar:: name_resolution_check_reverse
   :default: true

Run the ``reverse`` check only when this is true. With DNS as the single source
of truth it requires PTR records for the inventory hosts.

.. zuul:rolevar:: name_resolution_lookup_deadline
   :default: 120

After this many seconds no further lookup is started, and the remaining names
fail with a message that they were not checked.
