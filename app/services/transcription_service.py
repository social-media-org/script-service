"""Service for transcribing video content from YouTube and Facebook."""

import logging
import asyncio
import tempfile
from pathlib import Path
from typing import Optional
import httpx

from pytubefix import YouTube
import assemblyai as aai

from app.core.config import settings
from app.core.utils import extract_youtube_id, extract_facebook_video_id

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Service for transcribing videos using AssemblyAI."""

    def __init__(self):
        """Initialize transcription service."""
        if not settings.assemblyai_api_key:
            logger.warning("ASSEMBLYAI_API_KEY not set. Transcription will not work.")
            self.client = None
        else:
            aai.settings.api_key = settings.assemblyai_api_key
            self.client = aai.Transcriber()
            logger.info("TranscriptionService initialized with AssemblyAI")

    async def transcribe_youtube(self, url: str) -> Optional[str]:
        """Transcribe a YouTube video.

        Args:
            url: YouTube video URL

        Returns:
            Transcribed text or None if failed
        """
        if not self.client:
            logger.error("Transcription service not initialized. Check ASSEMBLYAI_API_KEY.")
            return None

        try:
            logger.info(f"Transcribing YouTube video: {url}")
            
            # Download audio from YouTube
            audio_path = await self._download_youtube_audio(url)
            if not audio_path:
                return None

            # Transcribe with AssemblyAI
            transcription = await asyncio.to_thread(
                self._transcribe_file,
                audio_path
            )

            # Cleanup
            Path(audio_path).unlink(missing_ok=True)

            return transcription

        except Exception as e:
            logger.error(f"YouTube transcription error: {e}")
            return None

    async def transcribe_facebook(self, url: str) -> Optional[str]:
        """Transcribe a Facebook video.

        Note: Facebook video download is restricted. This is a placeholder.
        
        Args:
            url: Facebook video URL

        Returns:
            Transcribed text or None if failed
        """
        logger.warning(f"Facebook video transcription not fully implemented: {url}")
        logger.info("Facebook videos require special handling due to download restrictions.")
        return None

    async def transcribe_videos(self, video_urls: list[str]) -> str:
        """Transcribe multiple videos and concatenate results.

        Args:
            video_urls: List of video URLs (YouTube/Facebook)

        Returns:
            Concatenated transcription text
        """
        if not video_urls:
            return ""

        transcriptions = []
        for url in video_urls:
            if "youtube.com" in url or "youtu.be" in url:
                text = await self.transcribe_youtube(url)
                if text:
                    transcriptions.append(text)
            elif "facebook.com" in url or "fb.watch" in url:
                text = await self.transcribe_facebook(url)
                if text:
                    transcriptions.append(text)
            else:
                logger.warning(f"Unsupported video URL: {url}")

        return "\n\n---\n\n".join(transcriptions)

    async def _download_youtube_audio(self, url: str) -> Optional[str]:
        """Download audio from YouTube video.

        Args:
            url: YouTube video URL

        Returns:
            Path to downloaded audio file or None if failed
        """
        try:
            # Create temporary file
            temp_dir = tempfile.mkdtemp()
            output_path = Path(temp_dir) / "audio.mp3"

            # Download with pytube
            def download():
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                if not audio_stream:
                    raise Exception("No audio stream found")
                audio_stream.download(output_path=temp_dir, filename="audio.mp3")

            await asyncio.to_thread(download)

            if output_path.exists():
                logger.info(f"Downloaded YouTube audio: {output_path}")
                return str(output_path)
            return None

        except Exception as e:
            logger.error(f"YouTube audio download error: {e}")
            return None

    def _transcribe_file(self, audio_path: str) -> Optional[str]:
        """Transcribe audio file using AssemblyAI.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcribed text or None if failed
        """
        try:
            transcript = self.client.transcribe(audio_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"Transcription failed: {transcript.error}")
                return None

            logger.info(f"Transcription completed: {len(transcript.text)} chars")
            return transcript.text

        except Exception as e:
            logger.error(f"AssemblyAI transcription error: {e}")
            return None


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
