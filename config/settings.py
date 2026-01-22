
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
import os
from pathlib import Path


class Settings(BaseSettings):
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    
    grok_api_key: str = Field(..., description="Grok API key (primary LLM)")
    deepseek_api_key: Optional[str] = Field(None, description="DeepSeek API key (backup)")
    
    # ============================================
    # MCP Server
    # ============================================
    mcp_server_url: str = Field(
        default="http://localhost:8000",
        description="MCP server URL"
    )
    mcp_timeout: int = Field(default=30, description="MCP request timeout in seconds")
    
    # ============================================
    # News Sources
    # ============================================
    news_sources: List[str] = Field(
        default=[
            "https://cryptonews.com/news/feed/",
            "https://www.coindesk.com/arc/outboundfeeds/rss/",
            "https://cointelegraph.com/rss",
        ],
        description="RSS feed URLs for crypto news"
    )
    
    # ============================================
    # Social Sentiment APIs
    # ============================================
    cryptopanic_api_key: Optional[str] = Field(None, description="CryptoPanic API key")
    
    
    twitter_bearer_token: Optional[str] = Field(None, description="Twitter API v2 bearer token")
    
    
    reddit_client_id: Optional[str] = Field(None, description="Reddit client ID")
    reddit_client_secret: Optional[str] = Field(None, description="Reddit client secret")
    reddit_user_agent: str = Field(
        default="CryptoTradingAgent/1.0",
        description="Reddit user agent"
    )
    
    # ============================================
    # Observability
    # ============================================
    langsmith_api_key: Optional[str] = Field(None, description="LangSmith API key")
    langsmith_project: str = Field(
        default="crypto-trading-agents",
        description="LangSmith project name"
    )
    langsmith_tracing: bool = Field(default=False, description="Enable LangSmith tracing")
    
    # ============================================
    # Application Settings
    # ============================================
    log_level: str = Field(default="INFO", description="Logging level")
    cache_enabled: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    max_retries: int = Field(default=3, description="Maximum API retry attempts")
    request_timeout: int = Field(default=30, description="Default request timeout")
    
    # ============================================
    # Agent Configuration
    # ============================================
    default_chain: str = Field(default="ethereum", description="Default blockchain")
    default_risk_profile: str = Field(
        default="moderate",
        description="Default risk profile (aggressive|moderate|conservative)"
    )
    debate_rounds: int = Field(default=3, description="Number of debate rounds")
    
    # ============================================
    # Paths
    # ============================================
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent,
        description="Project root directory"
    )
    logs_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "logs",
        description="Logs directory"
    )
    
    @validator("log_level")
    def validate_log_level(cls, v):
        
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v
    
    @validator("default_risk_profile")
    def validate_risk_profile(cls, v):
        
        valid_profiles = ["aggressive", "moderate", "conservative"]
        v = v.lower()
        if v not in valid_profiles:
            raise ValueError(f"Risk profile must be one of {valid_profiles}")
        return v
    
    @validator("logs_dir", always=True)
    def create_logs_dir(cls, v):
        
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    def has_twitter_config(self) -> bool:
        
        return self.twitter_bearer_token is not None
    
    def has_reddit_config(self) -> bool:
        
        return (
            self.reddit_client_id is not None
            and self.reddit_client_secret is not None
        )
    
    def has_langsmith_config(self) -> bool:
        
        return self.langsmith_api_key is not None and self.langsmith_tracing


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


settings = get_settings()