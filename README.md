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

*Version: 1.3.2*

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
  (RFC 8693) via `agent-connector-sdk`.
- **Multi-region / multi-service aware** — regional tenant pods, the consent
  privacy-portal host, and on-prem worker nodes are resolved per-operation.
- **Resilient** — honours `429` `Retry-After`, retries transient `5xx`, and
  handles both OneTrust pagination styles (offset and cursor).

## MCP

### Using as an MCP Server

The MCP Server runs in `stdio` (local) or `streamable-http` (networked) mode.
Each domain is a tool gated by a `{TAG}TOOL` environment variable (default `True`),
so the operator can scope the surface (e.g. set `ESGTOOL=False` to drop ESG).

#### Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `ONETRUST_URL` | — | ─── OneTrust connection ─────────────────────────────────────────────── Tenant host URL (overrides ONETRUST_REGION). e.g. https://acme.my.onetrust.com |
| `ONETRUST_REGION` | `us` | Or pick a shared regional pod: us, eu, de, uk, au, ca, fr, in, jp, trial, uat ... |
| `ONETRUST_TOKEN` | secret-injected | ─── Authentication (use ONE of the two) ─────────────────────────────── 1) Pre-minted OAuth2 bearer token (Global Settings > Access Management > Credentials) |
| `ONETRUST_CLIENT_ID` | — | 2) OAuth2 client-credentials (exchanged at /api/access/v1/oauth/token) |
| `ONETRUST_CLIENT_SECRET` | secret-injected |  |
| `ONETRUST_CONSENT_URL` | — | ─── Optional service hosts ──────────────────────────────────────────── Consent transaction / privacy-portal host (consent_receipts, universal_consent ...) |
| `ONETRUST_WORKER_URL` | — | On-prem Data Discovery worker-node host |
| `TLS_PROFILE` | `private-pki` | ─── HTTP behaviour ──────────────────────────────────────────────────── TLS verification is mandatory. Select a named runtime profile from AgentConfig. |
| `TLS_PROFILES_REF` | `secret://runtime/tls-profiles` |  |
| `FASTMCP_LOG_LEVEL` | `INFO` | ─── MCP transport / auth (agent-connector-sdk) ──────────────────────────── |
| `TRANSPORT` | `stdio` |  |
| `AUTH_TYPE` | `none` |  |
| `ACCESS_MANAGEMENTTOOL` | `True` | ─── Tool Toggle Switches (per-domain <DOMAIN>TOOL; set False to disable) ─ These names match the authoritative "Toggle Env Var" column in the README MCP tools table (condensed action-routed surface). |
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
| `ONETRUST_API_MCP_IMAGE` | — | ─── Deployment images ──────────────────────────────────────────────── Supply operator-approved immutable image@sha256 references for deployment. |
| `ONETRUST_API_AGENT_IMAGE` | — |  |
| `ONETRUST_TLS_PROFILE` | — | ─── Service-specific TLS selection ──────────────────────────────────── Optional named profile and runtime profile reference; verification stays mandatory. |
| `ONETRUST_TLS_PROFILE_REF` | — |  |
| `INGESTTOOL` | — | The drift scanner derives this name from register_ingest_tools, but this connector registers ingest tools directly and does not read this toggle. This is documentation of that limitation, not a working disable switch. |

#### Inherited agent-connector-sdk variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Loopback bind host (set an authenticated ingress explicitly) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `EUNOMIA_TYPE` | `none` | Authorization mode: `none` \| `embedded` \| `remote` |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` | Embedded Eunomia policy file |
| `EUNOMIA_REMOTE_URL` | — | Remote Eunomia authorization server URL |
| `ENABLE_OTEL` | `False` | Enable OpenTelemetry export |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | OTLP collector endpoint |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |

_53 package + 22 inherited variable(s). Auto-generated from `.env.example` + the shared agent-connector-sdk set — do not edit._
<!-- ENV-VARS-TABLE:END -->


