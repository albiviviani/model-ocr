"""Application settings and environment configuration for the local OCR microservice."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration values for the OCR microservice."""

    app_name: str = "Local OCR Service"
    cors_origins: list[str] = ["http://localhost:8000"]
    api_prefix: str = "/api"
    host: str = "0.0.0.0"
    port: int = 8000
    ocr_language: str = "eng"
    tesseract_cmd: str | None = None
    pdf_dpi: int = 300

    model_config = {
        "env_prefix": "",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
