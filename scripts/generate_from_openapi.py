#!/usr/bin/env python
"""Generate the OneTrust API client + MCP tools from the vendored OpenAPI specs.

This is an **author-time** developer tool, not a runtime dependency. It reads every
spec in ``onetrust_api/specs/*.json`` and emits fleet-conformant, committed code:

* ``onetrust_api/api/api_client_<domain>.py`` — one method per OpenAPI operation,
  composed into ``onetrust_api.api_client.Api`` via multiple inheritance.
* ``onetrust_api/api/_operation_manifest.py`` — the machine-readable
  ``operationId → method → action`` map that the coverage test asserts against.
* ``onetrust_api/mcp/mcp_<domain>.py`` — one consolidated, action-routed MCP tool
  per domain exposing every operation as an ``action``.
* ``onetrust_api/mcp/__init__.py`` — ``TOOL_REGISTRY`` consumed by ``mcp_server.py``.
* ``onetrust_api/api_client.py`` — the composite ``Api`` class.

Re-run after refreshing the specs:  ``python scripts/generate_from_openapi.py``
"""

from __future__ import annotations

import json
import keyword
import re
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent / "onetrust_api"
SPECS_DIR = PKG / "specs"
API_DIR = PKG / "api"
MCP_DIR = PKG / "mcp"

# Curated, concise domain name (== MCP tag, == client-module suffix) per spec file.
SPEC_DOMAIN = {
    "ai-governance": "ai_governance",
    "consent-preferences-consent-interfaces": "consent_interfaces",
    "consent-preferences-consent-management-platform-cmp": "cmp",
    "consent-preferences-consent-receipts": "consent_receipts",
    "consent-preferences-cookie-consent-swagger": "cookie_consent_legacy",
    "consent-preferences-cookie-consent": "cookie_consent",
    "consent-preferences-cookie-domain-data": "cookie_domain_data",
    "consent-preferences-cross-device-consent": "cross_device_consent",
    "consent-preferences-mobile-app-consent": "mobile_app_consent",
    "consent-preferences-policy-notice-management": "privacy_notices",
    "consent-preferences-universal-consent-preference-management-oas": "universal_consent",
    "data-use-governance-data-catalog": "data_catalog",
    "data-use-governance-data-discovery-worker-node": "data_discovery_worker",
    "data-use-governance-data-discovery": "data_discovery",
    "esg-program-reporting-disclosures": "esg",
    "platform-access-management": "access_management",
    "platform-bulk-export": "bulk_export",
    "platform-documents": "documents",
    "platform-integrations": "integrations",
    "platform-inventory": "inventory",
    "platform-object-manager": "object_manager",
    "platform-task-management": "task_management",
    "platform-user-provisioning": "user_provisioning",
    "privacy-automation-assessment-automation": "assessments",
    "privacy-automation-data-mapping-automation-swagger": "data_mapping_legacy",
    "privacy-automation-data-mapping-automation": "data_mapping",
    "privacy-automation-data-subject-request-dsr-automation": "dsar",
    "privacy-automation-incident-management": "incidents",
    "tech-risk-compliance-audit-management": "audit_management",
    "tech-risk-compliance-compliance-automation": "compliance_automation",
    "tech-risk-compliance-enterprise-policy-management": "policy_management",
    "tech-risk-compliance-issues-management": "issues_management",
    "tech-risk-compliance-it-risk-management": "it_risk_management",
    "tech-risk-compliance-training": "training",
    "third-party-management-third-party-risk-management": "tprm",
}

_CURSOR_KEYS = {
    "requestContinuation",
    "continuationToken",
    "nextPageToken",
    "bookmark",
    "pageId",
}
HTTP_METHODS = ("get", "post", "put", "delete", "patch")


def snake(name: str) -> str:
    """Convert an operationId / slug to a safe snake_case Python identifier."""
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = re.sub(r"_+", "_", name).strip("_").lower()
    if not name:
        name = "op"
    if name[0].isdigit():
        name = "op_" + name
    if keyword.iskeyword(name):
        name += "_"
    return name


def camel(domain: str) -> str:
    return "".join(part.capitalize() for part in domain.split("_"))


def server_template(spec: dict) -> str:
    """Absolute server prefix with ``{hostname}`` → ``__HOSTNAME__`` sentinel."""
    servers = spec.get("servers") or [{}]
    url = servers[0].get("url", "")
    variables = servers[0].get("variables") or {}
    for var, meta in variables.items():
        token = "{" + var + "}"
        if var == "hostname":
            url = url.replace(token, "__HOSTNAME__")
        else:
            url = url.replace(token, str(meta.get("default", "")))
    return url.rstrip("/")


