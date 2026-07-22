import requests

from api.client import APIError, post
from config import API_BASE_URL


def normalize_generated_image_path(
    image_path: str | None,
) -> str | None:
    if not image_path:
        return None

    return image_path.replace("\\", "/").lstrip("/")


def generate_ad(
    project_id: int,
    selected_slogan: str,
    image_width: int,
    image_height: int,
) -> dict:
    return post(
        "/generate",
        timeout=900,
        json={
            "project_id": project_id,
            "selected_slogan": selected_slogan,
            "image_width": image_width,
            "image_height": image_height,
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
        timeout=300,
        json={
            "project_id": project_id,
            "draft_id": draft_id,
            "feedback": feedback,
        },
    )


def download_generated_image(
    image_path: str,
) -> bytes:
    normalized_image_path = normalize_generated_image_path(image_path)

    try:
        response = requests.get(
            f"{API_BASE_URL}/{normalized_image_path}",
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
