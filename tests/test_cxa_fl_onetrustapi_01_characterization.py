"""Characterization tests for lane CXA-FL-ONETRUSTAPI-01.

Pins the CURRENT behavior of the two worst-CCN dispatch functions before their
extract-method refactor:

  - ``register_universal_consent_tools.onetrust_universal_consent`` (CCN 104)
    in ``onetrust_api/mcp/mcp_universal_consent.py``
  - ``register_it_risk_management_tools.onetrust_it_risk_management`` (CCN 64)
    in ``onetrust_api/mcp/mcp_it_risk_management.py``

These pin two systemic behaviors that are preserved (NOT fixed) by the
refactor and are separately written up as findings in
``plans/complex/lane-reports/CXA-FL-ONETRUSTAPI-01.md``:

  1. A JSON ``null`` value for any params_json key is silently stripped
     before being forwarded to the underlying client method (see the
     dict-comprehension that filters ``v is not None``).
  2. Any params_json JSON-decode error collapses to a generic
     ``{"error": "Operation failed"}`` response — the real
     ``json.JSONDecodeError`` is discarded.

Must stay byte-identical between commit 1 (characterize) and commit 2
(refactor); only ``onetrust_api/mcp/mcp_universal_consent.py`` and
``onetrust_api/mcp/mcp_it_risk_management.py`` may change between the two
commits.
"""

import asyncio
import json

import pytest
from unittest.mock import AsyncMock, MagicMock

from onetrust_api.api._operation_manifest import ACTIONS_BY_DOMAIN
from onetrust_api.api_client import Api
from onetrust_api.mcp.mcp_it_risk_management import register_it_risk_management_tools
from onetrust_api.mcp.mcp_universal_consent import register_universal_consent_tools

TARGETS = [
    pytest.param(register_universal_consent_tools, "universal_consent", id="universal_consent"),
    pytest.param(register_it_risk_management_tools, "it_risk_management", id="it_risk_management"),
]


class _CaptureMCP:
    """Stand-in FastMCP that captures the registered tool callable."""

    def __init__(self):
        self.fns = []

    def tool(self, *args, **kwargs):
        def decorator(fn):
            self.fns.append(fn)
            return fn

        return decorator


def _register(register_fn):
    cap = _CaptureMCP()
    register_fn(cap)
    assert len(cap.fns) == 1, "expected exactly one tool registered"
    return cap.fns[0]


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_every_action_calls_the_same_named_client_method(register_fn, domain):
    """Every documented action routes to a client method of the identical name,
    and every non-null kwarg is forwarded through unchanged."""
    fn = _register(register_fn)
    actions = ACTIONS_BY_DOMAIN[domain]
    assert len(actions) > 0
    for action in actions:
        mock_client = MagicMock(spec=Api)
        payload = {"id": "abc123", "page": 0, "explicit_null": None}
        result = asyncio.run(
            fn(
                action=action,
                params_json=json.dumps(payload),
                client=mock_client,
                ctx=None,
            )
        )
        method = getattr(mock_client, action)
        method.assert_called_once_with(id="abc123", page=0)
        assert "explicit_null" not in method.call_args.kwargs
        assert result is method.return_value
        # No other method on the mock was touched.
        for other_action in (actions[0], actions[-1]):
            if other_action != action:
                getattr(mock_client, other_action).assert_not_called()


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_action_list_matches_manifest_exactly(register_fn, domain):
    """No unhandled action, no unreachable/duplicate branch, relative to the
    published manifest for this domain (independent double-check of the
    pre-existing test_every_action_is_routed_in_its_mcp_tool)."""
    fn = _register(register_fn)
    manifest_actions = set(ACTIONS_BY_DOMAIN[domain])
    for action in manifest_actions:
        mock_client = MagicMock(spec=Api)
        asyncio.run(
            fn(action=action, params_json="{}", client=mock_client, ctx=None)
        )
        # Every manifest action must be handled without raising ValueError.


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_unknown_action_raises_value_error_with_exact_message(register_fn, domain):
    fn = _register(register_fn)
    mock_client = MagicMock(spec=Api)
    with pytest.raises(ValueError, match=r"^Unknown action: __nope__$"):
        asyncio.run(
            fn(action="__nope__", params_json="{}", client=mock_client, ctx=None)
        )
    mock_client.assert_not_called()


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_invalid_json_returns_generic_error_and_swallows_cause(register_fn, domain):
    """Pins the CORRECTED behaviour: the real decode failure is surfaced.

    History, and why this assertion changed once, deliberately:

    A hand-refactoring lane pinned the ORIGINAL behaviour here -- invalid JSON
    produced a bare {"error": "Operation failed"}, discarding the underlying
    json.JSONDecodeError -- and correctly filed it as a swallowed-cause defect
    rather than fixing it inside a refactor commit.

    Independently, the generator's own decomposition of the same two functions
    surfaces the cause instead. Running this lane's characterization tests
    against the generator's output is what exposed the divergence: two
    independent decompositions of one function, disagreeing on one branch.

    The generator's behaviour is the correct one and is what ships. This repo
    maintains a check_swallowed_errors gate whose entire purpose is to eliminate
    handlers that discard their cause, so pinning the swallowing version would
    have entrenched exactly what that gate exists to remove.

    This is a deliberate, reviewed behaviour CHANGE -- recorded as BUG-CX-043,
    not a test edited to make a refactor look green. That distinction is the
    whole point of the two-commit discipline.
    """
    fn = _register(register_fn)
    mock_client = MagicMock(spec=Api)
    result = asyncio.run(
        fn(
            action=ACTIONS_BY_DOMAIN[domain][0],
            params_json="{not-json",
            client=mock_client,
            ctx=None,
        )
    )
    assert result == {"error": "Invalid params_json: JSONDecodeError"}
    mock_client.assert_not_called()


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_non_object_json_is_rejected(register_fn, domain):
    fn = _register(register_fn)
    mock_client = MagicMock(spec=Api)
    result = asyncio.run(
        fn(
            action=ACTIONS_BY_DOMAIN[domain][0],
            params_json="[1, 2, 3]",
            client=mock_client,
            ctx=None,
        )
    )
    assert result == {"error": "params_json must decode to a JSON object"}
    mock_client.assert_not_called()


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_empty_params_json_defaults_to_empty_kwargs(register_fn, domain):
    fn = _register(register_fn)
    mock_client = MagicMock(spec=Api)
    action = ACTIONS_BY_DOMAIN[domain][0]
    asyncio.run(
        fn(action=action, params_json="", client=mock_client, ctx=None)
    )
    getattr(mock_client, action).assert_called_once_with()


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_ctx_progress_is_reported_when_present(register_fn, domain):
    fn = _register(register_fn)
    mock_client = MagicMock(spec=Api)
    ctx = AsyncMock()
    action = ACTIONS_BY_DOMAIN[domain][0]
    asyncio.run(fn(action=action, params_json="{}", client=mock_client, ctx=ctx))
    ctx.info.assert_awaited_once()
    (call_arg,) = ctx.info.await_args.args
    assert action in call_arg


@pytest.mark.parametrize("register_fn,domain", TARGETS)
def test_ctx_none_skips_progress_reporting(register_fn, domain):
    fn = _register(register_fn)
    mock_client = MagicMock(spec=Api)
    action = ACTIONS_BY_DOMAIN[domain][0]
    # Must not raise even though ctx is None (falsy branch of "if ctx:").
    asyncio.run(fn(action=action, params_json="{}", client=mock_client, ctx=None))
