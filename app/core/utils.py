"""Utility functions for the application."""

import re
from typing import Optional


def extract_youtube_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL.

    Args:
        url: YouTube URL

    Returns:
        Video ID or None if not found
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)',
        r'youtube\.com\/embed\/([\w-]+)',
        r'youtube\.com\/v\/([\w-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_facebook_video_id(url: str) -> Optional[str]:
    """Extract Facebook video ID from URL.

    Args:
        url: Facebook URL

    Returns:
        Video ID or None if not found
    """
    patterns = [
        r'facebook\.com\/.*\/videos\/(\d+)',
        r'fb\.watch\/([\w-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def clean_text(text: str) -> str:
    """Clean and normalize text.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration (e.g., "1m 30s")
    """
    minutes = seconds // 60
    secs = seconds % 60
    
    if minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"
