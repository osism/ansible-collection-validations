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
the device the route leaves through, as ``ip route get`` names it. The MTU of
the device comes from the facts of the host, so the role fails when the route
leaves through a device that was created after the facts were gathered. A
route to a local address leaves through ``lo``; its MTU is capped at 65535,
the largest IP packet.

A path MTU that the kernel learned from a hop is ignored. A failed ping
teaches the kernel the smaller MTU, so a check sized by it would pass on the
next run with nothing fixed. A path with an intentionally smaller hop
declares it with ``mtu`` on the route.

**Failure messages**

When a host does not answer the ping, the role pings it again with ping's
default payload of 56 bytes and reads the route again. It then fails with one
of three messages for that host. A run reports every host that failed.

A hop reported a smaller MTU::

   MTU <mtu> of the route from <source> to <target> through <device> is not usable: a ping with <payload> bytes and don't fragment is not answered, a ping with 56 bytes is. A hop on the path reported an MTU of <learned>.

A router on the path has a smaller MTU and said so with an ICMP
"fragmentation needed" or "packet too big" message. Raise the MTU of that hop
to the MTU of the route, or declare the smaller MTU with ``mtu`` on the route.

No hop reported a smaller MTU::

   MTU <mtu> of the route from <source> to <target> through <device> is not usable: a ping with <payload> bytes and don't fragment is not answered, a ping with 56 bytes is. No hop reported a smaller MTU, a device on the path drops packets of this size.

A device on the path, typically a switch port or the interface of the other
host, has a smaller MTU and drops the packet without a message. Compare the
MTU of the switch ports and of the other host with the MTU of the route.

The host is not reachable::

   <target> is not reachable from <source> through <device>: neither a ping with <payload> bytes and don't fragment nor a ping with 56 bytes is answered.

Not even a small packet gets through, so the MTU is not the cause. Check the
addresses, the routing and the firewalls between the hosts.

**Role Variables**

.. zuul:rolevar:: network_connectivity_group
   :default: all

The inventory hosts that ping each other, as a list of inventory host names,
for example ``groups['ceph-osd']``. It needs at least two hosts.

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
