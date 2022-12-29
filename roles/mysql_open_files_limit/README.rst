This role checks the value of open_files_limit within the mariadb
container.

**Role Variable**

.. zuul:rolevar:: mysql_open_files_limit_min
   :default: 16384

The open_files_limit option for mysql must be higher than this value.
