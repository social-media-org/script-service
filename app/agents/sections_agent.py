"""Agent for generating script sections."""

import logging
from typing import Optional, Tuple, List
from pathlib import Path

from app.core.config import settings
from string import Template
from app.llm.base_agent import BaseAgent


logger = logging.getLogger(__name__)


class SectionsAgent(BaseAgent):
    """Agent specialized in generating structured script sections."""

    def __init__(self, temperature: float = 0.7):
        """Initialize sections agent.

        Args:
            temperature: Balanced temperature for creative but coherent scripts
        """
        # BaseAgent now handles prompt loading dynamically based on prompt_name
        # We don't need to load two prompts here anymore; BaseAgent will get the right one
        super().__init__(prompt_name=None, temperature=temperature, translate_prompt=False) # prompt_name will be set in generate_section
        logger.info("SectionsAgent initialized with dynamic prompt selection from DB")

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for this agent (8000 for sections)."""
        return 8000

    async def generate_section(
        self,
        description: str,
        use_case: str,
        style: str,
        language: str = "en",
        duration: Optional[int] = None,
        nb_section: Optional[int] = None,
        inspiration_content: str = ""
    ) -> Tuple[List[str], str]:
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
        if inspiration_content:
            inspiration_content = "Inspiration Content : " + inspiration_content
        

        # Select appropriate prompt name
        if nb_section == 1:
            self.prompt_name = "sections_prompt_single"
        else:
            self.prompt_name = "sections_prompt_multiple"
        
        try:
            script_output = await super().generate(
                language=language,
                description=description,
                use_case=use_case,
                style=style,
                duration=duration,
                nb_section=nb_section,
                inspiration_content=inspiration_content,
            )
        except Exception as e:
            logger.error(f"Sections generation failed: {e}")
            raise

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
