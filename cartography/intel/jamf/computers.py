import logging
from typing import Dict
from typing import List

import neo4j

from cartography.client.core.tx import load
from cartography.intel.jamf.util import call_jamf_api
from cartography.util import run_cleanup_job
from cartography.util import timeit
from cartography.models.jamf.computergroup import JamfComputerGroupSchema
from cartography.graph.job import GraphJob

logger = logging.getLogger(__name__)


@timeit
def get_computer_groups(
    jamf_base_uri: str,
    jamf_user: str,
    jamf_password: str,
) -> List[Dict]:
    return call_jamf_api("/computergroups", jamf_base_uri, jamf_user, jamf_password)


@timeit
def load_computer_groups(
    data: Dict,
    neo4j_session: neo4j.Session,
    update_tag: int,
) -> None:
    groups = data.get("computer_groups", [])
    records = [
        {"id": g.get("id"), "name": g.get("name"), "is_smart": g.get("is_smart")}
        for g in (groups or [])
        if g.get("id") is not None
    ]
    if not records:
        return
    load(neo4j_session, JamfComputerGroupSchema(), records, lastupdated=update_tag)


@timeit
def cleanup(neo4j_session: neo4j.Session, common_job_parameters: Dict) -> None:
    GraphJob.from_node_schema(JamfComputerGroupSchema(), common_job_parameters).run(neo4j_session)


@timeit
def sync_computer_groups(
    neo4j_session: neo4j.Session,
    update_tag: int,
    jamf_base_uri: str,
    jamf_user: str,
    jamf_password: str,
) -> None:
    groups = get_computer_groups(jamf_base_uri, jamf_user, jamf_password)
    load_computer_groups(groups, neo4j_session, update_tag)  # type: ignore


@timeit
def sync(
    neo4j_session: neo4j.Session,
    jamf_base_uri: str,
    jamf_user: str,
    jamf_password: str,
    common_job_parameters: Dict,
) -> None:
    sync_computer_groups(
        neo4j_session,
        common_job_parameters["UPDATE_TAG"],
        jamf_base_uri,
        jamf_user,
        jamf_password,
    )
