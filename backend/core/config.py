from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    API_PREFIX: str = "/api" 
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./database.db"
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = ""
    LLM_BASE_URL: str = ""
    ALLOWED_ORIGINS: str = ""
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        if not v:
            return []
        return [origin.strip() for origin in v.split(",") if origin.strip()]
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }
settings = Settings()