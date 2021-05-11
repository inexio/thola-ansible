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
If you don't know how to install/run it have a look at [this section](#How to use the Thola API)

# Install thola-client
``pip install git+https://github.com/inexio/thola-client-module-python``

# Example
### Inventory file:
```INI
[devices]
device1 ansible_host='192.168.178.1'
```
### Playbook file:
```YAML
- name: thola identify
  hosts: device1
  gather_facts: False
  tasks:
    - name: thola identify facts
      inexio.thola.thola_identify_facts:
        api_host: 'http://api.domain.com:8237'
        community: 'exampleCommunity'
        version: '2c'
        port: 161
        discover_parallel_request: 5
        discover_retries: 0
        discover_timeout: 2
```

### Playbook Output:
```INI
$ ansible-playbook identify_playbook.yml

PLAY [thola identify] *********

TASK [thola identify facts] ****************************
ok: [device1] => {
    "thola_identify_facts": {
        "netsystem": "{{ netsystem }}",
        "net_model": "{{ net_model }}",
        "net_model_series": "{{ net_model_series }}",
        "net_version": "{{ net_version }}",
        "net_serial_number": "{{ net_serial_number }}",
        "net_vendor": "{{ net_vendor }}"}}
    }
    "changed": False
}

device1 : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

### Run the modules

To run the thola modules there has to be a running Thola API somewhere
where you can connect to. The hostname of the running API server must be
stored in ansible_host. You can set this variable in the playbook.

### How to use the Thola API

You can download the latest compiled thola version from its [repository](https://github.com/inexio/thola)
for your platform under the "Releases" tab or build it yourself:

    git clone https://github.com/inexio/thola.git
    cd thola
    go build

**Note: This requires Go 1.16 or newer**

To start a Thola API, simply execute:

    ./thola api

