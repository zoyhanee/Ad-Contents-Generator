from api.client import APIError, get, post


def signup(
    email: str,
    password: str,
    store_name: str,
) -> dict:

    return post(
        "/auth/signup",
        json={
            "email": email,
            "password": password,
            "store_name": store_name,
        },
    )


def login(
    email: str,
    password: str,
) -> dict:

    return post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def get_google_login_url() -> str:
    response = get("/auth/google/login-url")

    return response["login_url"]


def get_me() -> dict:
    return get("/auth/me")


AuthAPIError = APIError
