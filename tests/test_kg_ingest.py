"""Epistemic-graph typed-node ingestion -- Wire-First coverage for onetrust-api.

Exercises the real ``ingest_entities`` / ``ingest_documents`` seam and the OneTrust
domain mappers (``ingest_assessments`` / ``ingest_cookies`` / ``ingest_inventories`` /
``ingest_data_elements``) against a fake ``agent_connector_sdk.ingest`` transport (no
engine required). The real SDK request builder
(``agent_connector_sdk.ingest.request.build_request``) and privacy guard still run, so
a malformed change set and the PII redaction contract are still exercised by the SDK's
own code, not re-derived here; only the final network commit is faked.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest
from epistemic_graph.generated.source_ingestion import SourceIngestionRequest

from onetrust_api.kg_ingest import (
    assessment_documents,
    ingest_assessments,
    ingest_cookies,
    ingest_data_elements,
    ingest_documents,
    ingest_entities,
    ingest_inventories,
)


class _FakeTransport:
    """Records every submitted request; no epistemic-graph engine required."""

    def __init__(self) -> None:
        self.requests: list[SourceIngestionRequest] = []

    async def source_status(self, _connector: str, _stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: SourceIngestionRequest) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, _data: bytes) -> str:
        raise AssertionError("onetrust-api ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Assessment", "name": "PIA"},
            {"id": "b", "node_type": "AssessmentTemplate"},
        ],
        [{"source": "a", "target": "b", "relationship": "usesTemplate"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    request = transport.requests[0]
    record_ids = {record.record_id for record in request.records}
    assert record_ids == {"a", "b"}
    a_record = next(r for r in request.records if r.record_id == "a")
    assert a_record.payload["name"] == "PIA"
    assert request.relationships[0].relation_reference.endswith(
        "resources/Assessment/relations/usesTemplate"
    )


@pytest.mark.asyncio
async def test_ingest_assessments_maps_assessment_template_and_person(ingest):
    service, transport = ingest
    res = await ingest_assessments(
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
        ingest=service,
    )
    assert res == {"nodes": 3, "edges": 2}
    request = transport.requests[0]
    assessment = next(
        r for r in request.records if r.record_id == "onetrust:assessment:A1"
    )
    assert assessment.payload["number"] == "AS-7"
    assert assessment.payload["externalId"] == "A1"
    template = next(
        r
        for r in request.records
        if r.record_id == "onetrust:assessment_template:T9"
    )
    assert template.mapping_reference.endswith("AssessmentTemplate")
    person = next(
        r for r in request.records if r.record_id == "onetrust:person:u1"
    )
    assert person.mapping_reference.endswith("Person")
    relations = {r.relation_reference.rsplit("/", 1)[-1] for r in request.relationships}
    assert relations == {"usesTemplate", "respondedBy"}


@pytest.mark.asyncio
async def test_assessment_documents_and_ingest_documents(ingest):
    service, transport = ingest
    docs = assessment_documents(
        [{"assessmentId": "A1", "name": "Vendor PIA", "status": "COMPLETED"}]
    )
    assert docs and docs[0]["id"] == "onetrust:assessment_doc:A1"
    res = await ingest_documents(docs, ingest=service)
    assert res == {"nodes": 1, "edges": 0}
    record = transport.requests[0].records[0]
    assert record.record_id == "onetrust:assessment_doc:A1"
    assert "Vendor PIA" in record.payload["text"]


@pytest.mark.asyncio
async def test_ingest_cookies_maps_cookie_and_domain(ingest):
    service, transport = ingest
    res = await ingest_cookies(
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
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    cookie = next(r for r in request.records if r.record_id == "onetrust:cookie:CK1")
    # "host" is a recognized location field: the SDK's PersistencePrivacyGuard
    # redacts it outright (by field name, not just a value pattern match).
    assert cookie.payload["host"] == "[REDACTED_LOCATION]"
    assert cookie.payload["cookieCategory"] == "Performance"
    assert cookie.payload["thirdParty"] is True
    domain = next(
        r
        for r in request.records
        if r.record_id == "onetrust:cookie_domain:example.com"
    )
    assert domain.mapping_reference.endswith("CookieDomain")
    assert request.relationships[0].relation_reference.endswith("scannedOnDomain")


@pytest.mark.asyncio
async def test_ingest_inventories_extracts_data_elements_and_owner(ingest):
    service, transport = ingest
    res = await ingest_inventories(
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
        ingest=service,
    )
    # Inventory + Person + DataElement + DataSubject = 4 nodes
    assert res == {"nodes": 4, "edges": 3}
    request = transport.requests[0]
    inventory = next(
        r for r in request.records if r.record_id == "onetrust:inventory:INV1"
    )
    assert inventory.payload["inventoryType"] == "ASSETS"
    assert any(
        r.record_id == "onetrust:data_element:DE1" for r in request.records
    )
    assert any(
        r.record_id == "onetrust:data_subject:DS1" for r in request.records
    )
    relations = {r.relation_reference.rsplit("/", 1)[-1] for r in request.relationships}
    assert relations == {"ownedBy", "hasDataElement", "concernsDataSubject"}


@pytest.mark.asyncio
async def test_ingest_data_elements_standalone(ingest):
    service, transport = ingest
    res = await ingest_data_elements(
        [
            {
                "id": "DE9",
                "name": "SSN",
                "description": "national id",
                "status": "ACTIVE",
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    record = transport.requests[0].records[0]
    assert record.record_id == "onetrust:data_element:DE9"
    assert record.payload["name"] == "SSN"


@pytest.mark.asyncio
async def test_retired_node_type_alias_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="node_type"):
        await ingest_entities(
            [{"id": "retired", "type": "RetiredAlias"}], ingest=service
        )


@pytest.mark.asyncio
async def test_empty_ingest_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