def detect_pagination(http: str, query_params: list[str]) -> str:
    if http.upper() != "GET":
        return "none"
    qs = set(query_params)
    if {"page", "size"} <= qs or {"page", "per_page"} <= qs:
        return "offset"
    if qs & _CURSOR_KEYS:
        return "cursor"
    return "none"


def collect_operations() -> dict[str, list[dict]]:
    """Return ``{domain: [operation_meta, ...]}`` across all vendored specs."""
    by_domain: dict[str, list[dict]] = {}
    global_methods: set[str] = set()
    synthetic = 0

    for spec_path in sorted(SPECS_DIR.glob("*.json")):
        stem = spec_path.stem
        domain = SPEC_DOMAIN.get(stem, snake(stem))
        spec = json.loads(spec_path.read_text())
        base = server_template(spec)
        ops: list[dict] = []
        actions_seen: set[str] = set()

        for path, methods in (spec.get("paths") or {}).items():
            shared = methods.get("parameters", []) if isinstance(methods, dict) else []
            for http, op in methods.items():
                if http not in HTTP_METHODS or not isinstance(op, dict):
                    continue
                op_id = op.get("operationId")
                if not op_id:
                    synthetic += 1
                    op_id = snake(f"{http}_{path}")
                params = list(shared) + list(op.get("parameters") or [])
                path_params = [
                    p["name"] for p in params if p.get("in") == "path"
                ]
                # Path templating tokens not formally declared as parameters.
                for token in re.findall(r"\{([^}]+)\}", path):
                    if token not in path_params:
                        path_params.append(token)
                query_params = [p["name"] for p in params if p.get("in") == "query"]
                has_body = "requestBody" in op

                method_name = snake(op_id)
                while method_name in global_methods:
                    method_name += "_x"
                global_methods.add(method_name)

                action = snake(op_id)
                while action in actions_seen:
                    action += "_x"
                actions_seen.add(action)

                summary = (op.get("summary") or op.get("description") or op_id).strip()
                summary = re.sub(r"\s+", " ", summary.splitlines()[0])[:160]

                ops.append(
                    {
                        "operation_id": op_id,
                        "method": method_name,
                        "action": action,
                        "domain": domain,
                        "http": http.upper(),
                        "url_template": base + path,
                        "path_params": path_params,
                        "query_params": query_params,
                        "has_body": has_body,
                        "paginate": detect_pagination(http, query_params),
                        "summary": summary,
                    }
                )
        if ops:
            by_domain.setdefault(domain, []).extend(ops)

    print(f"Collected {sum(len(v) for v in by_domain.values())} operations "
          f"across {len(by_domain)} domains ({synthetic} synthetic ids).")
    return by_domain


# --------------------------------------------------------------------- emitters
AUTOGEN = '"""Auto-generated by scripts/generate_from_openapi.py — do not edit by hand."""'


def emit_client_module(domain: str, ops: list[dict]) -> None:
    cls = f"OneTrust{camel(domain)}"
    lines = [
        "#!/usr/bin/python",
        AUTOGEN,
        "",
        "from onetrust_api.api.api_client_base import OneTrustApiBase",
        "from onetrust_api.onetrust_models import Response",
        "",
        "",
        f"class {cls}(OneTrustApiBase):",
    ]
    for op in ops:
        doc = op["summary"].replace('"', "'")
        lines += [
            f"    def {op['method']}(self, **kwargs) -> Response:",
            f'        """{doc}"""',
            "        return self._call(",
            f"            http={op['http']!r},",
            f"            url_template={op['url_template']!r},",
            f"            path_params={op['path_params']!r},",
            f"            query_params={op['query_params']!r},",
            f"            has_body={op['has_body']!r},",
            f"            paginate={op['paginate']!r},",
            "            kwargs=kwargs,",
            "        )",
            "",
    ]
    (API_DIR / f"api_client_{domain}.py").write_text("\n".join(lines) + "\n")


