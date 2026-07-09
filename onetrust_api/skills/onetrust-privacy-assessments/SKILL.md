---
name: onetrust-privacy-assessments
skill_type: skill
description: >-
  Privacy & risk assessment operations on the OneTrust Assessment Automation API
  via the onetrust-api MCP server — list, launch, read, complete, and approve
  PIAs/DPIAs/TRAs with the domain-typed tool. Use when the agent must triage
  in-flight assessments, launch an assessment from a template, submit or review
  responses, or read an assessment's risk result. Do NOT use for cookie-consent
  scans (onetrust-cookie-consent) or the data inventory / data elements
  (onetrust-data-mapping); prefer those.
license: MIT
tags: [onetrust, privacy, assessment, pia, dpia, risk, grc, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# OneTrust Privacy Assessments

Domain-typed access to the OneTrust **Assessment Automation** API for privacy and
risk assessments (PIA / DPIA / TRA). Prefer the condensed `onetrust_assessments`
tool over raw HTTP — it carries the OneTrust assessment field conventions and
returns assessment-shaped records.

## When to use
- List / triage assessments by status, template type, or archival state.
- Launch a new assessment from a template (single or bulk).
- Read an assessment's basic details, results, workflow stage, or risk.
- Drive the lifecycle: submit responses, review, approve, reopen, reassign.

## When NOT to use
- Cookie / tracker scans and consent banners → `onetrust-cookie-consent`.
- The data inventory (assets/vendors/entities) and its data elements →
  `onetrust-data-mapping`.
- DSAR/DSR request handling, incidents, or TPRM → their own domain tools
  (`onetrust_dsar`, `onetrust_incidents`, `onetrust_tprm`).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`onetrust-api`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ONETRUST_HOSTNAME` | ✅ | Tenant host, e.g. `app.onetrust.com` |
| `ONETRUST_API_TOKEN` | ✅ | Bearer OAuth token (or client-credentials pair) |
| `ONETRUST_CLIENT_ID` / `ONETRUST_CLIENT_SECRET` | optional | OAuth2 client-credentials |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface
(used below) vs. the one-to-one verbose tools. The `assessments` tag must be
enabled (default in the condensed surface).

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Key actions |
|----------------|-------------|
| `onetrust_assessments` | `get_all_assessment_basic_details_using_get`, `get_assessments_using_post`, `create_assessment_using_post_1` (launch), `create_bulk_assessment_using_post`, `get_assessment_results_using_get`, `submit_responses_using_post`, `review_assessment_using_post`, `approve_assessment_using_post`, `reopen_assessment_using_post`, `reassign_assessment_using_put`, `get_workflow_details_for_assessment_using_get`, `get_all_basic_template_details_using_get` |

### Key parameters
- `assessmentId` — required for read/result/review/approve/reopen actions.
- Listing (`get_all_assessment_basic_details_using_get`) accepts `templateTypes`,
  `assessmentStatuses`, `assessmentArchivalState`, `page`, `size`, `sort`.
- Launch (`create_assessment_using_post_1`) takes a request body with the template
  id + primary record — pass it under the client method's body params.

## Recipes (`params_json`)
List the first page of in-progress assessments (100 per page):
```json
{"assessmentStatuses":"IN_PROGRESS","page":0,"size":100,"sort":"createDt,desc"}
```
Read one assessment's computed results:
```json
{"assessmentId":"<assessmentId>"}
```
Submit responses to an assessment:
```json
{"assessmentId":"<assessmentId>","responses":[{"questionId":"<qid>","responses":["Yes"]}]}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- The list endpoint is offset-paginated; the client aggregates pages, so a broad
  filter can be large — scope with `assessmentStatuses` + a sane `size`.
- Records come back under `content` in the raw payload; the client `.data` already
  unwraps the aggregated list.
- There are two launch actions (`create_assessment_using_post` and
  `create_assessment_using_post_1`) mapped from different spec versions — the `_1`
  variant is the v2 "Launch Assessment" endpoint; prefer it.
- `assessmentRiskScore` / `residualRiskScore` are only populated once risk is
  calculated — a freshly launched assessment has none.

## Related
- **KG ingestion:** `onetrust_ingest_assessments` (Wire-First) lists assessments
  and natively pushes them into the knowledge graph as typed `:Assessment` nodes
  (+ `:AssessmentTemplate` / `:Person` links) and `:Document` summaries. Use it for
  ingestion, not for the triage/launch recipes above.
- **Prompt:** the `privacy_governance_specialist` prompt composes this skill.
- **Sibling skills:** `onetrust-data-mapping`, `onetrust-cookie-consent`.
