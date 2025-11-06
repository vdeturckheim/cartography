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
from .common import ResourceToOktaOrgRel, MatchLinkProps


@dataclass(frozen=True)
class OktaAdministrationRoleNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    type: PropertyRef = PropertyRef("type")
    label: PropertyRef = PropertyRef("label")


@dataclass(frozen=True)
class OktaAdministrationRoleSchema(CartographyNodeSchema):
    label: str = "OktaAdministrationRole"
    properties: OktaAdministrationRoleNodeProperties = OktaAdministrationRoleNodeProperties()
    sub_resource_relationship: ResourceToOktaOrgRel = ResourceToOktaOrgRel()


@dataclass(frozen=True)
class OktaUserMemberOfRoleMatchLink(CartographyRelSchema):
    target_node_label: str = "OktaAdministrationRole"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("role_id"),
    })
    source_node_label: str = "OktaUser"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("user_id"),
    })
    rel_label: str = "MEMBER_OF_OKTA_ROLE"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()


@dataclass(frozen=True)
class OktaGroupMemberOfRoleMatchLink(CartographyRelSchema):
    target_node_label: str = "OktaAdministrationRole"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("role_id"),
    })
    source_node_label: str = "OktaGroup"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("group_id"),
    })
    rel_label: str = "MEMBER_OF_OKTA_ROLE"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()

