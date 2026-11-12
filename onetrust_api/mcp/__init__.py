"""Non-operation MCP tools of the OneTrust connector.

Every API operation is served as its own typed tool by the SDK from the operation
manifest, so only the generic request tool lives here.
"""

from onetrust_api.mcp.mcp_custom_api import register_custom_api_tools

__all__ = ["register_custom_api_tools"]
