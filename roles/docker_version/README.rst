This role compares the version of the running docker daemon with the
version of the installed package and an expected version.

**Role Variables**

.. zuul:rolevar:: docker_version_expected
   :default: {{ docker_version }}

Docker version for comparison.
