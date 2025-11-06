from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema
from cartography.models.core.relationships import (
    CartographyRelProperties,
    CartographyRelSchema,
    LinkDirection,
    TargetNodeMatcher,
    make_target_node_matcher,
    OtherRelationships,
)
from .common import ResourceToOktaOrgRel


@dataclass(frozen=True)
class OktaUserFactorNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    factor_type: PropertyRef = PropertyRef("factor_type")
    provider: PropertyRef = PropertyRef("provider")
    status: PropertyRef = PropertyRef("status")
    created: PropertyRef = PropertyRef("created")
    okta_last_updated: PropertyRef = PropertyRef("okta_last_updated")
    user_id: PropertyRef = PropertyRef("user_id")


@dataclass(frozen=True)
class FactorToUserRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class FactorToUserRel(CartographyRelSchema):
    target_node_label: str = "OktaUser"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("user_id"),
    })
    rel_label: str = "FACTOR"
    direction: LinkDirection = LinkDirection.INWARD  # OktaUser -> Factor
    properties: FactorToUserRelProps = FactorToUserRelProps()


@dataclass(frozen=True)
class OktaUserFactorSchema(CartographyNodeSchema):
    label: str = "OktaUserFactor"
    properties: OktaUserFactorNodeProperties = OktaUserFactorNodeProperties()
    sub_resource_relationship: ResourceToOktaOrgRel = ResourceToOktaOrgRel()
    other_relationships: OtherRelationships = OtherRelationships([
        FactorToUserRel(),
    ])

