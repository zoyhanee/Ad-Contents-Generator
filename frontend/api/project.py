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


def finalize_project(
    project_id: int,
    draft_id: str,
    post_copy: str | None = None,
) -> dict:
    return post(
        f"/projects/{project_id}/finalize",
        json={
            "draft_id": draft_id,
            "post_copy": post_copy,
        },
    )