This role validates that Docker on a host provides what the Docker Compose
based services of osism.services and kolla-ansible need. Run it when an
environment is deployed or upgraded, before the services are rolled out. It
validates Docker only; hosts that run Podman are not covered.

The role stops at the first failed check. Every failure message starts with the
label of the check, followed by the observed and the expected value:

* ``image-registry``: the test image is not pulled from Docker Hub.
* ``services``: the Docker and containerd services are running and enabled.
* ``socket``: the daemon answers on its local socket.
* ``storage-driver``, ``log-driver``, ``live-restore``, ``default-runtime``,
  ``registry-mirrors``, ``insecure-registries``, ``proxy``: the effective
  configuration of the running daemon matches what osism.services.docker
  rolls out.
* ``operator-user``: the operator user exists.
* ``operator-socket``: the operator user talks to the daemon without root.
* ``compose``: the ``docker compose`` plugin works for the operator user.
* ``python-sdk``: the Python Docker SDK is importable by the Python interpreter
  Ansible uses on the host.
* ``pull``: the test image can be pulled as the operator user.
* ``container``: a container started from the test image runs on a new
  bridge network, like the network of a Docker Compose project.
* ``log-opts``, ``default-ulimits``: the test container gets the log options
  and default ulimits of the daemon.
* ``dns``: the test container resolves the name of the registry, or of the
  proxy when one is configured.
* ``network``: the test container reaches the registry, or the proxy when one
  is configured.
* ``cleanup``: the test left neither its container, its network, nor the test
  image behind. The test image stays only if it was present before the run.

The defaults of the expected configuration read the inventory variables of
osism.services.docker (``docker_storage_driver``, ``docker_log_opts``,
``docker_registry_mirrors``, ...) and fall back to the defaults of that role.
They have to follow when osism.services.docker changes one of its defaults.

**Role Variables**

.. zuul:rolevar:: docker_ready_operator_user
   :default: {{ operator_user | default('dragon') }}

The user the Docker Compose services run as. The client checks and the pull
and run test run as this user.

.. zuul:rolevar:: docker_ready_docker_service_name
   :default: {{ docker_service_name | default('docker') }}

The systemd service of the Docker daemon.

.. zuul:rolevar:: docker_ready_containerd_service_name
   :default: {{ containerd_service_name | default('containerd') }}

The systemd service of containerd.

.. zuul:rolevar:: docker_ready_check_containerd
   :default: {{ docker_manage_containerd | default(true) }}

Check the containerd service only when this is true.

.. zuul:rolevar:: docker_ready_socket
   :default: /var/run/docker.sock

The local socket the daemon has to answer on.

.. zuul:rolevar:: docker_ready_storage_driver
   :default: overlayfs if docker_storage_containerd_snapshotter, else {{ docker_storage_driver | default('overlay2') }}

The expected storage driver.

.. zuul:rolevar:: docker_ready_log_driver
   :default: {{ docker_log_driver | default('json-file') }}

The expected log driver.

.. zuul:rolevar:: docker_ready_log_opts
   :default: {{ docker_log_opts | default({'max-size': '10m', 'max-file': 3}) }}

The expected log options of a new container.

.. zuul:rolevar:: docker_ready_live_restore
   :default: {{ docker_live_restore | default(true) }}

Whether live restore is expected to be enabled.

.. zuul:rolevar:: docker_ready_default_ulimits
   :default: {{ docker_default_ulimits | default({'nofile': {'Name': 'nofile', 'Soft': 262144, 'Hard': 1048576}}) }}

The expected default ulimits of a new container.

.. zuul:rolevar:: docker_ready_default_runtime
   :default: {{ docker_default_runtime | default('runc') }}

The expected default runtime.

.. zuul:rolevar:: docker_ready_registry_mirrors
   :default: {{ docker_registry_mirrors | default([]) }}

The expected registry mirrors.

.. zuul:rolevar:: docker_ready_insecure_registries
   :default: {{ docker_insecure_registries | default([]) }}

The expected insecure registries. A CIDR has to be written in network form,
for example ``10.0.0.0/8`` and not ``10.0.0.1/8``.

.. zuul:rolevar:: docker_ready_proxy_enabled
   :default: {{ docker_configure_proxy | default(false) }}

Whether the daemon is expected to use a proxy. Without a proxy, the daemon must
report empty proxy settings.

.. zuul:rolevar:: docker_ready_proxy_http
   :default: {{ docker_proxy_http | default('http://proxy.tld:8080') }}

The expected HTTP proxy. Credentials in the URL are compared, and shown,
masked as ``xxxxx:xxxxx``, the way the daemon reports them.

.. zuul:rolevar:: docker_ready_proxy_https
   :default: {{ docker_proxy_https | default(docker_ready_proxy_http) }}

The expected HTTPS proxy.

.. zuul:rolevar:: docker_ready_proxy_no_proxy
   :default: docker_proxy_no_proxy, else docker_proxy_no_proxy_default + docker_proxy_no_proxy_extra

The expected list of hosts that bypass the proxy.

.. zuul:rolevar:: docker_ready_image
   :default: {{ docker_registry_ansible | default('registry.osism.tech') }}/osism/rsync:3.5.0

The test image. It has to come from the registry the installation uses, never
from Docker Hub, and provide ``sleep``, ``cat``, ``getent`` and ``nc`` with
``-z``. An air-gapped registry has to carry ``osism/rsync:3.5.0``, otherwise
set this to an image it carries. The default image is available for
linux/amd64 only; on other architectures, set this to an image for that
architecture.

.. zuul:rolevar:: docker_ready_registry
   :default: the first component of docker_ready_image

The registry of the test image.

.. zuul:rolevar:: docker_ready_dns_check_name
   :default: the host of the HTTPS proxy (or of the HTTP proxy if that one is empty) if docker_ready_proxy_enabled, else docker_ready_registry without its port

The name the test container has to resolve. With a proxy, the proxy resolves
the name of the registry, so the container has to resolve only the name of the
proxy. The check is skipped when the name is empty, ``localhost`` or an IPv4
address.

.. zuul:rolevar:: docker_ready_network_check_host
   :default: the host of the HTTPS proxy (or of the HTTP proxy if that one is empty) if docker_ready_proxy_enabled, else docker_ready_dns_check_name

The host the test container has to connect to. The check is skipped when the
host is empty, ``localhost`` or a loopback address. A registry given as an
IPv6 address needs this, ``docker_ready_dns_check_name`` and
``docker_ready_network_check_port`` set explicitly.

.. zuul:rolevar:: docker_ready_network_check_port
   :default: the port of that proxy (443 for an https URL, else 80, if none) if docker_ready_proxy_enabled, else the registry port (443 if none)

The TCP port the test container has to connect to.

.. zuul:rolevar:: docker_ready_pull_timeout
   :default: 300

The timeout of the pull in seconds. A pull that takes longer is cancelled.

.. zuul:rolevar:: docker_ready_container_timeout
   :default: 300

The maximum lifetime of the test container in seconds.
