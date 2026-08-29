"""Characterization tests for scripts/generate_from_openapi.py.

This is an author-time developer tool with no prior test coverage. These tests
pin behaviour for the functions decomposed in this pass: ``normalize_params``,
``collect_operations``, ``_extract_client_signatures``, ``reconcile``, and
``_apply_domain`` (plus ``main``'s ``--apply``/``--scaffold`` orchestration).
Fixtures for reconcile/_apply_domain reuse the generator's own ``emit_client_module``
/ ``emit_mcp_module`` so the synthetic files have exactly the real generated shape.
"""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "generate_from_openapi.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("generate_from_openapi", _MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def gen(tmp_path, monkeypatch):
    """A fresh module instance with SPECS_DIR/API_DIR/MCP_DIR pointed at tmp_path."""
    module = _load_module()
    specs_dir = tmp_path / "specs"
    api_dir = tmp_path / "api"
    mcp_dir = tmp_path / "mcp"
    specs_dir.mkdir()
    api_dir.mkdir()
    mcp_dir.mkdir()
    monkeypatch.setattr(module, "SPECS_DIR", specs_dir)
    monkeypatch.setattr(module, "API_DIR", api_dir)
    monkeypatch.setattr(module, "MCP_DIR", mcp_dir)
    return module


def _op(action="do_thing", method="do_thing", http="GET", url="https://x/{id}",
        path_params=("id",), query_params=(), has_body=False, paginate="none",
        summary="Do the thing.", domain="widgets"):
    return {
        "operation_id": action,
        "method": method,
        "action": action,
        "domain": domain,
        "http": http,
        "url_template": url,
        "path_params": list(path_params),
        "query_params": list(query_params),
        "has_body": has_body,
        "paginate": paginate,
        "summary": summary,
        "params": [],
    }


# --------------------------------------------------------------- normalize_params


def test_normalize_params_dedupes_path_and_query(gen):
    params = [
        {"name": "id", "in": "path", "schema": {"type": "string"}},
        {"name": "id", "in": "path", "schema": {"type": "string"}},  # dupe, dropped
        {"name": "size", "in": "query", "schema": {"type": "integer"}},
        {"name": "unused", "in": "header", "schema": {"type": "string"}},  # not path/query
    ]
    out = gen.normalize_params(params, {}, {})
    names = [p["name"] for p in out]
    assert names == ["id", "size"]
    assert out[0]["required"] is True  # path params are always required
    assert out[1]["type"] == "integer"


def test_normalize_params_expands_request_body_properties(gen):
    op = {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "properties": {
                            "name": {"type": "string"},
                            "count": {"type": "integer"},
                        },
                        "required": ["name"],
                    }
                }
            }
        }
    }
    out = gen.normalize_params([], op, {})
    by_name = {p["name"]: p for p in out}
    assert by_name["name"]["required"] is True
    assert by_name["count"]["required"] is False


def test_normalize_params_falls_back_to_opaque_body(gen):
    op = {
        "requestBody": {
            "required": True,
            "content": {"application/json": {"schema": {}}},
        }
    }
    out = gen.normalize_params([], op, {})
    assert out == [
        {
            "name": "body",
            "type": "object",
            "required": True,
            "description": "Request body (JSON object).",
        }
    ]


def test_normalize_params_request_body_property_shadowed_by_path_param_is_skipped(gen):
    params = [{"name": "id", "in": "path", "schema": {"type": "string"}}]
    op = {
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {"properties": {"id": {"type": "string"}}}
                }
            }
        }
    }
    out = gen.normalize_params(params, op, {})
    assert len(out) == 1  # "id" from path wins; body's "id" is a dupe, skipped


# ------------------------------------------------------------- collect_operations


def _write_spec(specs_dir, stem, paths, servers=None):
    spec = {
        "servers": servers or [{"url": "https://{hostname}", "variables": {"hostname": {}}}],
        "paths": paths,
    }
    (specs_dir / f"{stem}.json").write_text(json.dumps(spec))


def test_collect_operations_builds_domain_with_synthetic_and_declared_ids(gen):
    _write_spec(
        gen.SPECS_DIR,
        "custom-widgets",
        {
            "/widgets/{id}": {
                "get": {
                    "operationId": "getWidget",
                    "parameters": [{"name": "id", "in": "path", "schema": {"type": "string"}}],
                },
                "post": {},  # no operationId -> synthesized
            }
        },
    )
    by_domain = gen.collect_operations()
    assert set(by_domain) == {"custom_widgets"}
    ops = {op["action"]: op for op in by_domain["custom_widgets"]}
    assert "get_widget" in ops
    assert ops["get_widget"]["path_params"] == ["id"]
    assert ops["get_widget"]["url_template"] == "https://__HOSTNAME__/widgets/{id}"
    # the synthesized POST id follows the http_path pattern
    assert any(a.startswith("post_widgets_id") for a in ops)


