"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.api_keyp_formatter import ApiKeyFormatter
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.routes import scripts

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup
    logger.info("Starting Script Generation Service")
    print("✅ Script Generation Service started")
    print("✅ DEEPSEEK api key :", ApiKeyFormatter.mask(settings.deepseek_api_key))
    print("✅ Assembly ai api key :", ApiKeyFormatter.mask(settings.assemblyai_api_key))

    yield

    # Shutdown
    logger.info("Shutting down application")
    print("❌ Script Generation Service stopped")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        description="""
        🎬 Script Generation Microservice
        
        Generate professional video scripts with AI-powered agents:
        - Transcribe inspiration videos (YouTube/Facebook)
        - Generate structured script sections
        - Create SEO-optimized titles and descriptions
        - Extract relevant keywords
        """
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    setup_exception_handlers(app)

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check() -> dict[str, str]:
        """Health check endpoint.

        Returns:
            dict: Health status
        """
        return {
            "status": "healthy",
            "service": "script-generation",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    # Include routers
    app.include_router(scripts.router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
