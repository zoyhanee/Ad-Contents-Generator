from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    PROJECT_NAME: str = "Ad Contents Generator API"
    VERSION: str = "1.0.0"

    TEXT_MODEL_PROVIDER: str = "openai"
    TEXT_MODEL_NAME: str = "gpt-5-mini"

    IMAGE_MODEL_PROVIDER: str = "openai"
    IMAGE_MODEL_NAME: str = "gpt-image-1.5"

    OPENAI_API_KEY: str

    #Prompt_Version
    PROMPT_VERSION: str = "v1"

    # Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    FRONTEND_BASE_URL: str = "http://localhost:8501"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