def test_collect_operations_dedupes_colliding_method_and_action_names(gen):
    _write_spec(
        gen.SPECS_DIR,
        "custom-widgets",
        {
            "/a": {"get": {"operationId": "doThing"}},
            "/b": {"get": {"operationId": "doThing"}},
        },
    )
    by_domain = gen.collect_operations()
    actions = [op["action"] for op in by_domain["custom_widgets"]]
    methods = [op["method"] for op in by_domain["custom_widgets"]]
    assert actions == ["do_thing", "do_thing_x"]
    assert methods == ["do_thing", "do_thing_x"]


def test_collect_operations_detects_offset_pagination(gen):
    _write_spec(
        gen.SPECS_DIR,
        "custom-widgets",
        {
            "/widgets": {
                "get": {
                    "operationId": "listWidgets",
                    "parameters": [
                        {"name": "page", "in": "query", "schema": {"type": "integer"}},
                        {"name": "size", "in": "query", "schema": {"type": "integer"}},
                    ],
                }
            }
        },
    )
    by_domain = gen.collect_operations()
    (op,) = by_domain["custom_widgets"]
    assert op["paginate"] == "offset"


# ------------------------------------------------------- _extract_client_signatures


def test_extract_client_signatures_reads_self_call_kwargs(gen):
    src = '''
class OneTrustWidgets:
    def get_widget(self, **kwargs) -> Response:
        """Get a widget."""
        return self._call(
            http='GET',
            url_template='__HOSTNAME__/widgets/{id}',
            path_params=['id'],
            query_params=[],
            has_body=False,
            paginate='none',
            kwargs=kwargs,
        )

    def not_a_call_method(self, **kwargs):
        return 42
'''
    sigs = gen._extract_client_signatures(src)
    assert set(sigs) == {"get_widget"}
    http, url, path_params, query_params, has_body = sigs["get_widget"]
    assert (http, url, path_params, query_params, has_body) == (
        "GET",
        "__HOSTNAME__/widgets/{id}",
        ("id",),
        (),
        False,
    )


def test_extract_client_signatures_skips_malformed_call(gen):
    src = '''
class OneTrustWidgets:
    def broken(self, **kwargs):
        return self._call(http='GET')
'''
    assert gen._extract_client_signatures(src) == {}


# ------------------------------------------------------------------------ reconcile


def test_reconcile_reports_new_domain_when_no_mcp_module_exists(gen):
    by_domain = {"widgets": [_op()]}
    findings = gen.reconcile(by_domain)
    assert [f.kind for f in findings] == ["NEW DOMAIN"]
    assert findings[0].domain == "widgets"


def test_reconcile_reports_orphaned_domain_when_spec_no_longer_has_it(gen):
    gen.emit_client_module("widgets", [_op()])
    gen.emit_mcp_module("widgets", [_op()])
    findings = gen.reconcile({})
    assert [f.kind for f in findings] == ["ORPHANED DOMAIN"]


def test_reconcile_reports_missing_and_orphaned_handlers(gen):
    original = [_op(action="get_widget", method="get_widget")]
    gen.emit_client_module("widgets", original)
    gen.emit_mcp_module("widgets", original)

    # spec now has a different action; get_widget disappeared, add_widget appeared
    by_domain = {"widgets": [_op(action="add_widget", method="add_widget", http="POST")]}
    findings = gen.reconcile(by_domain)
    kinds = {f.kind: f.action for f in findings}
    assert kinds["MISSING HANDLER"] == "add_widget"
    assert kinds["ORPHANED HANDLER"] == "get_widget"


def test_reconcile_reports_signature_drift(gen):
    original = [_op(action="get_widget", method="get_widget", url="__HOSTNAME__/widgets/{id}")]
    gen.emit_client_module("widgets", original)
    gen.emit_mcp_module("widgets", original)

    drifted = [_op(action="get_widget", method="get_widget", url="__HOSTNAME__/v2/widgets/{id}")]
    findings = gen.reconcile({"widgets": drifted})
    assert [f.kind for f in findings] == ["SIGNATURE DRIFT"]


