"""Pydantic models for script generation."""

from typing import Optional, Literal
from pydantic import BaseModel, Field


class ScriptGenerationRequest(BaseModel):
    """Request model for script generation."""

    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description/prompt")
    video_inspirations: Optional[list[str]] = Field(
        default=None,
        description="List of YouTube/Facebook video URLs for inspiration"
    )
    use_case: Literal[
        "storytelling",
        "youtube_short",
        "explanation",
        "commercial",
        "inspirational",
        "educational",
        "tutorial"
    ] = Field(..., description="Video use case type")
    language: Literal["en", "fr", "es", "de", "it", "pt"] = Field(
        ...,
        description="Target language for script"
    )
    style: Literal[
        "educational",
        "inspirational",
        "comedic",
        "dramatic",
        "casual",
        "professional"
    ] = Field(..., description="Video style/tone")
    keywords: Optional[str] = Field(
        default=None,
        description="SEO keywords (comma-separated)"
    )
    script_text: Optional[str] = Field(
        default=None,
        description="Pre-existing script text (if regenerating metadata only)"
    )
    regenerer_script: bool = Field(
        default=True,
        description="Whether to regenerate script or just metadata"
    )
    duration: Optional[int] = Field(
        default=None,
        description="Target duration in seconds"
    )
    nb_section: Optional[int] = Field(
        default=None,
        description="Number of sections (1 = single continuous script)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "How to Learn Python in 30 Days",
                "description": "A comprehensive guide for beginners",
                "use_case": "educational",
                "language": "en",
                "style": "professional",
                "duration": 60,
                "nb_section": 3
            }
        }


class ScriptGenerationResponse(BaseModel):
    """Response model for script generation."""

    script_sections: Optional[list[str]] = Field(
        default=None,
        description="List of script sections (None if nb_section=1)"
    )
    script_text: str = Field(..., description="Complete script text")
    status: str = Field(
        default="script_generated",
        description="Generation status"
    )
    keywords: Optional[str] = Field(
        default=None,
        description="Generated SEO keywords"
    )
    video_description: Optional[str] = Field(
        default=None,
        description="Generated video description"
    )
    title: Optional[str] = Field(
        default=None,
        description="Generated or refined title"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "script_text": "Welcome to our Python tutorial...",
                "status": "script_generated",
                "keywords": "python, programming, tutorial",
                "video_description": "Learn Python in 30 days with this comprehensive guide.",
                "title": "Master Python Programming in 30 Days"
            }
        }
