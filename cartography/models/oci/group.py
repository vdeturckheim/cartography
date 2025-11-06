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
)
from .common import ResourceToTenancyRel


@dataclass(frozen=True)
class OCIGroupNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    ocid: PropertyRef = PropertyRef("ocid")
    name: PropertyRef = PropertyRef("name")
    description: PropertyRef = PropertyRef("description")
    createdate: PropertyRef = PropertyRef("createdate")
    compartmentid: PropertyRef = PropertyRef("compartmentid")


@dataclass(frozen=True)
class OCIGroupSchema(CartographyNodeSchema):
    label: str = "OCIGroup"
    properties: OCIGroupNodeProperties = OCIGroupNodeProperties()
    sub_resource_relationship: ResourceToTenancyRel = ResourceToTenancyRel()


@dataclass(frozen=True)
class OCIUserGroupRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    _sub_resource_label: PropertyRef = PropertyRef("_sub_resource_label", set_in_kwargs=True)
    _sub_resource_id: PropertyRef = PropertyRef("_sub_resource_id", set_in_kwargs=True)


@dataclass(frozen=True)
class OCIUserMemberOfGroupMatchLink(CartographyRelSchema):
    target_node_label: str = "OCIGroup"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("group_id"),
    })
    source_node_label: str = "OCIUser"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("user_id"),
    })
    direction: LinkDirection = LinkDirection.OUTWARD
    rel_label: str = "MEMBER_OCID_GROUP"
    properties: OCIUserGroupRelProps = OCIUserGroupRelProps()

