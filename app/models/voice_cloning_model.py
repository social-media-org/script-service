"""Pydantic models for voice cloning endpoints."""

from typing import Optional
from pydantic import BaseModel, Field


class VoiceCloneRequest(BaseModel):
    """Request model for voice cloning."""
    
    voice_dir_path: str = Field(
        ..., 
        description="Path to directory containing audio files for voice cloning"
    )
    api_key_number: int = Field(
        ..., 
        description="API key number to use (1-5)",
        ge=1,
        le=5
    )
    voice_name: Optional[str] = Field(
        None,
        description="Optional name for the cloned voice"
    )
    voice_description: Optional[str] = Field(
        None,
        description="Optional description for the cloned voice"
    )


class VoiceCloneResponse(BaseModel):
    """Response model for voice cloning."""
    
    voice_id: str = Field(..., description="ID of the cloned voice")
    voice_name: str = Field(..., description="Name of the cloned voice")
    description: str = Field(..., description="Description of the cloned voice")
    api_key_number: int = Field(..., description="API key number used")
    audio_files_used: int = Field(..., description="Number of audio files used for cloning")
    success: bool = Field(..., description="Whether the cloning was successful")
    error: Optional[str] = Field(None, description="Error message if cloning failed")


class VoiceDetailsRequest(BaseModel):
    """Request model for getting voice details."""
    
    voice_id: str = Field(..., description="ID of the voice to get details for")
    api_key_number: int = Field(
        ..., 
        description="API key number to use (1-5)",
        ge=1,
        le=5
    )


class VoiceDetailsResponse(BaseModel):
    """Response model for voice details."""
    
    voice_id: str = Field(..., description="ID of the voice")
    name: str = Field(..., description="Name of the voice")
    description: str = Field(..., description="Description of the voice")
    category: str = Field(..., description="Category of the voice")
    labels: dict = Field(..., description="Labels of the voice")
    preview_url: Optional[str] = Field(None, description="Preview URL of the voice")
    success: bool = Field(..., description="Whether the request was successful")
    error: Optional[str] = Field(None, description="Error message if request failed")
