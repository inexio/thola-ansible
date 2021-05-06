# thola-ansible

Collection of ansible modules that uses Thola to retrieve data about network devices.

# Modules:
Currently the following modules are available:

- ``thola_check_cpu_load_facts``
- ``thola_check_disk_facts``
- ``thola_check_hardware_health_facts``
- ``thola_check_identify``
- ``thola_check_interface_metrics_facts``
- ``thola_check_memory_usage_facts``
- ``thola_check_sbc_facts``
- ``thola_check_server_facts``
- ``thola_check_snmp_facts``
- ``thola_check_thola_server_facts``
- ``thola_check_ups_facts``
- ``thola_check_identify_facts``

# Dependencies:
- ``thola-client``

# Install thola-client
``pip install git+https://github.com/inexio/thola-client-module-python``
