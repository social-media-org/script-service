"""Service for coordinating contextual description generation."""

import logging
from typing import Optional, Any 
import datetime
import humanize

from app.models.contextual_description import ContextualDescriptionRequest, ContextualDescriptionResponse
from app.services.transcription_service import get_transcription_service
from app.services.prompt_service import PromptService, get_prompt_service

logger = logging.getLogger(__name__)


class ContextualDescriptionService:
    """Orchestrates the contextual description generation pipeline."""

    def __init__(self, transcription_service: Any, prompt_service: PromptService):
        """Initialize service with all agents."""
        self.transcription_service = transcription_service
        self.prompt_service = prompt_service
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

        # Step 2: Retrieve and format the contextual description prompt
        prompt_template = await self.prompt_service.get_prompt_content(
            request.type_video,
            request.language
        )
        
        if not prompt_template:
            logger.error(f"No prompt found for video type: {request.type_video} and language: {request.language}")
            raise ValueError("Prompt template not found")

        formatted_title = f"title: {request.title}" if request.title else ""
        formatted_description = f"description: {request.description}" if request.description else ""

        # Format duration into human-readable format using humanize
        if request.duration is not None:
            duration_delta = datetime.timedelta(seconds=request.duration)
            formatted_duration = humanize.naturaldelta(duration_delta)
        else:
            formatted_duration = ""

        contextual_description = prompt_template.format(
            script_inspiration=inspiration_content,
            duration=formatted_duration,
            title=formatted_title,
            description=formatted_description
        )

        # Build response
        response = ContextualDescriptionResponse(
            description=contextual_description,
            status="contextual_description_generated"
        )

        logger.info("Contextual description generation completed successfully")
        return response


async def create_contextual_description_service() -> ContextualDescriptionService:
    """Factory function to create a ContextualDescriptionService instance with awaited dependencies."""
    transcription_service = get_transcription_service()
    prompt_service = await get_prompt_service()
    return ContextualDescriptionService(transcription_service, prompt_service)
