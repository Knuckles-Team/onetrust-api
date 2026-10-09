"""Epistemic-graph ingestion for OneTrust records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. ``agent_connector_sdk.ingest`` --
the generated ``SourceIngest`` client, not a local ingestion helper -- owns the
transaction and raises ``IngestError`` when epistemic-graph cannot commit.
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

_BINDING = IngestBinding(connector="onetrust-api", stream="onetrust")

_ENTITY_RESERVED_KEYS = frozenset({"id", "node_type"})
_RELATIONSHIP_RESERVED_KEYS = frozenset({"source", "target", "relationship"})
_DOCUMENT_RESERVED_KEYS = frozenset({"id", "text", "title", "source_uri"})


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _ENTITY_RESERVED_KEYS
        },
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        key: value
        for key, value in record.items()
        if key not in _RELATIONSHIP_RESERVED_KEYS
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


def _to_document(record: dict[str, Any]) -> Document:
    return Document(
        id=record["id"],
        text=record["text"],
        title=record.get("title"),
        source_uri=record.get("source_uri"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _DOCUMENT_RESERVED_KEYS
        },
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write typed OWL nodes (+ edges) into epistemic-graph via the SDK ingest facade.

    Uses canonical ``node_type`` / ``relationship`` structural fields and surfaces
    a malformed change set or a refused commit as ``IngestError``.
    """
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(entity) for entity in entities),
        relationships=tuple(
            _to_relationship(relationship) for relationship in relationships or ()
        ),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write text records as canonical ``:Document`` nodes."""
    if not documents:
        raise IngestError("ingest_documents needs at least one document")
    change_set = ChangeSet(
        documents=tuple(_to_document(document) for document in documents)
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


def _s(value: Any) -> str | None:
    return str(value) if value is not None else None


async def ingest_assessments(
    assessments: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map assessment records → ``:Assessment`` (+ ``:AssessmentTemplate``/``:Person``) nodes.

    Accepts the ``AssessmentListViewBasicDto`` / ``AssessmentListViewResponseV2`` shape
    returned by ``get_all_assessment_basic_details_using_get`` / ``get_assessments_using_post``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for a in assessments or []:
        ent, rels = _assessment_entities(a)
        entities.extend(ent)
        relationships.extend(rels)
    return await ingest_entities(entities, relationships, ingest=ingest)


def _assessment_entities(
    a: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Map one assessment record to its ``:Assessment`` node plus related nodes/edges."""
    aid = a.get("assessmentId") or a.get("id")
    if aid is None:
        return [], []
    node_id = f"onetrust:assessment:{aid}"
    entities: list[dict[str, Any]] = [
        {
            "id": node_id,
            "node_type": "Assessment",
            "name": a.get("name"),
            "number": a.get("number"),
            "status": a.get("status") or a.get("state"),
            "result": a.get("result") or a.get("resultName"),
            "riskScore": (
                a.get("residualRiskScore")
                if a.get("residualRiskScore") is not None
                else a.get("inherentRiskScore")
            ),
            "riskLevel": a.get("assessmentRiskLevelName"),
            "deadline": a.get("deadline"),
            "externalId": _s(aid),
        }
    ]
    relationships: list[dict[str, Any]] = []
    tid = a.get("templateId") or a.get("templateRootVersionId")
    if tid is not None:
        entities.append(
            {
                "id": f"onetrust:assessment_template:{tid}",
                "node_type": "AssessmentTemplate",
                "name": a.get("templateName"),
                "externalId": _s(tid),
            }
        )
        relationships.append(
            {
                "source": node_id,
                "target": f"onetrust:assessment_template:{tid}",
                "relationship": "usesTemplate",
            }
        )
    for person, rel in (
        (a.get("respondent"), "respondedBy"),
        (a.get("approver"), "approvedBy"),
    ):
        pid = _person_id(person)
        if pid:
            entities.append(_person_node(person, pid))
            relationships.append(
                {"source": node_id, "target": pid, "relationship": rel}
            )
    return entities, relationships


