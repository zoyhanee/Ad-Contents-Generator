import requests

import streamlit as st

from config import API_BASE_URL


DEFAULT_TIMEOUT = 10


class APIError(Exception):
    """API 요청 실패"""


def _get_error_message(response: requests.Response) -> str:
    try:
        return response.json().get("detail", "Unknown error")
    except ValueError:
        return response.text or "Unknown error"


def _get_headers() -> dict:
    access_token = st.session_state.get("access_token")

    if not access_token:
        return {}

    return {
        "Authorization": f"Bearer {access_token}",
    }


def _request(method: str, endpoint: str, **kwargs):
    response = requests.request(
        method=method,
        url=f"{API_BASE_URL}{endpoint}",
        headers=_get_headers(),
        timeout=DEFAULT_TIMEOUT,
        **kwargs,
    )

    if not response.ok:
        raise APIError(_get_error_message(response))

    return response.json()


def post(endpoint: str, **kwargs):
    return _request("POST", endpoint, **kwargs)


def get(endpoint: str):
    return _request("GET", endpoint)