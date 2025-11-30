"""Pydantic models for audio generation endpoints."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AudioGenerateRequest(BaseModel):
    """Request model for audio generation."""
    
    text: str = Field(..., description="Text to convert to speech", min_length=1)
    audio_path: str = Field(..., description="Path where to save the generated audio file")


class AudioGenerateResponse(BaseModel):
    """Response model for audio generation."""
    
    audio_path: str = Field(..., description="Path to the generated audio file")
    duration_ms: int = Field(..., description="Duration of the audio in milliseconds")
    text: str = Field(..., description="Original text that was converted")
    success: bool = Field(..., description="Whether the generation was successful")
    error: Optional[str] = Field(None, description="Error message if generation failed")
