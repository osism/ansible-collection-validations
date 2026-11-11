This role validates that the hosts of a network reach each other and that the
MTU they use on the network is usable. Every host of
``network_connectivity_group`` pings each other host with "don't fragment" set
and a packet of the size of the MTU of the route to that host. An answered
ping shows that the path carries packets of that size.

The role chooses the addresses in one of two ways:

* With ``network_connectivity_network_cidr``, a host pings from its first
  address in that network to every address the other hosts have in it.
* With ``network_connectivity_network``, the name of a network in the
  kolla-ansible sense such as ``api`` or ``tunnel``, every host's address is the
  one on its ``<network>_interface`` in the address family
  ``<network>_address_family``, chosen as kolla-ansible chooses it. The CIDR is
  not used then. Each host of ``network_connectivity_group`` needs gathered
  facts.

**MTU selection**

The packet size follows the MTU the host is configured to use on the route
to the other host, read with ``ip route get fibmatch``. That is the ``mtu`` of
the route, locked or not, when the route has one. Otherwise it is the MTU of
the device selected by the route lookup of ``ip route get``. The MTU of the
device comes from the facts of the host, so the role fails when the route
leaves through a device that was created after the facts were gathered. A
route to a local address leaves through ``lo``; its MTU is capped at 65535,
the largest IP packet.

A path MTU that the kernel learned from a hop is ignored. A failed ping
teaches the kernel the smaller MTU, so a check sized by it would pass on the
next run with nothing fixed. A path with an intentionally smaller hop
declares it with ``mtu`` on the route.

The kernel caches a learned path MTU for about ten minutes. The role pings
with ``ping -M probe``, which sets "don't fragment" and sends the packet
whatever path MTU is cached, so a run passes as soon as the path carries the
MTU of the route. ``ping`` of iputils 20221126 and older, as on Debian
bookworm and Ubuntu jammy, has no ``-M probe``. There the role pings with
``-M do``, and the kernel rejects the packet for as long as it caches a
smaller path MTU: a run within about ten minutes after a failed one fails
again, even with the path fixed.

**Failure messages**

When a host does not answer the ping, the role pings it again with ping's
default payload of 56 bytes and reads the route again. It then fails with one
message for that host. Every host that was pinged and did not answer gets its
message in the same run. An error before the pings, when ``ip route get``
fails for a host or a route leaves through a device without facts, stops the
role at that task.

The messages state what the pings and the route showed. They do not name a
cause, because pings without reply do not establish one.

Only the 56-byte ping is answered::

   <target> does not answer a ping of the size of the route MTU <mtu> from <source> through <device>: the ping with <payload> bytes and don't fragment received no reply, the 56-byte ping received a reply.

Possible causes:

* A device on the path carries less than the MTU of the route: a router, a
  switch port or the interface of the other host. Compare their MTUs with the
  MTU of the route, then raise the smaller one or declare it with ``mtu`` on
  the route.
* The large packet was lost and the small one was not. With
  ``network_connectivity_ping_count: 1`` a single lost packet is enough. Run
  the role again or raise the count.

Neither ping is answered::

   <target> does not answer ping from <source> through <device>: neither the ping with <payload> bytes and don't fragment nor the 56-byte ping received a reply.

Check the addresses, the routing and the firewalls between the hosts. A host
or a firewall that filters ICMP echo requests gives the same result. The
message says nothing about the MTU, which may be usable or not.

Either message ends with one more sentence when the route, read after the
pings, shows a cached path MTU below the MTU of the route::

   The kernel has a cached path MTU of <learned>.

A router on the path reported with an ICMP "fragmentation needed" or "packet
too big" message that it carries only this much. The kernel keeps the value
for about ten minutes, so it comes from this ping or from an earlier packet
to that host.

Without that sentence the kernel has no smaller path MTU cached. Either no
router reported one, as when a switch port or the other host drops the
packet without a message, or the kernel ignored the report: on an IPv4 route
with ``mtu lock`` it does not cache a reported path MTU.

An error of ``ping`` or ``ip`` itself is reported for the host with the exit
status and the error output of the command, for example::

   The ping with <payload> bytes and don't fragment from <source> to <target> through <device> failed with exit status <status>: <error>

**Role Variables**

.. zuul:rolevar:: network_connectivity_group
   :default: all

The inventory hosts that ping each other, as a list of inventory host names,
for example ``groups['ceph-osd']``, or ``groups['all']`` for all hosts. It
needs at least two hosts. The default is the string ``all``, which the role
does not expand to the hosts of the inventory, so always pass a list.

.. zuul:rolevar:: network_connectivity_network_cidr
   :default: 127.0.0.0/8

The network to check, as a CIDR. The role pings the addresses the hosts have
in this network. It is not used when ``network_connectivity_network`` is set.

.. zuul:rolevar:: network_connectivity_network
   :default: ""

The name of a network in the kolla-ansible sense, for example ``api`` or
``tunnel``. If set, every host's address is the one on its
``<network>_interface`` in the address family ``<network>_address_family``,
and ``network_connectivity_network_cidr`` is not used.

.. zuul:rolevar:: network_connectivity_ping_count
   :default: 1

The number of pings sent to each host per check.
