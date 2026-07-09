This role validates that the local chronyd is synchronized to an NTP source
and that the quality of the synchronization is sufficient.

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
