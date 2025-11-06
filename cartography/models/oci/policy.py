from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from cartography.models.core.relationships import (
    CartographyRelProperties,
    CartographyRelSchema,
    LinkDirection,
    TargetNodeMatcher,
    SourceNodeMatcher,
    make_target_node_matcher,
    make_source_node_matcher,
    OtherRelationships,
)
from .common import ResourceToTenancyRel, PolicyParentCompartmentRel


@dataclass(frozen=True)
class OCIPolicyNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    ocid: PropertyRef = PropertyRef("ocid")
    name: PropertyRef = PropertyRef("name")
    description: PropertyRef = PropertyRef("description")
    createdate: PropertyRef = PropertyRef("createdate")
    updatedate: PropertyRef = PropertyRef("updatedate")
    statements: PropertyRef = PropertyRef("statements")
    policy_parent_compartment_id: PropertyRef = PropertyRef("policy_parent_compartment_id")


@dataclass(frozen=True)
class OCIPolicySchema(CartographyNodeSchema):
    label: str = "OCIPolicy"
    properties: OCIPolicyNodeProperties = OCIPolicyNodeProperties()
    sub_resource_relationship: ResourceToTenancyRel = ResourceToTenancyRel()
    other_relationships: OtherRelationships = OtherRelationships([
        PolicyParentCompartmentRel(),
    ])


@dataclass(frozen=True)
class PolicyToGroupRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    _sub_resource_label: PropertyRef = PropertyRef("_sub_resource_label", set_in_kwargs=True)
    _sub_resource_id: PropertyRef = PropertyRef("_sub_resource_id", set_in_kwargs=True)


@dataclass(frozen=True)
class OCIPolicyToGroupMatchLink(CartographyRelSchema):
    target_node_label: str = "OCIGroup"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("group_id"),
    })
    source_node_label: str = "OCIPolicy"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("policy_id"),
    })
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "OCI_POLICY_REFERENCE"
    properties: PolicyToGroupRelProps = PolicyToGroupRelProps()


@dataclass(frozen=True)
class PolicyToCompartmentRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    _sub_resource_label: PropertyRef = PropertyRef("_sub_resource_label", set_in_kwargs=True)
    _sub_resource_id: PropertyRef = PropertyRef("_sub_resource_id", set_in_kwargs=True)


@dataclass(frozen=True)
class OCIPolicyToCompartmentMatchLink(CartographyRelSchema):
    target_node_label: str = "OCICompartment"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("compartment_id"),
    })
    source_node_label: str = "OCIPolicy"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("policy_id"),
    })
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "OCI_POLICY_REFERENCE"
    properties: PolicyToCompartmentRelProps = PolicyToCompartmentRelProps()

