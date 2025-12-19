from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "RetentionAI API"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # GenAI
    GEMINI_API_KEY: str

    model_config = ConfigDict(env_file="backend/.env")

@lru_cache
def get_settings():
    return Settings()
