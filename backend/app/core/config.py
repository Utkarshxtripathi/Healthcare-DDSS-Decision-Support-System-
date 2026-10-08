"""
Application Configuration
CSIR Healthcare Clinical Decision Support System (CDSS/DDSS)
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "CSIR Healthcare CDSS / DDSS"
    VERSION: str = "1.0.0-poc"
    API_V1_STR: str = "/api/v1"
    
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    ML_MODELS_DIR: Path = BASE_DIR / "ml" / "models"
    ML_DATA_DIR: Path = BASE_DIR / "ml" / "data"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://*.vercel.app",
    ]


settings = Settings()
