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

import argparse
import ast
import json
import keyword
import re
from dataclasses import dataclass
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


_OPENAPI_SCALAR = {"string", "integer", "number", "boolean", "array", "object"}


def _resolve_ref(spec: dict, node):
    """Follow ``$ref`` chains within a spec; return the resolved dict (or {})."""
    seen: set[str] = set()
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/") or ref in seen:
            break
        seen.add(ref)
        cur = spec
        for part in ref[2:].split("/"):
            cur = cur.get(part, {}) if isinstance(cur, dict) else {}
        node = cur
    return node if isinstance(node, dict) else {}


def _param_entry(name: str, schema: dict, required: bool, description) -> dict:
    schema = schema or {}
    t = schema.get("type")
    if not t and any(k in schema for k in ("$ref", "allOf", "properties")):
        t = "object"
    if t not in _OPENAPI_SCALAR:
        t = "string"
    return {
        "name": name,
        "type": t,
        "required": bool(required),
        "description": re.sub(r"\s+", " ", (description or "").strip())[:200],
    }


def normalize_params(params: list, op: dict, spec: dict) -> list[dict]:
    """Flatten path/query params + top-level requestBody fields into typed entries.

    Produces ``[{name, type, required, description}, ...]`` for the verbose 1:1
    tool tier (`register_verbose_tools` synthesizes a typed signature from it).
    All fields dispatch by name; the client routes path/query/body internally.
    """
    out: list[dict] = []
    seen: set[str] = set()
    _normalize_path_query_params(params, spec, out, seen)
    _normalize_request_body_params(op, spec, out, seen)
    return out


def _normalize_path_query_params(
    params: list, spec: dict, out: list[dict], seen: set[str]
) -> None:
    """Append one typed entry per path/query parameter, skipping dupes/unnamed."""
    for p in params:
        p = _resolve_ref(spec, p)
        name = p.get("name")
        if not name or p.get("in") not in ("path", "query") or name in seen:
            continue
        seen.add(name)
        out.append(
            _param_entry(
                name,
                p.get("schema") or {},
                p.get("required") or p.get("in") == "path",
                p.get("description"),
            )
        )


def _normalize_request_body_params(
    op: dict, spec: dict, out: list[dict], seen: set[str]
) -> None:
    """Append typed entries for the operation's requestBody, if any."""
    request_body = _resolve_ref(spec, op.get("requestBody") or {})
    if not request_body:
        return
    content = request_body.get("content") or {}
    media = content.get("application/json") or next(iter(content.values()), {})
    schema = _resolve_ref(spec, (media or {}).get("schema") or {})
    props = schema.get("properties") or {}
    if props:
        _append_body_property_params(props, schema, spec, out, seen)
        return
    out.append(
        {
            "name": "body",
            "type": "object",
            "required": bool(request_body.get("required")),
            "description": "Request body (JSON object).",
        }
    )


def _append_body_property_params(
    props: dict, schema: dict, spec: dict, out: list[dict], seen: set[str]
) -> None:
    """Append one typed entry per top-level requestBody property."""
    required = set(schema.get("required") or [])
    for pname, pschema in props.items():
        if pname in seen:
            continue
        seen.add(pname)
        ps = _resolve_ref(spec, pschema)
        out.append(_param_entry(pname, ps, pname in required, ps.get("description")))


def collect_operations() -> dict[str, list[dict]]:
    """Return ``{domain: [operation_meta, ...]}`` across all vendored specs."""
    by_domain: dict[str, list[dict]] = {}
    global_methods: set[str] = set()
    synthetic = 0

    for spec_path in sorted(SPECS_DIR.glob("*.json")):
        domain, ops, spec_synthetic = _collect_spec_operations(
            spec_path, global_methods
        )
        synthetic += spec_synthetic
        if ops:
            by_domain.setdefault(domain, []).extend(ops)

    print(
        f"Collected {sum(len(v) for v in by_domain.values())} operations "
        f"across {len(by_domain)} domains ({synthetic} synthetic ids)."
    )
    return by_domain


