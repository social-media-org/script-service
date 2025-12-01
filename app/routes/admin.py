import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.llm.prompts_migrator import migrate_prompts_to_mongodb

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/migrate_prompts", summary="Trigger prompt migration to MongoDB")
async def trigger_prompt_migration():
    """
    Triggers the migration of prompt templates from files to MongoDB.
    Existing prompts will be updated, and new ones will be inserted.
    """
    logger.info("Admin endpoint /migrate_prompts called.")
    try:
        await migrate_prompts_to_mongodb()
        return {"message": "Prompt migration initiated successfully."}
    except Exception as e:
        logger.error(f"Prompt migration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to migrate prompts: {e}"
        )
