# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file was started on March 15, 2022. Changes prior to this date are not included in the CHANGELOG.

## [v0.20260318.0] - 2026-03-18

### Added
- Tempest: add SCS compatible test list (osism/ansible-collection-validations#254)
- Tempest: add keystone identity feature enabled configuration with security_compliance support (osism/ansible-collection-validations#253)

## [v0.20260127.0] - 2026-01-27

### Dependencies
- ansible 11.10.0 → 12.3.0 (osism/ansible-collection-validations#242, osism/ansible-collection-validations#245, osism/ansible-collection-validations#246, osism/ansible-collection-validations#252)
- molecule 25.9.0 → 25.12.0 (osism/ansible-collection-validations#248, osism/ansible-collection-validations#251)
- pytest 8.4.2 → 9.0.2 (osism/ansible-collection-validations#247)
- actions/checkout v5 → v6 (osism/ansible-collection-validations#250)

## [v0.20250927.0] - 2025-09-27

### Changed
- Cleanup `.ansible-lint` file (osism/ansible-collection-validations#239)

### Fixed
- Tempest: fix typo in exclude list logic and fix include/exclude lists path inside container (osism/ansible-collection-validations#244)

### Dependencies
- actions/checkout v4 → v5 (osism/ansible-collection-validations#237)
- actions/setup-python v4 → v6 (osism/ansible-collection-validations#240)
- ansible 11.8.0 → 11.10.0 (osism/ansible-collection-validations#238)
- molecule 25.7.0 → 25.9.0 (osism/ansible-collection-validations#243)
- pytest 8.4.1 → 8.4.2 (osism/ansible-collection-validations#241)

## [v0.20250902.0] - 2025-09-02

### Added
- Cosign secrets to Zuul configuration (osism/ansible-collection-validations#233)

### Removed
- Gate pipeline from Zuul configuration (osism/ansible-collection-validations#232)

### Dependencies
- ansible 11.6.0 → 11.8.0 (osism/ansible-collection-validations#230, osism/ansible-collection-validations#234)
- molecule 25.5.0 → 25.7.0 (osism/ansible-collection-validations#231, osism/ansible-collection-validations#235)
- pytest 8.3.5 → 8.4.1 (osism/ansible-collection-validations#228)

## [v0.20250605.0] - 2025-06-05

### Added
- Tempest wrapper script for running tempest via Docker (osism/ansible-collection-validations#225)
- Role to validate expected, installed and running docker versions (osism/ansible-collection-validations#229)

### Changed
- Assign load-balancer_member role to tempest user (osism/ansible-collection-validations#226)
- Use amphora as default Octavia provider driver instead of OVN (osism/ansible-collection-validations#227)

## [v0.20250529.0] - 2025-05-29

### Changed
- Refresh Zuul secrets (osism/ansible-collection-validations#221)

### Dependencies
- ansible 11.4.0 → 11.5.0 (osism/ansible-collection-validations#220)
- ansible 11.5.0 → 11.6.0 (osism/ansible-collection-validations#222)
- molecule 25.4.0 → 25.5.0 (osism/ansible-collection-validations#224)

## [v0.20250407.0] - 2025-04-07

### Dependencies
- pytest-testinfra 10.1.1 → 10.2.2 (osism/ansible-collection-validations#218)
- molecule 25.3.1 → 25.4.0 (osism/ansible-collection-validations#219)

## [v0.20250327.0] - 2025-03-27

### Added
- Stress role for CPU and memory stress testing with stress-ng (osism/ansible-collection-validations#217)
- ANSIBLE_COLLECTIONS_PATH to molecule provisioner environment (osism/ansible-collection-validations#209)

### Changed
- Tempest container registry from quay.io to registry.osism.tech (osism/ansible-collection-validations#214)
- Cleaned up ansible-lint configuration by removing unused rules directory and warn list (osism/ansible-collection-validations#216)

### Fixed
- ANSIBLE_COLLECTIONS_PATH for CentOS by adding fallback collections path (osism/ansible-collection-validations#210)

### Dependencies
- ansible 10.7.0 → 11.4.0 (osism/ansible-collection-validations#190, osism/ansible-collection-validations#212, osism/ansible-collection-validations#215)
- molecule 24.12.0 → 25.3.1 (osism/ansible-collection-validations#207, osism/ansible-collection-validations#211)
- pytest 8.3.4 → 8.3.5 (osism/ansible-collection-validations#213)

## [v0.20241219.0] - 2024-12-19

### Added
- Tempest volume multi-attach test support (osism/ansible-collection-validations#203)

### Changed
- Re-enabled Octavia and Barbican services in Tempest by default (osism/ansible-collection-validations#204)
- Changed default Tempest loadbalancer provider from Amphora to OVN (osism/ansible-collection-validations#205)

## [v0.20241217.0] - 2024-12-17

### Added
- Support for tempest include and exclude lists (osism/ansible-collection-validations#202)
- Set `catalog_type = volumev3` for tempest volume service (osism/ansible-collection-validations#196)
- Set `admin_system = all` in tempest identity configuration (osism/ansible-collection-validations#200)
- Set `vnc_console = true` in tempest compute feature configuration (osism/ansible-collection-validations#201)
- Always assign the `member` role to tempest user (osism/ansible-collection-validations#199)

### Changed
- Do not include or exclude tempest tests by default (osism/ansible-collection-validations#195)
- Use default resource name prefix instead of custom `osism-validation-tempest` (osism/ansible-collection-validations#198)

### Fixed
- Fix wrong parameters in tempest network section (`public_network_id` and `floating_network_name` used colons instead of equals signs, wrong key name) (osism/ansible-collection-validations#197)

## [v0.20241206.0] - 2024-12-06

### Changed
- kernel_version: Improved version comparison using `ansible.builtin.version` with configurable comparison operators (osism/ansible-collection-validations#179)
- tempest: Bumped default Cirros image versions (0.6.2 → 0.6.3, 0.6.1 → 0.6.2) (osism/ansible-collection-validations#181)
- tempest: Renamed `tempest_tag`/`tempest_image` to `tempest_osism_tag`/`tempest_osism_image` to avoid overlapping with kolla parameter names (osism/ansible-collection-validations#182)
- tempest: Convert downloaded raw image to qcow2 format (osism/ansible-collection-validations#184)
- tempest: Changed default loadbalancer provider from ovn to amphora (osism/ansible-collection-validations#185)
- tempest: Disabled barbican by default (osism/ansible-collection-validations#187)
- tempest: Disabled octavia by default (osism/ansible-collection-validations#189)
- network_connectivity: Added redundant defaults for `network_connectivity_network_cidr` to work around ansible-lint bug (osism/ansible-collection-validations#194)

### Fixed
- tempest: Fixed typo in parameter names (`tempest_osims_tag`/`tempest_osims_image` → `tempest_osism_tag`/`tempest_osism_image`) (osism/ansible-collection-validations#183)

### Dependencies
- ansible 10.4.0 → 10.5.0 (osism/ansible-collection-validations#180)
- ansible 10.5.0 → 10.6.0 (osism/ansible-collection-validations#188)
- ansible 10.6.0 → 10.7.0 (osism/ansible-collection-validations#192)
- pytest 8.3.3 → 8.3.4 (osism/ansible-collection-validations#191)
- molecule 24.9.0 → 24.12.0 (osism/ansible-collection-validations#193)

## [v0.20240924.0] - 2024-09-24

### Added
- Role `python_version` to validate the installed Python version (osism/ansible-collection-validations#176)
- Role `ansible_version` to validate the installed ansible-core version (osism/ansible-collection-validations#177)

### Changed
- Use galaxy dependency manager instead of force-installing ansible requirements via shell in molecule (osism/ansible-collection-validations#178)

### Dependencies
- pytest 8.3.2 → 8.3.3 (osism/ansible-collection-validations#173)
- ansible 10.3.0 → 10.4.0 (osism/ansible-collection-validations#174)
- molecule 24.8.0 → 24.9.0 (osism/ansible-collection-validations#175)

## [v0.20240904.0] - 2024-09-04

No changes.

## [v0.20240825.0] - 2024-08-25

_No changes since v0.20240818.0._

## [v0.20240818.0] - 2024-08-18

### Added
- DTRACK_API_KEY secret to Zuul configuration (osism/ansible-collection-validations#172)

### Removed
- Refstack role (osism/ansible-collection-validations#170)

### Dependencies
- ansible 10.2.0 → 10.3.0 (osism/ansible-collection-validations#168)
- molecule 24.7.0 → 24.8.0 (osism/ansible-collection-validations#171)

## [v0.20240812.0] - 2024-08-12

### Added
- Role to verify network connectivity between hosts using MTU-sized ping requests (osism/ansible-collection-validations#166)
- Zuul job `ansible-collection-ensure-readme` (osism/ansible-collection-validations#165)

### Fixed
- Use correct variable `network_connectivity_network_cidr` in network_connectivity role (osism/ansible-collection-validations#167)

### Removed
- Old and out-of-date README files from multiple roles (osism/ansible-collection-validations#164)

### Dependencies
- pytest 8.3.1 → 8.3.2 (osism/ansible-collection-validations#163)

## [v0.20240723.0] - 2024-07-23

### Added
- Missing EPEL repository to molecule preparation for RedHat systems (osism/ansible-collection-validations#160)

### Changed
- Require ansible >= 2.16 (osism/ansible-collection-validations#161)

### Dependencies
- ansible 9.7.0 → 10.2.0 (osism/ansible-collection-validations#147)
- pytest 8.2.2 → 8.3.1 (osism/ansible-collection-validations#162)

## [v0.20240711.1] - 2024-07-11

### Added
- Tags to make it possible to not run tempest (osism/ansible-collection-validations#158)

## [v0.20240711.0] - 2024-07-11

### Changed
- Revert refstack workdir from `/share` back to `/opt/refstack` (osism/ansible-collection-validations#156)

### Fixed
- Fix "sudo: not found" issue in tempest by adjusting task delegation (osism/ansible-collection-validations#157)

### Dependencies
- molecule 24.6.1 → 24.7.0 (osism/ansible-collection-validations#154)

## [v0.20240710.0] - 2024-07-10

### Changed
- Refstack: use `/share` as default workdir since the role runs within the manager service (osism/ansible-collection-validations#152)

### Dependencies
- molecule 24.6.0 → 24.6.1 (osism/ansible-collection-validations#153)

## [v0.20240702.0] - 2024-07-02

### Added
- Allow filtering on arbitrary labels in prometheus-alert-status role (osism/ansible-collection-validations#145)

### Changed
- Do not set `ansible_python_interpreter` in molecule configuration (osism/ansible-collection-validations#150)
- Support Ansible version 2.17 in collection metadata (osism/ansible-collection-validations#151)

### Dependencies
- ansible 9.6.0 → 9.7.0 (osism/ansible-collection-validations#149)
- molecule 24.2.1 → 24.6.0 (osism/ansible-collection-validations#148)
- pytest 8.2.1 → 8.2.2 (osism/ansible-collection-validations#146)

## [v0.20240531.0] - 2024-05-31

### Dependencies
- pytest-testinfra 10.1.0 → 10.1.1 (osism/ansible-collection-validations#144)

## [v0.20240524.0] - 2024-05-24

### Added
- Role `prometheus_alert_status` to check Prometheus for active alerts (osism/ansible-collection-validations#140)

### Changed
- Cleaned up README and updated documentation link (osism/ansible-collection-validations#143)

### Dependencies
- pytest 8.2.0 → 8.2.1 (osism/ansible-collection-validations#141)
- ansible 9.5.1 → 9.6.0 (osism/ansible-collection-validations#142)

## [v0.20240503.0] - 2024-05-03

### Added
- Zuul CI integration with molecule test jobs for container_status, kernel_version, mysql_open_files_limit, system_encoding, and ulimits roles (osism/ansible-collection-validations#130)
- Ubuntu 24.04 (Noble) to Zuul CI test matrix (osism/ansible-collection-validations#134)
- Tempest role for running OpenStack tempest tests (osism/ansible-collection-validations#133)

### Changed
- Use ubuntu-jammy nodes in Zuul CI instead of ubuntu-jammy-large (osism/ansible-collection-validations#132)
- Update role metadata to support Debian bookworm, CentOS 9, and Ubuntu Noble, bump min_ansible_version to 2.16.0 (osism/ansible-collection-validations#135)
- Use configurable `operator_user`/`operator_group` variables in refstack role instead of hardcoded values (osism/ansible-collection-validations#130)
- Delegate tempest config and img_file creation to manager node, replace hardcoded user/group with variables (osism/ansible-collection-validations#139)

### Removed
- GitHub Actions workflows for role testing, replaced by Zuul CI (osism/ansible-collection-validations#130)

### Dependencies
- pytest 8.1.1 → 8.2.0 (osism/ansible-collection-validations#137) (osism/ansible-collection-validations#138)
- ansible 9.4.0 → 9.5.1 (osism/ansible-collection-validations#136)

## [v0.20240417.0] - 2024-04-17

### Dependencies
- molecule 24.2.0 → 24.2.1 (osism/ansible-collection-validations#131)

## [v0.20240327.0] - 2024-03-27

### Changed
- Replace osism.github.io with osism.tech in documentation URLs (osism/ansible-collection-validations#129)

## [v0.20240319.0] - 2024-03-19

No changes.

## [v0.20240311.0] - 2024-03-11

No changes from previous release v0.20240307.0.

## [v0.20240307.0] - 2024-03-07

No changes.

## [v0.20240221.0] - 2024-02-21

### Added
- Zuul job to push osism-ansible container image (osism/ansible-collection-validations#128)

### Dependencies
- molecule 6.0.3 → 24.2.0 (osism/ansible-collection-validations#127)

## [v0.20240204.0] - 2024-02-04

### Changed
- Refstack: run more tests by changing target from "compute" to "platform", enable swift endpoint checking, RGW user account creation, and dynamic credentials (osism/ansible-collection-validations#126)
- Refstack: update tempest version from 31.1.0 to 36.0.0 and tempest plugin versions (barbican 3.0.0, designate 0.20.0, heat 2.0.0, octavia 2.4.1) (osism/ansible-collection-validations#126)

### Dependencies
- molecule 6.0.2 → 6.0.3 (osism/ansible-collection-validations#125)

## [v0.20231126.0] - 2023-11-26

### Changed
- Default expected kernel version updated from 5.4 to 6.2 (osism/ansible-collection-validations#121)
- Allow use of ansible-core 2.16 by extending version constraint to <2.17.0 (osism/ansible-collection-validations#123)

### Fixed
- Fix yamllint issues in `.zuul.yaml` and `roles/refstack/tasks/install.yml` (osism/ansible-collection-validations#120)

### Removed
- Remove Sphinx docs build, documentation migrated to osism.github.io (osism/ansible-collection-validations#122)

### Dependencies
- molecule 5.1.0 → 6.0.2 (osism/ansible-collection-validations#111)

## [v0.20230919.0] - 2023-09-19

No changes.

## [v0.20230915.0] - 2023-09-15

### Changed
- Link to new docs website (osism/ansible-collection-validations#119)

### Fixed
- Fix typo in refstack comment ("admoun" → "admin") (osism/ansible-collection-validations#116)

### Dependencies
- ansible 8.3.0 → 8.4.0 (osism/ansible-collection-validations#118)
- docker/setup-buildx-action v2 → v3 (osism/ansible-collection-validations#117)

## [v0.20230906.1] - 2023-09-06

### Changed
- Refstack: disable `test_list_show_extensions` test as l3_agent_scheduler extension is not available with OVN (osism/ansible-collection-validations#115)

## [v0.20230906.0] - 2023-09-06

### Dependencies
- actions/checkout v3 → v4 (osism/ansible-collection-validations#113, osism/ansible-collection-validations#114)

## [v0.20230901.0] - 2023-09-01

### Changed
- Use refstack guideline 2022.11 by default (osism/ansible-collection-validations#110)

### Fixed
- Pin Sphinx version to fix broken build pipeline (osism/ansible-collection-validations#105)

### Dependencies
- ansible 8.0.0 → 8.3.0 (osism/ansible-collection-validations#106, osism/ansible-collection-validations#109, osism/ansible-collection-validations#112)
- molecule 5.0.1 → 5.1.0 (osism/ansible-collection-validations#107)

## [v0.20230614.0] - 2023-06-14

### Changed
- Enable ansible-lint rules: `var-spacing`, `fqcn-builtins`, `parser-error`, `name[template]` (osism/ansible-collection-validations#96) (osism/ansible-collection-validations#97) (osism/ansible-collection-validations#99) (osism/ansible-collection-validations#100)
- Ignore ansible-lint `var-naming[no-role-prefix]` rule (osism/ansible-collection-validations#95)
- Update supported ansible versions to `>=2.14.0,<2.16.0` (osism/ansible-collection-validations#104)

### Removed
- Remove Ubuntu 20.04 from CI test matrix (osism/ansible-collection-validations#98)

### Dependencies
- ansible 7.4.0 → 7.5.0 (osism/ansible-collection-validations#94)
- ansible 7.5.0 → 7.6.0 (osism/ansible-collection-validations#101)
- ansible 7.6.0 → 8.0.0 (osism/ansible-collection-validations#102)
- molecule 4.0.4 → 5.0.1 (osism/ansible-collection-validations#93)

## [v0.20230407.0] - 2023-04-07

### Added
- Periodic-daily jobs for yamllint and ansible-lint in Zuul for better visibility of linting errors

### Dependencies
- ansible 7.3.0 → 7.4.0 (osism/ansible-collection-validations#90)

## [v0.20230313.0] - 2023-03-13

### Changed
- Refstack: use SCS flavors v2 naming format (osism/ansible-collection-validations#89)

## [v0.20230312.0] - 2023-03-12

No changes.

## [v0.20230308.1] - 2023-03-08

### Changed
- Refstack bootstrap tasks are now compatible with openstacksdk v1 (osism/ansible-collection-validations#88)

## [v0.20230308.0] - 2023-03-08

### Added
- Add ca-cert configuration to "Create refstack keypairs" task in refstack role (osism/ansible-collection-validations#87)

### Changed
- Refstack role no longer hardcodes user/project names, using configurable `refstack_users` variable instead (osism/ansible-collection-validations#85)

### Fixed
- Refstack role no longer injects testbed CA on non-testbed nodes (osism/ansible-collection-validations#86)

## [v0.6.1] - 2023-03-07

### Changed
- Refstack keypair creation now uses auth parameters instead of cloud config (osism/ansible-collection-validations#84)
- Refstack uses Ubuntu 22.04 Minimal instead of a second Cirros image (osism/ansible-collection-validations#84)

### Fixed
- Wrong use of password arguments in refstack role (osism/ansible-collection-validations#84)

## [v0.6.0] - 2023-03-05

### Added
- Port security configuration for network feature in refstack tempest config (osism/ansible-collection-validations#76)
- Installation of octavia-tempest-plugin in refstack prepare script (osism/ansible-collection-validations#78)
- Installation of barbican-tempest-plugin in refstack prepare script (osism/ansible-collection-validations#79)
- Helper scripts `list.sh` and `sign.sh` for refstack (osism/ansible-collection-validations#80)

### Changed
- Refstack validator now uses existing flavors and images instead of creating them (osism/ansible-collection-validations#74)
- Refstack logging switched from silent redirect to `tee` for real-time output (osism/ansible-collection-validations#74)
- Log filenames now include hours and minutes in timestamp (osism/ansible-collection-validations#74)
- Default refstack image changed from Ubuntu 22.04 Minimal to Cirros 0.6.0 (osism/ansible-collection-validations#75)
- Default refstack guideline updated from 2020.11 to 2021.11 for Yoga compatibility (osism/ansible-collection-validations#77)
- Refstack install enabled by default (osism/ansible-collection-validations#81)
- Upload script now uses full path for test results (osism/ansible-collection-validations#80)

### Fixed
- Heat flavor references in refstack tempest configuration (osism/ansible-collection-validations#76)
- Refstack-client repository URL updated to openinfra namespace (osism/ansible-collection-validations#82)
- Refstack `setup_env` call to use absolute path (osism/ansible-collection-validations#83)

## [v0.5.0] - 2023-03-01

### Added
- Refstack role for running OpenStack refstack tests (osism/ansible-collection-validations#63)
- Zuul docs publish job for production

### Changed
- Use Python 3.10 for test-role CI workflows (osism/ansible-collection-validations#60)
- Transfer ansible-lint check from GitHub Actions to Zuul (osism/ansible-collection-validations#59)
- Transfer yamllint check from GitHub Actions to Zuul (osism/ansible-collection-validations#61)
- Add squash-merge mode to Zuul configuration (osism/ansible-collection-validations#62)
- Log refstack run details to /opt/refstack (osism/ansible-collection-validations#64)
- Update refstack tempest and plugin versions (osism/ansible-collection-validations#67)
- Add Ubuntu Jammy to supported platforms in role metadata (osism/ansible-collection-validations#70)

### Fixed
- Fix role descriptions using osism.services instead of osism.validations (osism/ansible-collection-validations#69)
- Fix typo in refstack prepare.sh.j2 template (osism/ansible-collection-validations#66)
- Fix refstack domain name/id usage and add missing delegate_to (osism/ansible-collection-validations#65)

### Removed
- Custom ansible-lint rule directory (osism/ansible-collection-validations#71)

### Dependencies
- ansible 6.7.0 → 7.3.0 (osism/ansible-collection-validations#53, osism/ansible-collection-validations#72)

## [v0.4.0] - 2022-12-29

### Changed
- Extend supported Ansible version range to include 2.13 (osism/ansible-collection-validations#39)
- Refactor ansible-lint rules configuration (osism/ansible-collection-validations#46)
- Only warn about experimental ansible-lint rules (osism/ansible-collection-validations#57)
- Rename `system_encoding_wanted` parameter to `system_encoding_expected` (osism/ansible-collection-validations#58)
- Remove `kernel_version_fact` parameter, use `ansible_facts.kernel` directly (osism/ansible-collection-validations#58)
- Simplify molecule test converge playbook (osism/ansible-collection-validations#58)
- Improve role documentation (osism/ansible-collection-validations#58)

### Fixed
- Fix ansible-lint errors after version update (osism/ansible-collection-validations#47)
- Fix typo "local" to "locale" in system_encoding role (osism/ansible-collection-validations#58)

### Removed
- Remove unused molecule/default scenario (osism/ansible-collection-validations#58)
- Remove unused molecule_old.yml file (osism/ansible-collection-validations#46)

### Dependencies
- ansible 6.3.0 → 6.4.0 (osism/ansible-collection-validations#45)
- ansible 6.4.0 → 6.5.0 (osism/ansible-collection-validations#49)
- ansible 6.5.0 → 6.6.0 (osism/ansible-collection-validations#52)
- ansible 6.6.0 → 6.7.0 (osism/ansible-collection-validations#55)
- molecule 4.0.1 → 4.0.2 (osism/ansible-collection-validations#50)
- molecule 4.0.2 → 4.0.3 (osism/ansible-collection-validations#51)
- molecule 4.0.3 → 4.0.4 (osism/ansible-collection-validations#54)
- molecule-docker 2.0.0 → 2.1.0 (osism/ansible-collection-validations#48)

## [v0.3.0] - 2022-09-12

### Added
- Ansible-lint rules for attribute order check and FQCN usage check (osism/ansible-collection-validations#36)
- Documentation for container_status role (osism/ansible-collection-validations#26)
- Documentation for kernel_version role (osism/ansible-collection-validations#27)
- Documentation for mysql_open_files_limit role (osism/ansible-collection-validations#28)
- Documentation for system_encoding role (osism/ansible-collection-validations#29)
- Sphinx documentation build infrastructure (osism/ansible-collection-validations#31)
- Molecule tests for all roles (osism/ansible-collection-validations#40)
- Empty README files for roles (osism/ansible-collection-validations#44)

### Changed
- Cleanup Ansible-lint warnings and remove skipped rules (osism/ansible-collection-validations#38)

### Dependencies
- molecule 3.6.1 → 4.0.1 (osism/ansible-collection-validations#34)
- molecule-docker 1.1.0 → 2.0.0 (osism/ansible-collection-validations#37)
- ansible 6.2.0 → 6.3.0 (osism/ansible-collection-validations#43)

## [v0.2.0] - 2022-06-30

### Added
- Documentation for the ulimits role (osism/ansible-collection-validations#30)
- Missing README.md files (osism/ansible-collection-validations#35)

### Changed
- Moved `changed_when` condition in container_status role to follow task parameters convention (osism/ansible-collection-validations#33)
- Added python preset to Renovate configuration

### Dependencies
- actions/setup-python v3 → v4 (osism/ansible-collection-validations#32)

## [v0.1.0] - 2022-03-15

### Added
- Initial project with validation roles: container_status, kernel_version, mysql_open_files_limit, system_encoding, and ulimits
- Molecule testing framework with Docker driver
- CI workflows for Ansible and YAML syntax checking
- Publish collection workflow for Ansible Galaxy
- Added `osism` tag to collection and role metadata (osism/ansible-collection-validations#15)

### Changed
- Company name changed from "Betacloud Solutions GmbH" to "OSISM GmbH" (osism/ansible-collection-validations#1)
- Updated URLs from osism.de to osism.tech
- Updated minimum Ansible version to 2.10.0 in role metadata (osism/ansible-collection-validations#6)
- Updated requires_ansible to `>=2.10.0,<2.13.0`
- Use `ansible.builtin` FQCNs in molecule playbooks (osism/ansible-collection-validations#8)
- Use `ansible.builtin` FQCNs in container_status role (osism/ansible-collection-validations#9)
- Use `ansible.builtin` FQCNs in kernel_version role (osism/ansible-collection-validations#10)
- Use `ansible.builtin` FQCNs in mysql_open_files_limit role (osism/ansible-collection-validations#11)
- Use `ansible.builtin` FQCNs in system_encoding role (osism/ansible-collection-validations#12)
- Use `ansible.builtin` FQCNs in ulimits role (osism/ansible-collection-validations#13)
- Restrict CI branch builds to main only (osism/ansible-collection-validations#14)
- Use osism/renovate-config for Renovate configuration

### Fixed
- Fixed typo in kernel_version role (`ansible.buitlin.fail` → `ansible.builtin.fail`)

### Dependencies
- molecule 3.3.0 → 3.6.1 (osism/ansible-collection-validations#20)
- molecule-docker 0.2.4 → 1.1.0 (osism/ansible-collection-validations#24)
- actions/checkout v2 → v3 (osism/ansible-collection-validations#21)
- actions/setup-python v2 → v3 (osism/ansible-collection-validations#23)

