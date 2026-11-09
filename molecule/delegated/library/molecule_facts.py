#!/usr/bin/python
# SPDX-License-Identifier: Apache-2.0
"""Return the given facts as facts of the host the task runs for.

Used by molecule scenarios to give an added inventory host facts that
setup cannot gather for it, together with delegate_to and
delegate_facts.
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={"facts": {"type": "dict", "required": True}},
        supports_check_mode=True,
    )
    module.exit_json(changed=False, ansible_facts=module.params["facts"])


if __name__ == "__main__":
    main()
