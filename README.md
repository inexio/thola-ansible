# Thola-ansible

This is a [collection](https://galaxy.ansible.com/inexio/thola) of ansible modules that uses Thola to retrieve data about network devices.
Thola is an open-source tool for monitoring network devices written in Go.

If you are interested in Thola have a look at our [website](https://thola.io/) and
the [repository](https://github.com/inexio/thola).

## Modules
Currently the following modules are available:

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
``thola_identify_facts``                 | Identifies properties of a device

## Requirements
To be able to execute the module properly, you have to run a thola API.
If you don't know how to install / run it have a look at [this section](https://github.com/inexio/thola-ansible#how-to-run-a-thola-api)

You also need to have the thola-client python module installed on your system.
This can be done by the following command:

    pip install thola-client

## How to run a Thola API

If you want to know how to install Thola have a look at [this page](https://docs.thola.io/getting-started/installing-the-binaries/).

If you don't know how to start a Thola API have a look at our [this page](https://docs.thola.io/getting-started/api-mode/)

## Example
### Inventory file:
```INI
[devices]
device1 ansible_host="192.168.178.1" snmp_community="public" snmp_version="2c" snmp_port=161
```
### Playbook file:
```YAML
- name: "thola identify facts"
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
                                                       
ok: [device1] => {
    "ansible_facts": {
        "net_model": "VMX",
        "net_model_series": null,
        "net_serialnum": "V21FA5ZG2FG9",
        "net_vendor": "Juniper",
        "net_version": null,
        "net_system": "junos"
    }
}

device1 : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```
