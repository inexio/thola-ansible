import json

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: thola_check_ups_facts
author: "Thola team"
version_added: "1.0.0"
short_description: "Checks if a UPS device has its main voltage applied"
description:
    - "Checks if a UPS device has its main voltage applied"
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
    battery_current_critical_max:
        description:
          - Sets the critical max threshold for the battery current
    battery_current_critical_min:
        description:
          - Sets the critical min threshold for the battery current
    battery_current_warning_max:
        description:
          - Sets the warning max threshold for the battery current
    battery_current_warning_min:
        description:
          - Sets the warning min threshold for the battery current
    battery_temp_critical_max:
        description:
          - Sets the critical max threshold for the battery temperature
    battery_temp_critical_min:
        description:
          - Sets the critical min threshold for the battery temperature
    battery_temp_warning_max:
        description:
          - Sets the warning max threshold for the battery temperature
    battery_temp_warning_min:
        description:
          - Sets the warning min threshold for the battery temperature
    current_load_critical_max:
        description:
          - Sets the critical max threshold for the current load
    current_load_critical_min:
        description:
          - Sets the critical min threshold for the current load
    current_load_warning_max:
        description:
          - Sets the warning max threshold for the current load
    current_load_warning_min:
        description:
          - Sets the warning min threshold for the current load
    rectifier_current_critical_max:
        description:
          - Sets the critical max threshold for the rectifier current
    rectifier_current_critical_min:
        description:
          - Sets the critical min threshold for the rectifier current
    rectifier_current_warning_max:
        description:
          - Sets the warning max threshold for the rectifier current
    rectifier_current_warning_min:
        description:
          - Sets the warning min threshold for the rectifier current
    system_voltage_critical_max:
        description:
          - Sets the critical max threshold for the system voltage
    system_voltage_critical_min:
        description:
          - Sets the critical min threshold for the system voltage
    system_voltage_warning_max:
        description:
          - Sets the warning max threshold for the system voltage
    system_voltage_warning_min:
        description:
          - Sets the warning min threshold for the system voltage
"""

EXAMPLES = """
- name: thola check ups
  thola_check_ups_facts:
    api_host: '{{ api_host }}'
    ansible_host: '{{ ansible_host }}'
    community: '{{ community }}'
    version: '{{ version }}'
    port: '{{ port }}'
    discover_parallel_request: '{{ discover_parallel_request }}'
    discover_retries: '{{ discover_retries }}'
    discover_timeout: '{{ discover_timeout }}'
    battery_current_critical_max: '{{ battery_current_critical_max }}'
    battery_current_critical_min: '{{ battery_current_critical_min }}'
    battery_current_warning_max: '{{ battery_current_warning_max }}'
    battery_current_warning_min: '{{ battery_current_warning_min }}'
    battery_temp_critical_max: '{{ battery_temp_critical_max }}'
    battery_temp_critical_min: '{{ battery_temp_critical_min }}'
    battery_temp_warning_max: '{{ battery_temp_warning_max }}'
    battery_temp_warning_min: '{{ battery_temp_warning_min }}'
    current_load_critical_max: '{{ current_load_critical_max }}'
    current_load_critical_min: '{{ current_load_critical_min }}'
    current_load_warning_max: '{{ current_load_warning_max }}'
    current_load_warning_min: '{{ current_load_warning_min }}'
    rectifier_current_critical_max: '{{ rectifier_current_critical_max }}'
    rectifier_current_critical_min: '{{ rectifier_current_critical_min }}'
    rectifier_current_warning_max: '{{ rectifier_current_warning_max }}'
    rectifier_current_warning_min: '{{ rectifier_current_warning_min }}'
    system_voltage_critical_max: '{{ system_voltage_critical_max }}'
    system_voltage_critical_min: '{{ system_voltage_critical_min }}'
    system_voltage_warning_max: '{{ system_voltage_warning_max }}'
    system_voltage_warning_min: '{{ system_voltage_warning_min }}'
  register: result
"""

RETURN = """
changed:
    description: "whether the command has been executed on the device"
    returned: always
    type: bool
    sample: True
