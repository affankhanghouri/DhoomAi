from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        extra="ignore",
    )

    SUPABASE_URL: str = Field(
        default="",
        validation_alias=AliasChoices("SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_URL"),
    )
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    FRONTEND_URL: str = "http://localhost:3000"

    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-5.5-mini"
    OPENAI_IMAGE_MODEL: str = "gpt-image-1"
    OPENAI_IMAGE_SIZE: str = "1024x1024"
    OPENAI_IMAGE_QUALITY: str = "high"
    GENERATED_ASSETS_BUCKET: str = "generated-assets"


settings = Settings()
