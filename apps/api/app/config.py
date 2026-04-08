"""Application configuration using Pydantic Settings."""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "TalentMatch AI API"
    debug: bool = False
    version: str = "1.0.0"

    # CORS - Configure via env var BACKEND_CORS_ORIGINS as comma-separated list
    backend_cors_origins: List[str] = ["http://localhost:3000"]
    
    def model_post_init(self, __context):
        """Parse CORS origins from environment variable if provided."""
        import os
        cors_env = os.getenv("BACKEND_CORS_ORIGINS")
        if cors_env:
            self.backend_cors_origins = [origin.strip() for origin in cors_env.split(",")]

    # Database
    database_url: str = "sqlite+aiosqlite:///./talentmatch.db"

    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_embedding_model: str = "nomic-embed-text"
    ollama_llm_model: str = "llama3.2:3b"
    ollama_timeout: int = 120

    # Processing Limits
    max_file_size_mb: int = 10
    max_cv_pages: int = 10
    chunk_size: int = 512
    chunk_overlap: int = 50

    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024


# Global settings instance
settings = Settings()
