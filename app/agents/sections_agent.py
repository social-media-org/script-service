"""Agent for generating script sections."""

import logging
from typing import Optional
from pathlib import Path

from app.core.llm_client import get_llm_client
from app.core.config import settings

logger = logging.getLogger(__name__)


class SectionsAgent:
    """Agent specialized in generating structured script sections."""

    def __init__(self, temperature: float = 0.7):
        """Initialize sections agent.

        Args:
            temperature: Balanced temperature for creative but coherent scripts
        """
        self.llm_client = get_llm_client()
        self.temperature = temperature
        
        # Load both prompt templates
        prompts_dir = Path(__file__).parent.parent / "llm" / "prompts"
        with open(prompts_dir / "sections_prompt_single.txt", 'r', encoding='utf-8') as f:
            self.prompt_template_single = f.read()
        with open(prompts_dir / "sections_prompt_multiple.txt", 'r', encoding='utf-8') as f:
            self.prompt_template_multiple = f.read()
        
        logger.info("SectionsAgent initialized with dynamic prompt selection")

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

        # Select appropriate prompt template and build prompt
        if nb_section == 1:
            prompt_template = self.prompt_template_single
            prompt = prompt_template.format(
                description=description,
                use_case=use_case,
                style=style,
                duration=duration,
                inspiration_content=inspiration_content
            )
        else:
            prompt_template = self.prompt_template_multiple
            prompt = prompt_template.format(
                description=description,
                use_case=use_case,
                style=style,
                duration=duration,
                nb_section=nb_section,
                inspiration_content=inspiration_content
            )

        # Translate prompt if needed
        if language != "en":
            from app.agents.translation_agent import get_translation_agent
            translation_agent = get_translation_agent()
            prompt = await translation_agent.translate_prompt(prompt, language)

        # Generate script
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant specialized in video content creation."},
            {"role": "user", "content": prompt}
        ]

        try:
            script_output = await self.llm_client.chat_completion(
                messages=messages,
                temperature=self.temperature,
                max_tokens=2000
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
