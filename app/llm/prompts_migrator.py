import asyncio
import logging
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.prompt import Prompt

logger = logging.getLogger(__name__)

PROMPT_FILES = {
    "description_prompt": {
        "path": "description_prompt.txt",
        "type": "description",
        "name": "description_prompt"
    },
    "keywords_prompt": {
        "path": "keywords_prompt.txt",
        "type": "keywords",
        "name": "keywords_prompt"
    },
    "sections_prompt_multiple": {
        "path": "sections_prompt_multiple.txt",
        "type": "sections_multiple",
        "name": "sections_prompt_multiple"
    },
    "sections_prompt_single": {
        "path": "sections_prompt_single.txt",
        "type": "sections_single",
        "name": "sections_prompt_single"
    },
    "title_prompt": {
        "path": "title_prompt.txt",
        "type": "title",
        "name": "title_prompt"
    },
    # Assuming article_no_sections is a new prompt type you want to add
    "article_no_sections": {
        "path": "article_no_sections_prompt.txt", # This file would need to be created
        "type": "article_no_sections",
        "name": "article_no_sections_prompt"
    }
}

DEFAULT_LANGUAGES = ["en", "fr"] # Example languages

async def migrate_prompts_to_mongodb():
    """
    Migrates prompt templates from files to MongoDB.
    This function will be run once at application startup if the collection is empty.
    """
    client = None
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        database = client[settings.DB_NAME]
        prompts_collection = database["prompts"]

        logger.info("Starting prompt migration/update to MongoDB...")

        for prompt_key, prompt_info in PROMPT_FILES.items():
            prompt_file_path = Path(__file__).parent / "prompts" / prompt_info["path"]
            
            if not prompt_file_path.exists():
                logger.warning(f"Prompt file not found: {prompt_file_path}. Skipping.")
                continue

            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for lang in DEFAULT_LANGUAGES:
                full_prompt_name = f"{prompt_info['name']}_{lang}"
                prompt_data = Prompt(
                    name=full_prompt_name,
                    language=lang,
                    content=content,
                    type=prompt_info["type"]
                )
                
                # Use update_one with upsert=True to either insert or update the prompt
                result = await prompts_collection.update_one(
                    {"name": full_prompt_name, "language": lang},
                    {"$set": prompt_data.model_dump(by_alias=True, exclude_none=True)},
                    upsert=True
                )
                
                if result.upserted_id:
                    logger.info(f"Inserted new prompt '{full_prompt_name}' for language '{lang}' into MongoDB.")
                elif result.modified_count > 0:
                    logger.info(f"Updated existing prompt '{full_prompt_name}' for language '{lang}' in MongoDB.")
                else:
                    logger.info(f"Prompt '{full_prompt_name}' for language '{lang}' already up to date.")

        logger.info("Prompt migration/update completed.")

    except Exception as e:
        logger.error(f"Error during prompt migration: {e}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    # This block allows you to run the migration script independently for testing
    # You would typically call migrate_prompts_to_mongodb from your application's lifespan
    asyncio.run(migrate_prompts_to_mongodb())