def emit_mcp_module(domain: str, ops: list[dict]) -> None:
    tag = domain
    actions = ", ".join(f"'{op['action']}'" for op in ops)
    lines = [
        AUTOGEN,
        "",
        "from typing import Any",
        "",
        "from fastmcp import Context, FastMCP",
        "from fastmcp.dependencies import Depends",
        "from pydantic import Field",
        "",
        "from onetrust_api.auth import get_client",
        "",
        "",
        f"def register_{domain}_tools(mcp: FastMCP):",
        f'    @mcp.tool(tags={{"{tag}"}})',
        f"    async def onetrust_{domain}(",
        "        action: str = Field(",
        f'            description="Action to perform. One of: {actions}"',
        "        ),",
        "        params_json: str = Field(",
        '            default="{}",',
        '            description="JSON string of parameters (path, query, and body fields) for the action.",',
        "        ),",
        "        client=Depends(get_client),",
        "        ctx: Context | None = Field(",
        '            default=None, description="MCP context for progress reporting"',
        "        ),",
        "    ) -> Any:",
        f'        """Manage OneTrust {domain.replace("_", " ")} operations."""',
        "        if ctx:",
        '            await ctx.info(f"Executing onetrust_' + domain + ' action: {action}")',
        "        import json",
        "",
        "        try:",
        "            kwargs = json.loads(params_json) if params_json else {}",
        "        except Exception as e:",
        '            return {"error": f"Invalid params_json: {e}"}',
        "        if not isinstance(kwargs, dict):",
        '            return {"error": "params_json must decode to a JSON object"}',
        "        kwargs = {k: v for k, v in kwargs.items() if v is not None}",
        "",
    ]
    first = True
    for op in ops:
        kw = "if" if first else "elif"
        first = False
        lines.append(f'        {kw} action == "{op["action"]}":')
        lines.append(f"            return client.{op['method']}(**kwargs)")
    lines += [
        '        raise ValueError(f"Unknown action: {action}")',
        "",
    ]
    (MCP_DIR / f"mcp_{domain}.py").write_text("\n".join(lines) + "\n")


def emit_manifest(by_domain: dict[str, list[dict]]) -> None:
    # A LIST (not a dict): operationIds are NOT globally unique across specs
    # (22 collisions), so keying by operationId would silently drop operations.
    # method names ARE globally unique; actions are unique within a domain.
    operations = [
        {
            "operation_id": op["operation_id"],
            "domain": domain,
            "method": op["method"],
            "action": op["action"],
            "http": op["http"],
            "path": op["url_template"],
            "paginate": op["paginate"],
        }
        for domain in sorted(by_domain)
        for op in by_domain[domain]
    ]
    lines = [
        AUTOGEN,
        "",
        "# Each entry: {operation_id, domain, method, action, http, path, paginate}",
        f"OPERATIONS = {json.dumps(operations, indent=4)}",
        "",
        "DOMAINS = " + json.dumps(sorted(by_domain), indent=4),
        "",
        "# domain -> ordered list of MCP action names",
        "ACTIONS_BY_DOMAIN: dict[str, list[str]] = {}",
        "for _op in OPERATIONS:",
        "    ACTIONS_BY_DOMAIN.setdefault(_op['domain'], []).append(_op['action'])",
        "",
    ]
    (API_DIR / "_operation_manifest.py").write_text("\n".join(lines) + "\n")


def emit_api_client(by_domain: dict[str, list[dict]]) -> None:
    domains = sorted(by_domain)
    imports = [
        f"from onetrust_api.api.api_client_{d} import OneTrust{camel(d)}"
        for d in domains
    ]
    bases = ",\n    ".join(f"OneTrust{camel(d)}" for d in domains)
    lines = [
        "#!/usr/bin/python",
        AUTOGEN,
        "",
        *imports,
        "",
        "",
        f"class Api(\n    {bases},\n):",
        '    """Composite OneTrust API client — every domain client, one class."""',
        "",
        "    __slots__ = ()",
        "",
    ]
    (PKG / "api_client.py").write_text("\n".join(lines) + "\n")


def emit_mcp_init(by_domain: dict[str, list[dict]]) -> None:
    domains = sorted(by_domain)
    imports = [
        f"from onetrust_api.mcp.mcp_{d} import register_{d}_tools" for d in domains
    ]
    registry = [
        f'    ("{d}", "{d.upper()}TOOL", register_{d}_tools),' for d in domains
    ]
    lines = [
        AUTOGEN,
        "",
        *imports,
        "from onetrust_api.mcp.mcp_custom_api import register_custom_api_tools",
        "",
        "# (tag, toggle_env_var, register_fn) — consumed by mcp_server.get_mcp_instance().",
        "TOOL_REGISTRY = [",
        *registry,
        '    ("custom_api", "CUSTOM_APITOOL", register_custom_api_tools),',
        "]",
        "",
        "__all__ = [",
        *[f'    "register_{d}_tools",' for d in domains],
        '    "register_custom_api_tools",',
        '    "TOOL_REGISTRY",',
        "]",
        "",
    ]
    (MCP_DIR / "__init__.py").write_text("\n".join(lines) + "\n")


def main() -> None:
    API_DIR.mkdir(exist_ok=True)
    MCP_DIR.mkdir(exist_ok=True)
    by_domain = collect_operations()
    for domain, ops in by_domain.items():
        emit_client_module(domain, ops)
        emit_mcp_module(domain, ops)
    emit_manifest(by_domain)
    emit_api_client(by_domain)
    emit_mcp_init(by_domain)
    tools = len(by_domain) + 1  # + custom_api
    print(f"Generated {len(by_domain)} client modules, {tools} MCP tools.")


if __name__ == "__main__":
    main()
