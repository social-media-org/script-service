from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated
from bson import ObjectId

class Prompt(BaseModel):
    """
    Represents a prompt stored in MongoDB.
    """
    id: Optional[Annotated[str, BeforeValidator(str)]] = Field(alias="_id", default=None)
    name: str = Field(..., description="Unique name of the prompt (e.g., 'description_prompt')")
    language: str = Field(..., description="Language of the prompt (e.g., 'en', 'fr')")
    content: str = Field(..., description="The actual prompt text")
    type: str = Field(..., description="Type of content generation (e.g., 'description', 'keywords', 'sections_single', 'title', 'article_no_sections')")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "description_prompt",
                "language": "en",
                "content": "Generate a compelling description for a video about {video_topic} using the following transcription: {transcription_text}",
                "type": "description"
            }
        }
