"""Service for transcribing audio files."""

import logging
import asyncio
from pathlib import Path
from typing import Optional
from slugify import slugify

import assemblyai as aai

from app.core.config import settings
from app.core.utils import extract_youtube_id, extract_facebook_video_id
from app.services.video_download_service import get_video_download_service

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service for transcribing audio files using AssemblyAI."""

    def __init__(self):
        """Initialize transcription service."""
        if not settings.assemblyai_api_key:
            logger.warning("ASSEMBLYAI_API_KEY not set. Transcription will not work.")
            self.client = None
        else:
            aai.settings.api_key = settings.assemblyai_api_key
            self.client = aai.Transcriber()
            logger.info("TranscriptionService initialized with AssemblyAI")

    def _get_transcription_path(
        self,
        project_title: str,
        video_id: str
    ) -> Path:
        """Get transcription file path.

        Args:
            project_title: Project title for directory naming
            video_id: Video ID

        Returns:
            Path to transcription text file
        """
        # Slugify title for safe directory name
        slug_title = slugify(project_title)
        
        # Create path: resources/videos/{slug_title}/video-inspiration/{video_id}.txt
        trans_dir = settings.videos_storage_dir / slug_title / "video-inspiration"
        trans_dir.mkdir(parents=True, exist_ok=True)
        
        return trans_dir / f"{video_id}.txt"

    async def transcribe_audio_file(
        self,
        audio_path: Path,
        project_title: str,
        video_id: str
    ) -> Optional[str]:
        """Transcribe an audio file.

        Args:
            audio_path: Path to audio file
            project_title: Project title for cache directory
            video_id: Video ID for cache filename

        Returns:
            Transcribed text or None if failed
        """
        if not self.client:
            logger.error("Transcription service not initialized. Check ASSEMBLYAI_API_KEY.")
            return None

        # Check if transcription already exists
        trans_path = self._get_transcription_path(project_title, video_id)
        if trans_path.exists():
            logger.info(f"✅ Transcription already exists (cached): {trans_path}")
            with open(trans_path, 'r', encoding='utf-8') as f:
                return f.read()

        logger.info(f"🎤 Transcribing audio: {audio_path.name}")

        try:
            # Transcribe with AssemblyAI
            transcript = await asyncio.to_thread(
                self.client.transcribe,
                str(audio_path)
            )
            
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription failed: {transcript.error}")
                return None

            transcription_text = transcript.text
            
            # Save to cache
            with open(trans_path, 'w', encoding='utf-8') as f:
                f.write(transcription_text)
            
            logger.info(f"✅ Transcription completed and cached: {len(transcription_text)} chars")
            return transcription_text

        except Exception as e:
            logger.error(f"❌ AssemblyAI transcription error: {e}")
            return None

    async def transcribe_video_url(
        self,
        url: str,
        project_title: str
    ) -> Optional[str]:
        """Transcribe a video from URL.

        Args:
            url: Video URL (YouTube/Facebook)
            project_title: Project title

        Returns:
            Transcribed text or None if failed
        """
        # Extract video ID
        video_id = extract_youtube_id(url)
        if not video_id:
            video_id = extract_facebook_video_id(url)
        
        if not video_id:
            logger.error(f"Failed to extract video ID from: {url}")
            return None

        # Check if transcription already cached
        trans_path = self._get_transcription_path(project_title, video_id)
        if trans_path.exists():
            logger.info(f"✅ Transcription already exists (cached): {trans_path}")
            with open(trans_path, 'r', encoding='utf-8') as f:
                return f.read()

        # Download audio first
        video_service = get_video_download_service()
        audio_path = await video_service.download_video_audio(url, project_title)
        
        if not audio_path:
            logger.error(f"Failed to download audio from: {url}")
            return None

        # Transcribe the audio
        return await self.transcribe_audio_file(audio_path, project_title, video_id)

    async def transcribe_videos(
        self,
        video_urls: list[str],
        project_title: str
    ) -> str:
        """Transcribe multiple videos and concatenate results.

        Args:
            video_urls: List of video URLs
            project_title: Project title

        Returns:
            Concatenated transcription text
        """
        if not video_urls:
            return ""

        transcriptions = []
        for url in video_urls:
            text = await self.transcribe_video_url(url, project_title)
            if text:
                transcriptions.append(text)

        return "\n\n---\n\n".join(transcriptions)


# Global singleton
_transcription_service: Optional[TranscriptionService] = None


def get_transcription_service() -> TranscriptionService:
    """Get or create transcription service singleton.

    Returns:
        TranscriptionService instance
    """
    global _transcription_service
    if _transcription_service is None:
        _transcription_service = TranscriptionService()
    return _transcription_service
