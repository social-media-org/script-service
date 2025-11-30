"""Orchestrator for coordinating all script generation agents."""

import logging
from typing import Optional

from app.models.script import ScriptGenerationRequest, ScriptGenerationResponse
from app.agents.title_agent import TitleAgent
from app.agents.sections_agent import SectionsAgent
from app.agents.description_agent import DescriptionAgent
from app.agents.keywords_agent import KeywordsAgent
from app.services.transcription_service import get_transcription_service

logger = logging.getLogger(__name__)


class ScriptOrchestrator:
    """Orchestrates the script generation pipeline."""

    def __init__(self):
        """Initialize orchestrator with all agents."""
        self.title_agent = TitleAgent()
        self.sections_agent = SectionsAgent()
        self.description_agent = DescriptionAgent()
        self.keywords_agent = KeywordsAgent()
        self.transcription_service = get_transcription_service()
        logger.info("ScriptOrchestrator initialized with all agents")

    async def generate_script(
        self,
        request: ScriptGenerationRequest
    ) -> ScriptGenerationResponse:
        """Generate complete script with all metadata.

        This is the main pipeline that coordinates all agents.

        Args:
            request: Script generation request

        Returns:
            Complete script generation response
        """
        logger.info(f"Starting script generation pipeline for project")
        logger.info(f"Request: regenerer_script={request.regenerer_script}, "
                   f"use_case={request.use_case}, language={request.language}")

        # Step 1: Transcribe inspiration videos (if provided)
        inspiration_content = ""
        if request.video_inspirations:
            logger.info(f"Transcribing {len(request.video_inspirations)} inspiration video(s)")
            inspiration_content = await self.transcription_service.transcribe_videos(
                request.video_inspirations,
                request.title  # Pass title for cache directory
            )
            if inspiration_content:
                logger.info(f"Transcription completed: {len(inspiration_content)} chars")
            else:
                logger.warning("No transcription content obtained from videos")

        # Step 2: Generate or use existing script
        script_text: str
        script_sections: Optional[list[str]] = None

        if request.regenerer_script:
            # Generate new script
            logger.info("Generating new script sections")
            sections, script_text = await self.sections_agent.generate_section(
                description=request.description,
                use_case=request.use_case,
                style=request.style,
                language=request.language,
                duration=request.duration,
                nb_section=request.nb_section,
                inspiration_content=inspiration_content
            )
            
            # Only include sections list if more than 1 section
            if request.nb_section and request.nb_section > 1:
                script_sections = sections
        else:
            # Use provided script
            if not request.script_text:
                raise ValueError("script_text must be provided when regenerer_script=False")
            logger.info("Using provided script text (skipping script generation)")
            script_text = request.script_text

        # Step 3: Generate title (always)
        logger.info("Generating video title")
        title = await self.title_agent.generate_title(
            description=request.description,
            use_case=request.use_case,
            style=request.style,
            language=request.language
        )

        # Step 4: Generate keywords (always)
        logger.info("Generating SEO keywords")
        keywords = await self.keywords_agent.generate_keywords(
            script_text=script_text,
            description=request.description,
            use_case=request.use_case
        )

        # Step 5: Generate video description (always)
        logger.info("Generating video description")
        video_description = await self.description_agent.generate_description(
            script_text=script_text,
            keywords=keywords,
            language=request.language
        )

        # Build response
        response = ScriptGenerationResponse(
            script_sections=script_sections,
            script_text=script_text,
            status="script_generated",
            keywords=keywords,
            video_description=video_description,
            title=title
        )

        logger.info("Script generation pipeline completed successfully")
        return response


# Global singleton
_orchestrator: Optional[ScriptOrchestrator] = None


def get_orchestrator() -> ScriptOrchestrator:
    """Get or create orchestrator singleton.

    Returns:
        ScriptOrchestrator instance
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ScriptOrchestrator()
    return _orchestrator
