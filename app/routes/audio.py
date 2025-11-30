"""Audio generation and voice cloning endpoints."""

from typing import Annotated, List
from fastapi import APIRouter, Depends, status

from app.models.audio_model import AudioGenerateRequest, AudioGenerateResponse
from app.models.voice_cloning_model import (
    VoiceCloneRequest, 
    VoiceCloneResponse,
    VoiceDetailsRequest,
    VoiceDetailsResponse
)
from app.services.audio_service import AudioService, get_audio_service
from app.services.voice_cloning_service import VoiceCloningService, get_voice_cloning_service

router = APIRouter(prefix="/audio", tags=["Audio"])


@router.post(
    "/generate",
    response_model=AudioGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate audio from text",
    description="Generate audio file from text using ElevenLabs and save to specified path.",
)
async def generate_audio(
    request: AudioGenerateRequest,
    service: Annotated[AudioService, Depends(get_audio_service)],
) -> AudioGenerateResponse:
    """Generate audio from text.
    
    Args:
        request: Audio generation request with text and audio path
        service: Audio service instance (injected)
        
    Returns:
        AudioGenerateResponse: Audio generation result
    """
    return await service.generate_audio(request)


@router.post(
    "/generate-list",
    response_model=List[AudioGenerateResponse],
    status_code=status.HTTP_200_OK,
    summary="Generate multiple audios from text list",
    description="Generate multiple audio files from a list of text and path pairs.",
)
async def generate_audio_list(
    audio_requests: List[AudioGenerateRequest],
    service: Annotated[AudioService, Depends(get_audio_service)],
) -> List[AudioGenerateResponse]:
    """Generate multiple audio files from a list of text and path pairs.
    
    Args:
        audio_requests: List of AudioGenerateRequest objects
        service: Audio service instance (injected)
        
    Returns:
        List[AudioGenerateResponse]: Results for each audio generation request
    """
    return await service.generate_audio_list(audio_requests)


@router.post(
    "/clone-voice",
    response_model=VoiceCloneResponse,
    status_code=status.HTTP_200_OK,
    summary="Clone voice from audio files",
    description="Clone a voice using ElevenLabs instant voice cloning API from audio files in a directory.",
)
async def clone_voice(
    request: VoiceCloneRequest,
    service: Annotated[VoiceCloningService, Depends(get_voice_cloning_service)],
) -> VoiceCloneResponse:
    """Clone a voice from audio files in a directory.
    
    Args:
        request: Voice cloning request with directory path and API key number
        service: Voice cloning service instance (injected)
        
    Returns:
        VoiceCloneResponse: Voice cloning result with voice ID and details
    """
    try:
        result = await service.clone_voice(
            voice_dir_path=request.voice_dir_path,
            api_key_number=request.api_key_number,
            voice_name=request.voice_name,
            voice_description=request.voice_description
        )
        
        return VoiceCloneResponse(**result)
        
    except Exception as e:
        return VoiceCloneResponse(
            voice_id="",
            voice_name="",
            description="",
            api_key_number=request.api_key_number,
            audio_files_used=0,
            success=False,
            error=str(e)
        )


@router.post(
    "/voice-details",
    response_model=VoiceDetailsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get voice details",
    description="Get details of a cloned voice using its voice ID.",
)
async def get_voice_details(
    request: VoiceDetailsRequest,
    service: Annotated[VoiceCloningService, Depends(get_voice_cloning_service)],
) -> VoiceDetailsResponse:
    """Get details of a cloned voice.
    
    Args:
        request: Voice details request with voice ID and API key number
        service: Voice cloning service instance (injected)
        
    Returns:
        VoiceDetailsResponse: Voice details
    """
    try:
        result = await service.get_voice_details(
            voice_id=request.voice_id,
            api_key_number=request.api_key_number
        )
        
        return VoiceDetailsResponse(**result)
        
    except Exception as e:
        return VoiceDetailsResponse(
            voice_id=request.voice_id,
            name="",
            description="",
            category="",
            labels={},
            preview_url=None,
            success=False,
            error=str(e)
        )
