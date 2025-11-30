"""Base agent class for LLM-powered agents."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from app.core.llm_client import get_llm_client

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for LLM agents."""

    def __init__(self, prompt_file: str, temperature: float = 0.7):
        """Initialize base agent.

        Args:
            prompt_file: Path to prompt template file
            temperature: LLM sampling temperature
        """
        self.llm_client = get_llm_client()
        self.temperature = temperature
        self.prompt_template = self._load_prompt(prompt_file)
        logger.info(f"Initialized {self.__class__.__name__}")

    def _load_prompt(self, prompt_file: str) -> str:
        """Load prompt template from file.

        Args:
            prompt_file: Path to prompt file

        Returns:
            Prompt template string

        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        prompt_path = Path(__file__).parent / "prompts" / prompt_file
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _format_prompt(self, **kwargs) -> str:
        """Format prompt template with provided variables.

        Args:
            **kwargs: Variables to substitute in prompt

        Returns:
            Formatted prompt string
        """
        return self.prompt_template.format(**kwargs)

    async def generate(self, **kwargs) -> str:
        """Generate output using LLM.

        Args:
            **kwargs: Variables for prompt formatting

        Returns:
            Generated text

        Raises:
            ValueError: If LLM client not available
        """
        if not self.llm_client.is_available():
            raise ValueError(f"{self.__class__.__name__} requires LLM client. Check API key configuration.")

        # Format prompt
        prompt = self._format_prompt(**kwargs)
        
        # Prepare messages
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant specialized in video content creation."},
            {"role": "user", "content": prompt}
        ]

        # Generate response
        try:
            response = await self.llm_client.chat_completion(
                messages=messages,
                temperature=self.temperature,
                max_tokens=self._get_max_tokens()
            )
            logger.debug(f"{self.__class__.__name__} generated response: {len(response)} chars")
            return response
        except Exception as e:
            logger.error(f"{self.__class__.__name__} generation failed: {e}")
            raise

    @abstractmethod
    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for this agent.

        Returns:
            Max tokens or None for default
        """
        pass
