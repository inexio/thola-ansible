# Thola-ansible

This is a [collection](https://galaxy.ansible.com/inexio/thola) of ansible modules that uses Thola to retrieve data about network devices.
Thola is a new open source tool for identifying, reading and monitoring network devices.

If you are interested in Thola have a look at our [website](https://thola.io/) and
the [repository](https://github.com/inexio/thola).

## Modules
Modules are separated in read, check and identify. Currently the following modules are available:

### Read Modules

Module                                   | Description
-----------------------------------------|---------------------------------------------------------
``thola_check_cpu_load_facts``           | Checks the CPU load of a device
``thola_check_disk_facts``               | Checks the disk usage of a device
``thola_check_hardware_health_facts``    | Checks the hardware health of a device
``thola_check_identify_facts``           | Checks if identify matches some expectations
``thola_check_interface_metrics_facts``  | Checks the interfaces of a device
``thola_check_memory_usage_facts``       | Checks the memory usage of a device
``thola_check_sbc_facts``                | Checks an SBC device
``thola_check_server_facts``             | Checks a linux server
``thola_check_snmp_facts``               | Checks SNMP availibility
``thola_check_ups_facts``                | Checks whether a UPS device has its main voltage applied

### Check Modules

Module                                    | Description
------------------------------------------|---------------------------------------------------------
``thola_read_available_components_facts`` | Reads the available components for the device
``thola_read_count_interfaces_facts``     | Counts the interfaces of a device
``thola_read_cpu_load_facts``             | Reads the CPU load of a device
``thola_read_disk_facts``                 | Reads the disk of a device
``thola_read_hardware_health_facts``      | Reads the hardware health of a device
``thola_read_interfaces_facts``           | Reads the interfaces of a device
``thola_read_memory_usage_facts``         | Reads the memory usage of a device
``thola_read_sbc_facts``                  | Reads values of an sbc device
``thola_read_server_facts``               | Reads the server values of a device
``thola_read_ups_facts``                  | Reads values of a ups device

### Identify Module

Module                   | Description
-------------------------|---------------------------------------------------------
``thola_identify_facts`` | Identifies properties of a device

## Requirements
To be able to execute the module properly, you have to run a thola API.
If you don't know how to install / run it have a look at [this section](https://github.com/inexio/thola-ansible#how-to-run-a-thola-api)

You also need to have the thola-client python module installed on your system.
This can be done by the following command:

    pip install thola-client

## How to run a Thola API

Installation instructions can be found [here](https://docs.thola.io/getting-started/installing-the-binaries/).

To run the api take a look at [this page](https://docs.thola.io/getting-started/api-mode/).

## Example
### Inventory file:
```INI
[devices]
device1 ansible_host="192.168.178.1" snmp_community="public" snmp_version="2c" snmp_port=161
```
### Playbook file:
```YAML
- name: "thola identify some facts"
  hosts: devices
  gather_facts: no
  tasks:
    - name: Gather facts (thola)
      inexio.thola.thola_identify_facts:
        host: "{{ ansible_host }}"
        api_host: 'http://localhost:8237'
        community: "{{ snmp_community }}"          # Default: "public"
        version: "{{ snmp_version }}"              # Default: "2c"
        port: "{{ snmp_port }}"                    # Default:  161

    - name: Print gathered facts
      debug:
        var: ansible_facts
```

### Playbook Output:
```INI
$ ansible-playbook identify_playbook.yml

PLAY [thola identify facts] ****************************
                                                 
TASK [Gather facts (thola)] ****************************
                                               
TASK [Print gathered facts] ****************************
ok: [cisco7200] => {
    "ansible_facts": {
        "net_model": "7206VXR",
        "net_model_series": "7206",
        "net_os": "ios",
        "net_serialnum": "4279212345",
        "net_system": "ios",
        "net_vendor": "Cisco",
        "net_version": "12.4(24)T5"
    }
}

device1 : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

## Nautobot Integration

Thola's Ansible module can be used to inventory your network devices into an existing Nautobot instance.
The following example shows how to add basic property information (e.g. os, version) to a device in Nautobot.

```YAML
- name: "thola add to nautobot"
  hosts: devices
  gather_facts: no
  tasks:
    - name: Gather facts (thola)
      inexio.thola.thola_identify_facts:
        host: "{{ ansible_host }}"
        api_host: 'http://localhost:8237'
        community: "{{ snmp_community }}"
        version: "{{ snmp_version }}"
        port: "{{ snmp_port }}"
        
    - name: Add gathered data
      networktocode.nautobot.device:
        url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
        token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
        data:
          name: "{{ inventory_hostname }}"
          custom_fields:
            system: "{{ ansible_facts['net_system'] }}"
            os_family: "{{ ansible_facts['net_os'] }}"
            distribution: "{{ ansible_facts['net_os'] }}"
            distribution_version: "{{ ansible_facts['net_version'] }}"
            serialnumber: "{{ ansible_facts['net_serialnum'] }}"
          status: active
        state: present
        validate_certs: False
```