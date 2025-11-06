import gzip
import json
import os
import tempfile

import neo4j

from cartography.client.core.tx import load
from cartography.sinks import file_export as file_export_sink

# Models used for the tests
from cartography.models.lastpass.tenant import LastpassTenantSchema
from cartography.models.lastpass.user import LastpassUserSchema

from cartography.models.snipeit.tenant import SnipeitTenantSchema
from cartography.models.snipeit.user import SnipeitUserSchema
from cartography.models.snipeit.asset import SnipeitAssetSchema

from cartography.models.tailscale.tailnet import TailscaleTailnetSchema
from cartography.models.tailscale.user import TailscaleUserSchema
from cartography.models.tailscale.device import TailscaleDeviceSchema

from cartography.models.openai.organization import OpenAIOrganizationSchema
from cartography.models.openai.user import OpenAIUserSchema
from cartography.models.openai.project import OpenAIProjectSchema


def _read_ndjson_gz(path: str):
    with gzip.open(path, mode="rt", encoding="utf-8") as fh:  # type: ignore
        for line in fh:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _find_vertex(records, label, uid):
    return next(
        (r for r in records if r.get("record_type") == "vertex" and uid == r.get("uid") and label in r.get("labels", [])),
        None,
    )


def _edge_exists(records, rel_type, from_uid=None, to_uid=None):
    for r in records:
        if r.get("record_type") != "edge":
            continue
        if r.get("rel_type") != rel_type:
            continue
        if from_uid is not None and r.get("from_uid") != from_uid:
            continue
        if to_uid is not None and r.get("to_uid") != to_uid:
            continue
        return True
    return False


def _with_export(fn):
    def wrapper(*args, **kwargs):
        with tempfile.TemporaryDirectory() as td:
            out_path = os.path.join(td, "graph.ndjson.gz")
            file_export_sink.enable(out_path)
            try:
                file_export_sink.set_no_neo4j_write(False)  # Tee: write to both export and Neo4j
                fn_out = fn(out_path, *args, **kwargs)
            finally:
                file_export_sink.disable()
        return fn_out
    return wrapper


@_with_export
def test_lastpass_user_export_equivalence(out_path: str, neo4j_session: neo4j.Session):
    update_tag = 1700000100
    tenant_id = "lp-tenant-1"
    user_id = "lp-user-1"

    # Preload tenant
    load(neo4j_session, LastpassTenantSchema(), [{"id": tenant_id}], lastupdated=update_tag)
    # Load user
    data = [
        {
            "id": user_id,
            "username": "user@example.com",
            "fullname": "Example User",
        }
    ]
    load(
        neo4j_session,
        LastpassUserSchema(),
        data,
        lastupdated=update_tag,
        TENANT_ID=tenant_id,
    )

    # Neo4j assertions
    res = neo4j_session.run("MATCH (n:LastpassUser{id:$id}) RETURN count(n) AS c", id=user_id).single()
    assert res["c"] == 1
    rel = neo4j_session.run(
        "MATCH (u:LastpassUser{id:$id})-[:RESOURCE]->(t:LastpassTenant{id:$tid}) RETURN count(*) AS c",
        id=user_id,
        tid=tenant_id,
    ).single()
    assert rel["c"] == 1

    # Export assertions
    records = list(_read_ndjson_gz(out_path))
    assert _find_vertex(records, "LastpassUser", user_id)
    assert _edge_exists(records, "RESOURCE", from_uid=user_id, to_uid=tenant_id) or _edge_exists(
        records, "RESOURCE", from_uid=tenant_id, to_uid=user_id
    )


