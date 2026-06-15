"""Authentication factory tests."""

from onetrust_api.api_client import Api


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
