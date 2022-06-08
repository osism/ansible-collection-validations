This ansible role configures the ulimits from the system.

**Role Variables**

.. zuul:rolevar:: ulimits_nofiles_min
   :default: 1024

Set the limit number of files that a single process can have open at
one time, including pipes, sockets and terminals.

.. zuul:rolevar:: ulimits_nproc_min
   :default: 2048

Number of processes that could be running parallel by one user.
