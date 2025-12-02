"""Agent for generating contextual descriptions."""

import logging
from typing import Optional
from app.llm.base_agent import BaseAgent
from app.core.llm_client import get_llm_client
from app.services.prompt_service import PromptService

logger = logging.getLogger(__name__)


class ContextualDescriptionAgent(BaseAgent):
    """Generates contextual descriptions for videos."""

    def __init__(self):
        super().__init__()
        self.llm_client = get_llm_client()
        self.prompt_service = PromptService()
        logger.info("ContextualDescriptionAgent initialized")

    async def generate_contextual_description(
        self,
        title: str,
        language: str,
        type_video: str,
        duration: Optional[int],
        inspiration_content: str,
        description: Optional[str],
    ) -> str:
        """Generates a contextual description based on video type and inspiration.

        Args:
            title: The title of the project.
            language: The target language for the description.
            type_video: The type of video (LIFE_LESSON, STOICISM, X_THINGS_TO_DO).
            duration: The target duration of the video in seconds.
            inspiration_content: Transcribed content from inspiration videos.
            description: Existing description or context for generation.

        Returns:
            The generated contextual description.
        """
        logger.info(f"Generating contextual description for type_video: {type_video}, language: {language}")

        prompt_name = self._get_prompt_name(type_video)
        
        # Load the base prompt for contextual description from MongoDB
        base_prompt_template = await self.prompt_service.get_prompt_content(prompt_name, language)
        
        if not base_prompt_template:
            logger.error(f"Prompt '{prompt_name}' for language '{language}' not found in database.")
            raise ValueError(f"Prompt for video type '{type_video}' and language '{language}' not found.")

        # Dynamically build the context for the prompt
        prompt_context = self._build_prompt_context(
            type_video=type_video,
            duration=duration,
            inspiration_content=inspiration_content,
            description=description,
            title=title
        )
        
        final_prompt = base_prompt_template.format(context=prompt_context)

        # Call LLM
        response = await self.llm_client.text_generation(final_prompt, language)
        return response

    def _get_prompt_name(self, type_video: str) -> str:
        """Determines the appropriate base prompt name based on video type."""
        return f"contextual_description_{type_video.lower()}"

    def _build_prompt_context(
        self,
        type_video: str,
        duration: Optional[int],
        inspiration_content: str,
        description: Optional[str],
        title: str
    ) -> str:
        """Builds dynamic context string for the prompt based on video type."""
        context_parts = []
        
        context_parts.append(f"Title of the video project: {title}.")

        if description:
            context_parts.append(f"Here is some existing description or context: {description}.")

        if inspiration_content:
            context_parts.append(f"Consider the following content from inspiration videos: {inspiration_content}.")

        if type_video == "LIFE_LESSON":
            context_parts.append("The script should tell a short, impactful story that conveys a life lesson.")
            if duration:
                context_parts.append(f"The video is expected to be around {duration} seconds long.")
                if duration <= 240: # 4 minutes
                    context_parts.append("Emphasize conciseness and a format suitable for a short video.")
                else:
                    context_parts.append("Allow for more detailed storytelling suitable for a longer video.")
        elif type_video == "STOICISM":
            context_parts.append("The script should explore stoic principles and offer practical applications for modern life.")
        elif type_video == "X_THINGS_TO_DO":
            context_parts.append("The script must present a list of 'X things to do'. The narration style should be direct and action-oriented. The structure should be: Introduction - X things (e.g., Firstly, Secondly, Thirdly...).")
            if duration:
                context_parts.append(f"The video is expected to be around {duration} seconds long.")

        return " ".join(context_parts)
