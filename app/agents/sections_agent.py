"""Agent for generating script sections."""

import logging
from typing import Optional, Tuple, List
from pathlib import Path

from app.core.config import settings
from string import Template
from app.llm.base_agent import BaseAgent
from app.agents.translation_agent import get_translation_agent # Imported here for clarity


logger = logging.getLogger(__name__)


class SectionsAgent(BaseAgent):
    """Agent specialized in generating structured script sections."""

    def __init__(self, temperature: float = 0.7):
        """Initialize sections agent.

        Args:
            temperature: Balanced temperature for creative but coherent scripts
        """
        super().__init__(prompt_file=None, temperature=temperature, translate_prompt=False)
        
        # Load both prompt templates
        self.prompt_template_single = self._load_sections_prompt("sections_prompt_single.txt")
        self.prompt_template_multiple = self._load_sections_prompt("sections_prompt_multiple.txt")
        
        logger.info("SectionsAgent initialized with dynamic prompt selection")

    def _load_sections_prompt(self, prompt_file: str) -> str:
        """Load prompt template from file for sections agent."""
        prompt_path = Path(__file__).parent.parent / "llm" / "prompts" / prompt_file
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _get_max_tokens(self) -> Optional[int]:
        """Get maximum tokens for this agent (8000 for sections)."""
        return 8000

    async def generate(
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
        

        # Select appropriate prompt template and build prompt
        if nb_section == 1:
            prompt_template = self.prompt_template_single
            
        else:
            prompt_template = self.prompt_template_multiple
        
        formatted_prompt = self._format_prompt(
            prompt_template,
            description=description,
            use_case=use_case,
            style=style,
            duration=duration,
            nb_section=nb_section,
            inspiration_content=inspiration_content,
        )

        try:
            script_output = await super().generate(
                formatted_prompt=formatted_prompt,
                language=language
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
