This role checks for the maximum open files mysql can have.
If it's to low (less than 16384), you'll get an error.

**Role Variable**

.. zuul:rolevar:: mysql_open_files_limit_min
   :default: 16384

That is the (for openstack) required amount of files that can be opened
by the database.
