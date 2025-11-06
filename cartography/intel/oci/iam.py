# Copyright (c) 2020, Oracle and/or its affiliates.
# OCI Identity API-centric functions
# https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/overview.htm
import logging
import re
from typing import Any
from typing import Dict
from typing import List

import neo4j
import oci

from cartography.client.core.tx import read_list_of_dicts_tx
from cartography.client.core.tx import load, load_matchlinks
from cartography.util import run_cleanup_job
from cartography.models.oci.compartment import OCICompartmentSchema
from cartography.models.oci.user import OCIUserSchema
from cartography.models.oci.group import OCIGroupSchema, OCIUserMemberOfGroupMatchLink
from cartography.models.oci.policy import (
    OCIPolicySchema,
    OCIPolicyToGroupMatchLink,
    OCIPolicyToCompartmentMatchLink,
)
from cartography.models.oci.region import OCIRegionSchema
from cartography.graph.job import GraphJob

from . import utils

logger = logging.getLogger(__name__)


def sync_compartments(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.debug("Syncing IAM compartments for account '%s'.", current_tenancy_id)
    data = get_compartment_list_data(iam, current_tenancy_id)
    load_compartments(
        neo4j_session,
        data["Compartments"],
        current_tenancy_id,
        oci_update_tag,
    )
    GraphJob.from_node_schema(OCICompartmentSchema(), common_job_parameters).run(neo4j_session)


def get_compartment_list_data_recurse(
    iam: oci.identity.identity_client.IdentityClient,
    compartment_list: Dict[str, Any],
    compartment_id: str,
) -> None:

    response = oci.pagination.list_call_get_all_results(
        iam.list_compartments,
        compartment_id,
    )
    if not response.data:
        return
    compartment_list.update(
        {
            "Compartments": list(compartment_list["Compartments"])
            + utils.oci_object_to_json(response.data),
        },
    )
    for compartment in response.data:
        get_compartment_list_data_recurse(iam, compartment_list, compartment.id)


def get_compartment_list_data(
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
) -> Dict[str, Any]:
    compartment_list = {"Compartments": ""}
    get_compartment_list_data_recurse(iam, compartment_list, current_tenancy_id)
    return compartment_list


def load_compartments(
    neo4j_session: neo4j.Session,
    compartments: List[Dict[str, Any]],
    current_oci_tenancy_id: str,
    oci_update_tag: int,
) -> None:
    records: List[Dict[str, Any]] = []
    for c in compartments:
        records.append({
            "id": c.get("id"),
            "ocid": c.get("id"),
            "name": c.get("name"),
            "description": c.get("description"),
            "createdate": c.get("time-created"),
            "parent_tenancy_id": current_oci_tenancy_id,
            "parent_compartment_id": c.get("compartment-id"),
        })
    if records:
        load(
            neo4j_session,
            OCICompartmentSchema(),
            records,
            lastupdated=oci_update_tag,
            OCI_TENANCY_ID=current_oci_tenancy_id,
        )


def load_users(
    neo4j_session: neo4j.Session,
    users: List[Dict[str, Any]],
    current_oci_tenancy_id: str,
    oci_update_tag: int,
) -> None:
    records: List[Dict[str, Any]] = []
    for u in users:
        caps = u.get("capabilities", {})
        records.append({
            "id": u.get("id"),
            "ocid": u.get("id"),
            "name": u.get("name"),
            "description": u.get("description"),
            "email": u.get("email"),
            "lifecycle_state": u.get("lifecycle-state"),
            "is_mfa_activated": u.get("is-mfa-activated"),
            "can_use_api_keys": caps.get("can-use-api-keys"),
            "can_use_auth_tokens": caps.get("can-use-auth-tokens"),
            "can_use_console_password": caps.get("can-use-console-password"),
            "can_use_customer_secret_keys": caps.get("can-use-customer-secret-keys"),
            "can_use_smtp_credentials": caps.get("can-use-smtp-credentials"),
            "createdate": str(u.get("time-created")),
            "compartmentid": u.get("compartment-id"),
        })
    if records:
        load(
            neo4j_session,
            OCIUserSchema(),
            records,
            lastupdated=oci_update_tag,
            OCI_TENANCY_ID=current_oci_tenancy_id,
        )


def get_user_list_data(
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
) -> Dict[str, List[Dict[str, Any]]]:
    response = oci.pagination.list_call_get_all_results(
        iam.list_users,
        current_tenancy_id,
    )
    return {"Users": utils.oci_object_to_json(response.data)}


def sync_users(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.debug("Syncing IAM users for account '%s'.", current_tenancy_id)
    data = get_user_list_data(iam, current_tenancy_id)
    load_users(neo4j_session, data["Users"], current_tenancy_id, oci_update_tag)
    GraphJob.from_node_schema(OCIUserSchema(), common_job_parameters).run(neo4j_session)


def get_group_list_data(
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
) -> Dict[str, List[Dict[str, Any]]]:
    response = oci.pagination.list_call_get_all_results(
        iam.list_groups,
        current_tenancy_id,
    )
    return {"Groups": utils.oci_object_to_json(response.data)}


def load_groups(
    neo4j_session: neo4j.Session,
    groups: List[Dict[str, Any]],
    current_tenancy_id: str,
    oci_update_tag: int,
) -> None:
    records: List[Dict[str, Any]] = []
    for g in groups:
        records.append({
            "id": g.get("id"),
            "ocid": g.get("id"),
            "name": g.get("name"),
            "description": g.get("description"),
            "createdate": str(g.get("time-created")),
            "compartmentid": g.get("compartment-id"),
        })
    if records:
        load(
            neo4j_session,
            OCIGroupSchema(),
            records,
            lastupdated=oci_update_tag,
            OCI_TENANCY_ID=current_tenancy_id,
        )


def sync_groups(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.debug("Syncing IAM groups for account '%s'.", current_tenancy_id)
    data = get_group_list_data(iam, current_tenancy_id)
    load_groups(neo4j_session, data["Groups"], current_tenancy_id, oci_update_tag)
    GraphJob.from_node_schema(OCIGroupSchema(), common_job_parameters).run(neo4j_session)


def get_group_membership_data(
    iam: oci.identity.identity_client.IdentityClient,
    group_id: str,
    current_tenancy_id: str,
) -> Dict[str, List[Dict[str, Any]]]:
    response = oci.pagination.list_call_get_all_results(
        iam.list_user_group_memberships,
        compartment_id=current_tenancy_id,
        group_id=group_id,
    )
    return {"GroupMemberships": utils.oci_object_to_json(response.data)}


def sync_group_memberships(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.debug("Syncing IAM group membership for account '%s'.", current_tenancy_id)
    query = (
        "MATCH (group:OCIGroup)<-[:RESOURCE]-(OCITenancy{ocid: $OCI_TENANCY_ID}) "
        "return group.name as name, group.ocid as ocid;"
    )
    groups = neo4j_session.execute_read(
        read_list_of_dicts_tx,
        query,
        OCI_TENANCY_ID=current_tenancy_id,
    )
    groups_membership = {
        group["ocid"]: get_group_membership_data(iam, group["ocid"], current_tenancy_id)
        for group in groups
    }
    load_group_memberships(neo4j_session, groups_membership, current_tenancy_id, oci_update_tag)
    GraphJob.from_matchlink(
        OCIUserMemberOfGroupMatchLink(),
        "OCITenancy",
        current_tenancy_id,
        oci_update_tag,
    ).run(neo4j_session)


def load_group_memberships(
    neo4j_session: neo4j.Session,
    group_memberships: Dict[str, Any],
    tenancy_id: str,
    oci_update_tag: int,
) -> None:
    rows: List[Dict[str, Any]] = []
    for _, membership_data in group_memberships.items():
        for info in membership_data["GroupMemberships"]:
            rows.append({
                "group_id": info.get("group-id"),
                "user_id": info.get("user-id"),
            })
    if rows:
        load_matchlinks(
            neo4j_session,
            OCIUserMemberOfGroupMatchLink(),
            rows,
            lastupdated=oci_update_tag,
            _sub_resource_label="OCITenancy",
            _sub_resource_id=tenancy_id,
        )


def load_policies(
    neo4j_session: neo4j.Session,
    policies: List[Dict[str, Any]],
    current_tenancy_id: str,
    oci_update_tag: int,
) -> None:
    records: List[Dict[str, Any]] = []
    for p in policies:
        records.append({
            "id": p.get("id"),
            "ocid": p.get("id"),
            "name": p.get("name"),
            "description": p.get("description"),
            "statements": p.get("statements"),
            "createdate": str(p.get("time-created")),
            "updatedate": str(p.get("version-date")),
            "policy_parent_compartment_id": p.get("compartment-id"),
        })
    if records:
        load(
            neo4j_session,
            OCIPolicySchema(),
            records,
            lastupdated=oci_update_tag,
            OCI_TENANCY_ID=current_tenancy_id,
        )


def get_policy_list_data(
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
) -> Dict[str, List[Dict[str, Any]]]:
    response = oci.pagination.list_call_get_all_results(
        iam.list_policies,
        compartment_id=current_tenancy_id,
    )
    return {"Policies": utils.oci_object_to_json(response.data)}


def sync_policies(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.debug("Syncing IAM policies for account '%s'.", current_tenancy_id)
    compartments = utils.get_compartments_in_tenancy(neo4j_session, current_tenancy_id)
    for compartment in compartments:
        logger.debug(
            "Syncing OCI policies for compartment '%s' in account '%s'.",
            compartment["ocid"],
            current_tenancy_id,
        )
        data = get_policy_list_data(iam, compartment["ocid"])
        if data["Policies"]:
            load_policies(
                neo4j_session,
                data["Policies"],
                current_tenancy_id,
                oci_update_tag,
            )
    GraphJob.from_node_schema(OCIPolicySchema(), common_job_parameters).run(neo4j_session)


def load_oci_policy_group_reference(
    neo4j_session: neo4j.Session,
    policy_id: str,
    group_id: str,
    tenancy_id: str,
    oci_update_tag: int,
) -> None:
    ingest_policy_group_reference = """
    MATCH (aa:OCIPolicy{ocid: $POLICY_ID})
    MATCH (bb:OCIGroup{ocid: $GROUP_ID})
    MERGE (aa)-[r:OCI_POLICY_REFERENCE]->(bb)
    ON CREATE SET r.firstseen = timestamp()
    SET r.lastupdated = $oci_update_tag
    """
    load_matchlinks(
        neo4j_session,
        OCIPolicyToGroupMatchLink(),
        [{"policy_id": policy_id, "group_id": group_id}],
        lastupdated=oci_update_tag,
        _sub_resource_label="OCITenancy",
        _sub_resource_id=tenancy_id,
    )


def load_oci_policy_compartment_reference(
    neo4j_session: neo4j.Session,
    policy_id: str,
    compartment_id: str,
    tenancy_id: str,
    oci_update_tag: int,
) -> None:
    ingest_policy_compartment_reference = """
    MATCH (aa:OCIPolicy{ocid: $POLICY_ID})
    MATCH (bb:OCICompartment{ocid: $COMPARTMENT_ID})
    MERGE (aa)-[r:OCI_POLICY_REFERENCE]->(bb)
    ON CREATE SET r.firstseen = timestamp()
    SET r.lastupdated = $oci_update_tag
    """
    load_matchlinks(
        neo4j_session,
        OCIPolicyToCompartmentMatchLink(),
        [{"policy_id": policy_id, "compartment_id": compartment_id}],
        lastupdated=oci_update_tag,
        _sub_resource_label="OCITenancy",
        _sub_resource_id=tenancy_id,
    )


# Parse the statements inside OCI Policies and load the corresponding relationships they reference.
def sync_oci_policy_references(
    neo4j_session: neo4j.Session,
    tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    groups = list(utils.get_groups_in_tenancy(neo4j_session, tenancy_id))
    compartments = list(utils.get_compartments_in_tenancy(neo4j_session, tenancy_id))
    policies = list(utils.get_policies_in_tenancy(neo4j_session, tenancy_id))
    for policy in policies:
        check_compart = policy["compartmentid"]
        for statement in policy["statements"]:
            m = re.search("(?<=group\\s)[^ ]*(?=\\s)", statement)
            if m:
                for group in groups:
                    if group["name"].lower() == m.group(0).lower():
                        load_oci_policy_group_reference(
                            neo4j_session,
                            policy["ocid"],
                            group["ocid"],
                            tenancy_id,
                            oci_update_tag,
                        )
            m = re.search("(?<=compartment\\s)[^ ]*(?=$)", statement)
            if m:
                for compartment in compartments:
                    # Only look at the compartment or subcompartment name referenced in the policy statement
                    # in which the policy is a member of.
                    if (
                        compartment["ocid"] == check_compart
                        or compartment["compartmentid"] == check_compart
                    ):
                        if compartment["name"].lower() == m.group(0).lower():
                            load_oci_policy_compartment_reference(
                                neo4j_session,
                                policy["ocid"],
                                compartment["ocid"],
                                tenancy_id,
                                oci_update_tag,
                            )


def get_region_subscriptions_list_data(
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
) -> Dict[str, List[Dict[str, Any]]]:
    response = oci.pagination.list_call_get_all_results(
        iam.list_region_subscriptions,
        current_tenancy_id,
    )
    return {"RegionSubscriptions": utils.oci_object_to_json(response.data)}


def load_region_subscriptions(
    neo4j_session: neo4j.Session,
    regions: List[Dict[str, Any]],
    tenancy_id: str,
    oci_update_tag: int,
) -> None:
    records = [{"id": r.get("region-key"), "name": r.get("region-name")} for r in regions]
    if records:
        load(
            neo4j_session,
            OCIRegionSchema(),
            records,
            lastupdated=oci_update_tag,
            OCI_TENANCY_ID=tenancy_id,
        )


def sync_region_subscriptions(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    current_tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.debug(
        "Syncing IAM region subscriptions for account '%s'.",
        current_tenancy_id,
    )
    data = get_region_subscriptions_list_data(iam, current_tenancy_id)
    load_region_subscriptions(
        neo4j_session,
        data["RegionSubscriptions"],
        current_tenancy_id,
        oci_update_tag,
    )
    GraphJob.from_node_schema(OCIRegionSchema(), common_job_parameters).run(neo4j_session)


def sync(
    neo4j_session: neo4j.Session,
    iam: oci.identity.identity_client.IdentityClient,
    tenancy_id: str,
    oci_update_tag: int,
    common_job_parameters: Dict[str, Any],
) -> None:
    logger.info("Syncing IAM for account '%s'.", tenancy_id)
    sync_users(neo4j_session, iam, tenancy_id, oci_update_tag, common_job_parameters)
    sync_groups(neo4j_session, iam, tenancy_id, oci_update_tag, common_job_parameters)
    sync_group_memberships(
        neo4j_session,
        iam,
        tenancy_id,
        oci_update_tag,
        common_job_parameters,
    )
    sync_compartments(
        neo4j_session,
        iam,
        tenancy_id,
        oci_update_tag,
        common_job_parameters,
    )
    sync_policies(neo4j_session, iam, tenancy_id, oci_update_tag, common_job_parameters)
    sync_oci_policy_references(
        neo4j_session,
        tenancy_id,
        oci_update_tag,
        common_job_parameters,
    )
    sync_region_subscriptions(
        neo4j_session,
        iam,
        tenancy_id,
        oci_update_tag,
        common_job_parameters,
    )
