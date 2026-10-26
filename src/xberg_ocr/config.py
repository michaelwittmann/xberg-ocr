"""Configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    ollama_base_url: str = "http://localhost:11434"
    ollama_api_key: str | None = None
    vlm_model: str = "glm-ocr:latest"
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
