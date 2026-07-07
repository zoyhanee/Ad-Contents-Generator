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

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()