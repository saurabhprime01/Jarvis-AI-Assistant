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
    
    # Database (SQLite for local, PostgreSQL for Vercel/Supabase)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:////tmp/jarvis.db" if os.getenv("VERCEL") else "sqlite:///./jarvis.db")
    VECTOR_DB_PATH: str = "/tmp/vector_db" if os.getenv("VERCEL") else "./memory/data/vector_db"
    
    # Cloud Vector DB (Optional, falls back to ChromaDB locally if empty)
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX: str = "jarvis-memory"
    
    # Voice
    TTS_VOICE: str = "en-US-ChristopherNeural"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