def test_reconcile_is_clean_when_nothing_changed(gen):
    ops = [_op()]
    gen.emit_client_module("widgets", ops)
    gen.emit_mcp_module("widgets", ops)
    assert gen.reconcile({"widgets": ops}) == []


# --------------------------------------------------------------------- _apply_domain


def test_apply_domain_inserts_new_handler_and_client_method(gen):
    original = [_op(action="get_widget", method="get_widget")]
    gen.emit_client_module("widgets", original)
    gen.emit_mcp_module("widgets", original)

    new_op = _op(action="delete_widget", method="delete_widget", http="DELETE")
    all_ops = original + [new_op]
    changed = gen._apply_domain("widgets", all_ops, {"delete_widget"})
    assert changed is True

    client_src = (gen.API_DIR / "api_client_widgets.py").read_text()
    assert "def delete_widget(self, **kwargs) -> Response:" in client_src

    mcp_src = (gen.MCP_DIR / "mcp_widgets.py").read_text()
    assert 'action == "delete_widget"' in mcp_src
    assert "'delete_widget'" in mcp_src  # action description Field text updated

    # reconciling again with the full op list now reports nothing missing
    findings = gen.reconcile({"widgets": all_ops})
    assert [f.kind for f in findings] == []


def test_apply_domain_adds_new_dispatch_helper_when_group_is_full(gen):
    # exactly _DISPATCH_GROUP_SIZE branches fills the sole existing helper
    original = [
        _op(action=f"op_{i}", method=f"op_{i}") for i in range(gen._DISPATCH_GROUP_SIZE)
    ]
    gen.emit_client_module("widgets", original)
    gen.emit_mcp_module("widgets", original)

    new_op = _op(action="one_more", method="one_more")
    all_ops = original + [new_op]
    assert gen._apply_domain("widgets", all_ops, {"one_more"}) is True

    mcp_src = (gen.MCP_DIR / "mcp_widgets.py").read_text()
    assert "_dispatch_widgets_2" in mcp_src
    assert 'action == "one_more"' in mcp_src
    assert gen.reconcile({"widgets": all_ops}) == []


def test_apply_domain_returns_false_when_module_missing(gen):
    assert gen._apply_domain("nope", [_op()], {"do_thing"}) is False


def test_apply_domain_returns_false_when_no_missing_actions_matched(gen):
    ops = [_op()]
    gen.emit_client_module("widgets", ops)
    gen.emit_mcp_module("widgets", ops)
    assert gen._apply_domain("widgets", ops, {"nonexistent_action"}) is False


# ------------------------------------------------------------------------------ main


def test_main_exits_nonzero_when_findings_exist(gen, monkeypatch, capsys):
    monkeypatch.setattr(gen, "collect_operations", lambda: {"widgets": [_op()]})
    monkeypatch.setattr(sys, "argv", ["generate_from_openapi.py"])
    with pytest.raises(SystemExit) as exc:
        gen.main()
    assert exc.value.code == 1


def test_main_exits_cleanly_when_no_findings(gen, monkeypatch):
    monkeypatch.setattr(gen, "collect_operations", lambda: {})
    monkeypatch.setattr(sys, "argv", ["generate_from_openapi.py"])
    gen.main()  # no SystemExit


def test_main_apply_inserts_missing_handlers_then_reports_clean(gen, monkeypatch):
    original = [_op(action="get_widget", method="get_widget")]
    gen.emit_client_module("widgets", original)
    gen.emit_mcp_module("widgets", original)
    all_ops = original + [_op(action="delete_widget", method="delete_widget", http="DELETE")]

    monkeypatch.setattr(gen, "collect_operations", lambda: {"widgets": all_ops})
    monkeypatch.setattr(sys, "argv", ["generate_from_openapi.py", "--apply"])
    gen.main()  # applies the missing handler, re-reconciles clean, no SystemExit

    client_src = (gen.API_DIR / "api_client_widgets.py").read_text()
    assert "def delete_widget(self, **kwargs) -> Response:" in client_src


def test_main_scaffold_calls_scaffold_and_returns(gen, monkeypatch):
    calls = []
    monkeypatch.setattr(gen, "collect_operations", lambda: {"widgets": [_op()]})
    monkeypatch.setattr(gen, "scaffold", lambda by_domain: calls.append(by_domain))
    monkeypatch.setattr(sys, "argv", ["generate_from_openapi.py", "--scaffold"])
    gen.main()
    assert len(calls) == 1
