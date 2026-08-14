"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_documents`` seam and the OneTrust
domain mappers (``ingest_assessments`` / ``ingest_cookies`` / ``ingest_inventories`` /
``ingest_data_elements``) with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the record → typed-node mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from onetrust_api.kg_ingest import (
    assessment_documents,
    ingest_assessments,
    ingest_cookies,
    ingest_data_elements,
    ingest_documents,
    ingest_entities,
    ingest_inventories,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Assessment", "name": "PIA"},
            {"id": "b", "node_type": "AssessmentTemplate"},
        ],
        [{"source": "a", "target": "b", "relationship": "usesTemplate"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    assert c.nodes.values["a"]["source"] == "onetrust-api"
    assert c.nodes.values["a"]["domain"] == "onetrust"
    assert c.changes.edges == [("a", "b", {"relationship": "usesTemplate"})]


def test_ingest_assessments_maps_assessment_template_and_person():
    c = _FakeClient()
    res = ingest_assessments(
        [
            {
                "assessmentId": "A1",
                "number": "AS-7",
                "name": "Vendor PIA",
                "status": "IN_PROGRESS",
                "result": "Low",
                "residualRiskScore": 12,
                "templateId": "T9",
                "templateName": "PIA Template",
                "respondent": {"id": "u1", "fullName": "Ada", "email": "ada@x.io"},
            }
        ],
        client=c,
    )
    assert res == {"nodes": 3, "edges": 2}
    assert c.nodes.values["onetrust:assessment:A1"]["node_type"] == "Assessment"
    assert c.nodes.values["onetrust:assessment:A1"]["number"] == "AS-7"
    assert c.nodes.values["onetrust:assessment:A1"]["externalId"] == "A1"
    assert (
        c.nodes.values["onetrust:assessment_template:T9"]["node_type"]
        == "AssessmentTemplate"
    )
    assert c.nodes.values["onetrust:person:u1"]["node_type"] == "Person"
    assert (
        "onetrust:assessment:A1",
        "onetrust:assessment_template:T9",
        {"relationship": "usesTemplate"},
    ) in c.changes.edges
    assert (
        "onetrust:assessment:A1",
        "onetrust:person:u1",
        {"relationship": "respondedBy"},
    ) in c.changes.edges


def test_assessment_documents_and_ingest_documents():
    docs = assessment_documents(
        [{"assessmentId": "A1", "name": "Vendor PIA", "status": "COMPLETED"}]
    )
    assert docs and docs[0]["id"] == "onetrust:assessment_doc:A1"
    c = _FakeClient()
    res = ingest_documents(docs, client=c)
    assert res == {"nodes": 1, "edges": 0}
    node = c.nodes.values["onetrust:assessment_doc:A1"]
    assert node["node_type"] == "Document"
    assert "Vendor PIA" in node["text"]


def test_ingest_cookies_maps_cookie_and_domain():
    c = _FakeClient()
    res = ingest_cookies(
        [
            {
                "cookieId": "CK1",
                "cookieName": "_ga",
                "host": "example.com",
                "lifespan": "2 years",
                "displayGroupName": "Performance",
                "thirdParty": True,
            }
        ],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    ck = c.nodes.values["onetrust:cookie:CK1"]
    assert ck["node_type"] == "Cookie"
    assert ck["host"] == "example.com"
    assert ck["cookieCategory"] == "Performance"
    assert ck["thirdParty"] is True
    assert (
        c.nodes.values["onetrust:cookie_domain:example.com"]["node_type"] == "CookieDomain"
    )
    assert c.changes.edges == [
        (
            "onetrust:cookie:CK1",
            "onetrust:cookie_domain:example.com",
            {"relationship": "scannedOnDomain"},
        )
    ]


def test_ingest_inventories_extracts_data_elements_and_owner():
    c = _FakeClient()
    res = ingest_inventories(
        [
            {
                "id": "INV1",
                "name": "CRM",
                "number": "AST-3",
                "inventoryType": "ASSETS",
                "businessOwners": [{"id": "o1", "fullName": "Grace"}],
                "dataElements": [
                    {
                        "id": "DE1",
                        "name": "Email",
                        "status": "ACTIVE",
                        "dataSubjectTypes": [{"id": "DS1", "name": "Customer"}],
                    }
                ],
            }
        ],
        client=c,
    )
    # Inventory + Person + DataElement + DataSubject = 4 nodes
    assert res == {"nodes": 4, "edges": 3}
    assert c.nodes.values["onetrust:inventory:INV1"]["inventoryType"] == "ASSETS"
    assert c.nodes.values["onetrust:data_element:DE1"]["node_type"] == "DataElement"
    assert c.nodes.values["onetrust:data_subject:DS1"]["node_type"] == "DataSubject"
    edge_types = {e[2]["relationship"] for e in c.changes.edges}
    assert edge_types == {"ownedBy", "hasDataElement", "concernsDataSubject"}


def test_ingest_data_elements_standalone():
    c = _FakeClient()
    res = ingest_data_elements(
        [
            {
                "id": "DE9",
                "name": "SSN",
                "description": "national id",
                "status": "ACTIVE",
            }
        ],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.nodes.values["onetrust:data_element:DE9"]["name"] == "SSN"


def test_retired_node_type_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities(
            [{"id": "retired", "type": "RetiredAlias"}],
            client=_FakeClient(),
        )


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
