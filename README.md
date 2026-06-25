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

_36 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
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
