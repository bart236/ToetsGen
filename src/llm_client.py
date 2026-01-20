"""
LLM client voor het aanroepen van AI modellen.
"""
from typing import Literal
import json
from anthropic import Anthropic
from openai import OpenAI
from .config import settings


class LLMClient:
    """Wrapper voor LLM API calls."""

    def __init__(self, provider: Literal["anthropic", "openai"] | None = None):
        """
        Initialiseer LLM client.

        Args:
            provider: Welke LLM provider te gebruiken (anthropic of openai)
        """
        self.provider = provider or settings.default_llm_provider
        self.model = settings.get_model_name(self.provider)
        self.api_key = settings.get_api_key(self.provider)

        if self.provider == "anthropic":
            self.client = Anthropic(api_key=self.api_key)
        elif self.provider == "openai":
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Onbekende provider: {self.provider}")

    def generate_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> str:
        """
        Genereer tekst met het LLM model.

        Args:
            prompt: De user prompt
            system_prompt: Optionele system prompt
            temperature: Temperature voor generatie (default uit settings)
            max_tokens: Max tokens voor response (default uit settings)

        Returns:
            De gegenereerde tekst
        """
        temperature = temperature or settings.temperature
        max_tokens = max_tokens or settings.max_tokens

        if self.provider == "anthropic":
            return self._generate_anthropic(
                prompt, system_prompt, temperature, max_tokens
            )
        elif self.provider == "openai":
            return self._generate_openai(
                prompt, system_prompt, temperature, max_tokens
            )
        else:
            raise ValueError(f"Onbekende provider: {self.provider}")

    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: str | None,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Genereer tekst met Anthropic Claude."""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def _generate_openai(
        self,
        prompt: str,
        system_prompt: str | None,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Genereer tekst met OpenAI GPT."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def generate_json(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None
    ) -> dict:
        """
        Genereer JSON met het LLM model.

        Args:
            prompt: De user prompt
            system_prompt: Optionele system prompt
            temperature: Temperature voor generatie
            max_tokens: Max tokens voor response

        Returns:
            Geparseerde JSON als dictionary
        """
        response_text = self.generate_text(
            prompt, system_prompt, temperature, max_tokens
        )

        # Probeer JSON uit de response te extracten
        try:
            # Zoek naar JSON in code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text.strip()

            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Kon JSON niet parsen uit LLM response: {e}\n\n"
                f"Response: {response_text}"
            )
