from fastapi import APIRouter, Depends
from typing import List

from app.models.prompt import Prompt
from app.services.prompt_service import get_prompt_service

router = APIRouter()


@router.get("/prompts", response_model=List[Prompt])
async def read_prompts(
    skip: int = 0, 
    limit: int = 100, 
    prompt_service = Depends(get_prompt_service)
):
    """
    Retrieve prompts with pagination.
    
    Args:
        skip: Number of prompts to skip (for pagination)
        limit: Maximum number of prompts to return
        prompt_service: PromptService instance (injected)
    
    Returns:
        List of Prompt objects
    """
    return await prompt_service.get_prompts(skip=skip, limit=limit)
