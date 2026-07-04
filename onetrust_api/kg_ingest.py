"""Native epistemic-graph ingestion for OneTrust records (typed graph nodes + documents).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the onetrust-api package natively pushes its data into
the ONE epistemic-graph knowledge graph as **typed OWL nodes** (`:Assessment`,
`:AssessmentTemplate`, `:Inventory`, `:DataElement`, `:DataSubject`, `:Cookie`,
`:CookieDomain`, `:Person`) + links, and as **:Document** nodes (assessment summaries worth
semantic search), matching the classes federated by ``onetrust_api.ontology`` (onetrust.ttl).

The write path is the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` — this module is only a thin mapper
(records → entity/document dicts). The import is GUARDED: if that primitive is not present in
the installed agent_utilities, we fall back to a small self-contained txn writer over the
lightweight engine client (``GraphComputeEngine()._client`` + ``txn``), the same fast client
the blob ``MediaStore`` uses. Everything is dependency-/engine-guarded: with no KG stack or no
reachable engine, every entry point **no-ops** (returns ``None``), so the connector keeps
working with zero KG infrastructure. Node ids follow ``onetrust:<class>:<externalId>``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("onetrust_api.kg")

_SOURCE = "onetrust-api"
_DOMAIN = "onetrust"
_DEFAULT_GRAPH = "__commons__"


# --------------------------------------------------------------------------------------
# Write path — prefer the shared primitive; fall back to a self-contained txn writer.
# --------------------------------------------------------------------------------------
def _native():
    """Return the shared native_ingest module, or ``None`` if unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest

        return native_ingest
    except Exception as e:  # noqa: BLE001 — primitive not in installed agent_utilities
        logger.debug("native_ingest primitive unavailable: %s", e)
        return None


def _fallback_client() -> tuple[Any | None, str]:
    """Resolve ``(engine_client, graph)`` for the self-contained fallback writer."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write_nodes(
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any | None,
    graph: str | None,
) -> dict[str, int] | None:
    """Self-contained txn writer (used only when the shared primitive is absent)."""
    nodes = [n for n in (nodes or []) if n.get("id")]
    if not nodes:
        return None
    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    graph = graph or _DEFAULT_GRAPH
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None
    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)
    logger.info("KG ingest[onetrust]: wrote %d nodes, %d edges", len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    native = _native()
    if native is not None and client is None:
        return native.ingest_entities(
            entities, relationships, source=source, domain=domain, graph=graph
        )
    return _fallback_write_nodes(entities, relationships, client=client, graph=graph)


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    documents = [
        d
        for d in (documents or [])
        if d.get("id") and (d.get("text") or d.get("content"))
    ]
    if not documents:
        return None
    native = _native()
    if native is not None and client is None:
        return native.ingest_documents(
            documents, source=source, domain=domain, graph=graph
        )
    # Fallback: shape docs into :Document nodes and write them.
    nodes: list[dict[str, Any]] = []
    for doc in documents:
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["id"] = doc["id"]
        node["type"] = "Document"
        node["text"] = doc.get("text") or doc.get("content")
        nodes.append(node)
    return _fallback_write_nodes(nodes, None, client=client, graph=graph)


def media_store() -> Any | None:
    """Return a :class:`MediaStore` over a live engine (raw-blob ingestion), or ``None``."""
    native = _native()
    if native is not None:
        try:
            return native.media_store()
        except Exception as e:  # noqa: BLE001
            logger.debug("KG ingest: media_store unavailable: %s", e)
            return None
    return None


# --------------------------------------------------------------------------------------
# Domain mappers — OneTrust records → typed entity/document dicts.
# --------------------------------------------------------------------------------------
def _s(value: Any) -> str | None:
    return str(value) if value is not None else None


def ingest_assessments(
    assessments: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map assessment records → ``:Assessment`` (+ ``:AssessmentTemplate``/``:Person``) nodes.

    Accepts the ``AssessmentListViewBasicDto`` / ``AssessmentListViewResponseV2`` shape
    returned by ``get_all_assessment_basic_details_using_get`` / ``get_assessments_using_post``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for a in assessments or []:
        aid = a.get("assessmentId") or a.get("id")
        if aid is None:
            continue
        node_id = f"onetrust:assessment:{aid}"
        entities.append(
            {
                "id": node_id,
                "type": "Assessment",
                "name": a.get("name"),
                "number": a.get("number"),
                "status": a.get("status") or a.get("state"),
                "result": a.get("result") or a.get("resultName"),
                "riskScore": a.get("residualRiskScore")
                if a.get("residualRiskScore") is not None
                else a.get("inherentRiskScore"),
                "riskLevel": a.get("assessmentRiskLevelName"),
                "deadline": a.get("deadline"),
                "externalId": _s(aid),
            }
        )
        tid = a.get("templateId") or a.get("templateRootVersionId")
        if tid is not None:
            entities.append(
                {
                    "id": f"onetrust:assessment_template:{tid}",
                    "type": "AssessmentTemplate",
                    "name": a.get("templateName"),
                    "externalId": _s(tid),
                }
            )
            relationships.append(
                {
                    "source": node_id,
                    "target": f"onetrust:assessment_template:{tid}",
                    "type": "usesTemplate",
                }
            )
        for person, rel in (
            (a.get("respondent"), "respondedBy"),
            (a.get("approver"), "approvedBy"),
        ):
            pid = _person_id(person)
            if pid:
                entities.append(_person_node(person, pid))
                relationships.append({"source": node_id, "target": pid, "type": rel})
    return ingest_entities(entities, relationships, client=client, graph=graph)


def assessment_documents(assessments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build ``:Document`` payloads (semantic-search summaries) for assessments."""
    docs: list[dict[str, Any]] = []
    for a in assessments or []:
        aid = a.get("assessmentId") or a.get("id")
        if aid is None:
            continue
        parts = [
            a.get("name"),
            f"Number: {a.get('number')}" if a.get("number") else None,
            f"Template: {a.get('templateName')}" if a.get("templateName") else None,
            f"Status: {a.get('status') or a.get('state')}",
            f"Result: {a.get('result') or a.get('resultName')}"
            if (a.get("result") or a.get("resultName"))
            else None,
        ]
        text = "\n".join(p for p in parts if p)
        if not text.strip():
            continue
        docs.append(
            {
                "id": f"onetrust:assessment_doc:{aid}",
                "title": a.get("name"),
                "text": text,
                "assessment_id": _s(aid),
            }
        )
    return docs