| Variable | Description |
| --- | --- |
| `ONETRUST_URL` | Tenant host URL, e.g. `https://acme.my.onetrust.com` (overrides region). |
| `ONETRUST_REGION` | Shared pod when no URL is set: `us`, `eu`, `de`, `uk`, `au`, `ca`, `fr`, `in`, `jp`, `trial`, `uat`, … (default `us`). |
| `ONETRUST_TOKEN` | Pre-minted OAuth2 bearer token. |
| `ONETRUST_CLIENT_ID` / `ONETRUST_CLIENT_SECRET` | OAuth2 client-credentials (exchanged at `/api/access/v1/oauth/token`). |
| `ONETRUST_CONSENT_URL` | Optional host for consent-transaction APIs (privacy portal). |
| `ONETRUST_WORKER_URL` | Optional on-prem Data Discovery worker-node host. |
| `TLS_PROFILE` | Named `AgentConfig` transport-security profile; verification is mandatory. |
| `TLS_PROFILES_REF` | Runtime secret reference for the TLS profile catalog. |
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

<!-- This table is auto-generated by `python -m agent_connector_sdk.mcp.readme_tools` — do not edit by hand. -->

<!-- MCP-TOOLS-TABLE:START -->

#### Intent tools

| MCP Tool | Kind | Description |
|----------|------|-------------|
| `onetrust_access_management` | intent | Manage OneTrust access management operations. |
| `onetrust_ai_governance` | intent | Manage OneTrust ai governance operations. |
| `onetrust_api_request` | intent | Execute an arbitrary OneTrust REST API request directly. |
| `onetrust_assessments` | intent | Manage OneTrust assessments operations. |
| `onetrust_audit_management` | intent | Manage OneTrust audit management operations. |
| `onetrust_bulk_export` | intent | Manage OneTrust bulk export operations. |
| `onetrust_cmp` | intent | Manage OneTrust cmp operations. |
| `onetrust_compliance_automation` | intent | Manage OneTrust compliance automation operations. |
| `onetrust_consent_interfaces` | intent | Manage OneTrust consent interfaces operations. |
| `onetrust_consent_receipts` | intent | Manage OneTrust consent receipts operations. |
| `onetrust_cookie_consent` | intent | Manage OneTrust cookie consent operations. |
| `onetrust_cookie_consent_legacy` | intent | Manage OneTrust cookie consent legacy operations. |
| `onetrust_cookie_domain_data` | intent | Manage OneTrust cookie domain data operations. |
| `onetrust_cross_device_consent` | intent | Manage OneTrust cross device consent operations. |
| `onetrust_data_catalog` | intent | Manage OneTrust data catalog operations. |
| `onetrust_data_discovery` | intent | Manage OneTrust data discovery operations. |
| `onetrust_data_discovery_worker` | intent | Manage OneTrust data discovery worker operations. |
| `onetrust_data_mapping` | intent | Manage OneTrust data mapping operations. |
| `onetrust_data_mapping_legacy` | intent | Manage OneTrust data mapping legacy operations. |
| `onetrust_documents` | intent | Manage OneTrust documents operations. |
| `onetrust_dsar` | intent | Manage OneTrust dsar operations. |
| `onetrust_esg` | intent | Manage OneTrust esg operations. |
| `onetrust_incidents` | intent | Manage OneTrust incidents operations. |
| `onetrust_ingest_assessments` | intent | Ingest OneTrust assessments into the KG as typed :Assessment nodes + :Document summaries. |
| `onetrust_ingest_cookies` | intent | Ingest OneTrust cookie-scan results into the KG as typed :Cookie (+ :CookieDomain) nodes. |
| `onetrust_ingest_inventories` | intent | Ingest OneTrust data-inventory records into the KG as typed :Inventory (+ :DataElement) nodes. |
| `onetrust_integrations` | intent | Manage OneTrust integrations operations. |
| `onetrust_inventory` | intent | Manage OneTrust inventory operations. |
| `onetrust_issues_management` | intent | Manage OneTrust issues management operations. |
| `onetrust_it_risk_management` | intent | Manage OneTrust it risk management operations. |
| `onetrust_mobile_app_consent` | intent | Manage OneTrust mobile app consent operations. |
| `onetrust_object_manager` | intent | Manage OneTrust object manager operations. |
| `onetrust_policy_management` | intent | Manage OneTrust policy management operations. |
| `onetrust_privacy_notices` | intent | Manage OneTrust privacy notices operations. |
| `onetrust_task_management` | intent | Manage OneTrust task management operations. |
| `onetrust_tprm` | intent | Manage OneTrust tprm operations. |
| `onetrust_training` | intent | Manage OneTrust training operations. |
| `onetrust_universal_consent` | intent | Manage OneTrust universal consent operations. |
| `onetrust_user_provisioning` | intent | Manage OneTrust user provisioning operations. |

