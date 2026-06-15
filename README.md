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

*Version: 0.1.2*

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
  --name onetrust-api \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e ONETRUST_URL="http://your-service:8080" \
  -e ONETRUST_TOKEN="your_token" \
  knucklessg1/onetrust-api:latest
```

### Deploy with Docker Compose

```yaml
services:
  onetrust-api:
    image: knucklessg1/onetrust-api:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - ONETRUST_URL=http://your-service:8080
      - ONETRUST_TOKEN=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "onetrust": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "onetrust-api",
        "onetrust-mcp"
      ],
      "env": {
        "ONETRUST_URL": "http://your-service:8080",
        "ONETRUST_TOKEN": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install onetrust-api
```
```bash
uv pip install onetrust-api
```

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
