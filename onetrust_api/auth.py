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
from dataclasses import dataclass
from typing import Any

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

local = threading.local()
from onetrust_api.api_client import Api

logger = get_logger(__name__)


@dataclass
class _ClientOverrides:
    """Raw ``get_client()`` overrides, unresolved against the settings layer."""

    instance: str | None
    token: str | None
    client_id: str | None
    client_secret: str | None
    region: str | None
    consent_url: str | None
    worker_url: str | None
    tls_profile: ResolvedTLSProfile | None


def _resolve_client_config(overrides: _ClientOverrides) -> dict[str, Any]:
    """Resolve each override live through the shared config layer.

    Credentials resolve at call time (not frozen at import) from the one XDG
    ``config.json`` / env — an explicit override always wins over the setting.
    """
    return {
        "instance": (
            overrides.instance
            if overrides.instance is not None
            else setting("ONETRUST_URL")
        ),
        "token": (
            overrides.token
            if overrides.token is not None
            else setting("ONETRUST_TOKEN")
        ),
        "client_id": (
            overrides.client_id
            if overrides.client_id is not None
            else setting("ONETRUST_CLIENT_ID")
        ),
        "client_secret": (
            overrides.client_secret
            if overrides.client_secret is not None
            else setting("ONETRUST_CLIENT_SECRET")
        ),
        "region": (
            overrides.region
            if overrides.region is not None
            else setting("ONETRUST_REGION", "us")
        ),
        "consent_url": (
            overrides.consent_url
            if overrides.consent_url is not None
            else setting("ONETRUST_CONSENT_URL")
        ),
        "worker_url": (
            overrides.worker_url
            if overrides.worker_url is not None
            else setting("ONETRUST_WORKER_URL")
        ),
        "tls_profile": overrides.tls_profile
        or resolve_configured_tls_profile("onetrust"),
    }


def _delegated_client(
    instance: str | None, region: str | None, config: dict | None, common: dict
) -> Api:
    """Path 1: OIDC Delegation (RFC 8693 Token Exchange)."""
    from agent_utilities.mcp.delegated_auth import get_delegated_token

    try:
        delegated_token = get_delegated_token(
            config=config,
            audience=(config or {}).get("audience", instance or region),
            scopes=(config or {}).get("delegated_scopes", "api"),
        )
        logger.info("Using OIDC delegated token for OneTrust API")
        return Api(url=instance, token=delegated_token, **common)
    except Exception as e:
        logger.error(
            "OIDC delegation failed for OneTrust",
            extra={
                "error_type": type(e).__name__,
                "error_message": type(e).__name__,
            },
        )
        raise RuntimeError(f"Token exchange failed: {type(e).__name__}") from e


def _fixed_credentials_client(
    instance: str | None,
    token: str | None,
    client_id: str | None,
    client_secret: str | None,
    common: dict,
) -> Api:
    """Path 2: Fixed Credentials (token or client-credentials)."""
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
            f"Error details: {type(e).__name__}"
        ) from e


def get_client(
    instance: str | None = None,
    token: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    region: str | None = None,
    consent_url: str | None = None,
    worker_url: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict | None = None,
) -> Api:
    """Factory function to create the OneTrust :class:`Api` client.

    Credentials resolve live through the shared config layer (the one XDG
    ``config.json`` / env), read at call time rather than frozen at import.
    Supports OIDC delegation, a fixed bearer token, and the OAuth2
    client-credentials flow via the shared ``delegated_auth`` helper.
    """
    from agent_utilities.mcp.delegated_auth import is_delegation_enabled

    resolved = _resolve_client_config(
        _ClientOverrides(
            instance=instance,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            region=region,
            consent_url=consent_url,
            worker_url=worker_url,
            tls_profile=tls_profile,
        )
    )
    common = dict(
        region=resolved["region"],
        consent_url=resolved["consent_url"],
        worker_url=resolved["worker_url"],
        tls_profile=resolved["tls_profile"],
    )

    if is_delegation_enabled(config):
        return _delegated_client(
            resolved["instance"], resolved["region"], config, common
        )

    return _fixed_credentials_client(
        resolved["instance"],
        resolved["token"],
        resolved["client_id"],
        resolved["client_secret"],
        common,
    )
