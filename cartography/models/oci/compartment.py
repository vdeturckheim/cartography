from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from cartography.models.core.relationships import OtherRelationships

from .common import (
    ResourceToTenancyRel,
    CompartmentParentTenancyRel,
    CompartmentParentCompartmentRel,
)


@dataclass(frozen=True)
class OCICompartmentNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    ocid: PropertyRef = PropertyRef("ocid")
    name: PropertyRef = PropertyRef("name")
    description: PropertyRef = PropertyRef("description")
    createdate: PropertyRef = PropertyRef("createdate")
    parent_tenancy_id: PropertyRef = PropertyRef("parent_tenancy_id")
    parent_compartment_id: PropertyRef = PropertyRef("parent_compartment_id")


@dataclass(frozen=True)
class OCICompartmentSchema(CartographyNodeSchema):
    label: str = "OCICompartment"
    properties: OCICompartmentNodeProperties = OCICompartmentNodeProperties()
    sub_resource_relationship: ResourceToTenancyRel = ResourceToTenancyRel()
    other_relationships: OtherRelationships = OtherRelationships([
        CompartmentParentTenancyRel(),
        CompartmentParentCompartmentRel(),
    ])

