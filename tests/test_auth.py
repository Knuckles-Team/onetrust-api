"""Authentication factory tests."""

import pytest
from agent_connector_sdk.exceptions import AuthError

from onetrust_api.api_client import Api

_DELEGATION_SETTINGS_ENV = {
    "ENABLE_DELEGATION": "true",
    "OIDC_TOKEN_URL": "https://idp.example.invalid/token",
    "OIDC_CLIENT_ID": "onetrust-connector",
    "OIDC_CLIENT_SECRET_REF": "env://TEST_ONETRUST_OIDC_SECRET_UNUSED",
    "AUDIENCE": "https://onetrust.example.invalid",
}


def _set_delegation_settings_env(monkeypatch) -> None:
    for key, value in _DELEGATION_SETTINGS_ENV.items():
        monkeypatch.setenv(key, value)


def test_get_client_uses_delegated_token_when_enabled(monkeypatch):
    """Delegation path: exchange_token's return becomes the client's bearer token."""
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")
    _set_delegation_settings_env(monkeypatch)

    import agent_connector_sdk.auth.delegation as delegation
    from agent_connector_sdk.auth.tokens import AccessToken

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")
    monkeypatch.setattr(
        delegation,
        "exchange_token",
        lambda settings, *, subject_token, http_client, resolver=None: AccessToken(
            value="delegated-tok", ttl_seconds=3600, expires_at=0.0
        ),
    )

    from onetrust_api.auth import get_client

    client = get_client()
    assert isinstance(client, Api)
    assert client._token == "delegated-tok"


def test_get_client_wraps_delegation_failure_as_runtime_error(monkeypatch):
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")
    _set_delegation_settings_env(monkeypatch)

    import agent_connector_sdk.auth.delegation as delegation

    monkeypatch.setattr(delegation, "current_user_token", lambda: "caller-token")

    def _boom(settings, *, subject_token, http_client, resolver=None):
        raise ValueError("no token exchange available")

    monkeypatch.setattr(delegation, "exchange_token", _boom)

    from onetrust_api.auth import get_client

    with pytest.raises(RuntimeError, match="Token exchange failed"):
        get_client()


def test_get_client_wraps_bad_fixed_credentials_as_runtime_error(monkeypatch):
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")
    monkeypatch.setenv("ONETRUST_TOKEN", "tok")

    def _raise_auth_error(*args, **kwargs):
        raise AuthError("simulated invalid credentials")

    import onetrust_api.auth as auth_module

    monkeypatch.setattr(auth_module, "Api", _raise_auth_error)

    with pytest.raises(RuntimeError, match="AUTHENTICATION ERROR"):
        auth_module.get_client()


def test_get_client_token_path(monkeypatch):
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")
    monkeypatch.setenv("ONETRUST_TOKEN", "tok")
    from onetrust_api.auth import get_client

    client = get_client()
    assert isinstance(client, Api)


def test_get_client_client_credentials(monkeypatch):
    monkeypatch.delenv("ONETRUST_TOKEN", raising=False)
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")
    monkeypatch.setenv("ONETRUST_CLIENT_ID", "cid")
    monkeypatch.setenv("ONETRUST_CLIENT_SECRET", "secret")
    from onetrust_api.auth import get_client

    client = get_client()
    assert isinstance(client, Api)


def test_region_resolution():
    api = Api(region="eu", token="x")
    assert api.url == "https://app-eu.onetrust.com"


def test_url_overrides_region():
    api = Api(url="https://acme.my.onetrust.com", region="eu", token="x")
    assert api.hostname == "acme.my.onetrust.com"
