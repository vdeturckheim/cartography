from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema


@dataclass(frozen=True)
class OCITenancyNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    ocid: PropertyRef = PropertyRef("ocid")
    name: PropertyRef = PropertyRef("name")


@dataclass(frozen=True)
class OCITenancySchema(CartographyNodeSchema):
    label: str = "OCITenancy"
    properties: OCITenancyNodeProperties = OCITenancyNodeProperties()
    scoped_cleanup: bool = False

