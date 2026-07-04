"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_documents`` seam and the OneTrust
domain mappers (``ingest_assessments`` / ``ingest_cookies`` / ``ingest_inventories`` /
``ingest_data_elements``) with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the record → typed-node mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from onetrust_api.kg_ingest import (
    assessment_documents,
    ingest_assessments,
    ingest_cookies,
    ingest_data_elements,
    ingest_documents,
    ingest_entities,
    ingest_inventories,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Assessment", "name": "PIA"},
            {"id": "b", "type": "AssessmentTemplate"},
        ],
        [{"source": "a", "target": "b", "type": "usesTemplate"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    assert c.txn.nodes["a"]["source"] == "onetrust-api"
    assert c.txn.nodes["a"]["domain"] == "onetrust"
    assert c.edges.edges == [("a", "b", {"type": "usesTemplate"})]


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
        graph="__commons__",
    )
    assert res == {"nodes": 3, "edges": 2}
    assert c.txn.nodes["onetrust:assessment:A1"]["type"] == "Assessment"
    assert c.txn.nodes["onetrust:assessment:A1"]["number"] == "AS-7"
    assert c.txn.nodes["onetrust:assessment:A1"]["externalId"] == "A1"
    assert (
        c.txn.nodes["onetrust:assessment_template:T9"]["type"] == "AssessmentTemplate"
    )
    assert c.txn.nodes["onetrust:person:u1"]["type"] == "Person"
    assert (
        "onetrust:assessment:A1",
        "onetrust:assessment_template:T9",
        {"type": "usesTemplate"},
    ) in c.edges.edges
    assert (
        "onetrust:assessment:A1",
        "onetrust:person:u1",
        {"type": "respondedBy"},
    ) in c.edges.edges


def test_assessment_documents_and_ingest_documents():
    docs = assessment_documents(
        [{"assessmentId": "A1", "name": "Vendor PIA", "status": "COMPLETED"}]
    )
    assert docs and docs[0]["id"] == "onetrust:assessment_doc:A1"
    c = _FakeClient()
    res = ingest_documents(docs, client=c, graph="__commons__")
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["onetrust:assessment_doc:A1"]
    assert node["type"] == "Document"
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
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    ck = c.txn.nodes["onetrust:cookie:CK1"]
    assert ck["type"] == "Cookie"
    assert ck["host"] == "example.com"
    assert ck["cookieCategory"] == "Performance"
    assert ck["thirdParty"] is True
    assert c.txn.nodes["onetrust:cookie_domain:example.com"]["type"] == "CookieDomain"
    assert c.edges.edges == [
        (
            "onetrust:cookie:CK1",
            "onetrust:cookie_domain:example.com",
            {"type": "scannedOnDomain"},
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
        graph="__commons__",
    )
    # Inventory + Person + DataElement + DataSubject = 4 nodes
    assert res == {"nodes": 4, "edges": 3}
    assert c.txn.nodes["onetrust:inventory:INV1"]["inventoryType"] == "ASSETS"
    assert c.txn.nodes["onetrust:data_element:DE1"]["type"] == "DataElement"
    assert c.txn.nodes["onetrust:data_subject:DS1"]["type"] == "DataSubject"
    edge_types = {e[2]["type"] for e in c.edges.edges}
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["onetrust:data_element:DE9"]["name"] == "SSN"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Assessment"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_assessments([], client=_FakeClient()) is None
    assert ingest_cookies([], client=_FakeClient()) is None
    assert ingest_inventories([], client=_FakeClient()) is None
    assert ingest_data_elements([], client=_FakeClient()) is None
