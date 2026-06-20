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

import threading

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

local = threading.local()
from onetrust_api.api_client import Api

logger = get_logger(__name__)


def get_client(
    instance: str | None = None,
    token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    region: str | None = None,
    consent_url: str | None = None,
    worker_url: str | None = None,
    verify: bool | None = None,
    config: dict | None = None,
) -> Api:
    """Factory function to create the OneTrust :class:`Api` client.

    Credentials resolve live through the shared config layer (the one XDG
    ``config.json`` / env), read at call time rather than frozen at import.
    Supports OIDC delegation, a fixed bearer token, and the OAuth2
    client-credentials flow via the shared ``delegated_auth`` helper.
    """
    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        get_user_identity,
        is_delegation_enabled,
    )

    instance = instance if instance is not None else setting("ONETRUST_URL")
    token = token if token is not None else setting("ONETRUST_TOKEN")
    client_id = client_id if client_id is not None else setting("ONETRUST_CLIENT_ID")
    client_secret = (
        client_secret
        if client_secret is not None
        else setting("ONETRUST_CLIENT_SECRET")
    )
    region = region if region is not None else setting("ONETRUST_REGION", "us")
    consent_url = (
        consent_url if consent_url is not None else setting("ONETRUST_CONSENT_URL")
    )
    worker_url = (
        worker_url if worker_url is not None else setting("ONETRUST_WORKER_URL")
    )
    verify = verify if verify is not None else setting("ONETRUST_SSL_VERIFY", True)

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
