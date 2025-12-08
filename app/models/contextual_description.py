"""Pydantic models for contextual description generation."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class ContextualDescriptionRequest(BaseModel):
    """Request model for contextual description generation."""

    title: str = Field(..., description="Project title")
    duration: Optional[int] = Field(
        default=None,
        description="Target video duration in seconds"
    )
    inspiration_videos: Optional[list[str]] = Field(
        default=None,
        description="List of YouTube/Facebook video URLs for inspiration"
    )
    language: str = Field(
        ...,
        description="Target language for the description"
    )
    type_video: Literal[
        "LIFE_LESSON",
        "STOICISM",
        "X_THINGS_TO_DO"
    ] = Field(..., description="Type of video content")
    description: Optional[str] = Field(
        default=None,
        description="Existing description or context for generation"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A Life Lesson on Persistence",
                "duration": 240,
                "inspiration_videos": [
                    "https://www.youtube.com/watch?v=example1",
                    "https://www.youtube.com/watch?v=example2"
                ],
                "language": "fr",
                "type_video": "LIFE_LESSON",
                "description": "An inspiring story about overcoming challenges."
            }
        }


class ContextualDescriptionResponse(BaseModel):
    """Response model for contextual description generation."""

    contextual_description: str = Field(..., description="Generated contextual description")
    status: str = Field(
        default="contextual_description_generated",
        description="Generation status"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "contextual_description": "This video will explore the importance of persistence through a short, impactful story, suitable for a 4-minute YouTube video. It will highlight a key life lesson relevant to modern challenges.",
                "status": "contextual_description_generated"
            }
        }
