"""Characterization tests for ``OneTrustApiBase`` — the shared HTTP client base.

Covers the branches the existing suite never exercised directly: the OAuth2
client-credentials exchange (success / rejection / malformed response), offset and
cursor pagination traversal across multiple pages, host-literal remapping for the
consent/worker service hosts, and how ``_call`` builds a request body from leftover
kwargs. These pin behaviour ahead of decomposing ``__init__`` / ``_ensure_token`` /
``_fetch_all_pages`` / ``_call`` into smaller helpers.
"""

import json

import pytest
import requests
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from onetrust_api.api.api_client_base import OneTrustApiBase


def _response(payload=None, status=200, headers=None):
    resp = requests.Response()
    resp.status_code = status
    resp._content = json.dumps(payload if payload is not None else {}).encode()
    resp.headers["Content-Type"] = "application/json"
    if headers:
        resp.headers.update(headers)
    return resp


def _client_credentials_client(mock_session):
    client = OneTrustApiBase(
        url="https://acme.my.onetrust.com",
        client_id="cid",
        client_secret="secret",
    )
    return client


def test_client_credentials_exchange_returns_bearer_token(mock_session):
    client = _client_credentials_client(mock_session)
    mock_session.post.return_value = _response(
        {"access_token": "brand-new-token", "expires_in": 3600}
    )
    token = client._ensure_token()
    assert token == "brand-new-token"
    assert client._token_expiry > 0
    mock_session.post.assert_called_once()
    _, kwargs = mock_session.post.call_args
    assert kwargs["url"] == "https://acme.my.onetrust.com/api/access/v1/oauth/token"
    assert kwargs["data"] == {"grant_type": "client_credentials"}


def test_client_credentials_accepts_token_field_fallback(mock_session):
    client = _client_credentials_client(mock_session)
    mock_session.post.return_value = _response({"token": "legacy-field-token"})
    assert client._ensure_token() == "legacy-field-token"


def test_client_credentials_rejects_on_401(mock_session):
    client = _client_credentials_client(mock_session)
    mock_session.post.return_value = _response({}, status=401)
    with pytest.raises(UnauthorizedError):
        client._ensure_token()


def test_client_credentials_raises_when_access_token_missing(mock_session):
    client = _client_credentials_client(mock_session)
    mock_session.post.return_value = _response({"expires_in": 3600})
    with pytest.raises(AuthError):
        client._ensure_token()


def test_client_credentials_raises_on_non_ok_status(mock_session):
    client = _client_credentials_client(mock_session)
    mock_session.post.return_value = _response({"error": "boom"}, status=500)
    with pytest.raises(AuthError):
        client._ensure_token()


def test_fixed_token_short_circuits_the_exchange(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="fixed-token")
    assert client._ensure_token() == "fixed-token"
    mock_session.post.assert_not_called()


def test_offset_pagination_collects_all_pages(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    pages = [
        _response({"content": [1, 2], "page": {"totalPages": 3}}),
        _response({"content": [3, 4], "page": {"totalPages": 3}}),
        _response({"content": [5], "page": {"totalPages": 3}}),
    ]
    mock_session.request.side_effect = pages
    first, all_data = client._fetch_all_pages(
        "GET", "https://acme.my.onetrust.com/x", {}, "offset", 0
    )
    assert first is pages[0]
    assert all_data == [1, 2, 3, 4, 5]
    assert mock_session.request.call_count == 3


def test_offset_pagination_respects_max_pages(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    pages = [
        _response({"content": [1], "page": {"totalPages": 5}}),
        _response({"content": [2], "page": {"totalPages": 5}}),
    ]
    mock_session.request.side_effect = pages
    _, all_data = client._fetch_all_pages(
        "GET", "https://acme.my.onetrust.com/x", {}, "offset", 2
    )
    assert all_data == [1, 2]
    assert mock_session.request.call_count == 2


def test_cursor_pagination_collects_all_pages(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    pages = [
        _response({"content": [1], "continuationToken": "tok-2"}),
        _response({"content": [2], "continuationToken": "tok-3"}),
        _response({"content": [3]}),  # no cursor → stop
    ]
    mock_session.request.side_effect = pages
    first, all_data = client._fetch_all_pages(
        "GET", "https://acme.my.onetrust.com/x", {}, "cursor", 10
    )
    assert first is pages[0]
    assert all_data == [1, 2, 3]
    assert mock_session.request.call_count == 3


def test_non_paginated_style_returns_only_the_first_page(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    mock_session.request.return_value = _response({"content": [1, 2]})
    _, all_data = client._fetch_all_pages(
        "GET", "https://acme.my.onetrust.com/x", {}, "none", 0
    )
    assert all_data == [1, 2]
    assert mock_session.request.call_count == 1


def test_host_map_remaps_consent_and_worker_hosts(mock_session):
    client = OneTrustApiBase(
        url="https://acme.my.onetrust.com",
        token="tok",
        consent_url="https://consent.acme.example/",
        worker_url="https://worker.acme.example",
    )
    assert client._host_map["privacyportal.onetrust.com"] == "consent.acme.example"
    assert client._host_map["consent-api.onetrust.com"] == "consent.acme.example"
    assert client._host_map["localhost:8080"] == "worker.acme.example"
    assert client._host_map["__HOSTNAME__"] == "acme.my.onetrust.com"


def test_host_map_omits_optional_hosts_when_not_configured(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    assert "privacyportal.onetrust.com" not in client._host_map
    assert "localhost:8080" not in client._host_map


def test_call_folds_unknown_kwargs_into_body_when_body_missing(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    mock_session.request.return_value = _response({"ok": True})
    client._call(
        "POST",
        "https://acme.my.onetrust.com/x",
        path_params=[],
        query_params=[],
        has_body=True,
        paginate="none",
        kwargs={"name": "widget"},
    )
    _, kwargs = mock_session.request.call_args
    assert kwargs["json"] == {"name": "widget"}
    assert kwargs["params"] is None


def test_call_prefers_explicit_body_kwarg(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    mock_session.request.return_value = _response({"ok": True})
    client._call(
        "POST",
        "https://acme.my.onetrust.com/x",
        path_params=[],
        query_params=[],
        has_body=True,
        paginate="none",
        kwargs={"body": {"id": 1}, "extra": "ignored-as-body-present"},
    )
    _, kwargs = mock_session.request.call_args
    assert kwargs["json"] == {"id": 1}


def test_call_without_body_folds_leftover_into_query_params(mock_session):
    client = OneTrustApiBase(url="https://acme.my.onetrust.com", token="tok")
    mock_session.request.return_value = _response({"ok": True})
    client._call(
        "GET",
        "https://acme.my.onetrust.com/x",
        path_params=[],
        query_params=[],
        has_body=False,
        paginate="none",
        kwargs={"filter": "active"},
    )
    _, kwargs = mock_session.request.call_args
    assert kwargs["params"] == {"filter": "active"}
    assert kwargs["json"] is None
