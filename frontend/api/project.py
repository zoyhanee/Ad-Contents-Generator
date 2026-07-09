from api.client import post


def create_project(
    product_id: int,
) -> dict:
    return post(
        "/projects",
        json={
            "product_id": product_id,
        },
    )