"""Service for coordinating contextual description generation."""

import logging
from typing import Optional

from app.models.contextual_description import ContextualDescriptionRequest, ContextualDescriptionResponse
from app.agents.contextual_description_agent import ContextualDescriptionAgent
from app.services.transcription_service import get_transcription_service

logger = logging.getLogger(__name__)


class ContextualDescriptionService:
    """Orchestrates the contextual description generation pipeline."""

    def __init__(self):
        """Initialize service with all agents."""
        self.contextual_description_agent = ContextualDescriptionAgent()
        self.transcription_service = get_transcription_service()
        logger.info("ContextualDescriptionService initialized")

    async def generate_contextual_description(
        self,
        request: ContextualDescriptionRequest
    ) -> ContextualDescriptionResponse:
        """Generate a contextual description based on inspiration videos and video type.

        Args:
            request: Contextual description generation request

        Returns:
            Generated contextual description response
        """
        logger.info(f"Starting contextual description generation for project: {request.title}")
        
        # Step 1: Transcribe inspiration videos (if provided)
        inspiration_content = ""
        if request.inspiration_videos:
            logger.info(f"Transcribing {len(request.inspiration_videos)} inspiration video(s)")
            inspiration_content = await self.transcription_service.transcribe_videos(
                request.inspiration_videos,
                request.title  # Pass title for cache directory
            )
            if inspiration_content:
                logger.info(f"Transcription completed: {len(inspiration_content)} chars")
            else:
                logger.warning("No transcription content obtained from inspiration videos")

        # Step 2: Generate contextual description using the agent
        contextual_description = await self.contextual_description_agent.generate_contextual_description(
            title=request.title,
            language=request.language,
            type_video=request.type_video,
            duration=request.duration,
            inspiration_content=inspiration_content,
            description=request.description
        )

        # Build response
        response = ContextualDescriptionResponse(
            description=contextual_description,
            status="contextual_description_generated"
        )

        logger.info("Contextual description generation completed successfully")
        return response


# Global singleton
_contextual_description_service: Optional[ContextualDescriptionService] = None


def get_contextual_description_service() -> ContextualDescriptionService:
    """Get or create ContextualDescriptionService singleton.

    Returns:
        ContextualDescriptionService instance
    """
    global _contextual_description_service
    if _contextual_description_service is None:
        _contextual_description_service = ContextualDescriptionService()
    return _contextual_description_service