thola_check_ups_facts:
    description: "UPS facts"
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
            battery_current_critical_max=dict(type="int", required=False),
            battery_current_critical_min=dict(type="int", required=False),
            battery_current_warning_max=dict(type="int", required=False),
            battery_current_warning_min=dict(type="int", required=False),
            battery_temp_critical_max=dict(type="int", required=False),
            battery_temp_critical_min=dict(type="int", required=False),
            battery_temp_warning_max=dict(type="int", required=False),
            battery_temp_warning_min=dict(type="int", required=False),
            current_load_critical_max=dict(type="int", required=False),
            current_load_critical_min=dict(type="int", required=False),
            current_load_warning_max=dict(type="int", required=False),
            current_load_warning_min=dict(type="int", required=False),
            rectifier_current_critical_max=dict(type="int", required=False),
            rectifier_current_critical_min=dict(type="int", required=False),
            rectifier_current_warning_max=dict(type="int", required=False),
            rectifier_current_warning_min=dict(type="int", required=False),
            system_voltage_critical_max=dict(type="int", required=False),
            system_voltage_critical_min=dict(type="int", required=False),
            system_voltage_warning_max=dict(type="int", required=False),
            system_voltage_warning_min=dict(type="int", required=False)
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

    # battery current thresholds
    if module.params["battery_current_critical_max"] is None:
        battery_current_critical_max = None
    else:
        battery_current_critical_max = module.params["battery_current_critical_max"]
    if module.params["battery_current_critical_min"] is None:
        battery_current_critical_min = None
    else:
        battery_current_critical_min = module.params["battery_current_critical_min"]
    if module.params["battery_current_warning_max"] is None:
        battery_current_warning_max = None
    else:
        battery_current_warning_max = module.params["battery_current_warning_max"]
    if module.params["battery_current_warning_min"] is None:
        battery_current_warning_min = None
    else:
        battery_current_warning_min = module.params["battery_current_warning_min"]

    # battery temperature thresholds
    if module.params["battery_temp_critical_max"] is None:
        battery_temp_critical_max = None
    else:
        battery_temp_critical_max = module.params["battery_temp_critical_max"]
    if module.params["battery_temp_critical_min"] is None:
        battery_temp_critical_min = None
    else:
        battery_temp_critical_min = module.params["battery_temp_critical_min"]
    if module.params["battery_temp_warning_max"] is None:
        battery_temp_warning_max = None
    else:
        battery_temp_warning_max = module.params["battery_temp_warning_max"]
    if module.params["battery_temp_warning_min"] is None:
        battery_temp_warning_min = None
    else:
        battery_temp_warning_min = module.params["battery_temp_warning_min"]

    # current load thresholds
    if module.params["current_load_critical_max"] is None:
        current_load_critical_max = None
    else:
        current_load_critical_max = module.params["current_load_critical_max"]
    if module.params["current_load_critical_min"] is None:
        current_load_critical_min = None
    else:
        current_load_critical_min = module.params["current_load_critical_min"]
    if module.params["current_load_warning_max"] is None:
        current_load_warning_max = None
    else:
        current_load_warning_max = module.params["current_load_warning_max"]
    if module.params["current_load_warning_min"] is None:
        current_load_warning_min = None
    else:
        current_load_warning_min = module.params["current_load_warning_min"]

    # rectifier current thresholds
    if module.params["rectifier_current_critical_max"] is None:
        rectifier_current_critical_max = None
    else:
        rectifier_current_critical_max = module.params["rectifier_current_critical_max"]
    if module.params["rectifier_current_critical_min"] is None:
        rectifier_current_critical_min = None
    else:
        rectifier_current_critical_min = module.params["rectifier_current_critical_min"]
    if module.params["rectifier_current_warning_max"] is None:
        rectifier_current_warning_max = None
    else:
        rectifier_current_warning_max = module.params["rectifier_current_warning_max"]
    if module.params["rectifier_current_warning_min"] is None:
        rectifier_current_warning_min = None
    else:
        rectifier_current_warning_min = module.params["rectifier_current_warning_min"]

    # system voltage thresholds
    if module.params["system_voltage_critical_max"] is None:
        system_voltage_critical_max = None
    else:
        system_voltage_critical_max = module.params["system_voltage_critical_max"]
    if module.params["system_voltage_critical_min"] is None:
        system_voltage_critical_min = None
    else:
        system_voltage_critical_min = module.params["system_voltage_critical_min"]
    if module.params["system_voltage_warning_max"] is None:
        system_voltage_warning_max = None
    else:
        system_voltage_warning_max = module.params["system_voltage_warning_max"]
    if module.params["system_voltage_warning_min"] is None:
        system_voltage_warning_min = None
    else:
        system_voltage_warning_min = module.params["system_voltage_warning_min"]

    body = thola_client.CheckUPSRequest(
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
        battery_current_thresholds=thola_client.models.Thresholds(
            critical_max=battery_current_critical_max,
            critical_min=battery_current_critical_min,
            warning_max=battery_current_warning_max,
            warning_min=battery_current_warning_min
        ),
        battery_temperature_thresholds=thola_client.models.Thresholds(
            critical_max=battery_temp_critical_max,
            critical_min=battery_temp_critical_min,
            warning_max=battery_temp_warning_max,
            warning_min=battery_temp_warning_min
        ),
        current_load_thresholds=thola_client.models.Thresholds(
            critical_max=current_load_critical_max,
            critical_min=current_load_critical_min,
            warning_max=current_load_warning_max,
            warning_min=current_load_warning_min
        ),
        rectifier_current_thresholds=thola_client.models.Thresholds(
            critical_max=rectifier_current_critical_max,
            critical_min=rectifier_current_critical_min,
            warning_max=rectifier_current_warning_max,
            warning_min=rectifier_current_warning_min
        ),
        system_voltage_thresholds=thola_client.models.Thresholds(
            critical_max=system_voltage_critical_max,
            critical_min=system_voltage_critical_min,
            warning_max=system_voltage_warning_max,
            warning_min=system_voltage_warning_min
        )
    )

    check_api = check.CheckApi()
    check_api.api_client.configuration.host = api_host
    result = check_api.check_ups(body=body).__str__().replace("\'", "\"").replace("None", "null")
    try:
        result_dict = json.loads(result)
    except json.JSONDecodeError:
        module.fail_json("Repsonse couldn't be parsed")
        return

    results = {"changed": False, "ansible_facts": result_dict}
    module.exit_json(**results)


if __name__ == "__main__":
    main()
