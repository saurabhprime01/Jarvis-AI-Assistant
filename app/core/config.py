from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "JARVIS"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # LLM Settings
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    MODEL_NAME: str = "gemini-1.5-flash"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./jarvis.db"
    VECTOR_DB_PATH: str = "./memory/data/vector_db"
    
    # Voice
    TTS_VOICE: str = "en-US-ChristopherNeural"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
