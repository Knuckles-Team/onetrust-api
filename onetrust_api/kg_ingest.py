"""Native epistemic-graph ingestion for OneTrust records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. The required agent-utilities
native-ingest primitive owns the transaction and raises NativeIngestError when the
authoritative engine cannot commit.
"""

from __future__ import annotations

from typing import Any


_SOURCE = "onetrust-api"
_DOMAIN = "onetrust"


def ingest_entities(*args: object, **kwargs: object) -> object:
    """Write canonical typed nodes and relationships through agent-utilities.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("ingest_entities")


def ingest_documents(*args: object, **kwargs: object) -> object:
    """Write searchable documents through the authoritative native-ingest path.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("ingest_documents")


def media_store(*args: object, **kwargs: object) -> object:
    """Return the authoritative native media store.

    SDK-GAP: Always raises now; see KnowledgeGraphIngestUnavailable.
    """
    _kg_unavailable("media_store")


def _s(value: Any) -> str | None:
    return str(value) if value is not None else None


def ingest_assessments(
    assessments: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


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


def ingest_cookies(
    cookies: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_inventories(
    inventories: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


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


def ingest_data_elements(
    data_elements: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


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


class KnowledgeGraphIngestUnavailable(RuntimeError):
    """Direct-to-graph ingestion is unavailable from this connector.

    SDK-GAP (EH-48x, /var/tmp/l9/finish/au-decon-G4c/SDK-GAPS.md): raised in
    place of the old ``agent_utilities.knowledge_graph`` native-ingest call --
    agent-connector-sdk has no facade over EG's typed ingestion protocol yet,
    and the fleet precedent (agents/world-reference-mcp) moves direct-to-graph
    delivery to agent_connector_sdk.runner/sinks at the deployment layer, out
    of connector scope.
    """


def _kg_unavailable(name: str) -> None:
    raise KnowledgeGraphIngestUnavailable(
        f"{name}: direct-to-graph ingestion moved out of connector code "
        "(agent-utilities removed); no agent-connector-sdk facade exists yet "
        "-- see SDK-GAPS.md"
    )
