import sys
from unittest import TestCase

import urllib3


class IdentifyTests(TestCase):
    def test_no_connection(self):
        import thola_client
        import thola_client.api.identify_api as identify
        import thola_client.rest as rest

        sys.stderr = None

        ansible_host = "demo-snmp.thola.io"
        api_host = "http://127.0.0.1:8236"
        community = "public"
        version = "2c"
        port = 161
        discover_retries = None
        discover_timeout = None
        discover_parallel_request = None

        body = thola_client.CheckIdentifyRequest(
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
        )

        identify_api = identify.IdentifyApi()
        identify_api.api_client.configuration.host = api_host
        try:
            result = identify_api.identify(body=body).to_dict()
        except rest.ApiException as e:
            result = e.body
        except urllib3.exceptions.MaxRetryError:
            result = "No connection"
        self.assertEqual(result, "No connection")

    def test_invalid_query(self):
        import thola_client
        import thola_client.api.identify_api as identify
        import thola_client.rest as rest

        sys.stderr = None

        ansible_host = "demo-snmp.thola.io"
        api_host = "http://127.0.0.1:8237"
        community = "public"
        version = "2c"
        port = 161
        discover_retries = None
        discover_timeout = None
        discover_parallel_request = None

        body = thola_client.CheckIdentifyRequest(
            device_data=thola_client.DeviceData(
                ip_address=ansible_host,
                connection_data=thola_client.ConnectionData(
                    snmp=thola_client.SNMPConnectionData(
                        communities=[community],
                        versions=[version],
                        ports=port,
                        discover_retries=discover_retries,
                        discover_timeout=discover_timeout,
                        discover_parallel_requests=discover_parallel_request
                    )
                )
            ),
        )

        identify_api = identify.IdentifyApi()
        identify_api.api_client.configuration.host = api_host
        try:
            result = identify_api.identify(body=body).to_dict()
        except rest.ApiException as e:
            result = e.body
        except urllib3.exceptions.MaxRetryError:
            result = "No connection"
        self.assertIn(
            "{\"message\":\"Unmarshal type error: expected=[]int, got=number, field=device_data.connection_data.snmp.ports",
            result)

    def test_valid_query(self):
        import thola_client
        import thola_client.api.identify_api as identify
        import thola_client.rest as rest

        sys.stderr = None

        ansible_host = "demo-snmp.thola.io"
        api_host = "http://127.0.0.1:8237"
        community = "public"
        version = "2c"
        port = 161
        discover_retries = None
        discover_timeout = None
        discover_parallel_request = None

        body = thola_client.CheckIdentifyRequest(
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
        )

        identify_api = identify.IdentifyApi()
        identify_api.api_client.configuration.host = api_host
        try:
            result = identify_api.identify(body=body).to_dict()
        except rest.ApiException as e:
            result = e.body
        except urllib3.exceptions.MaxRetryError:
            result = "No connection"
        self.assertDictEqual({'_class': 'linux', 'properties':
                             {'model': None, 'model_series': None, 'os_version': None, 'serial_number': None, 'vendor': None}},
                             result)
