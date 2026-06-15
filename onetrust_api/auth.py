"""OneTrust Authentication Module.

Authentication priority:

1. **OIDC Delegation** — If ``ENABLE_DELEGATION`` is active, exchanges the
   IdP-issued user token for a downstream OneTrust access token via RFC 8693
   Token Exchange using the shared ``delegated_auth`` helper.
2. **Fixed Credentials** — Falls back to a pre-minted bearer token
   (``ONETRUST_TOKEN``) or an OAuth2 client-credentials pair
   (``ONETRUST_CLIENT_ID`` / ``ONETRUST_CLIENT_SECRET``).

See ``docs/guides/oauth_sso.md`` in agent-utilities for full details.
"""

import os
import threading

from agent_utilities.base_utilities import get_logger, to_boolean
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

local = threading.local()
from onetrust_api.api_client import Api

logger = get_logger(__name__)


def get_client(
    instance: str | None = os.getenv("ONETRUST_URL", None),
    token: str | None = os.getenv("ONETRUST_TOKEN", None),
    client_id: str | None = os.getenv("ONETRUST_CLIENT_ID", None),
    client_secret: str | None = os.getenv("ONETRUST_CLIENT_SECRET", None),
    region: str = os.getenv("ONETRUST_REGION", "us"),
    consent_url: str | None = os.getenv("ONETRUST_CONSENT_URL", None),
    worker_url: str | None = os.getenv("ONETRUST_WORKER_URL", None),
    verify: bool = to_boolean(string=os.getenv("ONETRUST_SSL_VERIFY", "True")),
    config: dict | None = None,
) -> Api:
    """Factory function to create the OneTrust :class:`Api` client.

    Supports OIDC delegation, a fixed bearer token, and the OAuth2
    client-credentials flow. Uses the shared ``delegated_auth`` helper from
    agent-utilities.
    """
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    common = dict(
        region=region,
        consent_url=consent_url,
        worker_url=worker_url,
        verify=verify,
    )

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if is_delegation_enabled(config):
        try:
            delegated_token = get_delegated_token(
                config=config,
                audience=(config or {}).get("audience", instance or region),
                scopes=(config or {}).get("delegated_scopes", "api"),
                verify=verify,
            )
            identity = get_user_identity()
            logger.info(
                "Using OIDC delegated token for OneTrust API",
                extra={"user_email": identity.get("email"), "instance": instance},
            )
            return Api(url=instance, token=delegated_token, **common)
        except Exception as e:
            logger.error(
                "OIDC delegation failed for OneTrust",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            raise RuntimeError(f"Token exchange failed: {str(e)}") from e

    # --- Path 2: Fixed Credentials (token or client-credentials) ---
    logger.info("Using fixed credentials for OneTrust API")
    try:
        return Api(
            url=instance,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            **common,
        )
    except (AuthError, UnauthorizedError) as e:
        raise RuntimeError(
            "AUTHENTICATION ERROR: The OneTrust credentials provided are not valid. "
            "Check ONETRUST_URL/ONETRUST_REGION and ONETRUST_TOKEN (or "
            "ONETRUST_CLIENT_ID/ONETRUST_CLIENT_SECRET). "
            f"Error details: {str(e)}"
        ) from e