@_with_export
def test_snipeit_asset_export_equivalence(out_path: str, neo4j_session: neo4j.Session):
    update_tag = 1700000200
    tenant_id = "snipe-tenant-1"
    user_email = "owner@example.com"
    asset_id = "asset-1"

    # Preload tenant and user
    load(neo4j_session, SnipeitTenantSchema(), [{"id": tenant_id}], lastupdated=update_tag)
    load(
        neo4j_session,
        SnipeitUserSchema(),
        [{"id": "su1", "email": user_email, "company_id.name": "Acme", "username": "owner"}],
        lastupdated=update_tag,
        TENANT_ID=tenant_id,
    )
    # Load asset referencing the user by email
    asset = {
        "id": asset_id,
        "name": "Laptop",
        "asset_tag": "A-1",
        "assigned_to.email": user_email,
        "category.name": "Hardware",
        "company.name": "Acme",
        "manufacturer.name": "Brand",
        "model.name": "ModelX",
        "serial": "SN-123",
        "status_label.name": "Assigned",
    }
    load(
        neo4j_session,
        SnipeitAssetSchema(),
        [asset],
        lastupdated=update_tag,
        TENANT_ID=tenant_id,
    )

    # Neo4j assertions
    res = neo4j_session.run("MATCH (n:SnipeitAsset{id:$id}) RETURN count(n) AS c", id=asset_id).single()
    assert res["c"] == 1
    rel = neo4j_session.run(
        "MATCH (:SnipeitTenant{id:$tid})-[:HAS_ASSET]->(:SnipeitAsset{id:$aid}) RETURN count(*) AS c",
        tid=tenant_id,
        aid=asset_id,
    ).single()
    assert rel["c"] == 1

    # Export assertions
    records = list(_read_ndjson_gz(out_path))
    assert _find_vertex(records, "SnipeitAsset", asset_id)
    assert _edge_exists(records, "HAS_ASSET")


@_with_export
def test_tailscale_device_export_equivalence(out_path: str, neo4j_session: neo4j.Session):
    update_tag = 1700000300
    tailnet = "tn-1"
    user_login = "user@tailscale.test"
    device_id = "node-1"

    # Preload tailnet and user
    load(neo4j_session, TailscaleTailnetSchema(), [{}], lastupdated=update_tag, org=tailnet)
    load(
        neo4j_session,
        TailscaleUserSchema(),
        [{"id": "tsu1", "displayName": "TS User", "loginName": user_login}],
        lastupdated=update_tag,
        org=tailnet,
    )
    # Load device referencing the user by login name under the same tailnet
    dev = {
        "nodeId": device_id,
        "name": "dev-1",
        "hostname": "host-1",
        "user": user_login,
    }
    load(
        neo4j_session,
        TailscaleDeviceSchema(),
        [dev],
        lastupdated=update_tag,
        org=tailnet,
    )

    res = neo4j_session.run("MATCH (n:TailscaleDevice{id:$id}) RETURN count(n) AS c", id=device_id).single()
    assert res["c"] == 1
    rel = neo4j_session.run(
        "MATCH (:TailscaleTailnet{id:$tid})-[:RESOURCE]->(:TailscaleDevice{id:$did}) RETURN count(*) AS c",
        tid=tailnet,
        did=device_id,
    ).single()
    assert rel["c"] == 1

    records = list(_read_ndjson_gz(out_path))
    assert _find_vertex(records, "TailscaleDevice", device_id)
    assert _edge_exists(records, "RESOURCE")


@_with_export
def test_openai_project_export_equivalence(out_path: str, neo4j_session: neo4j.Session):
    update_tag = 1700000400
    org = "org-1"
    user = "ou-1"
    project = "proj-1"

    # Preload organization and user
    load(neo4j_session, OpenAIOrganizationSchema(), [{"id": org}], lastupdated=update_tag)
    load(
        neo4j_session,
        OpenAIUserSchema(),
        [{"object": "organization.member", "id": user, "name": "User", "email": "user@openai.test"}],
        lastupdated=update_tag,
        ORG_ID=org,
    )
    # Load a project referencing the user
    proj = {
        "id": project,
        "object": "organization.project",
        "name": "Project",
        "created_at": 1,
        "archived_at": None,
        "status": "active",
        "users": [user],
        "admins": [user],
    }
    load(
        neo4j_session,
        OpenAIProjectSchema(),
        [proj],
        lastupdated=update_tag,
        ORG_ID=org,
    )

    res = neo4j_session.run("MATCH (n:OpenAIProject{id:$id}) RETURN count(n) AS c", id=project).single()
    assert res["c"] == 1
    rel = neo4j_session.run(
        "MATCH (:OpenAIOrganization{id:$org})-[:RESOURCE]->(:OpenAIProject{id:$pid}) RETURN count(*) AS c",
        org=org,
        pid=project,
    ).single()
    assert rel["c"] == 1

    records = list(_read_ndjson_gz(out_path))
    assert _find_vertex(records, "OpenAIProject", project)
    assert _edge_exists(records, "RESOURCE")

