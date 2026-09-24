"""Authentication factory tests."""

import pytest
from agent_connector_sdk.exceptions import AuthError

from onetrust_api.api_client import Api


def test_get_client_uses_delegated_token_when_enabled(monkeypatch):
    """Delegation path: get_delegated_token's return becomes the client's bearer token."""
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")

    import agent_utilities.mcp.delegated_auth as delegated_auth

    monkeypatch.setattr(
        delegated_auth, "get_delegated_token", lambda **kwargs: "delegated-tok"
    )

    from onetrust_api.auth import get_client

    client = get_client(config={"enable_delegation": True})
    assert isinstance(client, Api)
    assert client._token == "delegated-tok"


def test_get_client_wraps_delegation_failure_as_runtime_error(monkeypatch):
    monkeypatch.setenv("ONETRUST_URL", "https://acme.my.onetrust.com")

    import agent_utilities.mcp.delegated_auth as delegated_auth

    def _boom(**kwargs):
        raise ValueError("no token exchange available")

    monkeypatch.setattr(delegated_auth, "get_delegated_token", _boom)

    from onetrust_api.auth import get_client

    with pytest.raises(RuntimeError, match="Token exchange failed"):
        get_client(config={"enable_delegation": True})


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
