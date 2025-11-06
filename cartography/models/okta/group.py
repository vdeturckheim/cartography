from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from .common import ResourceToOktaOrgRel


@dataclass(frozen=True)
class OktaGroupNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    name: PropertyRef = PropertyRef("name")
    description: PropertyRef = PropertyRef("description")
    sam_account_name: PropertyRef = PropertyRef("sam_account_name")
    dn: PropertyRef = PropertyRef("dn")
    windows_domain_qualified_name: PropertyRef = PropertyRef("windows_domain_qualified_name")
    external_id: PropertyRef = PropertyRef("external_id")


@dataclass(frozen=True)
class OktaGroupSchema(CartographyNodeSchema):
    label: str = "OktaGroup"
    properties: OktaGroupNodeProperties = OktaGroupNodeProperties()
    sub_resource_relationship: ResourceToOktaOrgRel = ResourceToOktaOrgRel()

