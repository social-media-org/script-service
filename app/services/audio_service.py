"""Audio generation service using ElevenLabs."""

from functools import lru_cache
import os
from typing import List
from app.services.elevenlabs_custom_service import ElevenLabsService
from app.models.audio_model import AudioGenerateRequest, AudioGenerateResponse


class AudioService:
    """Service for audio generation operations."""
    
    def __init__(self):
        self.elevenlabs_service = ElevenLabsService()
    
    async def generate_audio(self, request: AudioGenerateRequest) -> AudioGenerateResponse:
        """Generate audio from text and save to specified path.
        
        Args:
            request: Audio generation request with text and audio path
            
        Returns:
            AudioGenerateResponse: Audio generation result
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(request.audio_path), exist_ok=True)
            
            # Generate audio using ElevenLabs service
            file_path, duration_ms = await self.elevenlabs_service.generate_audio(
                text=request.text, 
                output_path=request.audio_path
            )
            
            return AudioGenerateResponse(
                audio_path=file_path,
                duration_ms=duration_ms,
                text=request.text,
                success=True
            )
            
        except Exception as e:
            return AudioGenerateResponse(
                audio_path=request.audio_path,
                duration_ms=0,
                text=request.text,
                success=False,
                error=str(e)
            )
    
    async def generate_audio_list(self, audio_requests: List[AudioGenerateRequest]) -> List[AudioGenerateResponse]:
        """Generate multiple audio files from a list of text and path pairs.
        
        Args:
            audio_requests: List of AudioGenerateRequest objects
            
        Returns:
            List of AudioGenerateResponse for each audio generation request
        """
        results = []
        
        for request in audio_requests:
            result = await self.generate_audio(request)
            results.append(result)
        
        return results
    
@lru_cache
def get_audio_service() -> AudioService:
    return AudioService(config="my config")