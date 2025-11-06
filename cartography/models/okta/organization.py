from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema


@dataclass(frozen=True)
class OktaOrganizationNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    name: PropertyRef = PropertyRef("name")


@dataclass(frozen=True)
class OktaOrganizationSchema(CartographyNodeSchema):
    label: str = "OktaOrganization"
    properties: OktaOrganizationNodeProperties = OktaOrganizationNodeProperties()
    scoped_cleanup: bool = False

