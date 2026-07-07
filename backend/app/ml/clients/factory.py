from app.core.config import settings
from app.ml.clients.base import TextModelClient
from app.ml.clients.openai_client import OpenAITextClient


def create_text_model_client() -> TextModelClient:
    provider = settings.TEXT_MODEL_PROVIDER.lower()

    if provider == "openai":
        return OpenAITextClient(
            model_name=settings.TEXT_MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
        )

    raise ValueError(
        f"Unsupported text model provider: {provider}"
    )