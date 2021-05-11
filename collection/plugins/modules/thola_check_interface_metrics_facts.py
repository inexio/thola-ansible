import json

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: thola_check_interface_metrics_facts
author: "Thola team"
version_added: "1.0.0"
short_description: "Checks the interface metrics for a given device"
description:
    - "Checks the interface metrics for a given device with SNMP"
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
    discover_parallel_request:
        description:
          - Sets the number of possible parallel requests
    discover_retries:
        description:
          - Sets the number of discovery retries
    discover_timeout:
        description:
          - Sets the discover timeout
    ifName_filter:
        description:
          - Filters all interfaces out where ifName matches the regex
    ifType_filter:
          - Filters all interfaces out where ifType matches the regex
"""

EXAMPLES = """
- name: thola check interface metrics
  thola_check_interface_metrics_facts:
    api_host: '{{ api_host }}'
    ansible_host: '{{ ansible_host }}'
    community: '{{ community }}'
    version: '{{ version }}'
    port: '{{ port }}'
    discover_parallel_request: '{{ discover_parallel_request }}'
    discover_retries: '{{ discover_retries }}'
    discover_timeout: '{{ discover_timeout }}'
    ifName_filter: '{{ ifName_filter }}'
    ifType_filter: '{{ ifType_filter }}'
  register: result
"""

RETURN = """
changed:
    description: "whether the command has been executed on the device"
    returned: always
    type: bool
    sample: True
thola_check_interface_metrics_facts:
    description: "Interfeace metrics facts"
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
            discover_parallel_request=dict(type="int", required=False),
            discover_retries=dict(type="int", required=False),
            discover_timeout=dict(type="int", required=False),
            ifName_filter=dict(type="str", required=False),
            ifType_filter=dict(type="str", required=False)
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
        version = "2c"
    else:
        version = module.params["version"]
    if module.params["community"] is None:
        community = "public"
    else:
        community = module.params["community"]
    if module.params["port"] is None:
        port = "161"
    else:
        port = module.params["port"]
    if module.params["discover_parallel_request"] is None:
        discover_parallel_request = 5
    else:
        discover_parallel_request = module.params["discover_parallel_request"]
    if module.params["discover_retries"] is None:
        discover_retries = 0
    else:
        discover_retries = module.params["discover_retries"]
    if module.params["discover_timeout"] is None:
        discover_timeout = 2
    else:
        discover_timeout = module.params["discover_timeout"]

    # ifname filter
    if module.params["ifName_filter"] is None:
        if_name_filter = None
    else:
        if_name_filter = module.params["ifName_filter"]
    if module.params["ifType_filter"] is None:
        if_type_filter = None
    else:
        if_type_filter = module.params["ifName_filter"]

    body = thola_client.CheckInterfaceMetricsRequest(
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
        ),
        if_name_filter=if_name_filter,
        if_type_filter=if_type_filter
    )

    check_api = check.CheckApi()
    check_api.api_client.configuration.host = api_host
    result = check_api.check_interface_metrics(body=body).__str__().replace("\'", "\"").replace("None", "null")
    try:
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        module.fail_json("Repsonse couldn't be parsed")
        return

    results = {"changed": False, "ansible_facts": result_dict}
    module.exit_json(**results)


if __name__ == "__main__":
    main()