def ingest_cookies(
    cookies: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                "type": "Cookie",
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
            entities.append({"id": dom_id, "type": "CookieDomain", "name": host})
            relationships.append(
                {"source": node_id, "target": dom_id, "type": "scannedOnDomain"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_inventories(
    inventories: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map inventory records → ``:Inventory`` (+ embedded ``:DataElement``/``:Person``) nodes.

    Accepts the ``BulkUpsertInventoryResponse`` / inventory list shape; extracts any embedded
    ``dataElements`` list into ``:DataElement`` nodes with ``:hasDataElement`` edges.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for inv in inventories or []:
        iid = inv.get("id") or inv.get("externalId")
        if iid is None:
            continue
        node_id = f"onetrust:inventory:{iid}"
        entities.append(
            {
                "id": node_id,
                "type": "Inventory",
                "name": inv.get("name"),
                "number": inv.get("number"),
                "inventoryType": inv.get("inventoryType"),
                "status": inv.get("status"),
                "externalId": _s(iid),
            }
        )
        owners = inv.get("businessOwners") or []
        for owner in owners if isinstance(owners, list) else []:
            pid = _person_id(owner)
            if pid:
                entities.append(_person_node(owner, pid))
                relationships.append(
                    {"source": node_id, "target": pid, "type": "ownedBy"}
                )
        for de in inv.get("dataElements") or []:
            de_ent, de_rels = _data_element_entities(de, parent=node_id)
            entities.extend(de_ent)
            relationships.extend(de_rels)
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_data_elements(
    data_elements: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
            "type": "DataElement",
            "name": de.get("name"),
            "description": de.get("description"),
            "status": de.get("status"),
            "externalId": _s(did),
        }
    ]
    relationships: list[dict[str, Any]] = []
    if parent:
        relationships.append(
            {"source": parent, "target": node_id, "type": "hasDataElement"}
        )
    for ds in de.get("dataSubjectTypes") or []:
        ds_id = ds.get("id") if isinstance(ds, dict) else ds
        ds_name = ds.get("name") if isinstance(ds, dict) else ds
        if ds_id is None:
            continue
        subj_id = f"onetrust:data_subject:{ds_id}"
        entities.append({"id": subj_id, "type": "DataSubject", "name": ds_name})
        relationships.append(
            {"source": node_id, "target": subj_id, "type": "concernsDataSubject"}
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
        "type": "Person",
        "name": person.get("fullName") or person.get("name"),
        "email": person.get("email"),
    }
