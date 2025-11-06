from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.relationships import (
    CartographyRelProperties,
    CartographyRelSchema,
    LinkDirection,
    TargetNodeMatcher,
    make_target_node_matcher,
)


@dataclass(frozen=True)
class ToTenancyRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class ResourceToTenancyRel(CartographyRelSchema):
    target_node_label: str = "OCITenancy"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("OCI_TENANCY_ID", set_in_kwargs=True),
    })
    rel_label: str = "RESOURCE"
    direction: LinkDirection = LinkDirection.INWARD
    properties: ToTenancyRelProps = ToTenancyRelProps()


@dataclass(frozen=True)
class CompartmentParentTenancyRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class CompartmentParentTenancyRel(CartographyRelSchema):
    target_node_label: str = "OCITenancy"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("parent_tenancy_id"),
    })
    rel_label: str = "OCI_COMPARTMENT"
    direction: LinkDirection = LinkDirection.INWARD
    properties: CompartmentParentTenancyRelProps = CompartmentParentTenancyRelProps()


@dataclass(frozen=True)
class CompartmentParentCompartmentRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class CompartmentParentCompartmentRel(CartographyRelSchema):
    target_node_label: str = "OCICompartment"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("parent_compartment_id"),
    })
    rel_label: str = "OCI_COMPARTMENT"
    direction: LinkDirection = LinkDirection.INWARD
    properties: CompartmentParentCompartmentRelProps = CompartmentParentCompartmentRelProps()


@dataclass(frozen=True)
class PolicyParentCompartmentRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class PolicyParentCompartmentRel(CartographyRelSchema):
    target_node_label: str = "OCICompartment"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("policy_parent_compartment_id"),
    })
    rel_label: str = "OCI_POLICY"
    direction: LinkDirection = LinkDirection.INWARD
    properties: PolicyParentCompartmentRelProps = PolicyParentCompartmentRelProps()


@dataclass(frozen=True)
class RegionSubscriptionRelProps(CartographyRelProperties):
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)


@dataclass(frozen=True)
class RegionSubscriptionRel(CartographyRelSchema):
    target_node_label: str = "OCITenancy"
    target_node_matcher: TargetNodeMatcher = make_target_node_matcher({
        "id": PropertyRef("OCI_TENANCY_ID", set_in_kwargs=True),
    })
    rel_label: str = "OCI_REGION_SUBSCRIPTION"
    direction: LinkDirection = LinkDirection.INWARD
    properties: RegionSubscriptionRelProps = RegionSubscriptionRelProps()

