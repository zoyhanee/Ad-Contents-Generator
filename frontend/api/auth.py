from api.client import APIError, post


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


AuthAPIError = APIError