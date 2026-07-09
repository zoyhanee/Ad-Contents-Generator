import requests

from api.client import APIError, post
from config import API_BASE_URL


def generate_ad(
    *,
    project_id: int,
    selected_slogan: str,
) -> dict:
    return post(
        "/generate",
        json={
            "project_id": project_id,
            "selected_slogan": selected_slogan,
        },
    )


def regenerate_draft(
    *,
    project_id: int,
    draft_id: str,
    feedback: str,
) -> dict:
    return post(
        "/generate/regenerate",
        json={
            "project_id": project_id,
            "draft_id": draft_id,
            "feedback": feedback,
        },
    )


def download_generated_image(
    image_path: str,
) -> bytes:
    try:
        response = requests.get(
            f"{API_BASE_URL}/{image_path}",
            timeout=30,
        )
    except requests.RequestException as e:
        raise APIError(
            "결과 이미지를 다운로드할 수 없습니다."
        ) from e

    if not response.ok:
        raise APIError(
            "결과 이미지를 다운로드할 수 없습니다."
        )

    return response.content