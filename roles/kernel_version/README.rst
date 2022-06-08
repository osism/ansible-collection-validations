This ansible role checks the current kernel version and compares it
with the given kernel version.

**Role Variables**

.. zuul:rolevar:: kernel_version_fact
   :default: ansible_facts.kernel

Current kernel version which ansible gets from the system.

.. zuul:rolevar:: kernel_version_expected
   :default: 5.4

The kernel version it should have.
