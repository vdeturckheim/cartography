from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from .common import ResourceToTenancyRel


@dataclass(frozen=True)
class OCIUserNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    ocid: PropertyRef = PropertyRef("ocid")
    name: PropertyRef = PropertyRef("name")
    description: PropertyRef = PropertyRef("description")
    email: PropertyRef = PropertyRef("email")
    lifecycle_state: PropertyRef = PropertyRef("lifecycle_state")
    is_mfa_activated: PropertyRef = PropertyRef("is_mfa_activated")
    can_use_api_keys: PropertyRef = PropertyRef("can_use_api_keys")
    can_use_auth_tokens: PropertyRef = PropertyRef("can_use_auth_tokens")
    can_use_console_password: PropertyRef = PropertyRef("can_use_console_password")
    can_use_customer_secret_keys: PropertyRef = PropertyRef("can_use_customer_secret_keys")
    can_use_smtp_credentials: PropertyRef = PropertyRef("can_use_smtp_credentials")
    createdate: PropertyRef = PropertyRef("createdate")
    compartmentid: PropertyRef = PropertyRef("compartmentid")


@dataclass(frozen=True)
class OCIUserSchema(CartographyNodeSchema):
    label: str = "OCIUser"
    properties: OCIUserNodeProperties = OCIUserNodeProperties()
    sub_resource_relationship: ResourceToTenancyRel = ResourceToTenancyRel()

