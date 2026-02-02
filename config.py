# config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database (your existing)
    DATABASE_URL: str
    
    # Email Configuration (NEW)
    SMTP_HOST: str = "smtp.gmail.com"  # Default value
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool = True
    
    # Email From Details
    EMAIL_FROM_NAME: str = "Student Platform"
    EMAIL_FROM_ADDRESS: str
    
    # Templates Directory (relative to your project root)
    EMAIL_TEMPLATES_DIR: str = "email-templates"
    
    # Frontend URLs for email links (optional but recommended)
    FRONTEND_URL: str = "http://localhost:3000"
    VERIFICATION_PATH: str = "/verify-email"
    RESET_PASSWORD_PATH: str = "/reset-password"
    
    class Config:
        env_file = ".env"

settings = Settings()