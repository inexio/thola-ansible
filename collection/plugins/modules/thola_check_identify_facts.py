import json
import sys

import urllib3
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = """
---
module: thola_check_identify_facts
author: "Thola team"
version_added: "1.0.0"
short_description: "Checks if identify matches the expected properties"
description:
    - "Checks if identify matches the expected properties for a given device"
requirements:
    - thola-client-module-python
options:
    api_host:
        description:
          - Hostname of the running Thola API instance
        required: True
    host:
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
    device_class:
        description:
          - The expected class when identify is run
    model:
        description:
          - The expected model when identify is run
    model_series:
        description:
          - The expected model series when identify is run
    os_version:
        description:
          - The expected os version when identify is run
    serial_number:
        description:
          - The expected serial number when identify is run
    vendor:
        description:
          - The expected vendor when identify is run
    model_diff_warning:
        description:
          - Show warning when model differs
    model_series_diff_warning:
        description:
          - Show warning when model series differs
    os_diff_warning:
        description:
          - Show warning when OS differs
    os_version_diff_warning:
        description:
          - Show warning when OS version differs
    serial_number_diff_warning:
        description:
          - Show warning when serial number differs
    vendor_diff_warning:
        description:
          - Show warning when vendor differs
"""

EXAMPLES = """
- name: thola check identify
  thola_check_identify_facts:
    api_host: '{{ api_host }}'
    host: '{{ host }}'
    community: '{{ community }}'
    version: '{{ version }}'
    port: '{{ port }}'
    discover_parallel_request: '{{ discover_parallel_request }}'
    discover_retries: '{{ discover_retries }}'
    discover_timeout: '{{ discover_timeout }}'
    device_class: '{{ class }}'
    model: '{{ model }}'
    model_series: '{{ model_series }}'
    os_version: '{{ os_version }}'
    serial_number: '{{ serial_number }}'
    vendor: '{{ vendor }}'
    model_diff_warning: '{{ model_diff_warning }}'
    model_series_diff_warning: '{{ model_series_diff_warning }}'
    os_diff_warning: '{{ os_diff_warning }}'
    os_version_diff_warning: '{{ os_version_diff_warning }}'
    serial_number_diff_warning: '{{ serial_number_diff_warning }}'
    vendor_diff_warning: '{{ vendor_diff_warning }}'
  register: result '{{ discover_timeout }}'
"""

RETURN = """
changed:
    description: "whether the command has been executed on the device"
    returned: always
    type: bool
    sample: True
thola_check_identify_facts:
    description: "Whether expected values were correct"
    returned: always
    type: dict
"""

