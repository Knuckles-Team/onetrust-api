"""OneTrust API client layer.

``api_client_base`` holds the hand-authored HTTP/auth/pagination machinery; the
``api_client_<domain>`` modules are generated from the vendored OpenAPI specs by
``scripts/generate_from_openapi.py`` and composed into the single ``Api`` class in
``onetrust_api.api_client``.
"""
