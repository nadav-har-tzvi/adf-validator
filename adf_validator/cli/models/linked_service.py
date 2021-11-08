from marshmallow import fields
from marshmallow.schema import Schema
from .base import DataFactoryProperties, DataFactoryResource, EntityReference
from marshmallow_oneofschema import OneOfSchema

class AzureBlobFSTypeProperties(Schema):
    url = fields.Url(required=True)


class AzureBlobFSProperties(DataFactoryProperties):
    type = fields.Str(required=True)
    type_properties = fields.Nested(AzureBlobFSTypeProperties, required=True, data_key='typeProperties')
    connect_via = fields.Nested(EntityReference, required=True, data_key='connectVia')


class LinkedServicePropertiesOneOf(OneOfSchema):
    type_field_remove = False
    type_schemas = {
        'AzureBlobFS': AzureBlobFSProperties
    }

    def get_obj_type(self, obj):
        try:
            return [key for key, type in self.type_schemas.items() if isinstance(obj, type)][0]
        except IndexError:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class LinkedService(DataFactoryResource):
    properties = fields.Nested(LinkedServicePropertiesOneOf, required=True)


