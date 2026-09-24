#!/usr/bin/python
"""Base HTTP client for the OneTrust API.

Handles the cross-cutting concerns shared by every generated domain client:

* **Authentication** — a pre-minted OAuth2 bearer token (``ONETRUST_TOKEN``) or an
  OAuth2 *client-credentials* exchange (``ONETRUST_CLIENT_ID`` /
  ``ONETRUST_CLIENT_SECRET``) against ``/api/access/v1/oauth/token``, with
  automatic refresh before expiry.
* **Multi-region / multi-service hosts** — OneTrust serves different micro-services
  from different hosts (the tenant pod, the consent privacy-portal, on-prem worker
  nodes). Each generated method carries the absolute URL template declared by its
  OpenAPI spec; this base resolves ``{hostname}`` and known service-host literals
  against the configured environment.
* **Pagination** — both OneTrust styles: offset (``page``/``size``/``sort`` with
  ``page.totalPages`` in the body) and cursor (continuation tokens).
* **Rate limiting / transient errors** — honours ``429`` ``Retry-After`` and retries
  ``429``/``502``/``503``/``504`` with bounded exponential backoff.
"""

import logging
import threading
import time
from typing import Any, TypeVar

import requests
from agent_connector_sdk.utilities import get_logger
from agent_connector_sdk.exceptions import (
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile
from pydantic import ValidationError

from onetrust_api.onetrust_models import Response

logger = get_logger(__name__)

T = TypeVar("T")

# Regional tenant hosts (the "app" pod). ``ONETRUST_URL`` overrides outright.
REGION_HOSTS = {
    "us": "app.onetrust.com",
    "ae": "app-ae.onetrust.com",
    "apac": "app-apac.onetrust.com",
    "au": "app-au.onetrust.com",
    "br": "app-br.onetrust.com",
    "ca": "app-ca.onetrust.com",
    "ch": "app-ch.onetrust.com",
    "de": "app-de.onetrust.com",
    "eu": "app-eu.onetrust.com",
    "fr": "app-fr.onetrust.com",
    "in": "app-in.onetrust.com",
    "jp": "app-jp.onetrust.com",
    "uk": "app-uk.onetrust.com",
    "trial": "trial.onetrust.com",
    "uat": "uat.onetrust.com",
}

# Continuation-token field names OneTrust uses across its cursor-paginated APIs.
_CURSOR_KEYS = (
    "requestContinuation",
    "continuationToken",
    "nextPageToken",
    "bookmark",
    "pageId",
)


class OneTrustApiBase:
    def __init__(
        self,
        url: str | None = None,
        token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        region: str = "us",
        consent_url: str | None = None,
        worker_url: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
        max_retries: int = 3,
        debug: bool = False,
    ):
        logger.setLevel(logging.DEBUG if debug else logging.ERROR)

        self.tls_profile = tls_profile or resolve_tls_profile("onetrust")
        self.debug = debug
        self.max_retries = max_retries
        self._session = self.tls_profile.configure_requests_session(requests.Session())
        self._token_lock = threading.Lock()
        self._token = token
        self._token_expiry = 0.0
        self._client_id = client_id
        self._client_secret = client_secret

        self.hostname = self._resolve_tenant_host(url, region)
        self.url = f"https://{self.hostname}"
        self._host_map = self._build_host_map(self.hostname, consent_url, worker_url)

        if not self._token and not (self._client_id and self._client_secret):
            raise MissingParameterError(
                "Provide ONETRUST_TOKEN, or ONETRUST_CLIENT_ID and "
                "ONETRUST_CLIENT_SECRET for the client-credentials flow."
            )

    @staticmethod
    def _resolve_tenant_host(url: str | None, region: str) -> str:
        """Resolve the primary tenant host from an explicit URL or a region code."""
        host = (url or REGION_HOSTS.get(region, REGION_HOSTS["us"])).strip()
        return host.replace("https://", "").replace("http://", "").rstrip("/")

    @staticmethod
    def _build_host_map(
        hostname: str, consent_url: str | None, worker_url: str | None
    ) -> dict[str, str]:
        """Map spec host literals (and the ``__HOSTNAME__`` sentinel) to configured hosts.

        Default behaviour keeps the spec host except the tenant-pod placeholder, which
        always routes to the configured tenant host. The ``{hostname}`` spec variable is
        emitted by the generator as the ``__HOSTNAME__`` sentinel.
        """
        host_map = {
            "__HOSTNAME__": hostname,
            "customer.my.onetrust.com": hostname,
        }
        consent_host = (consent_url or "").replace("https://", "").rstrip("/")
        worker_host = (worker_url or "").replace("https://", "").rstrip("/")
        if consent_host:
            host_map["privacyportal.onetrust.com"] = consent_host
            host_map["consent-api.onetrust.com"] = consent_host
        if worker_host:
            host_map["localhost:8080"] = worker_host
        return host_map

    # ------------------------------------------------------------------ auth
    def _ensure_token(self) -> str:
        """Return a valid bearer token, refreshing via client-credentials if needed."""
        if self._token_is_fresh():
            return self._token
        with self._token_lock:
            if self._token_is_fresh():
                return self._token
            token, expires_in = self._exchange_client_credentials()
            self._token = token
            # Refresh 60s before the stated expiry.
            self._token_expiry = time.monotonic() + expires_in - 60
            return self._token

    def _token_is_fresh(self) -> bool:
        """True if the cached bearer token can be used without a refresh."""
        return bool(self._token) and (
            not self._client_id or time.monotonic() < self._token_expiry
        )

    def _exchange_client_credentials(self) -> tuple[str, int]:
        """Perform the OAuth2 client-credentials exchange and return (token, expires_in)."""
        token_url = f"{self.url}/api/access/v1/oauth/token"
        try:
            resp = self._session.post(
                url=token_url,
                data={"grant_type": "client_credentials"},
                auth=(self._client_id or "", self._client_secret or ""),
                headers={"Accept": "application/json"},
                timeout=30,
            )
        except requests.RequestException as e:
            raise AuthError(f"OneTrust token request failed: {type(e).__name__}") from e
        if resp.status_code in (401, 403):
            raise UnauthorizedError(
                f"OneTrust client-credentials rejected ({resp.status_code})."
            )
        if not resp.ok:
            raise AuthError(
                f"OneTrust token endpoint returned {resp.status_code}: {resp.text}"
            )
        payload = resp.json()
        token = payload.get("access_token") or payload.get("token")
        if not token:
            raise AuthError("OneTrust token response contained no access_token.")
        return token, int(payload.get("expires_in", 3600))

    def _auth_headers(self, content_type: str | None = "application/json") -> dict:
        headers = {
            "Authorization": f"Bearer {self._ensure_token()}",
            "Accept": "application/json",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    # --------------------------------------------------------------- url build
    def _resolve_url(self, url_template: str, path_kwargs: dict) -> str:
        """Resolve a spec URL template into an absolute URL.

        Substitutes the ``__HOSTNAME__`` sentinel and known service-host literals,
        then interpolates any remaining ``{param}`` path parameters by name.
        """
        url = url_template
        for literal, override in self._host_map.items():
            if literal in url:
                url = url.replace(literal, override)
        for key, value in (path_kwargs or {}).items():
            url = url.replace("{" + key + "}", str(value))
        if "{" in url:
            missing = url[url.index("{") + 1 : url.index("}")] if "}" in url else "?"
            raise MissingParameterError(f"Missing required path parameter: {missing}")
        return url

    # ----------------------------------------------------------------- request
    def _request(
        self,
        method: str,
        url: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
        headers: dict | None = None,
    ) -> requests.Response:
        """Perform an HTTP request with rate-limit / transient-error retries."""
        request_headers = headers or self._auth_headers()
        attempt = 0
        while True:
            response = self._session.request(
                method=method.upper(),
                url=url,
                params=params or None,
                json=json,
                data=data,
                headers=request_headers,
                timeout=60,
            )
            if response.status_code == 429 and attempt < self.max_retries:
                delay = self._retry_delay(response, attempt)
                logger.debug("Rate limited (429); sleeping %.1fs", delay)
                time.sleep(delay)
                attempt += 1
                continue
            if response.status_code in (502, 503, 504) and attempt < self.max_retries:
                time.sleep(self._retry_delay(response, attempt))
                attempt += 1
                continue
            if response.status_code in (401, 403):
                raise (AuthError if response.status_code == 401 else UnauthorizedError)(
                    f"OneTrust request failed ({response.status_code})."
                )
            return response

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self._session.close()
        self.tls_profile.cleanup()

    @staticmethod
    def _retry_delay(response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(float(retry_after), 60.0)
            except ValueError:
                pass
        return min(2.0**attempt, 30.0)

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        if not response.content:
            return None
        if "application/json" in response.headers.get("Content-Type", ""):
            try:
                return response.json()
            except ValueError:
                return response.text
        return response.text

    # -------------------------------------------------------------- pagination
    def _fetch_all_pages(
        self, method: str, url: str, params: dict, paginate: str, max_pages: int
    ) -> tuple[requests.Response, list]:
        """Collect every page of a paginated collection (offset or cursor)."""
        params = dict(params or {})
        first = self._request(method, url, params=params)
        all_data = list(self._extract_items(self._decode(first)))
        max_pages = max_pages if max_pages and max_pages > 0 else 10

        if paginate == "offset":
            all_data.extend(
                self._fetch_offset_pages(method, url, params, first, max_pages)
            )
        elif paginate == "cursor":
            all_data.extend(
                self._fetch_cursor_pages(method, url, params, first, max_pages)
            )
        return first, all_data

    def _fetch_offset_pages(
        self,
        method: str,
        url: str,
        params: dict,
        first: requests.Response,
        max_pages: int,
    ) -> list:
        """Collect pages 2..N of an offset-paginated (``page``/``size``) collection."""
        body = self._decode(first) or {}
        total_pages = self._total_pages(body)
        page = int(params.get("page", 0))
        collected: list = []
        while page + 1 < min(total_pages, max_pages):
            page += 1
            params["page"] = page
            resp = self._request(method, url, params=params)
            collected.extend(self._extract_items(self._decode(resp)))
        return collected

    def _fetch_cursor_pages(
        self,
        method: str,
        url: str,
        params: dict,
        first: requests.Response,
        max_pages: int,
    ) -> list:
        """Collect pages 2..N of a cursor/continuation-token-paginated collection."""
        cursor = self._extract_cursor(self._decode(first))
        fetched = 1
        collected: list = []
        while cursor and fetched < max_pages:
            for key in _CURSOR_KEYS:
                if key in params or cursor:
                    params[key] = cursor
                    break
            resp = self._request(method, url, params=params)
            body = self._decode(resp)
            collected.extend(self._extract_items(body))
            cursor = self._extract_cursor(body)
            fetched += 1
        return collected

    @staticmethod
    def _extract_items(body: Any) -> list:
        if isinstance(body, list):
            return body
        if isinstance(body, dict):
            for key in ("content", "data", "items", "results", "records"):
                if isinstance(body.get(key), list):
                    return body[key]
        return []

    @staticmethod
    def _total_pages(body: dict) -> int:
        page = body.get("page") if isinstance(body.get("page"), dict) else body
        for key in ("totalPages", "total_pages"):
            if isinstance(page, dict) and key in page:
                return int(page[key] or 1)
            if key in body:
                return int(body[key] or 1)
        return 1

    @staticmethod
    def _extract_cursor(body: Any) -> str | None:
        if not isinstance(body, dict):
            return None
        for key in _CURSOR_KEYS:
            if body.get(key):
                return body[key]
        return None

    # ----------------------------------------------------------- generated call
    def _call(
        self,
        http: str,
        url_template: str,
        path_params: list[str],
        query_params: list[str],
        has_body: bool,
        paginate: str,
        kwargs: dict,
    ) -> Response:
        """Dispatch a single generated operation. Used by every domain method."""
        try:
            url, params, body = self._prepare_call(
                url_template, path_params, query_params, has_body, kwargs
            )

            if http.upper() == "GET" and paginate in ("offset", "cursor"):
                max_pages = int(params.pop("max_pages", 0) or 0)
                response, data = self._fetch_all_pages(
                    http, url, params, paginate, max_pages
                )
                return Response(response=response, data=data)

            params.pop("max_pages", None)
            response = self._request(http, url, params=params, json=body)
            return Response(response=response, data=self._decode(response))
        except (AuthError, UnauthorizedError, MissingParameterError):
            raise
        except ValidationError as e:
            raise ParameterError(f"Invalid parameters: {e.errors()}") from e
        except requests.RequestException as e:
            logger.error("Operation failed: error_type=%s", type(e).__name__)
            raise

    def _prepare_call(
        self,
        url_template: str,
        path_params: list[str],
        query_params: list[str],
        has_body: bool,
        kwargs: dict,
    ) -> tuple[str, dict, Any]:
        """Split raw call kwargs into the resolved URL, query params, and request body."""
        kwargs = {k: v for k, v in (kwargs or {}).items() if v is not None}
        path_kwargs = {k: kwargs.pop(k) for k in path_params if k in kwargs}
        url = self._resolve_url(url_template, path_kwargs)

        params = {k: kwargs.pop(k) for k in query_params if k in kwargs}
        body, leftover = self._extract_body(has_body, kwargs)
        # Remaining kwargs (unknown to the spec) fold into query params.
        params.update(leftover)
        return url, params, body

    @staticmethod
    def _extract_body(has_body: bool, kwargs: dict) -> tuple[Any, dict]:
        """Split the request body out of leftover kwargs.

        Anything left that isn't a query/path param is the request body. Returns the
        body plus whatever leftover kwargs should fold into query params instead.
        """
        if not has_body:
            return None, kwargs
        body = kwargs.pop("body", None)
        if body is None and kwargs:
            return kwargs, {}
        return body, kwargs

    # --------------------------------------------------------------- escape hatch
    def api_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> Response:
        """Make an arbitrary OneTrust REST request against the configured tenant host.

        ``endpoint`` is a path (e.g. ``/api/incident/v1/incidents``) appended to the
        tenant base URL. Use this for operations not covered by a typed method.
        """
        if method.upper() not in ("GET", "POST", "PUT", "DELETE", "PATCH"):
            raise ValueError(f"Unsupported HTTP method: {method.upper()}")
        url = f"{self.url}/{endpoint.lstrip('/')}"
        response = self._request(method, url, params=params, json=json, data=data)
        return Response(response=response, data=self._decode(response))
