from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from .common import RegionSubscriptionRel


@dataclass(frozen=True)
class OCIRegionNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    name: PropertyRef = PropertyRef("name")


@dataclass(frozen=True)
class OCIRegionSchema(CartographyNodeSchema):
    label: str = "OCIRegion"
    properties: OCIRegionNodeProperties = OCIRegionNodeProperties()
    sub_resource_relationship: RegionSubscriptionRel = RegionSubscriptionRel()

