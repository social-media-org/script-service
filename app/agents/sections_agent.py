"""Agent for generating script sections."""

import logging
from typing import Optional

from app.llm.base_agent import BaseAgent
from app.core.config import settings

logger = logging.getLogger(__name__)


class SectionsAgent(BaseAgent):
    """Agent specialized in generating structured script sections."""

    def __init__(self, temperature: float = 0.7):
        """Initialize sections agent.

        Args:
            temperature: Balanced temperature for creative but coherent scripts
        """
        super().__init__(prompt_file="sections_prompt.txt", temperature=temperature)

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for script generation.

        Returns:
            Max tokens (scripts can be long)
        """
        return 2000

    async def generate_sections(
        self,
        description: str,
        use_case: str,
        style: str,
        language: str,
        duration: Optional[int] = None,
        nb_section: Optional[int] = None,
        inspiration_content: str = ""
    ) -> tuple[list[str], str]:
        """Generate script sections.

        Args:
            description: Video description
            use_case: Video use case type
            style: Video style/tone
            language: Target language
            duration: Target duration in seconds
            nb_section: Number of sections
            inspiration_content: Transcribed inspiration videos

        Returns:
            Tuple of (list of sections, concatenated script text)
        """
        # Use defaults if not provided
        duration = duration or settings.default_duration
        nb_section = nb_section or settings.default_nb_sections

        logger.info(
            f"Generating {nb_section} section(s) for {duration}s video "
            f"(use_case={use_case}, language={language})"
        )

        # Prepare inspiration content message
        if not inspiration_content:
            inspiration_content = "No inspiration content provided."

        # Generate script
        script_output = await self.generate(
            description=description,
            use_case=use_case,
            style=style,
            language=language,
            duration=duration,
            nb_section=nb_section,
            inspiration_content=inspiration_content
        )

        # Parse sections
        if nb_section == 1:
            # Single section = entire script
            sections = [script_output.strip()]
            script_text = script_output.strip()
        else:
            # Multiple sections separated by marker
            sections = [
                section.strip()
                for section in script_output.split("---SECTION---")
                if section.strip()
            ]
            script_text = "\n\n".join(sections)

        logger.info(f"Generated {len(sections)} section(s), total {len(script_text)} chars")
        return sections, script_text
