"""Agent for generating video titles."""

import logging
from typing import Optional

from app.llm.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TitleAgent(BaseAgent):
    """Agent specialized in generating catchy video titles."""

    def __init__(self, temperature: float = 0.8):
        """Initialize title agent.

        Args:
            temperature: Higher temperature for more creative titles
        """
        super().__init__(prompt_file="title_prompt.txt", temperature=temperature)

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for title generation.

        Returns:
            Max tokens (titles are short)
        """
        return 100

    async def generate_title(
        self,
        description: str,
        use_case: str,
        style: str,
        language: str
    ) -> str:
        """Generate a video title.

        Args:
            description: Video description
            use_case: Video use case type
            style: Video style/tone
            language: Target language

        Returns:
            Generated title
        """
        logger.info(f"Generating title for use_case={use_case}, language={language}")
        
        title = await self.generate(
            description=description,
            use_case=use_case,
            style=style,
            language=language
        )

        # Clean up the title (remove quotes if present)
        title = title.strip('"').strip("'").strip()
        
        logger.info(f"Generated title: {title}")
        return title
