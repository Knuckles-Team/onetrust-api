#!/usr/bin/python
"""Shared models for the OneTrust API client.

The OneTrust surface spans 35 OpenAPI specifications and ~600 operations. Rather
than generate hundreds of brittle per-schema Pydantic models, the client passes
request/response payloads through as plain ``dict``/``list`` and wraps every
result in :class:`Response` — a thin wrapper (mirroring the fleet convention used
by ``gitlab-api``/``servicenow-api``) that exposes the parsed JSON alongside the
original ``requests.Response`` metadata (status code, headers).
"""

from typing import Generic, TypeVar

import requests
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """Wrapper holding the parsed JSON payload plus the original HTTP response.

    Provides access to response metadata (``status_code``, ``headers``) while
    exposing the decoded JSON body via ``data``.
    """

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    base_type: str | None = Field(default="Response")
    response: requests.Response = Field(  # type: ignore[assignment]
        default=None,
        description="The original requests.Response object",
        exclude=True,
    )
    data: T | list[T] | None = Field(
        default=None, description="The decoded JSON body of the response"
    )

    @property
    def status_code(self) -> int | None:
        return self.response.status_code if self.response is not None else None

    @property
    def headers(self) -> dict | None:
        return dict(self.response.headers) if self.response is not None else None