@dataclass
class _SpecContext:
    """The parsed spec plus the values every operation in it shares."""

    spec: dict
    domain: str
    base: str


def _collect_spec_operations(
    spec_path: Path, global_methods: set[str]
) -> tuple[str, list[dict], int]:
    """Collect every operation declared in one vendored spec file.

    Returns ``(domain, operations, synthetic_id_count)``.
    """
    stem = spec_path.stem
    domain = SPEC_DOMAIN.get(stem, snake(stem))
    spec = json.loads(spec_path.read_text())
    ctx = _SpecContext(spec=spec, domain=domain, base=server_template(spec))
    ops: list[dict] = []
    actions_seen: set[str] = set()
    synthetic = 0

    for path, methods in (spec.get("paths") or {}).items():
        shared = methods.get("parameters", []) if isinstance(methods, dict) else []
        for http, op in methods.items():
            if http not in HTTP_METHODS or not isinstance(op, dict):
                continue
            entry, is_synthetic = _build_operation_entry(
                http, op, path, shared, ctx, global_methods, actions_seen
            )
            ops.append(entry)
            synthetic += is_synthetic

    return domain, ops, synthetic


def _build_operation_entry(
    http: str,
    op: dict,
    path: str,
    shared: list,
    ctx: _SpecContext,
    global_methods: set[str],
    actions_seen: set[str],
) -> tuple[dict, int]:
    """Build one operation's manifest entry.

    Returns ``(entry, 1)`` if the operationId had to be synthesized, else
    ``(entry, 0)``.
    """
    op_id = op.get("operationId")
    synthetic = 0
    if not op_id:
        synthetic = 1
        op_id = snake(f"{http}_{path}")

    params = list(shared) + list(op.get("parameters") or [])
    path_params = _collect_path_params(params, path)
    query_params = [p["name"] for p in params if p.get("in") == "query"]

    summary = (op.get("summary") or op.get("description") or op_id).strip()
    summary = re.sub(r"\s+", " ", summary.splitlines()[0])[:160]

    entry = {
        "operation_id": op_id,
        "method": _unique_name(snake(op_id), global_methods),
        "action": _unique_name(snake(op_id), actions_seen),
        "domain": ctx.domain,
        "http": http.upper(),
        "url_template": ctx.base + path,
        "path_params": path_params,
        "query_params": query_params,
        "has_body": "requestBody" in op,
        "paginate": detect_pagination(http, query_params),
        "summary": summary,
        "params": normalize_params(params, op, ctx.spec),
    }
    return entry, synthetic


def _collect_path_params(params: list, path: str) -> list[str]:
    """Path parameters declared formally plus any bare ``{token}`` in the path."""
    path_params = [p["name"] for p in params if p.get("in") == "path"]
    for token in re.findall(r"\{([^}]+)\}", path):
        if token not in path_params:
            path_params.append(token)
    return path_params


def _unique_name(base_name: str, seen: set[str]) -> str:
    """Disambiguate ``base_name`` against ``seen`` (appending ``_x``), recording it."""
    name = base_name
    while name in seen:
        name += "_x"
    seen.add(name)
    return name


# --------------------------------------------------------------------- emitters
AUTOGEN = (
    '"""Auto-generated by scripts/generate_from_openapi.py — do not edit by hand."""'
)


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


# Cap on branches per generated ``_dispatch_<domain>_<n>`` helper -- 9 elif
# branches + the implicit function-entry edge keeps each helper's cyclomatic
# complexity at exactly 10 (the fleet's ``check_complexity.py`` cap), so a
# freshly generated file never needs a follow-up decomposition pass.
_DISPATCH_GROUP_SIZE = 9


