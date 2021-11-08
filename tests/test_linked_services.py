import unittest
from copy import deepcopy

from marshmallow import ValidationError

from adf_validator.cli.handler import validate_linked_services

class TestAzureBlobFSConfiguration(unittest.TestCase):

    valid_data = {
        "name": "datalake",
        "properties": {
            "annotations": [],
            "type": "AzureBlobFS",
            "typeProperties": {
                "url": "https://test.test/"
            },
            "connectVia": {
                "referenceName": "AutoResolveIntegrationRuntime",
                "type": "IntegrationRuntimeReference"
            }
        }
    }

    def test_minimal_required_valid_input_should_return_linked_service(self):
        ls = validate_linked_services([self.valid_data])
        self.assertIsNotNone(ls)

    def test_missing_url_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data['properties']['typeProperties'].pop('url')
        self.assertRaises(ValidationError, validate_linked_services, [data])

    def test_missing_name_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data.pop('name')
        self.assertRaises(ValidationError, validate_linked_services, [data])

    def test_missing_properties_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data.pop('properties')
        self.assertRaises(ValidationError, validate_linked_services, [data])

    def test_missing_annotations_should_validate(self):
        data = deepcopy(self.valid_data)
        data['properties'].pop('annotations')
        ls = validate_linked_services([data])
        self.assertIsNotNone(ls)

    def test_missing_type_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data['properties'].pop('type')
        self.assertRaises(ValidationError, validate_linked_services, [data])

    def test_missing_type_properties_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data['properties'].pop('typeProperties')
        self.assertRaises(ValidationError, validate_linked_services, [data])

    def test_missing_connect_via_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data['properties'].pop('connectVia')
        self.assertRaises(ValidationError, validate_linked_services, [data])

    def test_missing_connect_via_reference_name_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data['properties']['connectVia'].pop('referenceName')
        self.assertRaises(ValidationError, validate_linked_services, [data])
    
    def test_missing_connect_via_type_should_raise_error(self):
        data = deepcopy(self.valid_data)
        data['properties']['connectVia'].pop('type')
        self.assertRaises(ValidationError, validate_linked_services, [data])