This role compaes the current kernel version  with the
expected kernel version.

**Role Variables**

.. zuul:rolevar:: kernel_version_expected
   :default: 6.2

Kernel version for comparison.
OSISM does not have a fixed requirement of a kernel version in general.
The requirements for the kernel version depend on the components used (e.g. hardware, OpenStack, Ceph, Docker, etc.).

.. zuul:rolevar:: kernel_version_comparison_operator
   :default: >=

The validation fails, if the comparison of active kernel and the defined kernel version does not
successfully evaluate to the specified operator.
(see https://docs.ansible.com/ansible/latest/collections/ansible/builtin/version_test.html for the available operators)

