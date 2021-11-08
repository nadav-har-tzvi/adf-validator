from marshmallow import fields, validate, Schema
from .base import DataFactoryResource, EntityReference, DataFactoryProperties
from marshmallow_oneofschema import OneOfSchema


class AzureBlobFSLocation(Schema):
    type = fields.Str(required=True)
    file_name = fields.Str(required=True, data_key='fileName')
    file_system = fields.Str(required=True, data_key='fileSystem')

class DataSetLocation(OneOfSchema):
    type_field_remove = False
    type_schemas = {
        'AzureBlobFSLocation': AzureBlobFSLocation
    }

    def get_obj_type(self, obj):
        try:
            return [key for key, type in self.type_schemas.items() if isinstance(obj, type)][0]
        except IndexError:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))
    

class DelimitedTextProperties(Schema):
    location = fields.Nested(DataSetLocation)
    column_delimiter = fields.Str(required=True, data_key='columnDelimiter')
    escape_char = fields.Str(required=True, data_key='escapeChar')
    first_row_as_header = fields.Bool(required=True, data_key='firstRowAsHeader')
    quote_char = fields.Str(required=True, data_key='quoteChar')


class SchemaField(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)


class DataSetProperties(DataFactoryProperties):
    linked_service_name = fields.Nested(EntityReference(), required=True, data_key='linkedServiceName')
    type = fields.Str(required=True)
    schema = fields.Nested(SchemaField, many=True, default=lambda: [])


class DelimitedTextDataSet(DataSetProperties):
    type_properties = fields.Nested(DelimitedTextProperties, data_key='typeProperties')


class DataSetPropertiesOneOf(OneOfSchema):
    type_field_remove = False
    type_schemas = {
        'DelimitedText': DelimitedTextDataSet
    }


class DataSet(DataFactoryResource):
    properties = fields.Nested(DataSetPropertiesOneOf)