from marshmallow import Schema, fields

class EntityReference(Schema):
    reference_name = fields.Str(required=True, data_key='referenceName')
    type = fields.Str(required=True)

class DataFactoryEntity(Schema):
    type = fields.Str(required=True)

class DataFactoryProperties(Schema):
    annotations = fields.List(fields.Str(), load_default=list)

class DataFactoryResource(Schema):
    name = fields.Str(required=True)
