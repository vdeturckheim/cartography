from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties
from cartography.models.core.nodes import CartographyNodeSchema


@dataclass(frozen=True)
class JamfComputerGroupNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    name: PropertyRef = PropertyRef("name")
    is_smart: PropertyRef = PropertyRef("is_smart")


@dataclass(frozen=True)
class JamfComputerGroupSchema(CartographyNodeSchema):
    label: str = "JamfComputerGroup"
    properties: JamfComputerGroupNodeProperties = JamfComputerGroupNodeProperties()
    # No tenant-like object available; perform unscoped cleanup
    scoped_cleanup: bool = False

