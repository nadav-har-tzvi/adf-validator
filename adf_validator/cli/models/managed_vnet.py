from marshmallow import fields, schema, validate
from .base import DataFactoryResource

class ManagedVnetProperties(schema.Schema):
    prevent_data_exfiltration = fields.Bool(required=True, data_key='preventDataExfiltration')


class ManagedVirtualNetwork(DataFactoryResource):
    type = fields.Str(required=True, validate=validate.Equal('Microsoft.DataFactory/factories/managedvirtualnetworks'))
    properties = fields.Nested(ManagedVnetProperties, required=True)