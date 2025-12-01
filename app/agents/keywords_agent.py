"""Agent for generating SEO keywords."""

import logging
from typing import Optional

from app.llm.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class KeywordsAgent(BaseAgent):
    """Agent specialized in generating SEO keywords."""

    def __init__(self, temperature: float = 0.6):
        """Initialize keywords agent.

        Args:
            temperature: Lower temperature for more focused keywords
        """
        super().__init__(
            prompt_name="keywords_prompt", # Changed from prompt_file to prompt_name
            temperature=temperature,
            translate_prompt=False # No longer translating, as prompts are language-specific
        )

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for keywords generation.

        Returns:
            Max tokens
        """
        return 4000

    async def generate_keywords(
        self,
        script_text: str,
        description: str,
        use_case: str,
        language: str = "en"
    ) -> str:
        """Generate SEO keywords.

        Args:
            script_text: Complete script text
            description: Video description
            use_case: Video use case type
            language: Language (for context, but keywords stay international)

        Returns:
            Comma-separated keywords
        """
        logger.info(f"Generating keywords for use_case={use_case}")
        
        # Truncate texts if too long
        logger.info("Generation des keywords")

        keywords = await super().generate(
            language=language,
            script_text=script_text,
            description=description,
            use_case=use_case
        )

        # Clean up keywords
        keywords = keywords.strip()
        logger.info(f"Generated keywords: {keywords}")
        return keywords
