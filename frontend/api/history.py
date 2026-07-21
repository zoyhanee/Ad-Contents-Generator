from api.client import get, patch


def get_history() -> list[dict]:
    return get("/history")


def get_history_detail(
    project_id: int,
) -> dict:
    return get(
        f"/history/{project_id}"
    )


def update_history(
    project_id: int,
    post_copy: str | None = None,
    image_feedback: str | None = None,
) -> dict:
    return patch(
        f"/history/{project_id}",
        json={
            "post_copy": post_copy,
            "image_feedback": image_feedback,
        },
    )