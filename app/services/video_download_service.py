"""Service for downloading videos and extracting audio."""

import logging
import asyncio
import tempfile
from pathlib import Path
from typing import Optional
from slugify import slugify

from pytubefix import YouTube
import pytubefix.exceptions as pytubefix_exceptions # Changed import

from app.core.config import settings
from app.core.utils import extract_youtube_id, extract_facebook_video_id

logger = logging.getLogger(__name__)


class VideoDownloadService:
    """Service for downloading and caching video audio."""

    def __init__(self):
        """Initialize video download service."""
        logger.info("VideoDownloadService initialized")

    def _get_audio_path(
        self,
        project_title: str,
        video_id: str,
        platform: str = "youtube"
    ) -> Path:
        """Get audio file path for a video.

        Args:
            project_title: Project title for directory naming
            video_id: Video ID (YouTube ID, Facebook ID, etc.)
            platform: Platform name (youtube, facebook)

        Returns:
            Path to audio file
        """
        # Slugify title for safe directory name
        slug_title = slugify(project_title)
        
        # Create path: resources/videos/{slug_title}/video-inspiration/{video_id}.mp3
        audio_dir = settings.videos_storage_dir / slug_title / "video-inspiration"
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        return audio_dir / f"{video_id}.mp3"

    async def download_youtube_audio(
        self,
        url: str,
        project_title: str
    ) -> Optional[Path]:
        """Download audio from YouTube video.

        Args:
            url: YouTube video URL
            project_title: Project title for directory naming

        Returns:
            Path to downloaded audio file or None if failed
        """
        # Extract video ID
        video_id = extract_youtube_id(url)
        if not video_id:
            logger.error(f"Failed to extract YouTube ID from: {url}")
            return None

        # Check if already downloaded
        audio_path = self._get_audio_path(project_title, video_id, "youtube")
        if audio_path.exists():
            logger.info(f"✅ Audio already exists (cached): {audio_path}")
            return audio_path

        logger.info(f"📥 Downloading YouTube audio: {video_id}")

        try:
            # Download with pytube
            def download():
                yt = YouTube(url, use_oauth=False, allow_oauth_cache=True) # Add oauth params
                audio_stream = yt.streams.filter(only_audio=True).first()
                if not audio_stream:
                    raise pytubefix_exceptions.PytubeError("No audio stream found") # Use full path

                # Download directly to the final location
                # pytubefix's download method returns the full path of the downloaded file
                downloaded_file_path = audio_stream.download(
                    output_path=audio_path.parent,
                    filename=audio_path.name
                )
                return Path(downloaded_file_path)

            final_audio_path = await asyncio.to_thread(download)

            if final_audio_path and final_audio_path.exists():
                logger.info(f"✅ Downloaded YouTube audio: {final_audio_path}")
                return final_audio_path
            return None

        except pytubefix_exceptions.PytubeError as e: # Catch specific pytube errors
            logger.error(f"❌ YouTube audio download (PytubeError) error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ YouTube audio download (General Error) error: {e}")
            return None

    async def download_facebook_video(
        self,
        url: str,
        project_title: str
    ) -> Optional[Path]:
        """Download audio from Facebook video.

        Note: Facebook video download is restricted. This is a placeholder.
        
        Args:
            url: Facebook video URL
            project_title: Project title for directory naming

        Returns:
            Path to downloaded audio file or None if failed
        """
        logger.warning(f"⚠️ Facebook video download not fully implemented: {url}")
        logger.info("Facebook videos require special handling due to download restrictions.")
        return None

    async def download_video_audio(
        self,
        url: str,
        project_title: str
    ) -> Optional[Path]:
        """Download audio from video URL (auto-detect platform).

        Args:
            url: Video URL (YouTube/Facebook)
            project_title: Project title for directory naming

        Returns:
            Path to downloaded audio file or None if failed
        """
        if "youtube.com" in url or "youtu.be" in url:
            return await self.download_youtube_audio(url, project_title)
        elif "facebook.com" in url or "fb.watch" in url:
            return await self.download_facebook_video(url, project_title)
        else:
            logger.warning(f"Unsupported video URL: {url}")
            return None


# Global singleton
_video_download_service: Optional[VideoDownloadService] = None


def get_video_download_service() -> VideoDownloadService:
    """Get or create video download service singleton.

    Returns:
        VideoDownloadService instance
    """
    global _video_download_service
    if _video_download_service is None:
        _video_download_service = VideoDownloadService()
    return _video_download_service
