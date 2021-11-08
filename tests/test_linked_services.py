import unittest

from adf_validator.cli.models.linked_service import LinkedService

class TestAzureBlobFSConfiguration(unittest.TestCase):

    def test_minimal_required_valid_input_should_return_linked_service(self):
        data = {
            "name": "datalake",
            "properties": {
                "annotations": [],
                "type": "AzureBlobFS",
                "typeProperties": {
                },
                "connectVia": {
                    "referenceName": "AutoResolveIntegrationRuntime",
                    "type": "IntegrationRuntimeReference"
                }
            }
        }
        ls = LinkedService().load(data)