def assessment_documents(assessments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build ``:Document`` payloads (semantic-search summaries) for assessments."""
    docs: list[dict[str, Any]] = []
    for a in assessments or []:
        doc = _assessment_document(a)
        if doc is not None:
            docs.append(doc)
    return docs


def _assessment_document(a: dict[str, Any]) -> dict[str, Any] | None:
    """Build one assessment's ``:Document`` payload, or ``None`` if it has no text."""
    aid = a.get("assessmentId") or a.get("id")
    if aid is None:
        return None
    text = "\n".join(p for p in _assessment_document_parts(a) if p)
    if not text.strip():
        return None
    return {
        "id": f"onetrust:assessment_doc:{aid}",
        "title": a.get("name"),
        "text": text,
        "assessment_id": _s(aid),
    }


def _assessment_document_parts(a: dict[str, Any]) -> list[str | None]:
    """Build the summary text fragments for one assessment's ``:Document`` payload."""
    return [
        a.get("name"),
        f"Number: {a.get('number')}" if a.get("number") else None,
        f"Template: {a.get('templateName')}" if a.get("templateName") else None,
        f"Status: {a.get('status') or a.get('state')}",
        (
            f"Result: {a.get('result') or a.get('resultName')}"
            if (a.get("result") or a.get("resultName"))
            else None
        ),
    ]


async def ingest_cookies(
    cookies: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map cookie scan records → ``:Cookie`` (+ ``:CookieDomain``) nodes.

    Accepts the ``CookieResponseDto`` / ``CookieInformationDetailed`` shape returned by
    ``get_cookies_by_filter`` / ``get_categorized_cookies``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for c in cookies or []:
        cid = c.get("cookieId") or c.get("id")
        if cid is None:
            continue
        node_id = f"onetrust:cookie:{cid}"
        host = c.get("host") or c.get("urlDomain")
        entities.append(
            {
                "id": node_id,
                "node_type": "Cookie",
                "name": c.get("cookieName") or c.get("name"),
                "host": host,
                "lifespan": _s(c.get("lifespan") or c.get("cookieLifeSpan")),
                "cookieCategory": c.get("displayGroupName")
                or c.get("cookiepediaCategory"),
                "thirdParty": c.get("thirdParty"),
                "externalId": _s(cid),
            }
        )
        if host:
            dom_id = f"onetrust:cookie_domain:{host}"
            entities.append({"id": dom_id, "node_type": "CookieDomain", "name": host})
            relationships.append(
                {"source": node_id, "target": dom_id, "relationship": "scannedOnDomain"}
            )
    return await ingest_entities(entities, relationships, ingest=ingest)


async def ingest_inventories(
    inventories: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map inventory records → ``:Inventory`` (+ embedded ``:DataElement``/``:Person``) nodes.

    Accepts the ``BulkUpsertInventoryResponse`` / inventory list shape; extracts any embedded
    ``dataElements`` list into ``:DataElement`` nodes with ``:hasDataElement`` edges.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for inv in inventories or []:
        ent, rels = _inventory_entities(inv)
        entities.extend(ent)
        relationships.extend(rels)
    return await ingest_entities(entities, relationships, ingest=ingest)


def _inventory_entities(
    inv: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Map one inventory record to its ``:Inventory`` node plus owners/data elements."""
    iid = inv.get("id") or inv.get("externalId")
    if iid is None:
        return [], []
    node_id = f"onetrust:inventory:{iid}"
    entities: list[dict[str, Any]] = [
        {
            "id": node_id,
            "node_type": "Inventory",
            "name": inv.get("name"),
            "number": inv.get("number"),
            "inventoryType": inv.get("inventoryType"),
            "status": inv.get("status"),
            "externalId": _s(iid),
        }
    ]
    relationships: list[dict[str, Any]] = []
    owners = inv.get("businessOwners") or []
    for owner in owners if isinstance(owners, list) else []:
        pid = _person_id(owner)
        if pid:
            entities.append(_person_node(owner, pid))
            relationships.append(
                {"source": node_id, "target": pid, "relationship": "ownedBy"}
            )
    for de in inv.get("dataElements") or []:
        de_ent, de_rels = _data_element_entities(de, parent=node_id)
        entities.extend(de_ent)
        relationships.extend(de_rels)
    return entities, relationships


async def ingest_data_elements(
    data_elements: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map data-element records → ``:DataElement`` (+ ``:DataSubject``) nodes.

    Accepts the ``DataElementDetailedResponse`` shape returned by
    ``get_data_element_using_get``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for de in data_elements or []:
        ent, rels = _data_element_entities(de, parent=None)
        entities.extend(ent)
        relationships.extend(rels)
    return await ingest_entities(entities, relationships, ingest=ingest)


def _data_element_entities(
    de: dict[str, Any], *, parent: str | None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    did = de.get("id")
    if did is None:
        return [], []
    node_id = f"onetrust:data_element:{did}"
    entities: list[dict[str, Any]] = [
        {
            "id": node_id,
            "node_type": "DataElement",
            "name": de.get("name"),
            "description": de.get("description"),
            "status": de.get("status"),
            "externalId": _s(did),
        }
    ]
    relationships: list[dict[str, Any]] = []
    if parent:
        relationships.append(
            {"source": parent, "target": node_id, "relationship": "hasDataElement"}
        )
    for ds in de.get("dataSubjectTypes") or []:
        ds_id = ds.get("id") if isinstance(ds, dict) else ds
        ds_name = ds.get("name") if isinstance(ds, dict) else ds
        if ds_id is None:
            continue
        subj_id = f"onetrust:data_subject:{ds_id}"
        entities.append({"id": subj_id, "node_type": "DataSubject", "name": ds_name})
        relationships.append(
            {
                "source": node_id,
                "target": subj_id,
                "relationship": "concernsDataSubject",
            }
        )
    return entities, relationships


def _person_id(person: Any) -> str | None:
    if not isinstance(person, dict):
        return None
    pid = person.get("id") or person.get("email")
    return f"onetrust:person:{pid}" if pid else None


def _person_node(person: dict[str, Any], node_id: str) -> dict[str, Any]:
    return {
        "id": node_id,
        "node_type": "Person",
        "name": person.get("fullName") or person.get("name"),
        "email": person.get("email"),
    }
