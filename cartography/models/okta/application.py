from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from .common import ResourceToOktaOrgRel


@dataclass(frozen=True)
class OktaApplicationNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    name: PropertyRef = PropertyRef("name")
    label: PropertyRef = PropertyRef("label")
    created: PropertyRef = PropertyRef("created")
    okta_last_updated: PropertyRef = PropertyRef("okta_last_updated")
    status: PropertyRef = PropertyRef("status")
    activated: PropertyRef = PropertyRef("activated")
    features: PropertyRef = PropertyRef("features")
    sign_on_mode: PropertyRef = PropertyRef("sign_on_mode")


@dataclass(frozen=True)
class OktaApplicationSchema(CartographyNodeSchema):
    label: str = "OktaApplication"
    properties: OktaApplicationNodeProperties = OktaApplicationNodeProperties()
    sub_resource_relationship: ResourceToOktaOrgRel = ResourceToOktaOrgRel()


@dataclass(frozen=True)
class ReplyUriNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    uri: PropertyRef = PropertyRef("uri")


@dataclass(frozen=True)
class ReplyUriSchema(CartographyNodeSchema):
    label: str = "ReplyUri"
    properties: ReplyUriNodeProperties = ReplyUriNodeProperties()
    # No sub-resource relationship; these are generic URIs referenced by apps
    scoped_cleanup: bool = False

