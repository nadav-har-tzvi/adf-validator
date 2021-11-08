from .base import DataFactoryEntity, DataFactoryProperties, DataFactoryResource, EntityReference
from marshmallow import fields, Schema
from marshmallow_oneofschema import OneOfSchema

#region ActivityBase

class UserProperty(Schema):
    name = fields.Str(required=True)
    value = fields.Str(required=True)


class ActivityDependency(Schema):
    activity = fields.Str(required=True)
    dependency_conditions = fields.List(fields.Str(), required=True, data_key='dependencyConditions')


class ActivityPolicy(Schema):
    timeout = fields.Str(required=True)
    retry = fields.Int(required=True)
    retry_interval_in_seconds = fields.Int(required=True, data_key='retryIntervalInSeconds')
    secure_output = fields.Bool(required=True, data_key='secureOutput')
    secure_input = fields.Bool(required=True, data_key='secureInput')


class Activity(DataFactoryEntity):
    name = fields.Str(required=True)
    depends_on = fields.List(fields.Nested(ActivityDependency), load_default=list, data_key='dependsOn')
    user_properties = fields.List(fields.Nested(UserProperty), load_default=list, data_key='userProperties')
    policy = fields.Nested(ActivityPolicy)

#endregion


class Settings(Schema):
    type = fields.Str(required=True)

#region Sources

class AzureBlobFSReadSettings(Settings):
    recursive = fields.Bool()
    enable_partition_discovery = fields.Bool(required=True, data_key='enablePartitionDiscovery')

class DelimitedTextReadSettings(Settings):
    pass

#endregion
#region Sinks

class AzureBlobFSWriteSettings(Settings):
    pass

class DelimitedTextWriteSettings(Settings):
    quote_all_text = fields.Bool(required=True, data_key='quoteAllText')
    file_extension = fields.Str(required=True, data_key='fileExtension')

#endregion

#region Translators

class TypeConversionSettings(Schema):
    allow_data_truncation = fields.Bool(required=True, data_key='allowDataTruncation')
    treat_boolean_as_number = fields.Bool(required=True, data_key='treatBooleanAsNumber')

class TabularTranslator(DataFactoryEntity):
    type_conversion = fields.Bool(required=True, data_key='typeConversion')
    type_conversion_settings = fields.Nested(TypeConversionSettings, data_key='typeConversionSettings')

#endregion
#region CopyActivity

class StoreSettings(OneOfSchema):
    type_field_remove = False
    type_schemas = {
        "AzureBlobFSReadSettings": AzureBlobFSReadSettings,
        "AzureBlobFSWriteSettings": AzureBlobFSWriteSettings
    }

    def get_obj_type(self, obj):
        if isinstance(obj, AzureBlobFSReadSettings):
            return 'AzureBlobFSReadSettings'
        elif isinstance(obj, AzureBlobFSWriteSettings):
            return 'AzureBlobFSWriteSettings'
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class FormatSettings(OneOfSchema):
    type_field_remove = False
    type_schemas = {
        'DelimitedTextReadSettings': DelimitedTextReadSettings,
        'DelimitedTextWriteSettings': DelimitedTextWriteSettings
    }

    def get_obj_type(self, obj):
        if isinstance(obj, DelimitedTextReadSettings):
            return 'DelimitedTextReadSettings'
        elif isinstance(obj, DelimitedTextWriteSettings):
            return 'DelimitedTextWriteSettings'
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class CopyTargetSettings(Settings):
    store_settings = fields.Nested(StoreSettings, data_key='storeSettings')
    format_settings = fields.Nested(FormatSettings, data_key='formatSettings')


class CopyActivityProperties(Schema):
    source = fields.Nested(CopyTargetSettings, required=True)
    sink = fields.Nested(CopyTargetSettings, required=True)
    enable_staging = fields.Bool(required=True, data_key='enableStaging')
    translator = fields.Nested(TabularTranslator)


class CopyActivity(Activity):
    type_properties = fields.Nested(CopyActivityProperties, data_key='typeProperties')
    inputs = fields.List(fields.Nested(EntityReference), required=True)
    outputs = fields.List(fields.Nested(EntityReference), required=True)

#endregion
#region MetadataActivity

class MetadataProperties(Schema):
    dataset = fields.Nested(EntityReference, required=True)
    field_list = fields.List(fields.Str, required=True, data_key='fieldList')
    store_settings = fields.Nested(AzureBlobFSReadSettings, required=True, data_key='storeSettings')
    format_settings = fields.Nested(DelimitedTextReadSettings, Required=True, data_key='formatSettings')


class MetadataActivity(Activity):
    type_properties = fields.Nested(MetadataProperties, required=True, data_key='typeProperties')


class ActivityOneOf(OneOfSchema):
    type_field_remove = False
    type_schemas = {
        'GetMetadata': MetadataActivity,
        'Copy': CopyActivity
    }

    def get_obj_type(self, obj):
        if isinstance(obj, MetadataActivity):
            return 'GetMetadata'
        elif isinstance(obj, CopyActivity):
            return 'Copy'
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class PipelineProperties(DataFactoryProperties):
    activities = fields.List(fields.Nested(ActivityOneOf))


class Pipeline(DataFactoryResource):
    properties = fields.Nested(PipelineProperties)
