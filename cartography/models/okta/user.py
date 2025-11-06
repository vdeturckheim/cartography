from dataclasses import dataclass

from cartography.models.core.common import PropertyRef
from cartography.models.core.nodes import CartographyNodeProperties, CartographyNodeSchema, ExtraNodeLabels
from cartography.models.core.relationships import OtherRelationships
from .common import ResourceToOktaOrgRel, HumanIdentityOktaRel


@dataclass(frozen=True)
class OktaUserNodeProperties(CartographyNodeProperties):
    id: PropertyRef = PropertyRef("id")
    lastupdated: PropertyRef = PropertyRef("lastupdated", set_in_kwargs=True)
    first_name: PropertyRef = PropertyRef("first_name")
    last_name: PropertyRef = PropertyRef("last_name")
    login: PropertyRef = PropertyRef("login")
    email: PropertyRef = PropertyRef("email", extra_index=True)
    second_email: PropertyRef = PropertyRef("second_email")
    created: PropertyRef = PropertyRef("created")
    activated: PropertyRef = PropertyRef("activated")
    status_changed: PropertyRef = PropertyRef("status_changed")
    last_login: PropertyRef = PropertyRef("last_login")
    okta_last_updated: PropertyRef = PropertyRef("okta_last_updated")
    password_changed: PropertyRef = PropertyRef("password_changed")
    transition_to_status: PropertyRef = PropertyRef("transition_to_status")
    _module_name: PropertyRef = PropertyRef("_module_name")


@dataclass(frozen=True)
class OktaUserSchema(CartographyNodeSchema):
    label: str = "OktaUser"
    properties: OktaUserNodeProperties = OktaUserNodeProperties()
    extra_node_labels: ExtraNodeLabels = ExtraNodeLabels(["UserAccount"])  # for ontology
    sub_resource_relationship: ResourceToOktaOrgRel = ResourceToOktaOrgRel()
    other_relationships: OtherRelationships = OtherRelationships([
        HumanIdentityOktaRel(),
    ])

