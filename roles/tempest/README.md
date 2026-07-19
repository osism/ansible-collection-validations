# tempest

Prepares a Tempest workspace on the manager and runs the OpenStack integration
test suite against the deployed cloud via the OSISM Tempest container image.

## Running

### Full run

```
osism apply tempest
```

Stages everything (workspace init, image download and qcow2 conversion,
image/flavor/endpoint resolution, `tempest.conf` render, exclude/include lists),
runs the full suite, and removes the flavors it created. This is the normal
invocation and takes several hours.

### Setup only — stage the workspace without running the tests

```
osism apply tempest --skip-tags run-tempest
```

Runs the entire setup and stops before executing the tests, leaving a staged
workspace (and the created flavors) in place. Use it either to check that staging
works — image download/convert, flavor creation, `tempest.conf` render — in
minutes instead of hours, or to prepare the workspace cheaply for a subset run
with the `tempest` wrapper (below), without first paying for a full run.

Do **not** invoke the `run-tempest` tag the other way as `-t run-tempest` /
`--tags run-tempest`: that runs *only* the tagged tasks and skips the setup
they depend on (it fails on an undefined `result_exclude_list` and would remove
flavors it did not create).

### Run a subset — iterate on specific tests while debugging

After a setup-only run (above) has staged the workspace, run a subset directly on
the manager with the wrapper the role installs at `/usr/local/bin/tempest`:

```
tempest '<regex>'
```

for example:

```
tempest 'PortForwardingTestJSON.*udp'
```

The wrapper runs the Tempest container against the persisted workspace and
`tempest.conf` — no image download, no re-resolution, no Ansible — and appends
output to a timestamped log in the work directory. This is the fast way to re-run
specific tests during debugging.

A full `osism apply tempest` is not a suitable predecessor: it removes the
flavors it created, leaving `tempest.conf` pointing at flavor IDs that no longer
exist (unless `tempest_create_flavors` is `false`, where flavors are pre-existing
and kept).
