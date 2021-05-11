# thola-ansible

Collection of ansible modules that uses Thola to retrieve data about network devices.

# Modules:
Currently the following modules are available:

- ``thola_check_cpu_load_facts``
- ``thola_check_disk_facts``
- ``thola_check_hardware_health_facts``
- ``thola_check_identify_facts``
- ``thola_check_interface_metrics_facts``
- ``thola_check_memory_usage_facts``
- ``thola_check_sbc_facts``
- ``thola_check_server_facts``
- ``thola_check_snmp_facts``
- ``thola_check_thola_server_facts``
- ``thola_check_ups_facts``
- ``thola_identify_facts``

# Dependencies:
- ``thola-client``

# Requirements
To be able to execute the module properly, you have to run a thola API.
If you don't know how to install/run it have a look at [this section](https://github.com/inexio/thola-ansible#how-to-use-the-thola-api)

# Install thola-client
``pip install git+https://github.com/inexio/thola-client-module-python``

# Example
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
        ansible_host: "{{ ansible_host }}"
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
        "netsystem": "junos"
    }
}

device1 : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

### Run the modules

To run the thola modules there has to be a running Thola API somewhere
where you can connect to. The hostname of the running API server must be
stored in api_host. You can set this variable in the playbook.

### How to use the Thola API

You can download the latest compiled thola version from its [repository](https://github.com/inexio/thola)
for your platform under the "Releases" tab or build it yourself:

    git clone https://github.com/inexio/thola.git
    cd thola
    go build

**Note: This requires Go 1.16 or newer**

To start a Thola API, simply execute:

    ./thola api

More information about Thola and how to use it can be found in our [documentation](https://docs.thola.io/).
