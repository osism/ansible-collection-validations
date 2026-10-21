This role validates that the local chronyd is synchronized to an NTP source
and that the quality of the synchronization is sufficient. It then compares
the system clocks of the nodes it runs on and fails when two of them differ by
more than ``chrony_max_clock_difference``.

For the comparison every node measures the offset of its system clock against
one common NTP server, the reference, with ``chronyd -Q``. This one-shot mode
of chronyd neither steps nor slews the clock, opens no server or command port
and runs next to the running chronyd. Half the round-trip delay to the
reference bounds the error of each measurement. Each node spends at most
``chrony_reference_timeout`` seconds on its measurement.

The role compares the nodes of the current batch that passed the checks of
their own synchronization. Run it against all nodes at once, the manager
included, so that it compares the whole installation; in OSISM
``hosts_chrony`` defaults to ``all``. Apply the role to every host of the play:
a ``when`` on the role that excludes some hosts can skip the selection of the
reference for all of them. With ``serial`` each batch is compared on its own.
The comparison needs the default ``linear`` strategy, because with ``free`` a
node only compares with the nodes that measured before it.

The comparison fails when the offsets of the compared nodes differ by more
than ``chrony_max_clock_difference``. Then every node whose offset is more than
half of it away from the median offset fails. With one outlier among nodes
that agree within half the tolerance, only the outlier fails. With two nodes
that disagree both fail, because nothing tells which one is right. A single
node always passes the comparison.

**Role Variables**

.. zuul:rolevar:: chrony_max_stratum
   :default: 9

The validation fails, if the stratum of the source chronyd is synchronized to
is greater than this value.

.. zuul:rolevar:: chrony_max_system_clock_deviation
   :default: 0.005

The validation fails, if the absolute offset of the system clock from NTP time
in seconds is greater than this value.

.. zuul:rolevar:: chrony_max_upper_clock_error_bound
   :default: chrony_max_system_clock_deviation + 0.02

The validation fails, if the upper bound of the clock error in seconds is
greater than this value. The upper bound is calculated as
``|system time offset| + root dispersion + 0.5 * root delay``.

OSISM does not have a fixed requirement regarding the quality of the NTP time.
Usually ceph is one of the most time sensitive applications in an OSISM
deployment. In its default ceph starts to show warnings when it detects a clock
drift above 0.05 seconds between monitors. The default therefore ensures that
the drift between two systems stays less or equal to 0.05 seconds.

.. zuul:rolevar:: chrony_max_clock_difference
   :default: 0.05

The validation fails, if the offsets of two compared nodes against the
reference differ by more than this value in seconds. The default is the clock
drift between monitors above which ceph starts to show warnings.

.. zuul:rolevar:: chrony_reference_server
   :default: ""

The NTP server all nodes measure their offset against, as a host name or an IP
address. Every node has to reach it. If empty, the role uses the NTP server
the first node of the batch, sorted by name, is synchronized to. This is the
internal NTP server in an air-gapped installation. Nodes synchronized to a
reference clock instead of an NTP server are skipped; if no node is
synchronized to an NTP server, set this variable.

Do not set it to a name that resolves to several servers, such as the name of
a pool like ``de.pool.ntp.org``. Such a name can resolve to different servers
on different nodes, so the nodes would not measure against the same server.

All nodes query the reference at the same time. When they reach a public NTP
server through one NAT address, the server can drop the queries as too many
from one client, and the measurement fails with ``No suitable source for
synchronisation``. Set this variable to an internal NTP server then.

.. zuul:rolevar:: chrony_reference_timeout
   :default: 30

The time in seconds a node waits for the measurement against the reference.
The validation fails, if the measurement does not finish in this time.
