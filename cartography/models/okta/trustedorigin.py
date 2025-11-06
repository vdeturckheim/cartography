from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from .common import ResourceToOktaOrgRel


@dataclass(frozen=True)
class OktaTrustedOriginNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    name: PropertyRef = PropertyRef("name")
    origin: PropertyRef = PropertyRef("origin")
    scopes: PropertyRef = PropertyRef("scopes")
    status: PropertyRef = PropertyRef("status")
    created: PropertyRef = PropertyRef("created")
    created_by: PropertyRef = PropertyRef("created_by")
    okta_last_updated: PropertyRef = PropertyRef("okta_last_updated")
    okta_last_updated_by: PropertyRef = PropertyRef("okta_last_updated_by")


@dataclass(frozen=True)
class OktaTrustedOriginSchema(CartographyNodeSchema):
    label: str = "OktaTrustedOrigin"
    properties: OktaTrustedOriginNodeProperties = OktaTrustedOriginNodeProperties()
    sub_resource_relationship: ResourceToOktaOrgRel = ResourceToOktaOrgRel()

