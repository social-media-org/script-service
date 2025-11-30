"""API routes for script generation."""

import logging
import traceback
from fastapi import APIRouter, HTTPException, status

from app.models.script import ScriptGenerationRequest, ScriptGenerationResponse
from app.services.script_orchestrator import get_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scripts", tags=["Scripts"])


@router.post(
    "/generate",
    response_model=ScriptGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate video script",
    description="""
    Generate a complete video script with sections, title, description, and keywords.
    
    Features:
    - Transcribe inspiration videos (YouTube/Facebook)
    - Generate structured script sections
    - Create SEO-optimized metadata
    - Support for partial regeneration (metadata only)
    """
)
async def generate_script(
    request: ScriptGenerationRequest
) -> ScriptGenerationResponse:
    """Generate video script for a project.

    Args:
        request: Script generation request

    Returns:
        Generated script with metadata

    Raises:
        HTTPException: If generation fails
    """
    logger.info(f"Received script generation request for {request.title}")
    
    try:
        # Get orchestrator and generate script
        orchestrator = get_orchestrator()
        response = await orchestrator.generate_script(request)
        
        logger.info(f"Script generation successful")
        return response

    except Exception as e:
        traceback.print_exc()
        logger.error(f"Script generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Script generation failed: {str(e)}"
        )


@router.get(
    "/health",
    summary="Check script service health",
    description="Check if all required services (LLM, Transcription) are configured"
)
async def health_check() -> dict:
    """Check health of script generation service.

    Returns:
        Health status with service availability
    """
    from app.core.llm_client import get_llm_client
    from app.services.transcription_service import get_transcription_service
    from app.core.config import settings
    
    llm_client = get_llm_client()
    transcription_service = get_transcription_service()
    
    return {
        "status": "healthy",
        "services": {
            "llm": "available" if llm_client.is_available() else "unavailable",
            "transcription": "available" if transcription_service.client else "unavailable"
        },
        "config": {
            "default_duration": settings.default_duration,
            "default_nb_sections": settings.default_nb_sections,
            "llm_model": settings.openai_model
        }
    }
