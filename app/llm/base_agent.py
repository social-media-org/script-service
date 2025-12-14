"""Base agent class for LLM-powered agents."""

from collections import defaultdict
import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from pathlib import Path
from string import Template
from typing import Optional

import humanize

from app.core.llm_client import get_llm_client
from app.services.prompt_service import get_prompt_service

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class for LLM agents."""

    def __init__(
        self,
        prompt_name: Optional[str] = None, # Changed from prompt_file to prompt_name
        temperature: float = 0.7,
        translate_prompt: bool = True
    ):
        """Initialize base agent.

        Args:
            prompt_name: Name of the prompt in the database
            temperature: LLM sampling temperature
            translate_prompt: Whether to translate prompt to target language
        """
        self.llm_client = get_llm_client()
        self.temperature = temperature
        self.translate_prompt = translate_prompt
        self.prompt_name = prompt_name # Store prompt_name
        self.prompt_template: Optional[str] = None # Will be loaded dynamically
        logger.info(f"Initialized {self.__class__.__name__} with prompt_name={self.prompt_name}")

    async def _load_prompt_from_db(self, language: str) -> str:
        """Load prompt template from database.

        Args:
            language: Target language for the prompt

        Returns:
            Prompt template string

        Raises:
            ValueError: If prompt not found in database
        """
        if not self.prompt_name:
            raise ValueError("Prompt name not provided for agent.")

        prompt_service = await get_prompt_service()
        prompt_content = await prompt_service.get_prompt_content(self.prompt_name, language)

        if not prompt_content:
            # Fallback to English if French not found, or raise error if English also not found
            if language != "en":
                logger.warning(f"Prompt '{self.prompt_name}' not found for language '{language}', trying 'en'.")
                prompt_content = await prompt_service.get_prompt_content(self.prompt_name, "en")
            
            if not prompt_content:
                raise ValueError(f"Prompt '{self.prompt_name}' not found in database for any language.")
        
        return prompt_content

    def _format_prompt(self, template: str, **kwargs) -> str:
    # Remplacer None par ""
        cleaned = {k: ("" if v is None else v) for k, v in kwargs.items()}

        # Toutes les clés manquantes retournent une chaîne vide
        dd = defaultdict(str, cleaned)

        return template.format_map(dd)

    async def generate(self, language: str = "en", **kwargs) -> str:
        """Generate output using LLM.

        Args:
            language: Target language for response
            **kwargs: Placeholder values for prompt template

        Returns:
            Generated text

        Raises:
            ValueError: If LLM client not available or prompt not found
        """
        if not self.llm_client.is_available():
            raise ValueError(f"{self.__class__.__name__} requires LLM client. Check API key configuration.")
        
        # Load prompt dynamically based on language
        self.prompt_template = await self._load_prompt_from_db(language)
        
        # Format duration if present
        if 'duration' in kwargs and kwargs['duration'] is not None:
            try:
                # Convert to float then int (handle float values)
                seconds = float(kwargs['duration'])
                # Round to nearest integer
                seconds_int = int(round(seconds))
                # Format using humanize
                formatted_duration = humanize.precisedelta(timedelta(seconds=seconds_int))
                kwargs['duration'] = "Important: the duration should be approximately " + formatted_duration
                logger.info(f"Formatted duration: {seconds} seconds -> {formatted_duration}")
            except (ValueError, TypeError):
                # If conversion fails, keep original value
                logger.warning(f"Could not convert duration '{kwargs['duration']}' to numeric seconds")
        
        formatted_prompt = self._format_prompt(self.prompt_template, **kwargs)
        logger.info(f"Prompt brut ({language}) : {formatted_prompt}")
        
        # Prepare messages
        messages = [
            {"role": "system", "content": "YYou are an AI assistant specialized in video content creation. Your mission is to generate catchy titles, compelling descriptions, structured sections, and complete content, ensuring that each element is relevant and tailored to the target theme and language."},
            {"role": "user", "content": formatted_prompt}
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
