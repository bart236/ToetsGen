"""
Configuratie voor de toetsgenerator.
"""
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Applicatie instellingen."""

    # API Keys
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # Provider configuratie
    default_llm_provider: Literal["anthropic", "openai"] = Field(
        default="anthropic",
        alias="DEFAULT_LLM_PROVIDER"
    )

    # Model configuratie
    anthropic_model: str = Field(
        default="claude-sonnet-4-5-20250929",
        alias="ANTHROPIC_MODEL"
    )
    openai_model: str = Field(
        default="gpt-4-turbo-preview",
        alias="OPENAI_MODEL"
    )

    # Generatie instellingen
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature voor LLM generatie"
    )
    max_tokens: int = Field(
        default=2000,
        ge=1,
        description="Maximum aantal tokens voor response"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def get_api_key(self, provider: str | None = None) -> str:
        """Haal de API key op voor de gekozen provider."""
        provider = provider or self.default_llm_provider

        if provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY niet gevonden. "
                    "Zet deze in .env of als environment variable."
                )
            return self.anthropic_api_key
        elif provider == "openai":
            if not self.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY niet gevonden. "
                    "Zet deze in .env of als environment variable."
                )
            return self.openai_api_key
        else:
            raise ValueError(f"Onbekende provider: {provider}")

    def get_model_name(self, provider: str | None = None) -> str:
        """Haal de model naam op voor de gekozen provider."""
        provider = provider or self.default_llm_provider

        if provider == "anthropic":
            return self.anthropic_model
        elif provider == "openai":
            return self.openai_model
        else:
            raise ValueError(f"Onbekende provider: {provider}")


# Singleton instance
settings = Settings()
