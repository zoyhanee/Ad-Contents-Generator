import base64
from openai import OpenAI

from app.core.config import settings

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def generate_image(prompt: str, size: str = "1024x1024", quality: str = "high") -> bytes:
    client = _get_client()
    response = client.images.generate(
        model=settings.IMAGE_MODEL_NAME,
        prompt=prompt,
        size=size,
        quality=quality,
    )
    return base64.b64decode(response.data[0].b64_json)


def generate_transparent_prop(prompt: str, size: str = "1024x1024", quality: str = "high") -> bytes:
    client = _get_client()
    full_prompt = (
        f"{prompt}. Professional product photography of only this single object, "
        f"isolated on a fully transparent background, no shadow, no surface, no other objects."
    )
    response = client.images.generate(
        model=settings.IMAGE_MODEL_NAME,
        prompt=full_prompt,
        size=size,
        quality=quality,
        background="transparent",
    )
    return base64.b64decode(response.data[0].b64_json)


def edit_image_region(
    image_path: str,
    mask_path: str,
    instruction: str,
    size: str = "1024x1024",
) -> bytes:

    client = _get_client()
    with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
        response = client.images.edit(
            model=settings.IMAGE_MODEL_NAME,
            image=image_file,
            mask=mask_file,
            prompt=instruction,
            size=size,
        )
    return base64.b64decode(response.data[0].b64_json)