def change_quotation_marks(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                change_quotation_marks(value)
            elif isinstance(value, str):
                obj[key] = obj[key].replace("\"", "'")
    else:
        pass
    return obj

thola_client_found = False
try:
    import thola_client.api.check_api as check
    import thola_client.rest as rest
    import thola_client

    thola_client_found = True
except ImportError:
    pass


def change_property_names(properties):
    properties["ansible_net_model"] = properties["model"]
    del properties["model"]
    properties["ansible_net_version"] = properties["os_version"]
    del properties["os_version"]
    properties["ansible_net_serialnum"] = properties["serial_number"]
    del properties["serial_number"]
    properties["ansible_net_vendor"] = properties["vendor"]
    del properties["vendor"]
    properties["ansible_net_model_series"] = properties["model_series"]
    del properties["model_series"]
    return properties


def main():
    sys.stderr = None
    module = AnsibleModule(
        argument_spec=dict(
            api_host=dict(type="str", required=True),
            host=dict(type="str", required=True),
            community=dict(type="str", required=False),
            version=dict(type="str", required=False),
            port=dict(type="int", required=False),
            discover_parallel_request=dict(type="int", required=False),
            discover_retries=dict(type="int", required=False),
            discover_timeout=dict(type="int", required=False),
            device_class=dict(type="str", required=False),
            model=dict(type="str", required=False),
            model_series=dict(type="str", required=False),
            os_version=dict(type="str", required=False),
            serial_number=dict(type="str", required=False),
            vendor=dict(type="str", required=False),
            model_diff_warning=dict(type="bool", required=False),
            model_series_diff_warning=dict(type="bool", required=False),
            os_diff_warning=dict(type="bool", required=False),
            os_version_diff_warning=dict(type="bool", required=False),
            serial_number_diff_warning=dict(type="bool", required=False),
            vendor_diff_warning=dict(type="bool", required=False)
        ),
        supports_check_mode=True,
    )

    if not thola_client_found:
        module.fail_json("The thola-client-module is not installed")

    host = module.params["host"]
    api_host = module.params["api_host"]

    argument_check = {"host": host, "api_host": api_host}
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
        port = 161
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

    # properties
    if module.params["device_class"] is None:
        device_class = None
    else:
        device_class = module.params["device_class"]
    if module.params["model"] is None:
        model = None
    else:
        model = module.params["model"]
    if module.params["model_series"] is None:
        model_series = None
    else:
        model_series = module.params["model_series"]
    if module.params["os_version"] is None:
        os_version = None
    else:
        os_version = module.params["os_version"]
    if module.params["serial_number"] is None:
        serial_number = None
    else:
        serial_number = module.params["serial_number"]
    if module.params["vendor"] is None:
        vendor = None
    else:
        vendor = module.params["vendor"]

    # warnings
    if module.params["model_diff_warning"] is None:
        model_diff_warning = None
    else:
        model_diff_warning = module.params["model_diff_warning"]
    if module.params["model_series_diff_warning"] is None:
        model_series_diff_warning = None
    else:
        model_series_diff_warning = module.params["model_series_diff_warning"]
    if module.params["os_diff_warning"] is None:
        os_diff_warning = None
    else:
        os_diff_warning = module.params["os_diff_warning"]
    if module.params["os_version_diff_warning"] is None:
        os_version_diff_warning = None
    else:
        os_version_diff_warning = module.params["os_version_diff_warning"]
    if module.params["serial_number_diff_warning"] is None:
        serial_number_diff_warning = None
    else:
        serial_number_diff_warning = module.params["serial_number_diff_warning"]
    if module.params["vendor_diff_warning"] is None:
        vendor_diff_warning = None
    else:
        vendor_diff_warning = module.params["vendor_diff_warning"]

    if device_class is None and model is None and model_series is None and os_version is None and serial_number is None and vendor is None:
        module.fail_json("One of the following parameters must be set:"
                         " device_class,"
                         " model,"
                         " model_series,"
                         " os_version,"
                         " serial_number,"
                         " vendor")

    body = thola_client.CheckIdentifyRequest(
        device_data=thola_client.DeviceData(
            ip_address=host,
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
        expectations=thola_client.models.Device(
            _class=device_class,
            properties=thola_client.models.Properties(
                model=model,
                model_series=model_series,
                os_version=os_version,
                serial_number=serial_number,
                vendor=vendor
            )
        ),
        model_diff_warning=model_diff_warning,
        model_series_diff_warning=model_series_diff_warning,
        os_diff_warning=os_diff_warning,
        os_version_diff_warning=os_version_diff_warning,
        serial_number_diff_warning=serial_number_diff_warning,
        vendor_diff_warning=vendor_diff_warning
    )

    check_api = check.CheckApi()
    check_api.api_client.configuration.host = api_host
    try:
        result_dict = check_api.check_identify(body=body).to_dict()
    except rest.ApiException as e:
        module.fail_json(**json.loads(e.body))
        return
    except urllib3.exceptions.MaxRetryError:
        module.fail_json("Can't connect to Thola API!")
        return

    result_dict_identify = result_dict["identify_result"]
    result_dict_identify["ansible_net_system"] = result_dict_identify["_class"]
    result_dict_identify["ansible_net_os"] = result_dict_identify["_class"]
    del result_dict_identify["_class"]
    properties = result_dict_identify["properties"]
    del result_dict_identify["properties"]
    updated_properties = change_property_names(properties)
    result_dict_identify.update(updated_properties)
    result_dict["identify_result"] = result_dict_identify

    if result_dict["status_code"] == 0:
        result_dict = change_quotation_marks(result_dict)
        results = {"changed": False, "ansible_facts": result_dict}
        module.exit_json(**results)
    else:
        result_dict = change_quotation_marks(result_dict)
        results = {"changed": False, "ansible_facts": result_dict["raw_output"]}
        module.fail_json(results)


if __name__ == "__main__":
    main()
