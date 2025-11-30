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
            prompt_file="keywords_prompt.txt",
            temperature=temperature,
            translate_prompt=False  # Keywords don't need translation
        )

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for keywords generation.

        Returns:
            Max tokens
        """
        return 200

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
        script_preview = script_text[:1000] + "..." if len(script_text) > 1000 else script_text
        desc_preview = description[:500] + "..." if len(description) > 500 else description

        formatted_prompt = self._format_prompt(
            self.prompt_template,
            script_text=script_preview,
            description=desc_preview,
            use_case=use_case
        )

        keywords = await super().generate(
            formatted_prompt=formatted_prompt,
            language=language
        )

        # Clean up keywords
        keywords = keywords.strip()
        logger.info(f"Generated keywords: {keywords}")
        return keywords