_39 intent tool(s) · 0 operation(s). Call an operation as `act(action='<operation>', params={...})` (`ask` for reads); `find(action='describe', params={'action': '<operation>'})` returns its arguments. An operation is enabled unless its `<DOMAIN>TOOL` toggle is set false. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `onetrust-api[mcp]` to add
> FastMCP / FastAPI through `agent-connector-sdk[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "onetrust-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "onetrust-api[mcp]",
        "onetrust-mcp"
      ],
      "env": {
        "ACCESS_MANAGEMENTTOOL": "True",
        "AI_GOVERNANCETOOL": "True",
        "ASSESSMENTSTOOL": "True",
        "AUDIT_MANAGEMENTTOOL": "True",
        "BULK_EXPORTTOOL": "True",
        "CMPTOOL": "True",
        "COMPLIANCE_AUTOMATIONTOOL": "True",
        "CONSENT_INTERFACESTOOL": "True",
        "CONSENT_RECEIPTSTOOL": "True",
        "COOKIE_CONSENTTOOL": "True",
        "COOKIE_CONSENT_LEGACYTOOL": "True",
        "COOKIE_DOMAIN_DATATOOL": "True",
        "CROSS_DEVICE_CONSENTTOOL": "True",
        "CUSTOM_APITOOL": "True",
        "DATA_CATALOGTOOL": "True",
        "DATA_DISCOVERYTOOL": "True",
        "DATA_DISCOVERY_WORKERTOOL": "True",
        "DATA_MAPPINGTOOL": "True",
        "DATA_MAPPING_LEGACYTOOL": "True",
        "DOCUMENTSTOOL": "True",
        "DSARTOOL": "True",
        "ESGTOOL": "True",
        "INCIDENTSTOOL": "True",
        "INTEGRATIONSTOOL": "True",
        "INVENTORYTOOL": "True",
        "ISSUES_MANAGEMENTTOOL": "True",
        "IT_RISK_MANAGEMENTTOOL": "True",
        "MOBILE_APP_CONSENTTOOL": "True",
        "OBJECT_MANAGERTOOL": "True",
        "ONETRUST_REGION": "us",
        "POLICY_MANAGEMENTTOOL": "True",
        "PRIVACY_NOTICESTOOL": "True",
        "TASK_MANAGEMENTTOOL": "True",
        "TPRMTOOL": "True",
        "TRAININGTOOL": "True",
        "UNIVERSAL_CONSENTTOOL": "True",
        "USER_PROVISIONINGTOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as Arbora. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "onetrust-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "onetrust-api[mcp]",
        "onetrust-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "ACCESS_MANAGEMENTTOOL": "True",
        "AI_GOVERNANCETOOL": "True",
        "ASSESSMENTSTOOL": "True",
        "AUDIT_MANAGEMENTTOOL": "True",
        "BULK_EXPORTTOOL": "True",
        "CMPTOOL": "True",
        "COMPLIANCE_AUTOMATIONTOOL": "True",
        "CONSENT_INTERFACESTOOL": "True",
        "CONSENT_RECEIPTSTOOL": "True",
        "COOKIE_CONSENTTOOL": "True",
        "COOKIE_CONSENT_LEGACYTOOL": "True",
        "COOKIE_DOMAIN_DATATOOL": "True",
        "CROSS_DEVICE_CONSENTTOOL": "True",
        "CUSTOM_APITOOL": "True",
        "DATA_CATALOGTOOL": "True",
        "DATA_DISCOVERYTOOL": "True",
        "DATA_DISCOVERY_WORKERTOOL": "True",
        "DATA_MAPPINGTOOL": "True",
        "DATA_MAPPING_LEGACYTOOL": "True",
        "DOCUMENTSTOOL": "True",
        "DSARTOOL": "True",
        "ESGTOOL": "True",
        "INCIDENTSTOOL": "True",
        "INTEGRATIONSTOOL": "True",
        "INVENTORYTOOL": "True",
        "ISSUES_MANAGEMENTTOOL": "True",
        "IT_RISK_MANAGEMENTTOOL": "True",
        "MOBILE_APP_CONSENTTOOL": "True",
        "OBJECT_MANAGERTOOL": "True",
        "ONETRUST_REGION": "us",
        "POLICY_MANAGEMENTTOOL": "True",
        "PRIVACY_NOTICESTOOL": "True",
        "TASK_MANAGEMENTTOOL": "True",
        "TPRMTOOL": "True",
        "TRAININGTOOL": "True",
        "UNIVERSAL_CONSENTTOOL": "True",
        "USER_PROVISIONINGTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "onetrust-mcp": {
      "url": "http://localhost:8000/onetrust-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e ACCESS_MANAGEMENTTOOL=True \
  -e AI_GOVERNANCETOOL=True \
  -e ASSESSMENTSTOOL=True \
  -e AUDIT_MANAGEMENTTOOL=True \
  -e BULK_EXPORTTOOL=True \
  -e CMPTOOL=True \
  -e COMPLIANCE_AUTOMATIONTOOL=True \
  -e CONSENT_INTERFACESTOOL=True \
  -e CONSENT_RECEIPTSTOOL=True \
  -e COOKIE_CONSENTTOOL=True \
  -e COOKIE_CONSENT_LEGACYTOOL=True \
  -e COOKIE_DOMAIN_DATATOOL=True \
  -e CROSS_DEVICE_CONSENTTOOL=True \
  -e CUSTOM_APITOOL=True \
  -e DATA_CATALOGTOOL=True \
  -e DATA_DISCOVERYTOOL=True \
  -e DATA_DISCOVERY_WORKERTOOL=True \
  -e DATA_MAPPINGTOOL=True \
  -e DATA_MAPPING_LEGACYTOOL=True \
  -e DOCUMENTSTOOL=True \
  -e DSARTOOL=True \
  -e ESGTOOL=True \
  -e INCIDENTSTOOL=True \
  -e INTEGRATIONSTOOL=True \
  -e INVENTORYTOOL=True \
  -e ISSUES_MANAGEMENTTOOL=True \
  -e IT_RISK_MANAGEMENTTOOL=True \
  -e MOBILE_APP_CONSENTTOOL=True \
  -e OBJECT_MANAGERTOOL=True \
  -e ONETRUST_REGION=us \
  -e POLICY_MANAGEMENTTOOL=True \
  -e PRIVACY_NOTICESTOOL=True \
  -e TASK_MANAGEMENTTOOL=True \
  -e TPRMTOOL=True \
  -e TRAININGTOOL=True \
  -e UNIVERSAL_CONSENTTOOL=True \
  -e USER_PROVISIONINGTOOL=True \
  registry.example.invalid/onetrust-api@sha256:<digest> onetrust-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

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
  example/onetrust-api:mcp
```

