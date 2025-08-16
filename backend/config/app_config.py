"""
Centralized Configuration System for Finance Wizardry Bot
=========================================================

This module provides centralized configuration management for the entire application.
All settings, models, and configurations can be modified from this single location.

Usage:
    from config.app_config import AppConfig
    config = AppConfig()
    print(config.ollama.model_name)
"""

import os
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class Environment(str, Enum):
    """Application environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class DatabaseConfig(BaseModel):
    """Database configuration settings"""
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(default="finance_wizardry", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="password", description="Database password")
    
    @property
    def url(self) -> str:
        """Generate database URL"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class OllamaConfig(BaseModel):
    """Ollama LLM configuration settings"""
    base_url: str = Field(default="http://localhost:11434", description="Ollama API base URL")
    model_name: str = Field(default="deepseek-r1:1.5b", description="Default Ollama model name")
    temperature: float = Field(default=0.7, description="Response creativity (0.0-1.0)")
    max_tokens: int = Field(default=1000, description="Maximum response length")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    
    # Model-specific configurations
    available_models: List[str] = Field(
        default=[
            "deepseek-r1:1.5b",      # Fast, good for general tasks
            "llama3.1:8b",           # Better reasoning, slower
            "mistral:7b",            # Good balance
            "codellama:13b",         # Best for code
            "phi3:14b",              # Microsoft model
        ],
        description="Available Ollama models"
    )
    
    # Agent-specific model overrides
    agent_models: Dict[str, str] = Field(
        default={
            "news_intelligence": "deepseek-r1:1.5b",    # Fast for news analysis
            "financial_advisor": "llama3.1:8b",         # Better for complex advice
            "credit_specialist": "deepseek-r1:1.5b",    # Good for credit analysis
        },
        description="Specific models for each agent type"
    )


class NewsConfig(BaseModel):
    """News intelligence configuration"""
    update_interval_minutes: int = Field(default=30, description="News update frequency")
    max_articles_per_fetch: int = Field(default=50, description="Maximum articles to fetch")
    sentiment_threshold: float = Field(default=0.1, description="Sentiment significance threshold")
    
    # News sources and keywords
    financial_keywords: List[str] = Field(
        default=[
            "stocks", "market", "economy", "inflation", "GDP", "Federal Reserve",
            "interest rates", "earnings", "revenue", "profit", "financial",
            "investment", "trading", "NYSE", "NASDAQ", "S&P 500", "Dow Jones",
            "bonds", "commodities", "crypto", "bitcoin", "ethereum",
            "tech stocks", "healthcare", "energy", "banking", "real estate"
        ],
        description="Keywords for financial news filtering"
    )


class UIConfig(BaseModel):
    """UI/Frontend configuration"""
    theme: str = Field(default="dark", description="UI theme (dark/light)")
    primary_color: str = Field(default="#fbbf24", description="Primary color (yellow/gold)")
    secondary_color: str = Field(default="#f59e0b", description="Secondary color (amber)")
    accent_color: str = Field(default="#3b82f6", description="Accent color (blue)")
    
    # Agent colors
    agent_colors: Dict[str, str] = Field(
        default={
            "news_intelligence": "#3b82f6",    # Blue
            "financial_advisor": "#fbbf24",    # Yellow/Gold
            "credit_specialist": "#f59e0b",    # Amber
            "system": "#6b7280",               # Gray
            "error": "#ef4444",                # Red
            "success": "#10b981",              # Green
        },
        description="Color scheme for different agents"
    )


class SecurityConfig(BaseModel):
    """Security and authentication configuration"""
    secret_key: str = Field(default="your-secret-key-here", description="Application secret key")
    jwt_expiry_hours: int = Field(default=24, description="JWT token expiry time")
    rate_limit_per_minute: int = Field(default=60, description="API rate limit per minute")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    file_path: Optional[str] = Field(default=None, description="Log file path (None for console only)")


class AppConfig(BaseModel):
    """Main application configuration class"""
    
    # Environment
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    debug: bool = Field(default=True, description="Debug mode")
    
    # Sub-configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    news: NewsConfig = Field(default_factory=NewsConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"  # Allows OLLAMA__MODEL_NAME=llama3.1:8b
        case_sensitive = False
        extra = "ignore"
        protected_namespaces = ()  # Allow model_ prefixed fields
    
    @classmethod
    def load_from_env(cls) -> "AppConfig":
        """Load configuration from environment variables"""
        return cls()
    
    def get_ollama_model_for_agent(self, agent_type: str) -> str:
        """Get the appropriate Ollama model for a specific agent"""
        return self.ollama.agent_models.get(agent_type, self.ollama.model_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return self.dict()
    
    def save_to_file(self, file_path: str) -> None:
        """Save configuration to JSON file"""
        import json
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, file_path: str) -> "AppConfig":
        """Load configuration from JSON file"""
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(**data)


# Global configuration instance
app_config = AppConfig.load_from_env()


# Convenience functions for easy access
def get_ollama_config() -> OllamaConfig:
    """Get Ollama configuration"""
    return app_config.ollama


def get_database_url() -> str:
    """Get database URL"""
    return app_config.database.url


def get_agent_model(agent_type: str) -> str:
    """Get Ollama model for specific agent"""
    return app_config.get_ollama_model_for_agent(agent_type)


def update_ollama_model(model_name: str, agent_type: Optional[str] = None) -> None:
    """Update Ollama model configuration"""
    if agent_type:
        app_config.ollama.agent_models[agent_type] = model_name
    else:
        app_config.ollama.model_name = model_name


# Example usage and documentation
if __name__ == "__main__":
    print("=== Finance Wizardry Bot Configuration ===")
    print(f"Environment: {app_config.environment}")
    print(f"Database URL: {app_config.database.url}")
    print(f"Ollama Model: {app_config.ollama.model_name}")
    print(f"Available Models: {app_config.ollama.available_models}")
    print("\nAgent-specific models:")
    for agent, model in app_config.ollama.agent_models.items():
        print(f"  {agent}: {model}")
