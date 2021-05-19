from unittest import TestCase

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

class ChangeQuotationMarksTests(TestCase):
    def test_fail_output(self):
        dictio = {"changed": False, "msg": {"ansible_facts": "CRITICAL: Vendor: expected: \"Cisco\", got: \"Mikrotik\"", "changed": False}}
        dictio_changed = change_quotation_marks(dictio)
        self.assertDictEqual(dictio_changed, {"changed": False, "msg": {"ansible_facts": "CRITICAL: Vendor: expected: 'Cisco', got: 'Mikrotik'", "changed": False}})
