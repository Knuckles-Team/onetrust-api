#!/usr/bin/python
# coding: utf-8

import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agent_utilities.exceptions import AuthError, UnauthorizedError

# TODO: Import your API wrapper class here
# from onetrust_api.api_client import OnetrustApiClient

_client = None


def get_client():
    """Get or create a singleton API client instance."""
    global _client
    if _client is None:
        base_url = os.getenv("ONETRUST_URL", "http://localhost:8080")
        token = os.getenv("ONETRUST_TOKEN", "")
        verify = os.getenv("ONETRUST_API_VERIFY", "True").lower() in ("true", "1", "yes")

        try:
            # TODO: Uncomment and configure once the API wrapper class is created
            # _client = OnetrustApiClient(
            #     base_url=base_url,
            #     token=token,
            #     verify=verify,
            # )

            # Placeholder until API wrapper is implemented
            if _client is None:
                session = requests.Session()
                session.headers.update({"Authorization": f"Bearer {token}"})
                session.verify = verify
                _client = type("Client", (), {"session": session, "base_url": base_url})()
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
                f"Please check your ONETRUST_TOKEN and ONETRUST_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    return _client
