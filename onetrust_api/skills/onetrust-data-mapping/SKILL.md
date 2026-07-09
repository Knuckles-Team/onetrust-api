---
name: onetrust-data-mapping
skill_type: skill
description: >-
  Data inventory & data-mapping operations on the OneTrust Data Mapping /
  Inventory API via the onetrust-api MCP server — list and read inventory records
  (assets, vendors, legal entities, processing activities) and their data elements
  with the domain-typed tool. Use when the agent must enumerate the data map, read
  an inventory record by id/external id, inspect a record's relationships, or read
  a data element. Do NOT use for privacy assessments (onetrust-privacy-assessments)
  or cookie scans (onetrust-cookie-consent); prefer those.
license: MIT
tags: [onetrust, data-mapping, inventory, data-element, ropa, privacy, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# OneTrust Data Mapping

Domain-typed access to the OneTrust **Data Mapping / Inventory** API — the data
map of assets, vendors, legal entities, and processing activities, plus the
personal-data elements they process. Prefer the condensed `onetrust_data_mapping`
and `onetrust_inventory` tools over raw HTTP.

## When to use
- Enumerate the data inventory (optionally filtered) and read a record by id or
  external id.
- Inspect an inventory record's relationships and hierarchy.
- Read a data element and its data categories / data-subject types.
- Read inventory relationships and the personal data flowing across them.

## When NOT to use
- Privacy / risk assessments over these records → `onetrust-privacy-assessments`.
- Cookie / tracker scans → `onetrust-cookie-consent`.
- Bulk export of the whole tenant → `onetrust_bulk_export`.
- Generic object CRUD across arbitrary object types → `onetrust_object_manager`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`onetrust-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ONETRUST_HOSTNAME` | ✅ | Tenant host, e.g. `app.onetrust.com` |
| `ONETRUST_API_TOKEN` | ✅ | Bearer OAuth token (or client-credentials pair) |
| `ONETRUST_CLIENT_ID` / `ONETRUST_CLIENT_SECRET` | optional | OAuth2 client-credentials |

Enable the `data_mapping` and `inventory` tags (default in the condensed surface).

## Tools & actions
| Condensed tool | Key actions |
|----------------|-------------|
| `onetrust_data_mapping` | `get_list_of_inventories_using_get`, `get_list_of_inventories_by_filter_criteria_using_post`, `get_inventory_by_id_using_get`, `get_inventory_by_external_id_using_get`, `get_inventory_relations_by_id_using_get`, `get_hierarchy_for_inventory_id_using_get`, `get_data_element_using_get`, `get_all_schemas_using_get` |
| `onetrust_inventory` | `list_all_inventory_relationships_using_post`, `get_personal_data_for_relationships_using_post`, `get_inventory_relationship_using_relationship_type_name` |

### Key parameters
- `inventoryType` — one of `ASSETS`, `VENDORS`, `ENTITIES`, `PROCESSING_ACTIVITIES`.
- `inventoryId` / `externalId` — required for the by-id read actions.
- Inventory records expose `id`, `name`, `number`, `inventoryType`,
  `businessOwners`, `externalId`.
- Data-element records (`DataElementDetailedResponse`) expose `id`, `name`,
  `description`, `status`, `dataSubjectTypes`, `categories`, `classifications`.

## Recipes (`params_json`)
List asset inventory records (first page):
```json
{"inventoryType":"ASSETS","page":0,"size":100}
```
Read one inventory record by id:
```json
{"inventoryId":"<inventoryId>"}
```
Read a data element:
```json
{"dataElementId":"<dataElementId>"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `inventoryType` is required and case-sensitive on the list endpoints — the four
  inventory kinds are distinct object types with distinct records.
- There is no single "list all data elements" endpoint — data elements are read by
  id (`get_data_element_using_get`) or discovered via an inventory record's schema;
  the KG ingestion tool extracts them from inventory records that embed them.
- Records are offset-paginated; the client aggregates pages, so a broad
  `inventoryType` sweep can be large — page it.

## Related
- **KG ingestion:** `onetrust_ingest_inventories` (Wire-First) lists inventory
  records and pushes them into the knowledge graph as typed `:Inventory` nodes,
  extracting embedded data elements into `:DataElement` nodes with `:hasDataElement`
  (and `:ownedBy` Person) links. Use it for ingestion, not the read recipes above.
- **Prompt:** the `privacy_governance_specialist` prompt composes this skill.
- **Sibling skills:** `onetrust-privacy-assessments`, `onetrust-cookie-consent`.
