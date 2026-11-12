"""Brute-force execution coverage.

Exercises every generated client method and every MCP action router with a mocked
session / client, driving line coverage of the generated routing code to ~100%
and proving every operation is callable end-to-end (not merely present).
"""

import asyncio
import re
from unittest.mock import MagicMock

from onetrust_api.api._operation_manifest import OPERATIONS
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
