---
name: onetrust-api-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the onetrust-api connector. Use this skill when
  changing the connector's API mappings, MCP tools, packaging, documentation,
  or repository gates.
license: MIT
tags: [onetrust-api, development, connector, test, gates]
tier: repository
metadata:
  author: Genius
  version: '0.2.0'
---

# onetrust-api development

This repository owns the OneTrust connector. API coverage is generated from the vendored OpenAPI specs in `onetrust_api/specs/*.json`, not written by hand. Shared connector contracts and transports belong to `scion-sdk`;
admission, serving, and durable graph state belong to their owning
repositories. Read `AGENTS.md` before changing code and keep provider
credentials and endpoints out of source, logs, and skill content.

Do not hand-edit generated files (`onetrust_api/api/api_client_<domain>.py`,
`api_client.py`, `api/_operation_manifest.py`, `mcp/mcp_<domain>.py`,
`mcp/__init__.py`). Change `scripts/generate_from_openapi.py` and re-run it.
Hand-authored core: `api/api_client_base.py`, `auth.py`, `onetrust_models.py`,
`mcp/mcp_custom_api.py`.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend
  that spec before adding new requirement text.
- Reuse existing SDK clients, transport policies, and tool factories. Do not
  create a second implementation of a connector capability.
- Keep changes scoped to this connector. A change owned by the SDK, Arbora,
  or the knowledge graph belongs in that repository instead.
- Every delivered requirement needs a bound test. Generated `status.json`
  files are produced by `pipelines-hook spec-status`; never hand-edit them.
- One logical change per commit, with `Spec: <ID>` and the assisting agent
  trailer adjacent in the final paragraph.

## Setup and gates

Use the pinned environment from `uv sync --locked --all-extras`. Run the
repository gate from the checkout root:

```bash
uvx pre-commit run --all-files
```

For focused feedback, run the relevant tests with the repository's pinned
environment, for example:

```bash
uv run --all-extras pytest tests/test_onetrust_coverage.py -q
uv run --all-extras pytest tests/test_auth.py tests/test_mcp_server.py -q
# after a spec refresh
uv run python scripts/generate_from_openapi.py && uvx ruff format .
```

The canonical `.pre-commit-config.yaml` delegates connector-standard,
secrets, spec, tests-fast, and dependency-readiness checks to
`Knuckles-Team/pipelines` at `rev: main`. Do not replace those shared hooks
with local copies or bypass a failing check.

## Connector-specific checks

- Refresh flow: replace the specs, run the generator, format, then run
  `tests/test_onetrust_coverage.py`, which proves spec operations equal client
  methods equal MCP actions.
- Tool surface follows `MCP_TOOL_MODE` (`condensed` default, `verbose`, `both`);
  parameter types come from the generated operation manifest.
- Authentication is either `ONETRUST_TOKEN` or `ONETRUST_CLIENT_ID` plus
  `ONETRUST_CLIENT_SECRET`; the tenant comes from `ONETRUST_URL` or
  `ONETRUST_REGION`. Mock every OneTrust call; never use a live tenant in a gate.
- Keep the MCP surface aligned with `scion-sdk`; read the version from package
  metadata rather than spelling it in a module.
- Keep `onetrust_api/skills/` package data intact when adding skills.
- Documentation lives under `docs/` and is published by the shared Pages
  workflow; source status records live under `specs/`.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths, and verify `git status --short` after every gate.
Do not use `git stash`, `git add -A`, or `git add .`; do not claim Pages
publication until a successful exact-source workflow run and the public page
are both observed.
