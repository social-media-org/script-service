"""LLM client configuration for DeepSeek API (OpenAI compatible)."""

import logging
from typing import Optional

from openai import AsyncOpenAI
import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Wrapper for LLM API client (DeepSeek via OpenAI SDK)."""

    def __init__(self) -> None:
        """Initialize LLM client."""
        if not settings.deepseek_api_key:
            logger.warning("DEEPSEEK_API_KEY not set. LLM features will not work.")
            self.client = None
        else:
            self.client = AsyncOpenAI(
                api_key=settings.deepseek_api_key,
                base_url=settings.openai_api_base,
                http_client=httpx.AsyncClient(trust_env=False)
            )
            logger.info(f"LLM Client initialized with base URL: {settings.openai_api_base}")

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (defaults to settings.openai_model)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response

        Raises:
            ValueError: If client not initialized
            Exception: If API call fails
        """
        if not self.client:
            raise ValueError("LLM client not initialized. Check DEEPSEEK_API_KEY.")

        try:
            response = await self.client.chat.completions.create(
                model=model or settings.openai_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            raise

    def is_available(self) -> bool:
        """Check if LLM client is available.

        Returns:
            True if client initialized, False otherwise
        """
        return self.client is not None


# Global singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client singleton.

    Returns:
        LLMClient instance
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
