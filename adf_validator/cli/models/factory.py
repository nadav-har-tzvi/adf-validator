import enum
from marshmallow import fields
from marshmallow.schema import Schema
from marshmallow import validate

from .base import DataFactoryResource

class IdentityType(enum.Enum):
    SystemAssigned = "SystemAssigned"


class IdentityProperties(Schema):
    type = fields.Str(validate=validate.OneOf([e.value for e in IdentityType]))
    principal_id = fields.UUID(data_key='principalId')
    tenant_id = fields.UUID(data_key='tenantId')


class Factory(DataFactoryResource):
    location = fields.Str(required=True)
    identity = fields.Nested(IdentityProperties)