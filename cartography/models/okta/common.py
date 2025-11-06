from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.relationships import (
    CartographyRelProperties,
    CartographyRelSchema,
    LinkDirection,
    TargetNodeMatcher,
    SourceNodeMatcher,
    make_target_node_matcher,
    make_source_node_matcher,
)


@dataclass(frozen=True)
class ToOktaOrgRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class ResourceToOktaOrgRel(CartographyRelSchema):
    target_node_label: str = "OktaOrganization"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("OKTA_ORG_ID", set_in_kwargs=True),
    })
    rel_label: str = "RESOURCE"
    direction: LinkDirection = LinkDirection.INWARD
    properties: ToOktaOrgRelProps = ToOktaOrgRelProps()


@dataclass(frozen=True)
class HumanIdentityRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class HumanIdentityOktaRel(CartographyRelSchema):
    target_node_label: str = "Human"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "email": PropertyRef("email"),
    })
    rel_label: str = "IDENTITY_OKTA"
    direction: LinkDirection = LinkDirection.INWARD  # Human -> OktaUser
    properties: HumanIdentityRelProps = HumanIdentityRelProps()


# MatchLinks

@dataclass(frozen=True)
class MatchLinkProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    _sub_resource_label: PropertyRef = PropertyRef("_sub_resource_label", set_in_kwargs=True)
    _sub_resource_id: PropertyRef = PropertyRef("_sub_resource_id", set_in_kwargs=True)


@dataclass(frozen=True)
class OktaUserMemberOfGroupMatchLink(CartographyRelSchema):
    target_node_label: str = "OktaGroup"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("group_id"),
    })
    source_node_label: str = "OktaUser"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("user_id"),
    })
    rel_label: str = "MEMBER_OF_OKTA_GROUP"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()


@dataclass(frozen=True)
class OktaUserApplicationMatchLink(CartographyRelSchema):
    target_node_label: str = "OktaApplication"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("app_id"),
    })
    source_node_label: str = "OktaUser"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("user_id"),
    })
    rel_label: str = "APPLICATION"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()


@dataclass(frozen=True)
class OktaGroupApplicationMatchLink(CartographyRelSchema):
    target_node_label: str = "OktaApplication"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("app_id"),
    })
    source_node_label: str = "OktaGroup"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("group_id"),
    })
    rel_label: str = "APPLICATION"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()


@dataclass(frozen=True)
class OktaApplicationToReplyUriMatchLink(CartographyRelSchema):
    target_node_label: str = "ReplyUri"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("uri"),
    })
    source_node_label: str = "OktaApplication"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("app_id"),
    })
    rel_label: str = "REPLYURI"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()


@dataclass(frozen=True)
class OktaGroupAllowedByAWSRoleMatchLink(CartographyRelSchema):
    target_node_label: str = "AWSRole"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "arn": PropertyRef("role_arn"),
    })
    source_node_label: str = "OktaGroup"
    source_node_matcher: SourceNodeMatcher = make_source_node_matcher({
        "id": PropertyRef("group_id"),
    })
    rel_label: str = "ALLOWED_BY"
    direction: LinkDirection = LinkDirection.OUTWARD
    properties: MatchLinkProps = MatchLinkProps()

