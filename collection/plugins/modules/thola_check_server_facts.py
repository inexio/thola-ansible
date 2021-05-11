import json

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: thola_check_server_facts
author: "Thola team"
version_added: "1.0.0"
short_description: "Checks a server"
description:
    - "Checks a server given its IP"
requirements:
    - thola-client-module-python
options:
    api_host:
        description:
          - Hostname of the running Thola API instance
        required: True
    ansible_host:
        description:
          - IP of the device you want to identify
        required: True
    community:
        description:
          - SNMP community of the device
    version:
        description:
          - SNMP version that should be used to connect to the device
    port:
        description:
          - The port you want Thola to connect to the device
    user_critical_max:
        description:
          - The maximum user critical threshold
    user_critical_min:
        description:
          - The minimum user critical threshold
    user_warning_max:
        description:
          - The maximum user warning threshold
    user_warning_min:
        description:
          - The minimum user warning threshold
    procs_critical_max:
        description:
          - The maximum process critical threshold
    procs_critical_min:
        description:
          - The minimum process critical threshold
    procs_warning_max:
        description:
          - The maximum process warning threshold
    procs_warning_min:
        description:
          - The minimum process warning threshold
    discover_parallel_request:
        description:
          - Sets the number of possible parallel requests
    discover_retries:
        description:
          - Sets the number of discovery retries
    discover_timeout:
        description:
          - Sets the discover timeout
"""

EXAMPLES = """
- name: thola check server
  thola_check_server_facts:
    ansible_host: '{{ ansible_host }}'
    community: '{{ community }}'
    version: '{{ version }}'
    port: '{{ port }}'
    critical_max: '{{ critical_max }}'
    critical_min: '{{ critical_min }}'
    warning_max: '{{ warning_max }}'
    warning_min:  '{{ warning_min }}'
    discover_parallel_request: '{{ discover_parallel_request }}'
    discover_retries: '{{ discover_retries }}'
    discover_timeout: '{{ discover_timeout }}'
    user_critical_max: '{{ user_critical_max }}'
    user_critical_min: '{{ user_critical_min }}'
    user_warning_max: '{{ user_warning_max }}'
    user_warning_min: '{{ user_warning_min }}'
    procs_critical_max: '{{ procs_critical_max }}'
    procs_critical_min: '{{ procs_critical_min }}'
    procs_warning_max: '{{ procs_warning_max }}'
    procs_warning_min: '{{ procs_warning_min }}'
  register: result '{{ user_critical_max }}'
"""

RETURN = """
changed:
    description: "whether the command has been executed on the device"
    returned: always
    type: bool
    sample: True
thola_check_server_facts:
    description: "Server facts"
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
            api_host=dict(type="str", required=True),
            ansible_host=dict(type="str", required=True),
            community=dict(type="str", required=False),
            version=dict(type="str", required=False),
            port=dict(type="int", required=False),
            user_critical_max=dict(type="int", required=False),
            user_critical_min=dict(type="int", required=False),
            user_warning_max=dict(type="int", required=False),
            user_warning_min=dict(type="int", required=False),
            procs_critical_max=dict(type="int", required=False),
            procs_critical_min=dict(type="int", required=False),
            procs_warning_max=dict(type="int", required=False),
            procs_warning_min=dict(type="int", required=False),
            discover_parallel_request=dict(type="int", required=False),
            discover_retries=dict(type="int", required=False),
            discover_timeout=dict(type="int", required=False)
        ),
        supports_check_mode=True,
    )

    if not thola_client_found:
        module.fail_json("The thola-client-module is not installed")

    ansible_host = module.params["ansible_host"]
    api_host = module.params["api_host"]

    argument_check = {"ansible_host": ansible_host, "api_host": api_host}
    for key, val in argument_check.items():
        if val is None:
            module.fail_json(msg=str(key) + " is required")
            return

    if module.params["version"] is None:
        version = None
    else:
        version = module.params["version"]
    if module.params["community"] is None:
        community = None
    else:
        community = module.params["community"]
    if module.params["user_critical_max"] is None:
        user_critical_max = None
    else:
        user_critical_max = module.params["user_critical_max"]
    if module.params["user_critical_min"] is None:
        user_critical_min = None
    else:
        user_critical_min = module.params["user_critical_min"]
    if module.params["user_warning_max"] is None:
        user_warning_max = None
    else:
        user_warning_max = module.params["user_warning_max"]
    if module.params["user_warning_min"] is None:
        user_warning_min = None
    else:
        user_warning_min = module.params["user_warning_min"]
    if module.params["procs_critical_max"] is None:
        procs_critical_max = None
    else:
        procs_critical_max = module.params["procs_critical_max"]
    if module.params["procs_critical_min"] is None:
        procs_critical_min = None
    else:
        procs_critical_min = module.params["procs_critical_min"]
    if module.params["procs_warning_max"] is None:
        procs_warning_max = None
    else:
        procs_warning_max = module.params["procs_warning_max"]
    if module.params["procs_warning_min"] is None:
        procs_warning_min = None
    else:
        procs_warning_min = module.params["procs_warning_min"]
    if module.params["port"] is None:
        port = None
    else:
        port = module.params["port"]
    if module.params["discover_parallel_request"] is None:
        discover_parallel_request = None
    else:
        discover_parallel_request = module.params["discover_parallel_request"]
    if module.params["discover_retries"] is None:
        discover_retries = None
    else:
        discover_retries = module.params["discover_retries"]
    if module.params["discover_timeout"] is None:
        discover_timeout = None
    else:
        discover_timeout = module.params["discover_timeout"]

    body = thola_client.CheckServerRequest(
        procs_threshold=thola_client.models.Thresholds(
            critical_max=user_critical_max,
            critical_min=user_critical_min,
            warning_max=user_warning_max,
            warning_min=user_warning_min
        ),
        users_threshold=thola_client.models.Thresholds(
            critical_max=procs_critical_max,
            critical_min=procs_critical_min,
            warning_max=procs_warning_max,
            warning_min=procs_warning_min
        ),
        device_data=thola_client.DeviceData(
            ip_address=ansible_host,
            connection_data=thola_client.ConnectionData(
                snmp=thola_client.SNMPConnectionData(
                    communities=[community],
                    versions=[version],
                    ports=[port],
                    discover_retries=discover_retries,
                    discover_timeout=discover_timeout,
                    discover_parallel_requests=discover_parallel_request
                )
            )
        )
    )

    check_api = check.CheckApi()
    check_api.api_client.configuration.host = api_host
    result = check_api.check_server(body=body).__str__().replace("\'", "\"").replace("None", "null")
    try:
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        module.fail_json("Repsonse couldn't be parsed")
        return

    results = {"changed": False, "ansible_facts": result_dict}
    module.exit_json(**results)


if __name__ == "__main__":
    main()
