import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.models.prompt import Prompt

logger = logging.getLogger(__name__)

class PromptService:
    """
    Service for retrieving prompts from MongoDB.
    """
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database["prompts"]

    async def get_prompt_content(self, prompt_name: str, language: str) -> Optional[str]:
        """
        Retrieves the content of a prompt from MongoDB by its name and language.

        Args:
            prompt_name: The base name of the prompt (e.g., "description_prompt").
            language: The target language of the prompt (e.g., "en", "fr").

        Returns:
            The prompt content as a string, or None if not found.
        """
        full_prompt_name = f"{prompt_name}_{language}"
        logger.debug(f"Attempting to retrieve prompt: {full_prompt_name}")

        prompt_doc = await self.collection.find_one(
            {"name": full_prompt_name, "language": language}
        )

        if prompt_doc:
            prompt = Prompt(**prompt_doc)
            logger.info(f"Successfully retrieved prompt '{full_prompt_name}'.")
            return prompt.content
        else:
            logger.warning(f"Prompt '{full_prompt_name}' not found in database.")
            return None

# Singleton instance
_prompt_service: Optional[PromptService] = None

async def get_prompt_service() -> PromptService:
    """
    Dependency to get a singleton instance of PromptService.
    """
    global _prompt_service
    if _prompt_service is None:
        database = await get_database()
        _prompt_service = PromptService(database)
    return _prompt_service