> The `:mcp` tag is the **MCP-serving image** (built from
> `docker/Dockerfile --target mcp`, installing `onetrust-api[mcp]`). The default
> the immutable agent image is the **full agent image** (`--target agent`, `onetrust-api[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when the operator run `onetrust-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

### Deploy with Docker Compose

```yaml
services:
  onetrust-api-mcp:
    image: example/onetrust-api:mcp
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

Pick the extra that matches what the operator want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `onetrust-api[mcp]` | Connector-focused MCP server (`agent-connector-sdk[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | The operator only run the **MCP server** (smallest install / image) |
| `onetrust-api[agent]` | Agent runtime (`agent-connector-sdk[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | The operator run the **integrated agent** |
| `onetrust-api[all]` | Everything (`mcp` + `agent`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "onetrust-api[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "onetrust-api[agent]"

# Everything (development)
uv pip install "onetrust-api[all]"      # or: python -m pip install "onetrust-api[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/onetrust-api:mcp` | `--target mcp` | `onetrust-api[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `onetrust-mcp` |
| `example/onetrust-api@sha256:<digest>` | `--target agent` (default) | `onetrust-api[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `onetrust-agent` |

```bash
docker build --target mcp   -t example/onetrust-api:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/onetrust-api:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` also enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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
| `TLS_PROFILE` | Named `AgentConfig` transport-security profile; verification is mandatory | — |
| `TLS_PROFILES_REF` | Runtime secret reference for the TLS profile catalog | — |

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

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)


<!-- BEGIN agent-connector-sdk-deployment (generated; do not edit between markers) -->

## Deploy with `agent-connector-sdk-deployment`

Provision this package with the consolidated **`agent-connector-sdk-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `onetrust-api` with agent-connector-sdk-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "onetrust-api[mcp]"`, then run `onetrust-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `onetrust-mcp` |
| Immutable container | deploy `registry.example.invalid/onetrust-api@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-connector-sdk-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, Arbora delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
