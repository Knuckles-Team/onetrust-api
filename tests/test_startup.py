"""Import / boot smoke tests."""


def test_package_imports():
    import onetrust_api

    assert hasattr(onetrust_api, "Api")
    assert onetrust_api._MCP_AVAILABLE is True
    assert onetrust_api._AGENT_AVAILABLE is True


def test_api_composes_all_domains():
    from onetrust_api.api._operation_manifest import DOMAINS
    from onetrust_api.api_client import Api

    # One base class per domain plus the shared base and Api itself.
    assert len(DOMAINS) == 35
    assert callable(getattr(Api, "api_request"))


def test_client_constructs_with_token():
    from onetrust_api.api_client import Api

    api = Api(url="https://acme.my.onetrust.com", token="x")
    assert api.url == "https://acme.my.onetrust.com"


def test_client_requires_credentials():
    import pytest
    from agent_utilities.core.exceptions import MissingParameterError

    from onetrust_api.api_client import Api

    with pytest.raises(MissingParameterError):
        Api(url="https://acme.my.onetrust.com")