def _chunk(items: list, size: int) -> list[list]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def _emit_dispatch_helpers(lines: list[str], domain: str, ops: list[dict]) -> list[str]:
    """Append grouped ``_dispatch_<domain>_<n>`` helpers to ``lines`` in place.

    Each helper keeps the exact same ``if/elif action == "<name>": return
    client.<method>(**kwargs)`` textual shape as a flat dispatch chain would --
    just chunked into groups of <= ``_DISPATCH_GROUP_SIZE`` branches -- so the
    coverage test that regex-scans generated source for literal
    ``action == "value"`` occurrences (``test_every_action_is_routed_in_its_mcp_tool``)
    keeps working unmodified. Returns the helper names in emission order.
    """
    names = []
    for i, group in enumerate(_chunk(ops, _DISPATCH_GROUP_SIZE), start=1):
        name = f"_dispatch_{domain}_{i}"
        names.append(name)
        lines.append(f"def {name}(action, kwargs, client):")
        lines.append(
            f"    # {group[0]['action']} .. {group[-1]['action']} ({len(group)} actions)"
        )
        for j, op in enumerate(group):
            kw = "if" if j == 0 else "elif"
            lines.append(f'    {kw} action == "{op["action"]}":')
            lines.append(f"        return client.{op['method']}(**kwargs)")
        lines.append("    return _UNHANDLED")
        lines.append("")
        lines.append("")
    return names


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
        "_UNHANDLED = object()",
        "",
        "",
    ]
    dispatcher_names = _emit_dispatch_helpers(lines, domain, ops)
    dispatchers_var = f"_{domain.upper()}_DISPATCHERS"
    lines.append(f"{dispatchers_var} = (")
    for name in dispatcher_names:
        lines.append(f"    {name},")
    lines.append(")")
    lines.append("")
    lines.append("")
    lines += [
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
        '            await ctx.info(f"Executing onetrust_'
        + domain
        + ' action: {action}")',
        "        import json",
        "",
        "        try:",
        "            kwargs = json.loads(params_json) if params_json else {}",
        "        except Exception as e:",
        '            return {"error": f"Invalid params_json: {type(e).__name__}"}',
        "        if not isinstance(kwargs, dict):",
        '            return {"error": "params_json must decode to a JSON object"}',
        "        kwargs = {k: v for k, v in kwargs.items() if v is not None}",
        "",
        f"        for _dispatch in {dispatchers_var}:",
        "            _result = _dispatch(action, kwargs, client)",
        "            if _result is not _UNHANDLED:",
        "                return _result",
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
            "summary": op["summary"],
            "params": op["params"],
        }
        for domain in sorted(by_domain)
        for op in by_domain[domain]
    ]
    lines = [
        AUTOGEN,
        "",
        "# Each entry: {operation_id, domain, method, action, http, path, paginate,",
        "#             summary, params:[{name,type,required,description}]}",
        "# `summary` + `params` drive the verbose 1:1 tool tier (register_verbose_tools).",
        # repr() (not json.dumps) — params carry Python bools; ruff format prettifies.
        f"OPERATIONS = {operations!r}",
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
    registry = [f'    ("{d}", "{d.upper()}TOOL", register_{d}_tools),' for d in domains]
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


# --------------------------------------------------------------- reconciler
#
# Regenerating whole files on every run is the defect this reconciler exists
# to remove: it silently overwrites hand-maintained code (the very refactor
# that decomposed these dispatch chains under the complexity cap). So the
# default mode of this script is now READ-ONLY reconciliation -- it diffs the
# vendored spec against the committed source and reports drift, never writes.
# ``--scaffold`` is the old full-generation behavior, kept only for a
# brand-new repo with no MCP module yet (it refuses to touch anything that
# already exists). ``--apply`` inserts ONLY the additive delta (new handlers
# for actions the spec added) in the exact shape the file already uses, and
# never touches an existing line; renames, signature changes, and removals
# are reported for a human, never auto-applied.


class Finding:
    __slots__ = ("kind", "domain", "action", "detail")

    def __init__(self, kind: str, domain: str, detail: str, action: str | None = None):
        self.kind = kind
        self.domain = domain
        self.action = action
        self.detail = detail

    def __str__(self) -> str:
        return f"[{self.kind}] {self.domain}: {self.detail}"


def _extract_handled_actions(src: str) -> set[str]:
    """Extract the set of action strings a module's dispatch chain handles.

    Matches the literal comparison text regardless of whether it sits in one
    flat chain or many grouped ``_dispatch_<domain>_<n>`` helpers -- the exact
    same text test_onetrust_coverage.py::test_every_action_is_routed_in_its_mcp_tool
    regex-scans for, so this extraction and that test agree by construction.
    """
    return set(re.findall(r'action\s*==\s*"([^"]+)"', src))


def _extract_client_signatures(src: str) -> dict[str, tuple]:
    """Parse an ``api_client_<domain>.py`` module and return
    ``{method_name: (http, url_template, path_params, query_params, has_body)}``
    by reading each method's ``self._call(...)`` keyword arguments via ``ast``
    -- never by re-deriving it, so a hand-edited call still reconciles
    honestly against what the code actually does.
    """
    sigs: dict[str, tuple] = {}
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        call = _find_self_call(node)
        if call is None:
            continue
        sig = _signature_from_call(call)
        if sig is not None:
            sigs[node.name] = sig
    return sigs


def _find_self_call(node: ast.FunctionDef) -> ast.Call | None:
    """Find the (first) ``self._call(...)`` invocation inside a function body."""
    for n in ast.walk(node):
        if (
            isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "_call"
        ):
            return n
    return None


def _signature_from_call(call: ast.Call) -> tuple | None:
    """Read a ``self._call(...)`` node's keyword arguments as a signature tuple."""
    kwargs = {kw.arg: kw.value for kw in call.keywords if kw.arg}
    try:
        http = ast.literal_eval(kwargs["http"])
        url_template = ast.literal_eval(kwargs["url_template"])
        path_params = tuple(ast.literal_eval(kwargs["path_params"]))
        query_params = tuple(sorted(ast.literal_eval(kwargs["query_params"])))
        has_body = ast.literal_eval(kwargs["has_body"])
    except (KeyError, ValueError):
        return None
    return (http, url_template, path_params, query_params, has_body)


def _op_signature(op: dict) -> tuple:
    return (
        op["http"],
        op["url_template"],
        tuple(op["path_params"]),
        tuple(sorted(op["query_params"])),
        op["has_body"],
    )


def reconcile(by_domain: dict[str, list[dict]]) -> list[Finding]:
    """Compare the current spec against the existing hand-maintained source.

    Read-only -- never writes anything. Detects: actions the spec has that no
    handler routes to (added upstream), handlers that route an action the
    spec no longer has (removed/renamed upstream -- a likely dead branch),
    operations whose (http, url_template, path_params, query_params,
    has_body) signature changed, and whole domains that appeared or vanished.
    """
    existing_mcp_domains = _existing_mcp_domains()
    spec_domains = set(by_domain)

    findings: list[Finding] = []
    findings.extend(_new_domain_findings(spec_domains, existing_mcp_domains, by_domain))
    findings.extend(_orphaned_domain_findings(spec_domains, existing_mcp_domains))
    for domain in sorted(spec_domains & existing_mcp_domains):
        findings.extend(_reconcile_domain(domain, by_domain[domain]))
    return findings


def _existing_mcp_domains() -> set[str]:
    """Domains with an existing generator-owned ``mcp_<domain>.py`` module."""
    return {
        p.stem[len("mcp_") :]
        for p in MCP_DIR.glob("mcp_*.py")
        if p.stem not in ("mcp_custom_api", "__init__")
        and p.read_text(errors="ignore").startswith(AUTOGEN)
    }


def _new_domain_findings(
    spec_domains: set[str],
    existing_mcp_domains: set[str],
    by_domain: dict[str, list[dict]],
) -> list[Finding]:
    """Spec domains that have no ``mcp_<domain>.py`` yet."""
    return [
        Finding(
            "NEW DOMAIN",
            domain,
            f"{len(by_domain[domain])} action(s) in the spec, no mcp_{domain}.py "
            f"yet -- scaffold is for a brand-new repo only "
            f"(refuses if any mcp_*.py already exists); hand-author this domain's "
            f"file once, then reconcile/--apply will track it going forward.",
        )
        for domain in sorted(spec_domains - existing_mcp_domains)
    ]


def _orphaned_domain_findings(
    spec_domains: set[str], existing_mcp_domains: set[str]
) -> list[Finding]:
    """``mcp_<domain>.py`` modules whose domain no longer exists in any spec."""
    return [
        Finding(
            "ORPHANED DOMAIN",
            domain,
            f"mcp_{domain}.py exists but the domain no longer appears in the spec "
            f"at all -- likely dropped upstream. Not auto-removed.",
        )
        for domain in sorted(existing_mcp_domains - spec_domains)
    ]


def _reconcile_domain(domain: str, ops: list[dict]) -> list[Finding]:
    """Reconcile one domain present on both the spec and the hand-maintained source."""
    spec_actions = {op["action"]: op for op in ops}
    mcp_src = (MCP_DIR / f"mcp_{domain}.py").read_text()
    handled = _extract_handled_actions(mcp_src)

    findings = _action_routing_findings(domain, spec_actions, handled)

    client_path = API_DIR / f"api_client_{domain}.py"
    if client_path.exists():
        client_sigs = _extract_client_signatures(client_path.read_text())
        findings.extend(
            _signature_drift_findings(domain, spec_actions, handled, client_sigs)
        )
    return findings


def _action_routing_findings(
    domain: str, spec_actions: dict[str, dict], handled: set[str]
) -> list[Finding]:
    """Actions the spec has but no handler routes to, and vice versa."""
    findings: list[Finding] = []
    for action in sorted(set(spec_actions) - handled):
        op = spec_actions[action]
        findings.append(
            Finding(
                "MISSING HANDLER",
                domain,
                f"action '{action}' ({op['operation_id']}) is in the spec but no "
                f"branch in mcp_{domain}.py routes to it.",
                action=action,
            )
        )
    for action in sorted(handled - set(spec_actions)):
        findings.append(
            Finding(
                "ORPHANED HANDLER",
                domain,
                f"mcp_{domain}.py routes action '{action}' but the spec no longer "
                f"has a matching operation -- likely renamed or removed upstream.",
                action=action,
            )
        )
    return findings


def _signature_drift_findings(
    domain: str,
    spec_actions: dict[str, dict],
    handled: set[str],
    client_sigs: dict[str, tuple],
) -> list[Finding]:
    """Operations whose (http, url_template, params, has_body) signature changed."""
    findings: list[Finding] = []
    for action in sorted(set(spec_actions) & handled):
        op = spec_actions[action]
        method = op["method"]
        if method not in client_sigs:
            continue
        if client_sigs[method] != _op_signature(op):
            findings.append(
                Finding(
                    "SIGNATURE DRIFT",
                    domain,
                    f"operation '{op['operation_id']}' (method {method}) "
                    f"parameters changed: code has {client_sigs[method]}, spec "
                    f"now has {_op_signature(op)}.",
                    action=action,
                )
            )
    return findings


def print_report(findings: list[Finding]) -> None:
    if not findings:
        print(
            "reconcile: OK -- no drift between the vendored spec and the committed "
            "source."
        )
        return
    by_kind: dict[str, int] = {}
    for f in findings:
        by_kind[f.kind] = by_kind.get(f.kind, 0) + 1
        print(str(f))
    print()
    print(
        "reconcile: DRIFT FOUND -- "
        + ", ".join(f"{n} {k}" for k, n in sorted(by_kind.items()))
    )


def scaffold(by_domain: dict[str, list[dict]]) -> None:
    """One-time bootstrap for a brand-new repo with no MCP module yet.

    Refuses outright if any mcp_<domain>.py already exists -- scaffold never
    overwrites hand-maintained code. Use the default reconcile mode (or
    --apply) on an established repo instead.
    """
    API_DIR.mkdir(exist_ok=True)
    MCP_DIR.mkdir(exist_ok=True)
    existing = [
        p
        for p in MCP_DIR.glob("mcp_*.py")
        if p.stem not in ("mcp_custom_api", "__init__")
        and p.read_text(errors="ignore").startswith(AUTOGEN)
    ]
    if existing:
        print(
            f"scaffold: refusing -- {len(existing)} mcp_*.py file(s) already exist "
            f"({', '.join(sorted(p.name for p in existing))}). scaffold is for a "
            f"brand-new repo only; use the default reconcile mode (or --apply) "
            f"instead."
        )
        raise SystemExit(1)

    for domain, ops in by_domain.items():
        emit_client_module(domain, ops)
        emit_mcp_module(domain, ops)
    emit_manifest(by_domain)
    emit_api_client(by_domain)
    emit_mcp_init(by_domain)
    tools = len(by_domain) + 1
    print(f"scaffold: generated {len(by_domain)} client modules, {tools} MCP tools.")


_DISPATCH_DEF_RE = re.compile(
    r"^def (_dispatch_(\w+)_(\d+))\(action, kwargs, client\):$"
)
_BRANCH_RE = re.compile(r'^\s*(?:if|elif) action == "([^"]+)":$')


def _parse_dispatch_helpers(lines: list[str], domain: str) -> list[dict]:
    """Return an ordered list of ``{name, start, end, branches}`` for each
    ``_dispatch_<domain>_<n>`` helper in ``lines`` (0-indexed; ``end`` is
    exclusive, one past the helper's ``return _UNHANDLED`` line)."""
    helpers = []
    i, n = 0, len(lines)
    while i < n:
        m = _DISPATCH_DEF_RE.match(lines[i])
        if m and m.group(2) == domain:
            start = i
            branch_count = 0
            j = i + 1
            while j < n and lines[j].strip() != "return _UNHANDLED":
                if _BRANCH_RE.match(lines[j]):
                    branch_count += 1
                j += 1
            end = j + 1
            helpers.append(
                {
                    "name": m.group(1),
                    "start": start,
                    "end": end,
                    "branches": branch_count,
                }
            )
            i = end
        else:
            i += 1
    return helpers


def _apply_domain(domain: str, ops: list[dict], missing_actions: set[str]) -> bool:
    """Additively insert handlers for ``missing_actions`` into
    ``mcp_<domain>.py`` and ``api_client_<domain>.py``. Never rewrites,
    reorders, or deletes an existing line -- only splices new lines in.
    Returns True if anything changed.
    """
    mcp_path = MCP_DIR / f"mcp_{domain}.py"
    client_path = API_DIR / f"api_client_{domain}.py"
    if not mcp_path.exists() or not client_path.exists():
        return False

    ops_by_action = {op["action"]: op for op in ops}
    new_ops = [ops_by_action[a] for a in sorted(missing_actions) if a in ops_by_action]
    if not new_ops:
        return False

    _append_client_methods(client_path, new_ops)
    _apply_mcp_domain(mcp_path, domain, new_ops)
    return True


def _append_client_methods(client_path: Path, new_ops: list[dict]) -> None:
    """api_client_<domain>.py -- append new methods at the end of the class."""
    client_lines = client_path.read_text().splitlines()
    insertion: list[str] = []
    for op in new_ops:
        insertion += _client_method_lines(op)
    while client_lines and client_lines[-1] == "":
        client_lines.pop()
    client_lines += [""] + insertion
    client_path.write_text("\n".join(client_lines) + "\n")


def _client_method_lines(op: dict) -> list[str]:
    """The generated method body lines for one new client operation."""
    doc = op["summary"].replace('"', "'")
    return [
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


def _apply_mcp_domain(mcp_path: Path, domain: str, new_ops: list[dict]) -> None:
    """mcp_<domain>.py -- fill spare dispatch capacity, add new helper(s),
    register them in the dispatcher tuple, and sync the action-description
    Field text."""
    mcp_lines = mcp_path.read_text().splitlines()
    helpers = _parse_dispatch_helpers(mcp_lines, domain)
    mcp_lines, remaining = _fill_spare_dispatch_capacity(
        mcp_lines, domain, helpers, new_ops
    )
    mcp_lines = _add_dispatch_helpers(mcp_lines, domain, remaining)
    mcp_lines = _sync_action_description(mcp_lines, new_ops)
    mcp_path.write_text("\n".join(mcp_lines) + "\n")


def _fill_spare_dispatch_capacity(
    mcp_lines: list[str], domain: str, helpers: list[dict], new_ops: list[dict]
) -> tuple[list[str], list[dict]]:
    """Fill the last dispatch helper's spare branch capacity (<=9 branches).

    Returns the (possibly updated) lines and whatever new ops didn't fit.
    """
    remaining = list(new_ops)
    if not (helpers and remaining):
        return mcp_lines, remaining
    last = helpers[-1]
    spare = _DISPATCH_GROUP_SIZE - last["branches"]
    if spare <= 0:
        return mcp_lines, remaining
    take, remaining = remaining[:spare], remaining[spare:]
    new_branch_lines: list[str] = []
    for op in take:
        new_branch_lines.append(f'    elif action == "{op["action"]}":')
        new_branch_lines.append(f"        return client.{op['method']}(**kwargs)")
    insert_at = last["end"] - 1  # the 'return _UNHANDLED' line itself
    mcp_lines = mcp_lines[:insert_at] + new_branch_lines + mcp_lines[insert_at:]
    return mcp_lines, remaining


def _add_dispatch_helpers(
    mcp_lines: list[str], domain: str, remaining: list[dict]
) -> list[str]:
    """Add new ``_dispatch_<domain>_<n>`` helper(s) for any remaining new ops,
    and register them in the domain's dispatcher tuple."""
    if not remaining:
        return mcp_lines
    helpers = _parse_dispatch_helpers(mcp_lines, domain)
    addition_lines, new_helper_names = _new_dispatch_helper_lines(
        domain, helpers, remaining
    )
    insert_at = (
        helpers[-1]["end"] if helpers else _first_dispatch_insert_point(mcp_lines)
    )
    mcp_lines = mcp_lines[:insert_at] + addition_lines + mcp_lines[insert_at:]
    return _register_dispatch_helpers(mcp_lines, domain, new_helper_names)


def _new_dispatch_helper_lines(
    domain: str, helpers: list[dict], remaining: list[dict]
) -> tuple[list[str], list[str]]:
    """Generate the source lines for enough new helpers to cover ``remaining``."""
    next_n = 0
    for h in helpers:
        m = re.match(rf"_dispatch_{re.escape(domain)}_(\d+)$", h["name"])
        if m:
            next_n = max(next_n, int(m.group(1)))
    addition_lines: list[str] = []
    new_helper_names: list[str] = []
    for group in _chunk(remaining, _DISPATCH_GROUP_SIZE):
        next_n += 1
        name = f"_dispatch_{domain}_{next_n}"
        new_helper_names.append(name)
        addition_lines += _dispatch_helper_block(name, group)
    return addition_lines, new_helper_names


def _dispatch_helper_block(name: str, group: list[dict]) -> list[str]:
    """The full source of one new ``_dispatch_<domain>_<n>`` helper function."""
    lines = [
        f"def {name}(action, kwargs, client):",
        f"    # {group[0]['action']} .. {group[-1]['action']} ({len(group)} actions)",
    ]
    for j, op in enumerate(group):
        kw = "if" if j == 0 else "elif"
        lines.append(f'    {kw} action == "{op["action"]}":')
        lines.append(f"        return client.{op['method']}(**kwargs)")
    lines.append("    return _UNHANDLED")
    lines.append("")
    lines.append("")
    return lines


def _first_dispatch_insert_point(mcp_lines: list[str]) -> int:
    """Where to insert the first-ever dispatch helper, just after ``_UNHANDLED``."""
    return (
        next(
            i
            for i, line in enumerate(mcp_lines)
            if line.strip() == "_UNHANDLED = object()"
        )
        + 3
    )


def _register_dispatch_helpers(
    mcp_lines: list[str], domain: str, new_helper_names: list[str]
) -> list[str]:
    """Splice new helper names into the domain's ``_<DOMAIN>_DISPATCHERS`` tuple."""
    if not new_helper_names:
        return mcp_lines
    dispatchers_var = f"_{domain.upper()}_DISPATCHERS"
    tuple_open = next(
        i
        for i, line in enumerate(mcp_lines)
        if line.strip() == f"{dispatchers_var} = ("
    )
    tuple_close = next(
        i for i in range(tuple_open + 1, len(mcp_lines)) if mcp_lines[i].strip() == ")"
    )
    return (
        mcp_lines[:tuple_close]
        + [f"    {name}," for name in new_helper_names]
        + mcp_lines[tuple_close:]
    )


def _sync_action_description(mcp_lines: list[str], new_ops: list[dict]) -> list[str]:
    """Keep the "Action to perform. One of: ..." Field description in sync --
    purely additive text appended before the closing quote."""
    i = _find_action_description_line(mcp_lines)
    if i is not None:
        mcp_lines[i] = _updated_action_description_line(mcp_lines[i], new_ops)
    return mcp_lines


def _find_action_description_line(mcp_lines: list[str]) -> int | None:
    """Index of the "Action to perform. One of: ..." Field description line."""
    for i, line in enumerate(mcp_lines):
        if 'description="Action to perform. One of:' in line:
            return i
    return None


def _updated_action_description_line(line: str, new_ops: list[dict]) -> str:
    """Append any newly-handled actions the line doesn't already list."""
    already_listed = set(re.findall(r"'([^']+)'", line))
    still_new = [op for op in new_ops if op["action"] not in already_listed]
    if not still_new:
        return line
    added = ", ".join(f"'{op['action']}'" for op in still_new)
    return line.rstrip()[:-1] + f', {added}"'


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reconcile (default, read-only) the vendored OpenAPI spec against "
            "the committed, hand-maintained MCP source; --scaffold bootstraps a "
            "brand-new repo once; --apply additively inserts new handlers only."
        )
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="One-time bootstrap for a brand-new repo with no MCP module yet. "
        "Refuses to touch anything that already exists.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Additively insert handlers for actions the spec has but the code "
        "doesn't. Never touches an existing line; renames, signature changes, "
        "and removals are reported for a human, never auto-applied.",
    )
    args = parser.parse_args()

    by_domain = collect_operations()

    if args.scaffold:
        scaffold(by_domain)
        return

    findings = reconcile(by_domain)

    if args.apply:
        findings = _apply_missing_handlers(by_domain, findings)

    print_report(findings)
    if findings:
        raise SystemExit(1)


def _apply_missing_handlers(
    by_domain: dict[str, list[dict]], findings: list[Finding]
) -> list[Finding]:
    """Additively apply every MISSING HANDLER finding, then re-reconcile."""
    missing_by_domain = _missing_actions_by_domain(findings)
    changed_any = False
    for domain, actions in missing_by_domain.items():
        if _apply_domain(domain, by_domain[domain], actions):
            changed_any = True
            print(f"apply: inserted {len(actions)} handler(s) into domain '{domain}'.")
    if changed_any:
        emit_manifest(by_domain)
        print("apply: regenerated _operation_manifest.py (pure derived data).")
    return reconcile(by_domain)


def _missing_actions_by_domain(findings: list[Finding]) -> dict[str, set[str]]:
    """Group MISSING HANDLER findings' actions by domain."""
    missing_by_domain: dict[str, set[str]] = {}
    for f in findings:
        if f.kind == "MISSING HANDLER" and f.action is not None:
            missing_by_domain.setdefault(f.domain, set()).add(f.action)
    return missing_by_domain


if __name__ == "__main__":
    main()
