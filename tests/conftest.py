import json
from unittest.mock import patch

import pytest
import requests

reason = "Unit tests using mocks"


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv("ONETRUST_URL", "https://test.my.onetrust.com")
    monkeypatch.setenv("ONETRUST_TOKEN", "mock_token")
    monkeypatch.delenv("ENABLE_DELEGATION", raising=False)


def _make_response(payload=None, status=200):
    # A real requests.Response — the Response model validates isinstance.
    resp = requests.Response()
    resp.status_code = status
    body = payload if payload is not None else {"id": 1, "name": "test", "content": []}
    resp._content = json.dumps(body).encode()
    resp.headers["Content-Type"] = "application/json"
    resp.headers["X-Total-Pages"] = "1"
    return resp


@pytest.fixture(autouse=True)
def mock_session():
    """Patch requests.Session so the client never touches the network."""
    with patch("requests.Session") as mock_cls:
        session = mock_cls.return_value
        resp = _make_response()
        session.request.return_value = resp
        session.get.return_value = resp
        session.post.return_value = resp
        session.put.return_value = resp
        session.delete.return_value = resp
        session.patch.return_value = resp
        yield session
