# OneTrust Api - A2A | AG-UI | MCP

![PyPI - Version](https://img.shields.io/pypi/v/onetrust-api)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/onetrust-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/onetrust-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/onetrust-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/onetrust-api)
![PyPI - License](https://img.shields.io/pypi/l/onetrust-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/onetrust-api)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/onetrust-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/onetrust-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/onetrust-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/onetrust-api)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/onetrust-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/onetrust-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/onetrust-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/onetrust-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/onetrust-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/onetrust-api)

*Version: 0.2.0*

## Overview

**OneTrust Api** is a production-grade Python API client, Model Context Protocol
(MCP) server, and A2A agent for the [OneTrust](https://www.onetrust.com/) privacy,
consent, data-governance, and risk platform.

It provides **100% coverage of the OneTrust public API** — every operation across
all **35 OpenAPI specifications** (~600 operations, 7 product areas) is exposed as
both a typed client method and an action-routed MCP tool. The client, MCP tools,
and a machine-readable coverage manifest are all **generated from the vendored
OpenAPI specs** (`onetrust_api/specs/*.json`) by `scripts/generate_from_openapi.py`,
and a coverage test asserts the three sets stay in lock-step.

### Key Features

- **100% Action-Routed MCP Tools** — one consolidated tool per domain (e.g.
  `onetrust_incidents`, `onetrust_dsar`, `onetrust_assessments`) takes an `action`
  plus a `params_json` payload and routes to the underlying API method. 36 tools
  cover every endpoint without flooding the IDE tool list.
- **Full OneTrust surface** — AI Governance, Consent & Preference Management,
  Data Use Governance, Privacy Automation (DSAR, Assessments, Data Mapping,
  Incidents), Tech Risk & Compliance, Third-Party Management, ESG, and Platform.
- **Flexible auth** — a pre-minted OAuth2 bearer token *or* the OAuth2
  client-credentials flow (auto-exchanged and refreshed), plus OIDC delegation
  (RFC 8693) via `agent-utilities`.
- **Multi-region / multi-service aware** — regional tenant pods, the consent
  privacy-portal host, and on-prem worker nodes are resolved per-operation.
- **Resilient** — honours `429` `Retry-After`, retries transient `5xx`, and
  handles both OneTrust pagination styles (offset and cursor).

## MCP

### Using as an MCP Server

The MCP Server runs in `stdio` (local) or `streamable-http` (networked) mode.
Each domain is a tool gated by a `{TAG}TOOL` environment variable (default `True`),
so you can scope the surface (e.g. set `ESGTOOL=False` to drop ESG).

#### Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `ONETRUST_URL` | — | Tenant host URL (overrides ONETRUST_REGION). e.g. https://acme.my.onetrust.com |
| `ONETRUST_REGION` | `us` | Or pick a shared regional pod: us, eu, de, uk, au, ca, fr, in, jp, trial, uat ... |
| `ONETRUST_TOKEN` | — | 1) Pre-minted OAuth2 bearer token (Global Settings > Access Management > Credentials) |
| `ONETRUST_CLIENT_ID` | — | 2) OAuth2 client-credentials (exchanged at /api/access/v1/oauth/token) |
| `ONETRUST_CLIENT_SECRET` | — |  |
| `ONETRUST_CONSENT_URL` | — | Consent transaction / privacy-portal host (consent_receipts, universal_consent ...) |
| `ONETRUST_WORKER_URL` | — | On-prem Data Discovery worker-node host |
| `ONETRUST_SSL_VERIFY` | `True` | ─── HTTP behaviour ──────────────────────────────────────────────────── |
| `FASTMCP_LOG_LEVEL` | `INFO` | ─── MCP transport / auth (agent-utilities) ──────────────────────────── |
| `TRANSPORT` | `stdio` |  |
| `AUTH_TYPE` | `none` |  |
| `ACCESS_MANAGEMENTTOOL` | `True` | MCP tools table (condensed action-routed surface). |
| `AI_GOVERNANCETOOL` | `True` |  |
| `CUSTOM_APITOOL` | `True` |  |
| `ASSESSMENTSTOOL` | `True` |  |
| `AUDIT_MANAGEMENTTOOL` | `True` |  |
| `BULK_EXPORTTOOL` | `True` |  |
| `CMPTOOL` | `True` |  |
| `COMPLIANCE_AUTOMATIONTOOL` | `True` |  |
| `CONSENT_INTERFACESTOOL` | `True` |  |
| `CONSENT_RECEIPTSTOOL` | `True` |  |
| `COOKIE_CONSENTTOOL` | `True` |  |
| `COOKIE_CONSENT_LEGACYTOOL` | `True` |  |
| `COOKIE_DOMAIN_DATATOOL` | `True` |  |
| `CROSS_DEVICE_CONSENTTOOL` | `True` |  |
| `DATA_CATALOGTOOL` | `True` |  |
| `DATA_DISCOVERYTOOL` | `True` |  |
| `DATA_DISCOVERY_WORKERTOOL` | `True` |  |
| `DATA_MAPPINGTOOL` | `True` |  |
| `DATA_MAPPING_LEGACYTOOL` | `True` |  |
| `DOCUMENTSTOOL` | `True` |  |
| `DSARTOOL` | `True` |  |
| `ESGTOOL` | `True` |  |
| `INCIDENTSTOOL` | `True` |  |
| `INTEGRATIONSTOOL` | `True` |  |
| `INVENTORYTOOL` | `True` |  |
| `ISSUES_MANAGEMENTTOOL` | `True` |  |
| `IT_RISK_MANAGEMENTTOOL` | `True` |  |
| `MOBILE_APP_CONSENTTOOL` | `True` |  |
| `OBJECT_MANAGERTOOL` | `True` |  |
| `POLICY_MANAGEMENTTOOL` | `True` |  |
| `PRIVACY_NOTICESTOOL` | `True` |  |
| `TASK_MANAGEMENTTOOL` | `True` |  |
| `TPRMTOOL` | `True` |  |
| `TRAININGTOOL` | `True` |  |
| `UNIVERSAL_CONSENTTOOL` | `True` |  |
| `USER_PROVISIONINGTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Bind host (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `EUNOMIA_TYPE` | `none` | Authorization mode: `none` | `embedded` | `remote` |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` | Embedded Eunomia policy file |
| `EUNOMIA_REMOTE_URL` | — | Remote Eunomia authorization server URL |
| `ENABLE_OTEL` | `False` | Enable OpenTelemetry export |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | OTLP collector endpoint |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_47 package + 21 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


| Variable | Description |
| --- | --- |
| `ONETRUST_URL` | Tenant host URL, e.g. `https://acme.my.onetrust.com` (overrides region). |
| `ONETRUST_REGION` | Shared pod when no URL is set: `us`, `eu`, `de`, `uk`, `au`, `ca`, `fr`, `in`, `jp`, `trial`, `uat`, … (default `us`). |
| `ONETRUST_TOKEN` | Pre-minted OAuth2 bearer token. |
| `ONETRUST_CLIENT_ID` / `ONETRUST_CLIENT_SECRET` | OAuth2 client-credentials (exchanged at `/api/access/v1/oauth/token`). |
| `ONETRUST_CONSENT_URL` | Optional host for consent-transaction APIs (privacy portal). |
| `ONETRUST_WORKER_URL` | Optional on-prem Data Discovery worker-node host. |
| `ONETRUST_SSL_VERIFY` | Verify TLS (default `True`). |
| `<DOMAIN>TOOL` | Toggle a domain tool, e.g. `INCIDENTSTOOL`, `DSARTOOL`, `CONSENT_RECEIPTSTOOL` (default `True`). |

#### Run in stdio mode (default):
```bash
export ONETRUST_URL="https://acme.my.onetrust.com"
export ONETRUST_TOKEN="your_token"
onetrust-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export ONETRUST_URL="https://acme.my.onetrust.com"
export ONETRUST_TOKEN="your_token"
onetrust-mcp --transport "streamable-http" --host "0.0.0.0" --port "8000"
```

### Tool Domains

`access_management`, `ai_governance`, `assessments`, `audit_management`,
`bulk_export`, `cmp`, `compliance_automation`, `consent_interfaces`,
`consent_receipts`, `cookie_consent`, `cookie_consent_legacy`,
`cookie_domain_data`, `cross_device_consent`, `data_catalog`, `data_discovery`,
`data_discovery_worker`, `data_mapping`, `data_mapping_legacy`, `documents`,
`dsar`, `esg`, `incidents`, `integrations`, `inventory`, `issues_management`,
`it_risk_management`, `mobile_app_consent`, `object_manager`, `policy_management`,
`privacy_notices`, `task_management`, `tprm`, `training`, `universal_consent`,
`user_provisioning` — plus `custom_api` (a raw REST escape hatch).

### Available MCP Tools

<!-- This table is auto-generated by `python -m agent_utilities.mcp.readme_tools` — do not edit by hand. -->

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `onetrust_access_management` | `ACCESS_MANAGEMENTTOOL` | Manage OneTrust access management operations. |
| `onetrust_ai_governance` | `AI_GOVERNANCETOOL` | Manage OneTrust ai governance operations. |
| `onetrust_api_request` | `CUSTOM_APITOOL` | Execute an arbitrary OneTrust REST API request directly. |
| `onetrust_assessments` | `ASSESSMENTSTOOL` | Manage OneTrust assessments operations. |
| `onetrust_audit_management` | `AUDIT_MANAGEMENTTOOL` | Manage OneTrust audit management operations. |
| `onetrust_bulk_export` | `BULK_EXPORTTOOL` | Manage OneTrust bulk export operations. |
| `onetrust_cmp` | `CMPTOOL` | Manage OneTrust cmp operations. |
| `onetrust_compliance_automation` | `COMPLIANCE_AUTOMATIONTOOL` | Manage OneTrust compliance automation operations. |
| `onetrust_consent_interfaces` | `CONSENT_INTERFACESTOOL` | Manage OneTrust consent interfaces operations. |
| `onetrust_consent_receipts` | `CONSENT_RECEIPTSTOOL` | Manage OneTrust consent receipts operations. |
| `onetrust_cookie_consent` | `COOKIE_CONSENTTOOL` | Manage OneTrust cookie consent operations. |
| `onetrust_cookie_consent_legacy` | `COOKIE_CONSENT_LEGACYTOOL` | Manage OneTrust cookie consent legacy operations. |
| `onetrust_cookie_domain_data` | `COOKIE_DOMAIN_DATATOOL` | Manage OneTrust cookie domain data operations. |
| `onetrust_cross_device_consent` | `CROSS_DEVICE_CONSENTTOOL` | Manage OneTrust cross device consent operations. |
| `onetrust_data_catalog` | `DATA_CATALOGTOOL` | Manage OneTrust data catalog operations. |
| `onetrust_data_discovery` | `DATA_DISCOVERYTOOL` | Manage OneTrust data discovery operations. |
| `onetrust_data_discovery_worker` | `DATA_DISCOVERY_WORKERTOOL` | Manage OneTrust data discovery worker operations. |
| `onetrust_data_mapping` | `DATA_MAPPINGTOOL` | Manage OneTrust data mapping operations. |
| `onetrust_data_mapping_legacy` | `DATA_MAPPING_LEGACYTOOL` | Manage OneTrust data mapping legacy operations. |
| `onetrust_documents` | `DOCUMENTSTOOL` | Manage OneTrust documents operations. |
| `onetrust_dsar` | `DSARTOOL` | Manage OneTrust dsar operations. |
| `onetrust_esg` | `ESGTOOL` | Manage OneTrust esg operations. |
| `onetrust_incidents` | `INCIDENTSTOOL` | Manage OneTrust incidents operations. |
| `onetrust_integrations` | `INTEGRATIONSTOOL` | Manage OneTrust integrations operations. |
| `onetrust_inventory` | `INVENTORYTOOL` | Manage OneTrust inventory operations. |
| `onetrust_issues_management` | `ISSUES_MANAGEMENTTOOL` | Manage OneTrust issues management operations. |
| `onetrust_it_risk_management` | `IT_RISK_MANAGEMENTTOOL` | Manage OneTrust it risk management operations. |
| `onetrust_mobile_app_consent` | `MOBILE_APP_CONSENTTOOL` | Manage OneTrust mobile app consent operations. |
| `onetrust_object_manager` | `OBJECT_MANAGERTOOL` | Manage OneTrust object manager operations. |
| `onetrust_policy_management` | `POLICY_MANAGEMENTTOOL` | Manage OneTrust policy management operations. |
| `onetrust_privacy_notices` | `PRIVACY_NOTICESTOOL` | Manage OneTrust privacy notices operations. |
| `onetrust_task_management` | `TASK_MANAGEMENTTOOL` | Manage OneTrust task management operations. |
| `onetrust_tprm` | `TPRMTOOL` | Manage OneTrust tprm operations. |
| `onetrust_training` | `TRAININGTOOL` | Manage OneTrust training operations. |
| `onetrust_universal_consent` | `UNIVERSAL_CONSENTTOOL` | Manage OneTrust universal consent operations. |
| `onetrust_user_provisioning` | `USER_PROVISIONINGTOOL` | Manage OneTrust user provisioning operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>597 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `onetrust_add_access_levels_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Add User Group Roles |
| `onetrust_add_amember_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Add User to User Group |
| `onetrust_add_attachments_to_implementation_using_post` | `IT_RISK_MANAGEMENTTOOL` | Attach Files to Control Implementation |
| `onetrust_add_attribute_using_post` | `AI_GOVERNANCETOOL` | Add Attribute to Schema |
| `onetrust_add_attribute_using_post_x` | `OBJECT_MANAGERTOOL` | Add Attribute to Schema |
| `onetrust_add_comments_using_put` | `DSARTOOL` | Add Comment to Request |
| `onetrust_add_consent_groups_to_consent_group_using_post` | `UNIVERSAL_CONSENTTOOL` | Add Consent Groups to Parent Consent Group |
| `onetrust_add_control_using_post` | `IT_RISK_MANAGEMENTTOOL` | Create Control |
| `onetrust_add_controls_to_inventory_using_post` | `DATA_MAPPINGTOOL` | Create Control Implementation |
| `onetrust_add_controls_to_risk_using_post` | `IT_RISK_MANAGEMENTTOOL` | Add Controls to Risk |
| `onetrust_add_data_discovery_using_put` | `DSARTOOL` | Add Targeted Data Discovery Details to Subtask |
| `onetrust_add_data_subjects_to_consent_group_using_post` | `UNIVERSAL_CONSENTTOOL` | Add Data Subjects to Parent Consent Group |
| `onetrust_add_document_to_policy` | `POLICY_MANAGEMENTTOOL` | Add Document Attachments |
| `onetrust_add_emission_factor` | `ESGTOOL` | Create Emission Factor |
| `onetrust_add_emission_transaction` | `ESGTOOL` | Create Emission Transaction |
| `onetrust_add_entity_using_entity_type_id_or_entity_type_name_using_post` | `AI_GOVERNANCETOOL` | Create Entity |
| `onetrust_add_entity_using_entity_type_id_or_entity_type_name_using_post_x` | `OBJECT_MANAGERTOOL` | Create Object |
| `onetrust_add_evidence_implementation_attachment` | `IT_RISK_MANAGEMENTTOOL` | Add Attachments to Evidence Task Implementation |
| `onetrust_add_manual_assessment_links_using_post` | `ASSESSMENTSTOOL` | Link Assessments |
| `onetrust_add_members_using_post` | `ACCESS_MANAGEMENTTOOL` | Add Members to User Group |
| `onetrust_add_multiple_members_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Add Multiple Users to User Group |
| `onetrust_add_new_resolution_using_post` | `DSARTOOL` | Create Resolution |
| `onetrust_add_options_using_post` | `AI_GOVERNANCETOOL` | Add Options to Attribute |
| `onetrust_add_options_using_post_x` | `OBJECT_MANAGERTOOL` | Add Options to Attribute |
| `onetrust_add_or_update_tags_using_put` | `ASSESSMENTSTOOL` | Update Assessment Tags |
| `onetrust_add_purpose_rules_to_consent_group_using_post` | `UNIVERSAL_CONSENTTOOL` | Add Purpose Rules to Consent Group |
| `onetrust_add_relationship_between_entities_using_post` | `INVENTORYTOOL` | Create Relationship |
| `onetrust_add_scans` | `COOKIE_CONSENTTOOL` | Scan Websites |
| `onetrust_add_threat_to_risk` | `IT_RISK_MANAGEMENTTOOL` | Add Threat to Risk |
| `onetrust_add_threat_using_post_1` | `IT_RISK_MANAGEMENTTOOL` | Create Threat |
| `onetrust_add_threats_using_post` | `IT_RISK_MANAGEMENTTOOL` | Create Multiple Threats |
| `onetrust_add_user_access_level_v2` | `ACCESS_MANAGEMENTTOOL` | Add User Role |
| `onetrust_add_vulnerabilities_to_risk` | `IT_RISK_MANAGEMENTTOOL` | Add Vulnerabilities to Risk |
| `onetrust_add_vulnerabilities_using_post` | `IT_RISK_MANAGEMENTTOOL` | Create Multiple Vulnerabilities |
| `onetrust_add_vulnerability_using_post_1` | `IT_RISK_MANAGEMENTTOOL` | Create Vulnerability |
| `onetrust_applicationdata` | `MOBILE_APP_CONSENTTOOL` | Get SDK Configuration |
| `onetrust_approve_assessment_using_post` | `ASSESSMENTSTOOL` | Approve Assessment |
| `onetrust_approve_risk_using_put` | `IT_RISK_MANAGEMENTTOOL` | Approve Risk |
| `onetrust_archive_assessments_using_put` | `ASSESSMENTSTOOL` | Archive Assessment |
| `onetrust_archive_scans` | `COOKIE_CONSENTTOOL` | Archive Scans |
| `onetrust_assign_entities_to_geo_rule_group` | `COOKIE_CONSENTTOOL` | Assign Geolocation Rule Group |
| `onetrust_assign_stage_by_name` | `AI_GOVERNANCETOOL` | Update Entity Workflow Stage |
| `onetrust_assign_stage_by_name_1` | `INCIDENTSTOOL` | Update Incident Stage by Type |
| `onetrust_assign_stage_by_name_x` | `INCIDENTSTOOL` | Update Incident Stage |
| `onetrust_bulk_add_cookies` | `COOKIE_CONSENTTOOL` | Add Cookies |
| `onetrust_bulk_cancel_domain_schedule` | `COOKIE_CONSENTTOOL` | Cancel Scheduled Website Scans |
| `onetrust_bulk_create_links_using_post` | `IT_RISK_MANAGEMENTTOOL` | Link Controls |
| `onetrust_bulk_delete_cookies` | `COOKIE_CONSENTTOOL` | Delete Cookies |
| `onetrust_bulk_delete_using_put` | `DSARTOOL` | Delete Requests |
| `onetrust_bulk_edit_cookies` | `COOKIE_CONSENTTOOL` | Edit Cookies |
| `onetrust_cancel_bulk_export_delete` | `BULK_EXPORTTOOL` | Cancel Bulk Export |
| `onetrust_cancel_job_using_patch` | `DATA_DISCOVERYTOOL` | Cancel Scan Job |
| `onetrust_cancel_scan` | `COOKIE_CONSENTTOOL` | Cancel Scan |
| `onetrust_cancel_scan_job` | `DATA_DISCOVERYTOOL` | Cancel Scan Job |
| `onetrust_catalog_data_using_post` | `DATA_DISCOVERY_WORKERTOOL` | Submit Data to Catalog |
| `onetrust_change_risk_stage_using_post` | `IT_RISK_MANAGEMENTTOOL` | Update Risk Stage |
| `onetrust_check_scans_status` | `COOKIE_CONSENTTOOL` | Get Scan Statuses |
| `onetrust_classify_data_using_post` | `DATA_DISCOVERY_WORKERTOOL` | Submit Data to Classify |
| `onetrust_complete_sub_task_using_put` | `DSARTOOL` | Complete Subtask |
| `onetrust_copy_inventory_using_post` | `DATA_MAPPINGTOOL` | Copy Inventory |
| `onetrust_create_application` | `COOKIE_CONSENTTOOL` | Create Application |
| `onetrust_create_assessment_risk_using_post` | `ASSESSMENTSTOOL` | Create Assessment Risk |
| `onetrust_create_assessment_using_post` | `ASSESSMENTSTOOL` | Launch Assessment |
| `onetrust_create_assessment_using_post_1` | `ASSESSMENTSTOOL` | Launch Assessment |
| `onetrust_create_bulk_assessment_using_post` | `ASSESSMENTSTOOL` | Launch Assessments in Bulk |
| `onetrust_create_bulk_consent_receipt_using_post` | `CONSENT_RECEIPTSTOOL` | Create Consent Receipts in Bulk |
| `onetrust_create_collection_point_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Collection Point |
| `onetrust_create_consent_group_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Consent Group |
| `onetrust_create_consent_receipt_using_post` | `CONSENT_RECEIPTSTOOL` | Create Consent Receipts |
| `onetrust_create_credential` | `DATA_DISCOVERYTOOL` | Create Credential |
| `onetrust_create_custom_link_type_using_post` | `OBJECT_MANAGERTOOL` | Create Relationship Type between Objects |
| `onetrust_create_custom_preference_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Purpose Preference |
| `onetrust_create_data_asset_tag_associations_v1` | `DATA_CATALOGTOOL` | Create Tag Associations |
| `onetrust_create_data_asset_term_associations_v1` | `DATA_CATALOGTOOL` | Create Term Associations |
| `onetrust_create_data_category_using_post` | `DATA_MAPPINGTOOL` | Create Data Category |
| `onetrust_create_data_classification_using_post` | `DATA_MAPPINGTOOL` | Create Data Classification |
| `onetrust_create_data_element_using_post` | `DATA_MAPPINGTOOL` | Create Data Element |
| `onetrust_create_data_subject_group_v4` | `UNIVERSAL_CONSENTTOOL` | Create Data Subject Group |
| `onetrust_create_data_subject_using_post` | `DATA_MAPPINGTOOL` | Create Data Subject |
| `onetrust_create_detector` | `DATA_DISCOVERYTOOL` | Create Custom Classifier |
| `onetrust_create_domain_group` | `COOKIE_CONSENTTOOL` | Create or Update Domain Group |
| `onetrust_create_domain_group_using_post` | `COOKIE_CONSENT_LEGACYTOOL` | Create or Update Domain Group |
| `onetrust_create_engagement_using_post` | `TPRMTOOL` | Create Engagement |
| `onetrust_create_group` | `USER_PROVISIONINGTOOL` | Create User Group |
| `onetrust_create_identified_consent_receipt_using_post` | `CONSENT_RECEIPTSTOOL` | Create Identified Consent Receipts |
| `onetrust_create_incident_using_post` | `INCIDENTSTOOL` | Create Incident |
| `onetrust_create_index` | `UNIVERSAL_CONSENTTOOL` | Create Custom Index |
| `onetrust_create_inventory_links` | `INCIDENTSTOOL` | Link Incident to Inventory |
| `onetrust_create_inventory_relations_using_post` | `INVENTORYTOOL` | Create Relationship |
| `onetrust_create_inventory_using_post` | `DATA_MAPPINGTOOL` | Create Inventory |
| `onetrust_create_issue_relationship_links_using_post` | `ISSUES_MANAGEMENTTOOL` | Create Issue Relationship |
| `onetrust_create_issue_using_post` | `ISSUES_MANAGEMENTTOOL` | Create Issue |
| `onetrust_create_job_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Job |
| `onetrust_create_job_using_post_x` | `DATA_DISCOVERYTOOL` | Create Scan Job |
| `onetrust_create_link_record_between_entities_using_link_type_id_using_post` | `AI_GOVERNANCETOOL` | Create Relationship Record between Entities |
| `onetrust_create_link_record_between_entities_using_link_type_id_using_post_x` | `OBJECT_MANAGERTOOL` | Create Relationship Record between Objects |
| `onetrust_create_linked_identity_group_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Data Subject Group |
| `onetrust_create_model_using_post` | `OBJECT_MANAGERTOOL` | Create Model Object |
| `onetrust_create_new_cookie` | `COOKIE_CONSENT_LEGACYTOOL` | Create Cookie |
| `onetrust_create_new_purpose_version_using_post` | `UNIVERSAL_CONSENTTOOL` | Create New Purpose Version |
| `onetrust_create_or_update_data_subject_using_post` | `UNIVERSAL_CONSENTTOOL` | Update Data Subject's Data Elements |
| `onetrust_create_or_upsert_data_asset_v1` | `DATA_CATALOGTOOL` | Create Data Asset |
| `onetrust_create_organization_using_post` | `ACCESS_MANAGEMENTTOOL` | Create Organization |
| `onetrust_create_policy` | `POLICY_MANAGEMENTTOOL` | Create Document |
| `onetrust_create_policy_versions` | `POLICY_MANAGEMENTTOOL` | Create Document Version |
| `onetrust_create_project_using_post` | `OBJECT_MANAGERTOOL` | Create Project Object |
| `onetrust_create_purpose_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Purpose |
| `onetrust_create_relations_using_post` | `DATA_MAPPINGTOOL` | Link Inventory |
| `onetrust_create_request_queue_from_message_using_post` | `DSARTOOL` | Create Request |
| `onetrust_create_request_queue_v2_using_post` | `DSARTOOL` | Create Request |
| `onetrust_create_risk_using_post` | `IT_RISK_MANAGEMENTTOOL` | Create Risk |
| `onetrust_create_stand_alone_risk_using_post` | `IT_RISK_MANAGEMENTTOOL` | Create Risk |
| `onetrust_create_sub_task_from_template_using_post` | `DSARTOOL` | Add Subtask to Request using Subtask Template |
| `onetrust_create_sub_task_using_post` | `DSARTOOL` | Add Subtask to Request |
| `onetrust_create_tag_v2` | `DATA_CATALOGTOOL` | Create Tag |
| `onetrust_create_task_using_post` | `TASK_MANAGEMENTTOOL` | Create Task |
| `onetrust_create_task_using_post_1` | `AI_GOVERNANCETOOL` | Create Task |
| `onetrust_create_task_using_post_1_x` | `OBJECT_MANAGERTOOL` | Create Task |
| `onetrust_create_task_using_post_x` | `ASSESSMENTSTOOL` | Create Assessment Task |
| `onetrust_create_term_using_post` | `DATA_CATALOGTOOL` | Create Term |
| `onetrust_create_update_risk_using_put` | `IT_RISK_MANAGEMENTTOOL` | Create or Update Risk |
| `onetrust_create_user` | `USER_PROVISIONINGTOOL` | Create User |
| `onetrust_create_user_group_using_post` | `ACCESS_MANAGEMENTTOOL` | Create User Group |
| `onetrust_create_user_group_v2` | `ACCESS_MANAGEMENTTOOL` | Create User Group |
| `onetrust_create_user_using_post` | `USER_PROVISIONINGTOOL` | Create User |
| `onetrust_create_user_v2` | `ACCESS_MANAGEMENTTOOL` | Create User |
| `onetrust_create_v2_using_post` | `DATA_DISCOVERYTOOL` | Create Scan Profile |
| `onetrust_create_v2_using_post_x` | `INTEGRATIONSTOOL` | Create System Credential |
| `onetrust_create_v2_verification_method_using_post` | `DSARTOOL` | Create Verification Method |
| `onetrust_create_vendor_contract_using_post` | `TPRMTOOL` | Create Contract |
| `onetrust_create_version_using_post` | `UNIVERSAL_CONSENTTOOL` | Create New Collection Point Version |
| `onetrust_cross_device_consent_using_delete` | `UNIVERSAL_CONSENTTOOL` | Delete Cross Device Consents and Receipts |
| `onetrust_data_discovery_updates_using_post` | `DSARTOOL` | Add Targeted Data Discovery Results Summary to Request |
| `onetrust_delete_audit_using_delete` | `AUDIT_MANAGEMENTTOOL` | Delete Audit |
| `onetrust_delete_consent_group_purpose_rule_using_delete` | `UNIVERSAL_CONSENTTOOL` | Remove Purpose Rule from Consent Group |
| `onetrust_delete_credential` | `DATA_DISCOVERYTOOL` | Delete Credential |
| `onetrust_delete_data_asset_tag_associations_v1` | `DATA_CATALOGTOOL` | Delete Multiple Data Asset Tag Associations |
| `onetrust_delete_data_asset_term_associations_v1` | `DATA_CATALOGTOOL` | Delete Multiple Data Asset Term Associations |
| `onetrust_delete_data_asset_v1` | `DATA_CATALOGTOOL` | Delete Data Asset |
| `onetrust_delete_data_category_using_delete` | `DATA_MAPPINGTOOL` | Delete Data Category |
| `onetrust_delete_data_classification_using_delete` | `DATA_MAPPINGTOOL` | Delete Data Classification |
| `onetrust_delete_data_element_using_delete` | `DATA_MAPPINGTOOL` | Delete Data Element |
| `onetrust_delete_data_subject_profile_using_delete` | `UNIVERSAL_CONSENTTOOL` | Delete Data Subjects |
| `onetrust_delete_data_subject_profiles_using_delete` | `UNIVERSAL_CONSENTTOOL` | Delete Purposes from Data Subject |
| `onetrust_delete_data_subject_using_delete` | `DATA_MAPPINGTOOL` | Delete Data Subject |
| `onetrust_delete_data_subject_using_ttl` | `UNIVERSAL_CONSENTTOOL` | Delete Data Subject |
| `onetrust_delete_data_subjects_to_consent_group_using_delete` | `UNIVERSAL_CONSENTTOOL` | Remove Data Subject from Parent Consent Group |
| `onetrust_delete_detector` | `DATA_DISCOVERYTOOL` | Delete Custom Classifier |
| `onetrust_delete_domain` | `COOKIE_CONSENTTOOL` | Delete Domain |
| `onetrust_delete_group` | `USER_PROVISIONINGTOOL` | Delete User Group |
| `onetrust_delete_inventory_relations_using_relationship_type_name` | `INVENTORYTOOL` | Delete Relationship by Type ID |
| `onetrust_delete_inventory_relations_using_relationship_type_name_1` | `INVENTORYTOOL` | Delete Relationship by Type Name |
| `onetrust_delete_inventory_using_delete` | `DATA_MAPPINGTOOL` | Delete Inventory |
| `onetrust_delete_link_record_by_id_and_type_using_link_type_id_using_delete` | `AI_GOVERNANCETOOL` | Remove Relationship Record |
| `onetrust_delete_link_record_by_id_and_type_using_link_type_id_using_delete_x` | `OBJECT_MANAGERTOOL` | Remove Relationship Record |
| `onetrust_delete_merge_request_using_delete` | `UNIVERSAL_CONSENTTOOL` | Delete Scheduled Export |
| `onetrust_delete_model_using_delete` | `OBJECT_MANAGERTOOL` | Delete Model Object |
| `onetrust_delete_organization_post` | `ACCESS_MANAGEMENTTOOL` | Delete Organization |
| `onetrust_delete_project_using_delete` | `OBJECT_MANAGERTOOL` | Delete Project Object |
| `onetrust_delete_purpose_from_data_subject_using_delete` | `UNIVERSAL_CONSENTTOOL` | Delete Purpose from Data Subjects |
| `onetrust_delete_purpose_from_data_subjects_using_ttl` | `UNIVERSAL_CONSENTTOOL` | Delete Purposes from Data Subjects |
| `onetrust_delete_relations_using_delete` | `DATA_MAPPINGTOOL` | Delete Inventory Link |
| `onetrust_delete_resolution_using_delete` | `DSARTOOL` | Delete Resolution |
| `onetrust_delete_risk_using_delete` | `IT_RISK_MANAGEMENTTOOL` | Delete Risk |
| `onetrust_delete_scan_profile_using_delete_1` | `DATA_DISCOVERYTOOL` | Delete Scan Profile |
| `onetrust_delete_scope_using_delete` | `AUDIT_MANAGEMENTTOOL` | Delete Audit Scope |
| `onetrust_delete_system_using_delete_1` | `DATA_DISCOVERYTOOL` | Delete Data Source |
| `onetrust_delete_template_versions_using_delete` | `ASSESSMENTSTOOL` | Delete Template |
| `onetrust_delete_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Delete User Group |
| `onetrust_delete_user_group_using_delete` | `ACCESS_MANAGEMENTTOOL` | Delete User Group |
| `onetrust_delete_user_using_delete` | `USER_PROVISIONINGTOOL` | Delete User |
| `onetrust_delete_using_delete` | `UNIVERSAL_CONSENTTOOL` | Delete Data Subject Group |
| `onetrust_delete_using_entity_type_id_or_entity_type_name_using_delete` | `AI_GOVERNANCETOOL` | Delete Entity |
| `onetrust_delete_using_entity_type_id_or_entity_type_name_using_delete_x` | `OBJECT_MANAGERTOOL` | Delete Object |
| `onetrust_disable_attribute_using_put` | `AI_GOVERNANCETOOL` | Disable Attribute |
| `onetrust_disable_attribute_using_put_x` | `OBJECT_MANAGERTOOL` | Disable Attribute |
| `onetrust_disable_collection_point_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Collection Point Status |
| `onetrust_domaindata` | `COOKIE_DOMAIN_DATATOOL` | Get Domain Data |
| `onetrust_download_consent_attachments` | `UNIVERSAL_CONSENTTOOL` | Download All Consent Attachments |
| `onetrust_download_given_consent_attachments` | `UNIVERSAL_CONSENTTOOL` | Download Consent Attachment |
| `onetrust_download_script_file` | `COOKIE_CONSENTTOOL` | Download Script File |
| `onetrust_download_to_local_using_get` | `COOKIE_CONSENT_LEGACYTOOL` | Download Script File |
| `onetrust_edit_collection_point_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Existing Collection Point |
| `onetrust_edit_custom_preference_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Purpose Preference |
| `onetrust_edit_purpose_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Purpose |
| `onetrust_edit_workpaper_details_using_post` | `AUDIT_MANAGEMENTTOOL` | Update Workpaper |
| `onetrust_enable_attribute_using_put` | `AI_GOVERNANCETOOL` | Enable Attribute |
| `onetrust_enable_attribute_using_put_x` | `OBJECT_MANAGERTOOL` | Enable Attribute |
| `onetrust_enabled_custom_entity_type_using_put` | `OBJECT_MANAGERTOOL` | Enable Custom Object Type by ID |
| `onetrust_enabled_custom_entity_type_using_put_1` | `OBJECT_MANAGERTOOL` | Enable Custom Object Type by Name |
| `onetrust_enroll_users_to_course_using_post` | `TRAININGTOOL` | Enroll Users to Course |
| `onetrust_export_assessment_using_get` | `ASSESSMENTSTOOL` | Get Assessment |
| `onetrust_export_template_with_business_keys_using_get` | `ASSESSMENTSTOOL` | Export Template |
| `onetrust_export_workflow_using_get_1` | `INTEGRATIONSTOOL` | Export Workflow |
| `onetrust_exportduplicatedatasubject` | `UNIVERSAL_CONSENTTOOL` | Generate Export of Duplicate Data Subjects |
| `onetrust_external_search` | `DATA_CATALOGTOOL` | Get Catalog Search Results |
| `onetrust_external_search_using_continuationtoken` | `DATA_CATALOGTOOL` | Get Catalog Search Results |
| `onetrust_fetch_all_contract_types_using_get` | `TPRMTOOL` | Get List of Contract Types |
| `onetrust_fetch_metrics_details` | `ESGTOOL` | Get Metric Details |
| `onetrust_file_location` | `DOCUMENTSTOOL` | Get File Location |
| `onetrust_file_upload` | `DOCUMENTSTOOL` | Upload File |
| `onetrust_find_all_by_link_type_and_criteria_using_post` | `OBJECT_MANAGERTOOL` | Get List of Relationship Link Types |
| `onetrust_find_all_by_type_and_criteria` | `ESGTOOL` | Get List of Emission Details |
| `onetrust_find_all_by_type_and_criteria_using_post` | `OBJECT_MANAGERTOOL` | Get List of Object Types |
| `onetrust_find_all_by_type_and_criteria_using_post_1` | `AI_GOVERNANCETOOL` | Get List of Entity Types |
| `onetrust_find_all_by_type_id_and_criteria_using_post` | `AI_GOVERNANCETOOL` | Get Full Entity Details |
| `onetrust_find_all_by_type_id_and_criteria_using_post_x` | `OBJECT_MANAGERTOOL` | Get Full Object Details |
| `onetrust_find_all_control_implementations_attributes_and_options_by_using_post` | `IT_RISK_MANAGEMENTTOOL` | Search Control Implementation Attributes |
| `onetrust_find_all_control_implementations_using_post` | `IT_RISK_MANAGEMENTTOOL` | Get List of Control Implementations |
| `onetrust_find_all_evidences_by_search_criteria_1` | `IT_RISK_MANAGEMENTTOOL` | Get List of Evidence Task Implementations |
| `onetrust_find_all_initiatives_by_filter_using_post` | `COMPLIANCE_AUTOMATIONTOOL` | Get List of Initiatives |
| `onetrust_find_all_issues_by_filter_using_post` | `ISSUES_MANAGEMENTTOOL` | Get List of Issues |
| `onetrust_find_associated_control_implementations_using_post` | `IT_RISK_MANAGEMENTTOOL` | Get List of Control Implementations by Entity |
| `onetrust_find_by_guid_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Purpose Preference |
| `onetrust_find_controls_by_criteria_using_post_1` | `IT_RISK_MANAGEMENTTOOL` | Get List of Controls |
| `onetrust_find_entity_basic_details_by_type_and_criteria_using_post` | `AI_GOVERNANCETOOL` | Get Basic Entity Details |
| `onetrust_find_entity_basic_details_by_type_and_criteria_using_post_x` | `OBJECT_MANAGERTOOL` | Get Basic Object Details |
| `onetrust_find_evidence_implementations_by_id_1` | `IT_RISK_MANAGEMENTTOOL` | Get Evidence Task Implementation |
| `onetrust_find_model_basic_details_by_query_criteria_using_post` | `OBJECT_MANAGERTOOL` | Get Basic Model Object Details |
| `onetrust_find_models_by_list_criteria_using_post` | `OBJECT_MANAGERTOOL` | Get Model Object Details |
| `onetrust_find_project_basic_details_by_query_criteria_using_post` | `OBJECT_MANAGERTOOL` | Get Basic Project Object Details |
| `onetrust_find_projects_by_list_criteria_using_post` | `OBJECT_MANAGERTOOL` | Get Project Object Details |
| `onetrust_find_receipt_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Receipt |
| `onetrust_find_task_using_get_1` | `AI_GOVERNANCETOOL` | Get Task |
| `onetrust_find_task_using_get_1_x` | `OBJECT_MANAGERTOOL` | Get Task |
| `onetrust_find_threats_by_criteria_using_post` | `IT_RISK_MANAGEMENTTOOL` | Get List of Threats |
| `onetrust_find_vulnerabilities_by_criteria_using_post` | `IT_RISK_MANAGEMENTTOOL` | Get List of Vulnerabilities |
| `onetrust_get_access_levels_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Get User Group Roles |
| `onetrust_get_active_categories_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get List of Risk Categories |
| `onetrust_get_all_assessment_basic_details_using_get` | `ASSESSMENTSTOOL` | Get List of Assessments |
| `onetrust_get_all_basic_template_details_using_get` | `ASSESSMENTSTOOL` | Get List of Templates |
| `onetrust_get_all_data_asset_attribute_names` | `DATA_CATALOGTOOL` | Get List of Data Asset Attributes |
| `onetrust_get_all_emission_factors_basic_entity_details` | `ESGTOOL` | Get List of Emission Factors |
| `onetrust_get_all_enabled_control_entity_types_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get List of Control Entity Source Types |
| `onetrust_get_all_enabled_risk_entity_types_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get List of Risk Entity Types |
| `onetrust_get_all_enabled_source_entity_types_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get List of Risk Entity Source Types |
| `onetrust_get_all_glossaries_by_names` | `DATA_CATALOGTOOL` | Get Glossary |
| `onetrust_get_all_glossaries_names` | `DATA_CATALOGTOOL` | Get List of Glossaries |
| `onetrust_get_all_group_and_attachment_details_using_get` | `DSARTOOL` | Get Targeted Data Discovery Group |
| `onetrust_get_all_group_by_request_using_get` | `DSARTOOL` | Get List of Targeted Data Discovery Groups |
| `onetrust_get_all_profiles_by_data_subject_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of All Purpose Details by Data Subject |
| `onetrust_get_all_related_control_entity_types_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get Related Control Entity Types |
| `onetrust_get_all_request_queues_v2_using_get` | `DSARTOOL` | Get List of Requests |
| `onetrust_get_all_schemas_using_get` | `DATA_MAPPINGTOOL` | Get List of Inventory Schemas |
| `onetrust_get_all_sub_task_by_ref_id_using_get` | `DSARTOOL` | Get List of Subtasks by Request |
| `onetrust_get_all_subtasks_v3_using_post` | `DSARTOOL` | Get List of Subtasks by Criteria |
| `onetrust_get_all_term_attribute_names` | `DATA_CATALOGTOOL` | Get List of Term Attributes |
| `onetrust_get_all_user_details_v2` | `ACCESS_MANAGEMENTTOOL` | Get List of Users |
| `onetrust_get_all_user_group_with_filters_v2` | `ACCESS_MANAGEMENTTOOL` | Get List of User Groups |
| `onetrust_get_all_users_using_get` | `USER_PROVISIONINGTOOL` | Get List of Users |
| `onetrust_get_all_using_get_1` | `DATA_DISCOVERYTOOL` | Get List of Data Sources |
| `onetrust_get_all_using_get_2` | `DATA_DISCOVERYTOOL` | Get List of Scan Profiles |
| `onetrust_get_all_v2_resolutions_using_get` | `DSARTOOL` | Get List of Resolutions |
| `onetrust_get_all_v2_verification_methods_by_id_using_get` | `DSARTOOL` | Get Verification Method |
| `onetrust_get_all_v2_verification_methods_using_get` | `DSARTOOL` | Get List of Verification Methods |
| `onetrust_get_app_script_details` | `COOKIE_CONSENTTOOL` | Get Script for Application |
| `onetrust_get_application_branding_attribute_list` | `COOKIE_CONSENTTOOL` | Get Branding Attributes for Application |
| `onetrust_get_applications` | `COOKIE_CONSENTTOOL` | Get List of Applications |
| `onetrust_get_assessment_delete_logs_using_get` | `ASSESSMENTSTOOL` | Export Deleted Assessment Audit Log |
| `onetrust_get_assessment_results_using_get` | `ASSESSMENTSTOOL` | Get List of Assessment Results |
| `onetrust_get_assessments_using_post` | `ASSESSMENTSTOOL` | Get List of Assessments by Criteria |
| `onetrust_get_attachment_download_commands_get` | `BULK_EXPORTTOOL` | Get Bulk Export Download Details |
| `onetrust_get_attributes_by_schema_name_using_get` | `ISSUES_MANAGEMENTTOOL` | Get Attribute Schema |
| `onetrust_get_audit_detail_using_get` | `AUDIT_MANAGEMENTTOOL` | Get Audit |
| `onetrust_get_audit_list_page_using_post` | `AUDIT_MANAGEMENTTOOL` | Get List of Audits |
| `onetrust_get_audit_workpaper_list_view_using_post` | `AUDIT_MANAGEMENTTOOL` | Get List of Workpapers |
| `onetrust_get_banner` | `CMPTOOL` | Get Banner Data |
| `onetrust_get_branding_attribute_list` | `COOKIE_CONSENTTOOL` | Get Branding Attributes for Domain |
| `onetrust_get_categorized_cookies` | `COOKIE_CONSENTTOOL` | Get Categorized Cookies |
| `onetrust_get_categorized_cookies_using_get` | `COOKIE_CONSENT_LEGACYTOOL` | Categorize Cookies by Domain |
| `onetrust_get_categorized_cookies_with_cookie_ids_using_get` | `COOKIE_CONSENT_LEGACYTOOL` | Categorize Cookies by Domain and Cookie ID |
| `onetrust_get_collection_points_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Collection Points |
| `onetrust_get_collection_points_using_get_1` | `UNIVERSAL_CONSENTTOOL` | Get List of Collection Points |
| `onetrust_get_consent_group_list_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Consent Groups |
| `onetrust_get_consent_group_settings_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Priority Scores for Purpose Statuses |
| `onetrust_get_consent_group_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Consent Group |
| `onetrust_get_contract_schema_using_get` | `TPRMTOOL` | Get Contract Schema |
| `onetrust_get_control_implementation_details_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get Control Implementation |
| `onetrust_get_cookie_reports_using_post` | `COOKIE_CONSENT_LEGACYTOOL` | Get List of Cookies by Criteria |
| `onetrust_get_cookies_by_filter` | `COOKIE_CONSENTTOOL` | Get List of Cookies by Criteria |
| `onetrust_get_credential_by_id` | `DATA_DISCOVERYTOOL` | Get Credential |
| `onetrust_get_credentials` | `DATA_DISCOVERYTOOL` | Get List of Credentials |
| `onetrust_get_credits_information_get` | `BULK_EXPORTTOOL` | Get Bulk Export Credit Details |
| `onetrust_get_data_asset_attribute_by_name` | `DATA_CATALOGTOOL` | Get Data Asset Attribute |
| `onetrust_get_data_asset_v1` | `DATA_CATALOGTOOL` | Get Data Asset |
| `onetrust_get_data_categories_by_partial_name_using_get` | `DATA_MAPPINGTOOL` | Get List of Data Categories |
| `onetrust_get_data_category_using_get` | `DATA_MAPPINGTOOL` | Get Data Category |
| `onetrust_get_data_classification_using_get` | `DATA_MAPPINGTOOL` | Get Data Classification |
| `onetrust_get_data_element_using_get` | `DATA_MAPPINGTOOL` | Get Data Element |
| `onetrust_get_data_source_by_id_using_get_1` | `DATA_DISCOVERYTOOL` | Get Data Source |
| `onetrust_get_data_subject_basic_details_v4` | `UNIVERSAL_CONSENTTOOL` | Get Data Subject |
| `onetrust_get_data_subject_details_v4` | `UNIVERSAL_CONSENTTOOL` | Get Data Subject Details |
| `onetrust_get_data_subject_groups_list_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subject Groups |
| `onetrust_get_data_subject_profile_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subjects |
| `onetrust_get_data_subject_profile_v4` | `UNIVERSAL_CONSENTTOOL` | Get Purpose Details by Data Subject |
| `onetrust_get_data_subject_profiles_unordered_v4` | `UNIVERSAL_CONSENTTOOL` | Get Optimized List of All Purpose Details for All Data Subjects |
| `onetrust_get_data_subject_profiles_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of All Purpose Details for All Data Subjects |
| `onetrust_get_data_subject_purposes_by_identifier_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Purposes for a Data Subject |
| `onetrust_get_data_subject_purposes_by_identifier_using_get_1` | `UNIVERSAL_CONSENTTOOL` | Get Data Subject's Preferences in a Preference Center |
| `onetrust_get_data_subject_using_get` | `DATA_MAPPINGTOOL` | Get Data Subject |
| `onetrust_get_data_subjects_by_partial_name_using_get` | `DATA_MAPPINGTOOL` | Get List of Data Subjects |
| `onetrust_get_data_subjects_for_purposes_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subjects by Purpose |
| `onetrust_get_data_subjects_unordered_v4` | `UNIVERSAL_CONSENTTOOL` | Get Optimized List of Data Subjects |
| `onetrust_get_data_subjects_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subjects |
| `onetrust_get_data_subjects_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subjects |
| `onetrust_get_deletion_certificate_using_get` | `DSARTOOL` | Get Deletion Certificate |
| `onetrust_get_detailed_scan_result_information` | `COOKIE_CONSENTTOOL` | Get Scan Results |
| `onetrust_get_detector_by_classifier_name` | `DATA_DISCOVERYTOOL` | Get Custom Classifier |
| `onetrust_get_docker_repository_tags_using_get` | `DATA_DISCOVERYTOOL` | Get List of Image tags |
| `onetrust_get_domain_scans` | `COOKIE_CONSENTTOOL` | Get List of Scans by Domain |
| `onetrust_get_domains_scanned_by_sort` | `COOKIE_CONSENTTOOL` | Get List of Websites |
| `onetrust_get_domains_scanned_by_sort_using_get` | `COOKIE_CONSENT_LEGACYTOOL` | Get List of Websites |
| `onetrust_get_eligible_jobs_using_get` | `DATA_DISCOVERY_WORKERTOOL` | Get List of Scan Jobs |
| `onetrust_get_email_link_token_by_data_subject_v4` | `UNIVERSAL_CONSENTTOOL` | Get Data Subject Token |
| `onetrust_get_email_link_tokens_list_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subject Tokens |
| `onetrust_get_engagement_schema_using_get` | `TPRMTOOL` | Get Engagement Schema |
| `onetrust_get_enrollment_details_using_post` | `TRAININGTOOL` | Get Enrollment Details |
| `onetrust_get_entity_information_using_entity_type_id_or_entity_type_name_using_get` | `AI_GOVERNANCETOOL` | Get Entity |
| `onetrust_get_entity_information_using_entity_type_id_or_entity_type_name_using_get_x` | `OBJECT_MANAGERTOOL` | Get Object |
| `onetrust_get_entity_type_information_using_get` | `OBJECT_MANAGERTOOL` | Get Object Type by ID |
| `onetrust_get_entity_type_information_using_get_1` | `AI_GOVERNANCETOOL` | Get Entity Type |
| `onetrust_get_entity_type_information_using_get_1_x` | `OBJECT_MANAGERTOOL` | Get Object Type by Name |
| `onetrust_get_export_run_details_get` | `BULK_EXPORTTOOL` | Get Bulk Export Status |
| `onetrust_get_export_runs_get` | `BULK_EXPORTTOOL` | Get List of Bulk Exports |
| `onetrust_get_geo_rule_group_details` | `COOKIE_CONSENTTOOL` | Get Geolocation Rule Group |
| `onetrust_get_geo_rule_groups` | `COOKIE_CONSENTTOOL` | Get List of Geolocation Rule Groups |
| `onetrust_get_group_by_id` | `USER_PROVISIONINGTOOL` | Get User Group |
| `onetrust_get_group_resource_using_get` | `USER_PROVISIONINGTOOL` | Get Group |
| `onetrust_get_grouped_purposes_v2` | `UNIVERSAL_CONSENTTOOL` | Get List of Purpose Versions |
| `onetrust_get_groups` | `USER_PROVISIONINGTOOL` | Get List of User Groups |
| `onetrust_get_hierarchy_for_inventory_id_using_get` | `DATA_MAPPINGTOOL` | Get List of Child Inventories by Root Inventory |
| `onetrust_get_incident_detail_by_incident_id_using_get` | `INCIDENTSTOOL` | Get Incident |
| `onetrust_get_index_creation_status` | `UNIVERSAL_CONSENTTOOL` | Get Index Creation Status |
| `onetrust_get_initiative_using_get` | `COMPLIANCE_AUTOMATIONTOOL` | Get Initiative |
| `onetrust_get_inventory_by_external_id_using_get` | `DATA_MAPPINGTOOL` | Get Inventory by External ID |
| `onetrust_get_inventory_by_id_using_get` | `DATA_MAPPINGTOOL` | Get Inventory by ID |
| `onetrust_get_inventory_relations_by_id_using_get` | `DATA_MAPPINGTOOL` | Get Inventory Links |
| `onetrust_get_inventory_relationship_using_relationship_type_name` | `INVENTORYTOOL` | Get Relationship by Type ID |
| `onetrust_get_inventory_relationship_using_relationship_type_name_1` | `INVENTORYTOOL` | Get Relationship by Type Name |
| `onetrust_get_inventory_v2_schemas_attributes_attribute_id_values_value_id` | `DATA_MAPPING_LEGACYTOOL` | Get Attribute Options |
| `onetrust_get_issue_links_using_get` | `ISSUES_MANAGEMENTTOOL` | Get Issue Relationships |
| `onetrust_get_issue_related_tasks_using_get` | `ISSUES_MANAGEMENTTOOL` | Get Issue Tasks |
| `onetrust_get_issue_using_get` | `ISSUES_MANAGEMENTTOOL` | Get Issue |
| `onetrust_get_job_by_id_using_get` | `DATA_DISCOVERYTOOL` | Get Scan Job |
| `onetrust_get_job_using_get_1` | `DATA_DISCOVERYTOOL` | Get Scan Job |
| `onetrust_get_latest_policies` | `POLICY_MANAGEMENTTOOL` | Get List of Documents |
| `onetrust_get_link_record_information_using_link_type_id_using_get` | `AI_GOVERNANCETOOL` | Get Relationship Record |
| `onetrust_get_link_record_information_using_link_type_id_using_get_x` | `OBJECT_MANAGERTOOL` | Get Relationship Record |
| `onetrust_get_link_tokens_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subject Tokens |
| `onetrust_get_link_type_using_get` | `OBJECT_MANAGERTOOL` | Get Relationship Type |
| `onetrust_get_linked_assessments_information_using_get` | `ASSESSMENTSTOOL` | Get List of Linked Assessments |
| `onetrust_get_linked_identity_group_members_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subject Group Members |
| `onetrust_get_linked_identity_group_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Data Subject Group |
| `onetrust_get_linked_identity_groups_by_data_subject_v4` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subject Group Associations by Data Subject |
| `onetrust_get_linked_identity_groups_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subject Groups |
| `onetrust_get_linked_risks_information_using_post` | `IT_RISK_MANAGEMENTTOOL` | Get List of Linked Risks |
| `onetrust_get_list_of_deletion_certificates` | `UNIVERSAL_CONSENTTOOL` | Get List of Deletion Certificates |
| `onetrust_get_list_of_inventories_by_filter_criteria_using_post` | `DATA_MAPPINGTOOL` | Get List of Inventories by Criteria |
| `onetrust_get_list_of_inventories_using_get` | `DATA_MAPPINGTOOL` | Get List of Inventories |
| `onetrust_get_list_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Purpose Preferences |
| `onetrust_get_matrix_score_setting_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get Risk Matrix Configuration |
| `onetrust_get_members_from_auser_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Get List of Users in User Group |
| `onetrust_get_merge_request_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Scheduled Export |
| `onetrust_get_model_using_get` | `OBJECT_MANAGERTOOL` | Get Model Object |
| `onetrust_get_oauth_token` | `ACCESS_MANAGEMENTTOOL` | Generate Access Token |
| `onetrust_get_paged_merge_request_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Scheduled Exports |
| `onetrust_get_paginated_attachment_download_commands_get` | `BULK_EXPORTTOOL` | Get List of Bulk Export Download Details |
| `onetrust_get_personal_data_for_relationships_using_post` | `INVENTORYTOOL` | Get Personal Data for Relationship by Type ID |
| `onetrust_get_personal_data_for_relationships_using_post_1` | `INVENTORYTOOL` | Get Personal Data for Relationship by Type Name |
| `onetrust_get_policy` | `POLICY_MANAGEMENTTOOL` | Get Document |
| `onetrust_get_preference_center_by_id_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Preference Center Schema |
| `onetrust_get_preference_center_page_schema_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Preference Center Page Schema |
| `onetrust_get_preference_centers_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Preference Centers |
| `onetrust_get_preferences` | `CMPTOOL` | Get Preference Center Data |
| `onetrust_get_preferences_using_get` | `CROSS_DEVICE_CONSENTTOOL` | Get Data Subject's Preferences |
| `onetrust_get_privacy_notice_version_by_published_date_using_get` | `PRIVACY_NOTICESTOOL` | Get Privacy Notice Version |
| `onetrust_get_privacy_notice_versions_using_get` | `PRIVACY_NOTICESTOOL` | Get List of Privacy Notice Versions |
| `onetrust_get_privacy_notices_using_get` | `PRIVACY_NOTICESTOOL` | Get List of Privacy Notices |
| `onetrust_get_project_using_get` | `OBJECT_MANAGERTOOL` | Get Project Object |
| `onetrust_get_published_policy_version` | `POLICY_MANAGEMENTTOOL` | Get Document Version |
| `onetrust_get_purpose_detail_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Purpose |
| `onetrust_get_purposes_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Purposes |
| `onetrust_get_realtime_preferences` | `CONSENT_INTERFACESTOOL` | Get Data Subject's Preferences |
| `onetrust_get_receipt_list_details_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Receipt Details by Data Subject |
| `onetrust_get_receipt_list_details_using_post` | `UNIVERSAL_CONSENTTOOL` | Get List of Receipts |
| `onetrust_get_receipt_list_using_get` | `UNIVERSAL_CONSENTTOOL` | Get List of Receipts by Data Subject |
| `onetrust_get_related_entities_for_an_entity_using_post` | `AI_GOVERNANCETOOL` | Get List of Relationship Records by Entity |
| `onetrust_get_request_by_id_using_get` | `DSARTOOL` | Get Request |
| `onetrust_get_request_creation_logs_using_get` | `DSARTOOL` | Get Request Creation Logs |
| `onetrust_get_request_history` | `DSARTOOL` | Get Request Audit History |
| `onetrust_get_request_history_by_id_using_get` | `DSARTOOL` | Get Request Audit History |
| `onetrust_get_resource_types_by_name_using_get` | `USER_PROVISIONINGTOOL` | Get Supported Resource Types |
| `onetrust_get_resource_types_using_get` | `USER_PROVISIONINGTOOL` | Get Supported Resources |
| `onetrust_get_risk_page_view_using_post` | `IT_RISK_MANAGEMENTTOOL` | Get List of Risks |
| `onetrust_get_risk_template_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get Risk Template |
| `onetrust_get_risk_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get Risk |
| `onetrust_get_root_schema_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Preference Center Root Schema |
| `onetrust_get_scan_delta_details` | `COOKIE_CONSENTTOOL` | Get List of Added or Removed Cookies |
| `onetrust_get_scan_jobs_by_data_source_using_get_1` | `DATA_DISCOVERYTOOL` | Get List of Scan Jobs |
| `onetrust_get_scan_profile_using_get_1` | `DATA_DISCOVERYTOOL` | Get Scan Profile |
| `onetrust_get_scan_result_summary` | `COOKIE_CONSENTTOOL` | Get Scan Result Summary |
| `onetrust_get_schema_details_using_field_name` | `DATA_MAPPINGTOOL` | Get Inventory Schema Details |
| `onetrust_get_schema_using_get_1` | `DATA_MAPPING_LEGACYTOOL` | Get Inventory Schema |
| `onetrust_get_schemas_by_name_using_get` | `USER_PROVISIONINGTOOL` | Get SCIM Schema |
| `onetrust_get_schemas_using_get` | `USER_PROVISIONINGTOOL` | Get List of Supported SCIM Schemas |
| `onetrust_get_script_details` | `COOKIE_CONSENTTOOL` | Get Script for Domain |
| `onetrust_get_script_for_website` | `COOKIE_CONSENTTOOL` | Get Script for Website |
| `onetrust_get_script_for_website_using_get` | `COOKIE_CONSENT_LEGACYTOOL` | Get Script for Website |
| `onetrust_get_service_provider_config_using_get` | `USER_PROVISIONINGTOOL` | Get Service Provider Configuration |
| `onetrust_get_standard_score_setting_using_get` | `IT_RISK_MANAGEMENTTOOL` | Get Standard Risk Configuration |
| `onetrust_get_status_of_enrollment_using_get` | `TRAININGTOOL` | Get User's Enrollment Status |
| `onetrust_get_subtask_by_idusing_get` | `DSARTOOL` | Get Subtask |
| `onetrust_get_tag_details_with_associated_terms` | `DATA_CATALOGTOOL` | Get Tag |
| `onetrust_get_tags_using_get` | `ASSESSMENTSTOOL` | Get List of Assessment Tags |
| `onetrust_get_task_by_id_and_task_type_name_key_using_get` | `TASK_MANAGEMENTTOOL` | Get Task |
| `onetrust_get_template_details` | `COOKIE_CONSENTTOOL` | Get Template Details |
| `onetrust_get_templates` | `COOKIE_CONSENTTOOL` | Get List of Templates |
| `onetrust_get_term_attribute_by_name` | `DATA_CATALOGTOOL` | Get Term Attribute |
| `onetrust_get_token_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Collection Point Token |
| `onetrust_get_transactions_using_post` | `UNIVERSAL_CONSENTTOOL` | Get List of Transactions |
| `onetrust_get_ucpurposes` | `CMPTOOL` | Get Universal Consent Purposes |
| `onetrust_get_user_access_levels_v2` | `ACCESS_MANAGEMENTTOOL` | Get User Roles |
| `onetrust_get_user_by_id` | `USER_PROVISIONINGTOOL` | Get User |
| `onetrust_get_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Get User Group |
| `onetrust_get_user_using_get` | `USER_PROVISIONINGTOOL` | Get User |
| `onetrust_get_user_v2` | `ACCESS_MANAGEMENTTOOL` | Get User |
| `onetrust_get_users` | `USER_PROVISIONINGTOOL` | Get List of Users |
| `onetrust_get_v1_field_details` | `DATA_CATALOGTOOL` | Get Search Fields |
| `onetrust_get_v3_datasubject_profiles_using_post` | `UNIVERSAL_CONSENTTOOL` | Get List of Data Subjects |
| `onetrust_get_v3_datasubjects_profile_using_get` | `UNIVERSAL_CONSENTTOOL` | Get Data Subject |
| `onetrust_get_vendors` | `CMPTOOL` | Get IAB and Google Vendors |
| `onetrust_get_workflow_details_for_assessment_using_get` | `ASSESSMENTSTOOL` | Get Assessment Workflow Stages |
| `onetrust_get_workpaper_basic_detail_information_using_get` | `AUDIT_MANAGEMENTTOOL` | Get Workpaper Control Details |
| `onetrust_get_workpaper_result_using_get` | `AUDIT_MANAGEMENTTOOL` | Get Workpaper Results |
| `onetrust_grant_risk_exception_using_put` | `IT_RISK_MANAGEMENTTOOL` | Grant Risk Exception |
| `onetrust_import_template_by_id_using_post` | `ASSESSMENTSTOOL` | Import Template |
| `onetrust_import_workflow_using_post_1` | `INTEGRATIONSTOOL` | Import Workflow |
| `onetrust_link_asset_inventory_to_parent_asset_id_using_post` | `DATA_MAPPINGTOOL` | Add Asset Inventory as Child to Parent Inventory |
| `onetrust_link_legal_entity_inventory_to_parent_legal_entity_id_using_post` | `DATA_MAPPINGTOOL` | Add Legal Entity Inventory as Child to Parent Inventory |
| `onetrust_link_or_unlink_inventory_relationships_using_relationship_using_put` | `INVENTORYTOOL` | Link or Unlink Personal Data to Relationship by Type ID |
| `onetrust_link_or_unlink_inventory_relationships_using_relationship_using_put_1` | `INVENTORYTOOL` | Link or Unlink Personal Data to Relationship by Type Name |
| `onetrust_link_processing_activity_inventory_to_parent_processing_activity_id_using_post` | `DATA_MAPPINGTOOL` | Add Processing Activity Inventory as Child to Parent Inventory |
| `onetrust_link_requests_using_put` | `DSARTOOL` | Link Requests |
| `onetrust_link_vendor_inventory_to_parent_vendor_id_using_post` | `DATA_MAPPINGTOOL` | Add Vendor Inventory as Child to Parent Inventory |
| `onetrust_list_all_data_classifications_using_get` | `DATA_MAPPING_LEGACYTOOL` | Get List of Data Classifications |
| `onetrust_list_all_data_elements_using_get` | `DATA_MAPPING_LEGACYTOOL` | Get List of Data Elements |
| `onetrust_list_all_inventory_relationships_using_post` | `INVENTORYTOOL` | Get List of Relationships |
| `onetrust_list_detectors` | `DATA_DISCOVERYTOOL` | Get List of Custom Classifiers |
| `onetrust_list_groups_using_get` | `USER_PROVISIONINGTOOL` | Get List of Groups |
| `onetrust_list_of_courses_using_get` | `TRAININGTOOL` | Get List of Courses |
| `onetrust_load_engagement_by_engagement_id_using_get` | `TPRMTOOL` | Get Engagement |
| `onetrust_load_engagement_using_get` | `TPRMTOOL` | Search Engagements |
| `onetrust_load_vendor_contract_by_contract_id_using_get` | `TPRMTOOL` | Get Contract |
| `onetrust_login_history` | `ACCESS_MANAGEMENTTOOL` | Get Audit Records for Login History |
| `onetrust_merge_data_subjects_using_post` | `UNIVERSAL_CONSENTTOOL` | Deduplicate Data Subjects |
| `onetrust_merge_datasubject_using_post` | `UNIVERSAL_CONSENTTOOL` | Deduplicate Data Subjects |
| `onetrust_modify_group` | `USER_PROVISIONINGTOOL` | Modify User Group |
| `onetrust_modify_user` | `USER_PROVISIONINGTOOL` | Modify User |
| `onetrust_move_status_by_request_ref_id_using_put` | `DSARTOOL` | Update Request Stage |
| `onetrust_organization_tree_structure_using_get` | `ACCESS_MANAGEMENTTOOL` | Get List of Organizations |
| `onetrust_patch_user_using_patch` | `USER_PROVISIONINGTOOL` | Modify User |
| `onetrust_pause_or_resume_deadline_using_put` | `DSARTOOL` | Pause Request Deadline |
| `onetrust_perform_risk_action_using_put` | `IT_RISK_MANAGEMENTTOOL` | Perform Risk Action |
| `onetrust_post_log_consent` | `CMPTOOL` | Log Consent |
| `onetrust_publish_app_script` | `COOKIE_CONSENTTOOL` | Publish Application SDK |
| `onetrust_publish_purpose_using_put` | `UNIVERSAL_CONSENTTOOL` | Publish Purpose |
| `onetrust_publish_script_to_site` | `COOKIE_CONSENTTOOL` | Publish Script to Website |
| `onetrust_publish_to_site_using_put` | `COOKIE_CONSENT_LEGACYTOOL` | Publish Script to Website |
| `onetrust_reassess_assessment_using_post` | `ASSESSMENTSTOOL` | Reassess Assessment |
| `onetrust_reassign_assessment_using_put` | `ASSESSMENTSTOOL` | Reassign Assessment |
| `onetrust_recategorize_cookies_by_scan` | `COOKIE_CONSENTTOOL` | Recategorize Cookies |
| `onetrust_remove_access_level_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Remove User Group Roles |
| `onetrust_remove_all_consent_attachment_refs` | `UNIVERSAL_CONSENTTOOL` | Remove All Consent Attachments |
| `onetrust_remove_amember_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Remove User from User Group |
| `onetrust_remove_control_implementation_by_entity_and_implementation_id_using_delete` | `IT_RISK_MANAGEMENTTOOL` | Delete Control Implementation |
| `onetrust_remove_control_using_delete_1` | `IT_RISK_MANAGEMENTTOOL` | Delete Control |
| `onetrust_remove_engagement_using_delete` | `TPRMTOOL` | Delete Engagement |
| `onetrust_remove_given_consent_attachment_refs` | `UNIVERSAL_CONSENTTOOL` | Remove Consent Attachment |
| `onetrust_remove_members_using_delete` | `ACCESS_MANAGEMENTTOOL` | Remove Members from User Group |
| `onetrust_remove_multiple_members_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Remove Multiple Users from User Group |
| `onetrust_remove_threat_using_delete` | `IT_RISK_MANAGEMENTTOOL` | Delete Threat |
| `onetrust_remove_user_access_level_v2` | `ACCESS_MANAGEMENTTOOL` | Remove User Role |
| `onetrust_remove_vendor_contract_using_delete` | `TPRMTOOL` | Delete Contract |
| `onetrust_remove_vulnerability_using_delete` | `IT_RISK_MANAGEMENTTOOL` | Delete Vulnerability |
| `onetrust_reopen_assessment_using_post` | `ASSESSMENTSTOOL` | Reopen Assessment |
| `onetrust_reopen_risk_using_put` | `IT_RISK_MANAGEMENTTOOL` | Reopen Risk |
| `onetrust_reprocess_subtask_using_put` | `DSARTOOL` | Reprocess System Subtask |
| `onetrust_request_bulk_add_domain_using_post` | `COOKIE_CONSENT_LEGACYTOOL` | Add Websites to Scan |
| `onetrust_request_risk_exception_using_put` | `IT_RISK_MANAGEMENTTOOL` | Request Risk Exception |
| `onetrust_retrieve_all_tags_name` | `DATA_CATALOGTOOL` | Get List of Tags |
| `onetrust_retrieve_all_terms` | `DATA_CATALOGTOOL` | Get List of Terms |
| `onetrust_retrieve_members_using_get` | `ACCESS_MANAGEMENTTOOL` | Get User Group Members |
| `onetrust_retrieve_terms_by_name` | `DATA_CATALOGTOOL` | Get Term |
| `onetrust_retrieve_terms_name` | `DATA_CATALOGTOOL` | Get List of Term Names |
| `onetrust_retrieve_user_groups_using_get` | `ACCESS_MANAGEMENTTOOL` | Get List of User Groups |
| `onetrust_review_assessment_using_post` | `ASSESSMENTSTOOL` | Complete Assessment |
| `onetrust_scan_application` | `COOKIE_CONSENTTOOL` | Scan Application |
| `onetrust_schedule_merge_request_using_post` | `UNIVERSAL_CONSENTTOOL` | Create Scheduled Export of Duplicate Data Subjects |
| `onetrust_schedule_scans` | `COOKIE_CONSENTTOOL` | Schedule Website Scans |
| `onetrust_search_contract_by_vendor_and_criteria_using_post` | `TPRMTOOL` | Search Contracts |
| `onetrust_search_data_subjects_by_element_v4` | `UNIVERSAL_CONSENTTOOL` | Search Data Subjects by Data Element |
| `onetrust_search_data_subjects_post_using_post` | `UNIVERSAL_CONSENTTOOL` | Search Data Subjects |
| `onetrust_search_for_request_using_post` | `DSARTOOL` | Search Requests |
| `onetrust_search_incidents_using_post` | `INCIDENTSTOOL` | Search Incidents |
| `onetrust_send_back_assessment_to_in_progress_using_post` | `ASSESSMENTSTOOL` | Send Back Assessment |
| `onetrust_send_back_risk_using_put` | `IT_RISK_MANAGEMENTTOOL` | Send Back Risk |
| `onetrust_set_inventory_as_parent_inventory_using_put` | `DATA_MAPPINGTOOL` | Set Inventory as Parent |
| `onetrust_set_retirement_using_put` | `UNIVERSAL_CONSENTTOOL` | Retire Purpose |
| `onetrust_set_user_default_organization_v2` | `ACCESS_MANAGEMENTTOOL` | Modify User Default Organization |
| `onetrust_share_results_summary_using_post` | `DSARTOOL` | Share Results Summary |
| `onetrust_soft_delete_assessment_using_put` | `ASSESSMENTSTOOL` | Move Assessment to Recycle Bin |
| `onetrust_start_export_run_post` | `BULK_EXPORTTOOL` | Create Bulk Export |
| `onetrust_submit_assessment_using_post` | `ASSESSMENTSTOOL` | Submit Assessment |
| `onetrust_submit_responses_using_post` | `ASSESSMENTSTOOL` | Submit Responses |
| `onetrust_submit_risk_using_put` | `IT_RISK_MANAGEMENTTOOL` | Submit Risk |
| `onetrust_subtasks_using_get` | `DSARTOOL` | Get List of Subtasks |
| `onetrust_un_enroll_user_using_delete` | `TRAININGTOOL` | Unenroll User from Course |
| `onetrust_unarchive_assessments_using_put` | `ASSESSMENTSTOOL` | Unarchive Assessment |
| `onetrust_unlink_child_inventory_from_hierarchy_using_delete` | `DATA_MAPPINGTOOL` | Remove Child Inventory from Root Inventory |
| `onetrust_unlink_consent_group_using_delete` | `UNIVERSAL_CONSENTTOOL` | Remove Consent Groups from Parent Consent Group |
| `onetrust_unlink_risks_from_entity_using_post` | `IT_RISK_MANAGEMENTTOOL` | Unlink Risks |
| `onetrust_unset_inventory_as_parent_inventory_using_put` | `DATA_MAPPINGTOOL` | Unset Inventory as Parent |
| `onetrust_unstructured_data_discovery_updates_using_post` | `DSARTOOL` | Add Data Points to Targeted Data Discovery Results Summary |
| `onetrust_update_access_level_for_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Update User Group Roles |
| `onetrust_update_advanced_attributes_for_personal_data_association_using_put` | `DATA_MAPPINGTOOL` | Update Advanced Attributes for Personal Data Association |
| `onetrust_update_application_branding_attributes_for_public_api` | `COOKIE_CONSENTTOOL` | Update Branding Attributes for Application |
| `onetrust_update_basic_assessment_details_using_patch` | `ASSESSMENTSTOOL` | Modify Assessment |
| `onetrust_update_branding_attributes_for_public_api` | `COOKIE_CONSENTTOOL` | Update Branding Attributes for Domain |
| `onetrust_update_consent_group_settings_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Priority Scores for Purpose Statuses |
| `onetrust_update_control_implementation_by_implementation_id_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Control Implementation |
| `onetrust_update_control_using_put_1` | `IT_RISK_MANAGEMENTTOOL` | Update Control |
| `onetrust_update_cookie` | `COOKIE_CONSENT_LEGACYTOOL` | Update Cookie |
| `onetrust_update_credential` | `DATA_DISCOVERYTOOL` | Update Credential |
| `onetrust_update_custom_entity_type_using_patch` | `OBJECT_MANAGERTOOL` | Modify Custom Object Type by ID |
| `onetrust_update_custom_entity_type_using_patch_1` | `OBJECT_MANAGERTOOL` | Modify Custom Object Type by Name |
| `onetrust_update_custom_fields_using_put` | `DSARTOOL` | Update Request Custom Fields |
| `onetrust_update_data_asset_v1` | `DATA_CATALOGTOOL` | Modify Data Asset |
| `onetrust_update_data_subject_group_v4` | `UNIVERSAL_CONSENTTOOL` | Update Data Subject Group |
| `onetrust_update_detector` | `DATA_DISCOVERYTOOL` | Update Custom Classifier |
| `onetrust_update_engagement_status` | `TPRMTOOL` | Update Engagement Status |
| `onetrust_update_engagement_using_patch` | `TPRMTOOL` | Modify Engagement |
| `onetrust_update_engagement_using_put` | `TPRMTOOL` | Update Engagement |
| `onetrust_update_group` | `USER_PROVISIONINGTOOL` | Update User Group |
| `onetrust_update_group_members_using_patch` | `USER_PROVISIONINGTOOL` | Modify Group |
| `onetrust_update_group_members_using_put` | `USER_PROVISIONINGTOOL` | Update Group |
| `onetrust_update_incident_using_put` | `INCIDENTSTOOL` | Update Incident |
| `onetrust_update_initiative_using_put` | `COMPLIANCE_AUTOMATIONTOOL` | Update Initiative |
| `onetrust_update_inventory_association_using_put` | `DATA_MAPPINGTOOL` | Update Inventory Link |
| `onetrust_update_inventory_relations_using_entity_type_name` | `INVENTORYTOOL` | Update Relationship by Type ID |
| `onetrust_update_inventory_relations_using_entity_type_name_1` | `INVENTORYTOOL` | Update Relationship by Type Name |
| `onetrust_update_inventory_status_by_id_using_put` | `DATA_MAPPINGTOOL` | Update Inventory Status |
| `onetrust_update_inventory_using_put` | `DATA_MAPPINGTOOL` | Update Inventory by ID |
| `onetrust_update_issue_using_patch` | `ISSUES_MANAGEMENTTOOL` | Modify Issue |
| `onetrust_update_issue_using_put` | `ISSUES_MANAGEMENTTOOL` | Update Issue |
| `onetrust_update_job_status_using_put` | `DATA_DISCOVERY_WORKERTOOL` | Update Scan Job Status |
| `onetrust_update_linked_identity_group_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Data Subject Group |
| `onetrust_update_model_using_put` | `OBJECT_MANAGERTOOL` | Modify Model Object |
| `onetrust_update_organization_using_put` | `ACCESS_MANAGEMENTTOOL` | Update Organization |
| `onetrust_update_preferences_for_data_subject_api_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Data Subject's Preferences in a Preference Center |
| `onetrust_update_primary_record_using_put` | `ASSESSMENTSTOOL` | Set Primary Record |
| `onetrust_update_project_using_put` | `OBJECT_MANAGERTOOL` | Modify Project Object |
| `onetrust_update_purpose_rules_to_consent_group_using_put` | `UNIVERSAL_CONSENTTOOL` | Update Consent Group Purpose Rule |
| `onetrust_update_relations_using_put` | `DATA_MAPPINGTOOL` | Link Inventory |
| `onetrust_update_resolution_using_put` | `DSARTOOL` | Update Resolution |
| `onetrust_update_risk_approvers_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Risk Approvers |
| `onetrust_update_risk_categories_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Risk Categories |
| `onetrust_update_risk_owners_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Risk Owners |
| `onetrust_update_risk_using_patch` | `IT_RISK_MANAGEMENTTOOL` | Modify Risk |
| `onetrust_update_risk_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Risk |
| `onetrust_update_sub_task_using_put` | `DSARTOOL` | Update Subtask |
| `onetrust_update_subtask_status_using_put` | `DSARTOOL` | Update Subtask Status |
| `onetrust_update_task_using_put` | `TASK_MANAGEMENTTOOL` | Update Task |
| `onetrust_update_task_using_put_1` | `AI_GOVERNANCETOOL` | Update Task |
| `onetrust_update_task_using_put_1_x` | `OBJECT_MANAGERTOOL` | Update Task |
| `onetrust_update_threats_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Threats |
| `onetrust_update_user` | `USER_PROVISIONINGTOOL` | Update User |
| `onetrust_update_user_group_by_id_v2` | `ACCESS_MANAGEMENTTOOL` | Update User Group |
| `onetrust_update_user_group_using_put` | `ACCESS_MANAGEMENTTOOL` | Update User Group |
| `onetrust_update_user_using_put` | `USER_PROVISIONINGTOOL` | Update User |
| `onetrust_update_user_v2` | `ACCESS_MANAGEMENTTOOL` | Update User |
| `onetrust_update_using_entity_type_id_or_entity_type_name_using_patch` | `AI_GOVERNANCETOOL` | Modify Entity |
| `onetrust_update_using_entity_type_id_or_entity_type_name_using_patch_x` | `OBJECT_MANAGERTOOL` | Modify Object |
| `onetrust_update_v2_using_put` | `DATA_DISCOVERYTOOL` | Update Scan Profile |
| `onetrust_update_v2_using_put_x` | `INTEGRATIONSTOOL` | Update System Credential |
| `onetrust_update_v2_verification_method_using_put` | `DSARTOOL` | Update Verification Method |
| `onetrust_update_vendor_contract_using_put` | `TPRMTOOL` | Update Contract |
| `onetrust_update_vulnerabilities_using_put` | `IT_RISK_MANAGEMENTTOOL` | Update Vulnerabilities |
| `onetrust_upload_consent_attachments` | `UNIVERSAL_CONSENTTOOL` | Upload Consent Attachment |
| `onetrust_upsert_inventory_using_put` | `DATA_MAPPINGTOOL` | Update Inventory by External ID |
| `onetrust_upsert_source_system_v3_using_put` | `DATA_DISCOVERYTOOL` | Create or Update Data Source |
| `onetrust_user_activity` | `ACCESS_MANAGEMENTTOOL` | Get Audit Records for User's Profile |
| `onetrust_validate_and_create_audit_using_post` | `AUDIT_MANAGEMENTTOOL` | Create Audit |
| `onetrust_validate_and_reassign_scopes_using_put` | `AUDIT_MANAGEMENTTOOL` | Update Audit Scope |
| `onetrust_validate_and_update_audit_using_put` | `AUDIT_MANAGEMENTTOOL` | Update Audit |
| `onetrust_withdraw_preferences_api_using_delete` | `UNIVERSAL_CONSENTTOOL` | Withdraw Data Subject's Consent for All Purposes in a Preference Center |
| `onetrust_withdraw_transaction_behalf_of_datasubject_using_put` | `UNIVERSAL_CONSENTTOOL` | Withdraw Consent on Behalf of a Data Subject |
| `onetrust_withdraw_transaction_by_purpose_and_identifier_using_get` | `UNIVERSAL_CONSENTTOOL` | Withdraw Data Subject's Consent |

</details>

_36 action-routed tool(s) (default) · 597 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

### MCP Configuration Examples

> **Install the slim `[mcp]` extra.** All examples below install
> `onetrust-api[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)

```json
{
  "mcpServers": {
    "onetrust": {
      "command": "uvx",
      "args": [
        "--from",
        "onetrust-api[mcp]",
        "onetrust-mcp"
      ],
      "env": {
        "ONETRUST_URL": "https://acme.my.onetrust.com",
        "ONETRUST_TOKEN": "your_token"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)

```json
{
  "mcpServers": {
    "onetrust": {
      "command": "uvx",
      "args": [
        "--from",
        "onetrust-api[mcp]",
        "onetrust-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "ONETRUST_URL": "https://acme.my.onetrust.com",
        "ONETRUST_TOKEN": "your_token"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "onetrust": {
      "url": "http://localhost:8000/onetrust-api/mcp"
    }
  }
}
```

## A2A Agent

### Run A2A Server
```bash
export ONETRUST_URL="https://acme.my.onetrust.com"
export ONETRUST_TOKEN="your_token"
onetrust-agent --provider openai --model-id gpt-4o --api-key sk-...
```

## Docker

### Build

```bash
docker build -t onetrust-api .
```

### Run MCP Server

```bash
docker run -d \
  --name onetrust-api-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e ONETRUST_URL="https://acme.my.onetrust.com" \
  -e ONETRUST_TOKEN="your_token" \
  knucklessg1/onetrust-api:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `onetrust-api[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `onetrust-api[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `onetrust-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

### Deploy with Docker Compose

```yaml
services:
  onetrust-api-mcp:
    image: knucklessg1/onetrust-api:mcp
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
      - ONETRUST_URL=https://acme.my.onetrust.com
      - ONETRUST_TOKEN=your_token
    ports:
      - 8000:8000
```

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `onetrust-api[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `onetrust-api[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `onetrust-api[all]` | Everything (`mcp` + `agent`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "onetrust-api[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "onetrust-api[agent]"

# Everything (development)
uv pip install "onetrust-api[all]"      # or: python -m pip install "onetrust-api[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/onetrust-api:mcp` | `--target mcp` | `onetrust-api[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `onetrust-mcp` |
| `knucklessg1/onetrust-api:latest` | `--target agent` (default) | `onetrust-api[agent]` — **full** agent runtime + epistemic-graph engine | `onetrust-agent` |

```bash
docker build --target mcp   -t knucklessg1/onetrust-api:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/onetrust-api:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

## Environment Variables

Every variable the server reads. See [`.env.example`](.env.example) for a copy-paste
starting point.

### Connection & credentials (OneTrust)
| Variable | Description | Default |
|----------|-------------|---------|
| `ONETRUST_URL` | Tenant host URL, e.g. `https://acme.my.onetrust.com` (overrides `ONETRUST_REGION`) | — |
| `ONETRUST_REGION` | Shared regional pod when no URL is set: `us`, `eu`, `de`, `uk`, `au`, `ca`, `fr`, `in`, `jp`, `trial`, `uat`, … | `us` |
| `ONETRUST_TOKEN` | Pre-minted OAuth2 bearer token | — |
| `ONETRUST_CLIENT_ID` | OAuth2 client-credentials client id (exchanged at `/api/access/v1/oauth/token`) | — |
| `ONETRUST_CLIENT_SECRET` | OAuth2 client-credentials client secret | — |
| `ONETRUST_CONSENT_URL` | Optional host for consent-transaction APIs (privacy portal) | — |
| `ONETRUST_WORKER_URL` | Optional on-prem Data Discovery worker-node host | — |
| `ONETRUST_SSL_VERIFY` | Verify TLS for OneTrust requests | `True` |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `AUTH_TYPE` | MCP transport auth mode (`none`, …) | `none` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |
| `FASTMCP_LOG_LEVEL` | FastMCP log level (e.g. `INFO`, `DEBUG`) | `INFO` |
| `DEBUG` | Verbose logging | `False` |
| `PYTHONUNBUFFERED` | Unbuffered stdout (recommended in containers) | `1` |

### Tool toggles
Each action-routed domain tool can be disabled individually via its `<DOMAIN>TOOL` toggle env
var (set to `false`). The full list is in the [Available MCP Tools](#available-mcp-tools) table
above (e.g. `INCIDENTSTOOL`, `DSARTOOL`, `CONSENT_RECEIPTSTOOL`, `ESGTOOL`).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/onetrust-api/) and is
the source of truth for installation, usage, and deployment.

| Page | Covers |
| --- | --- |
| [Overview](https://knuckles-team.github.io/onetrust-api/overview/) | the action-routed tool surface and architecture |
| [Installation](https://knuckles-team.github.io/onetrust-api/installation/) | pip, source, extras, prebuilt Docker image |
| [Usage (API / CLI / MCP)](https://knuckles-team.github.io/onetrust-api/usage/) | the MCP tools, the `Api` client, the CLI |
| [Deployment](https://knuckles-team.github.io/onetrust-api/deployment/) | run the MCP and agent servers, Compose, env config |

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `onetrust-api` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx onetrust-mcp` · or `uv tool install onetrust-api` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/onetrust-api:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
