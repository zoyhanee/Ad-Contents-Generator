from app.core.config import settings
from app.ml.image_clients.base import ImageModelClient
from app.ml.image_clients.openai_client import OpenAIImageClient
from app.ml.image_clients.qwen_client import QwenImageClient


def create_image_model_client() -> ImageModelClient:
    provider = settings.IMAGE_MODEL_PROVIDER.lower()

    if provider == "openai":
        return OpenAIImageClient(
            model_name=settings.IMAGE_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
        )

    if provider == "qwen":
        return QwenImageClient(
            model_name=settings.IMAGE_MODEL_NAME,
        )

    raise ValueError(
        f"Unsupported image model provider: {provider}"
    )