"""Brute-force execution coverage.

Exercises every generated client method and every MCP action router with a mocked
session / client, driving line coverage of the generated routing code to ~100%
and proving every operation is callable end-to-end (not merely present).
"""

import asyncio
import inspect
import re
from unittest.mock import AsyncMock, MagicMock

import pytest

from onetrust_api.api._operation_manifest import ACTIONS_BY_DOMAIN, OPERATIONS
from onetrust_api.api_client import Api


class _CaptureMCP:
    """Stand-in FastMCP that captures the registered tool callables."""

    def __init__(self):
        self.fns = []

    def tool(self, *args, **kwargs):
        def decorator(fn):
            self.fns.append(fn)
            return fn

        return decorator


def test_every_client_method_executes(mock_session):
    _ = mock_session
    api = Api(url="https://test.my.onetrust.com", token="test")
    for op in OPERATIONS:
        # Supply every path parameter this operation declares so the request builds.
        path_params = re.findall(r"\{([^}]+)\}", op["path"])
        kwargs = {p: "1" for p in path_params}
        kwargs.update({"page": 0, "size": 1, "body": {"name": "test"}})
        method = getattr(api, op["method"])
        result = method(**kwargs)
        assert result is not None


def test_every_mcp_action_routes():
    """Register each domain tool, then invoke every action against a mock client."""
    from onetrust_api import mcp as mcp_pkg

    mock_client = MagicMock(spec=Api)
    for domain, actions in ACTIONS_BY_DOMAIN.items():
        register = getattr(mcp_pkg, f"register_{domain}_tools")
        cap = _CaptureMCP()
        register(cap)
        assert len(cap.fns) == 1
        fn = cap.fns[0]
        ctx = AsyncMock()  # exercise the progress-reporting branch
        for action in actions:
            asyncio.run(
                fn(action=action, params_json="{}", client=mock_client, ctx=ctx)
            )
        # Unknown action raises.
        with pytest.raises(ValueError):
            asyncio.run(
                fn(action="__nope__", params_json="{}", client=mock_client, ctx=None)
            )
        # Invalid JSON returns an error dict, not an exception.
        bad = asyncio.run(
            fn(action=actions[0], params_json="{not json", client=mock_client, ctx=None)
        )
        assert isinstance(bad, dict) and "error" in bad
        # Non-object JSON is rejected.
        non_obj = asyncio.run(
            fn(action=actions[0], params_json="[1,2]", client=mock_client, ctx=None)
        )
        assert isinstance(non_obj, dict) and "error" in non_obj


def test_custom_api_tool_executes():
    from onetrust_api.mcp.mcp_custom_api import register_custom_api_tools

    mock_client = MagicMock(spec=Api)
    cap = _CaptureMCP()
    register_custom_api_tools(cap)
    fn = cap.fns[0]
    asyncio.run(
        fn(
            method="GET",
            endpoint="/api/incident/v1/incidents",
            params_json='{"params": {"page": 0}}',
            client=mock_client,
            ctx=None,
        )
    )
    mock_client.api_request.assert_called_once()


def test_mcp_action_signatures_consistent():
    """Every generated tool has the action/params_json/client/ctx contract."""
    from onetrust_api import mcp as mcp_pkg

    for domain in ACTIONS_BY_DOMAIN:
        register = getattr(mcp_pkg, f"register_{domain}_tools")
        cap = _CaptureMCP()
        register(cap)
        sig = inspect.signature(cap.fns[0])
        assert {"action", "params_json", "client", "ctx"} <= set(sig.parameters)
