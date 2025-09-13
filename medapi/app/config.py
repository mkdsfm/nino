import os
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Medical Personal Account API"
    
    # Database settings
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # Options: "sqlite", "postgresql"
    SQLITE_DATABASE_URI: str = os.getenv("SQLITE_DATABASE_URI", "sqlite:///./data/medapi.db")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "medapi")
    DATABASE_URI: Optional[str] = os.getenv("DATABASE_URI")

    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        if values.get("DB_TYPE") == "sqlite":
            return values.get("SQLITE_DATABASE_URI")
        
        if values.get("DB_TYPE") == "postgresql":
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_SERVER"),
                path=f"/{values.get('POSTGRES_DB') or ''}",
            )
        
        return values.get("SQLITE_DATABASE_URI")


settings = Settings()
