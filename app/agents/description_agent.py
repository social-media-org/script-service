"""Agent for generating video descriptions."""

import logging
from typing import Optional

from app.llm.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class DescriptionAgent(BaseAgent):
    """Agent specialized in generating video descriptions."""

    def __init__(self, temperature: float = 0.7):
        """Initialize description agent.

        Args:
            temperature: Balanced temperature for engaging descriptions
        """
        super().__init__(
            prompt_name="description_prompt", # Changed from prompt_file to prompt_name
            temperature=temperature,
            translate_prompt=False # No longer translating, as prompts are language-specific
        )

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for description generation.

        Returns:
            Max tokens
        """
        return 500

    async def generate_description(
        self,
        script_text: str,
        keywords: Optional[str],
        language: str
    ) -> str:
        """Generate a video description.

        Args:
            script_text: Complete script text
            keywords: SEO keywords (optional)
            language: Target language

        Returns:
            Generated description
        """
        logger.info(f"Generating description for script ({len(script_text)} chars)")
        
        # Truncate script if too long (keep first 1000 chars)
        if len(script_text) > 1000:
            script_preview = script_text[:1000] + "..."
        else:
            script_preview = script_text

        description = await super().generate(
            language=language,
            script_text=script_preview,
            keywords=keywords or "video content"
        )

        logger.info(f"Generated description: {len(description)} chars")
        return description.strip()
