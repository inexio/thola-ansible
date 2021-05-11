import json

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: thola_check_thola_server_facts
author: "Thola team"
version_added: "1.0.0"
short_description: "Checks if a server is running a Thola API"
description:
    - "Checks if a server is running a Thola API"
requirements:
    - thola-client-module-python
options:
    api_host:
        description:
          - Hostname of the running Thola API instance
        required: True
"""

EXAMPLES = """
- name: thola check thola-server
  thola_check_thola_server_facts:
    api_host: '{{ api_host }}'
  register: result
"""

RETURN = """
changed:
    description: "whether the command has been executed on the device"
    returned: always
    type: bool
    sample: True
thola_check_thola_server_facts:
    description: "Whether a server runs a Thola API"
    returned: always
    type: dict
"""

thola_client_found = False
try:
    import thola_client.api.check_api as check
    import thola_client

    thola_client_found = True
except ImportError:
    pass


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_host=dict(type="str", required=True)
        ),
        supports_check_mode=True,
    )

    if not thola_client_found:
        module.fail_json("The thola-client-module is not installed")

    api_host = module.params["api_host"]

    argument_check = {"api_host": api_host}
    for key, val in argument_check.items():
        if val is None:
            module.fail_json(msg=str(key) + " is required")
            return

    body = thola_client.CheckTholaServerRequest()

    check_api = check.CheckApi()
    check_api.api_client.configuration.host = api_host
    result = check_api.check_thola_server(body=body).__str__().replace("\'", "\"").replace("None", "null")
    try:
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        module.fail_json("Repsonse couldn't be parsed")
        return

    results = {"changed": False, "ansible_facts": result_dict}
    module.exit_json(**results)


if __name__ == "__main__":
    main()
