"""
Environment-based configuration using Pydantic Settings.
Demonstrates production-ready configuration management.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    nominatim_user_agent: str = "tripmind-ai-production"
    nominatim_email: str = "demo@example.com"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    frontend_url: str = "http://localhost:5500"
    
    # Cache Configuration
    cache_ttl_seconds: int = 3600
    
    # Rate Limiting
    rate_limit_requests: int = 10
    rate_limit_window: int = 60  # seconds
    
    # Retry Configuration
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
