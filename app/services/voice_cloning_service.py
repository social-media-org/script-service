"""Voice cloning service using ElevenLabs instant voice cloning API."""

import os
import glob
from typing import List, Optional
from elevenlabs import ElevenLabs
from elevenlabs import VoiceSettings
import traceback


class VoiceCloningService:
    """Service for voice cloning operations using ElevenLabs API."""
    
    def __init__(self):
        pass
    
    def _get_api_key(self, api_key_number: int) -> str:
        """Get the API key for the specified number.
        
        Args:
            api_key_number: The API key number (1-5)
            
        Returns:
            str: The API key
            
        Raises:
            ValueError: If the API key is not found or invalid
        """
        api_key = os.getenv(f"ELEVENLABS_API_KEY{api_key_number}")
        if not api_key:
            raise ValueError(f"ELEVENLABS_API_KEY{api_key_number} not found in environment variables")
        
        if not api_key.startswith("sk_"):
            raise ValueError(f"ELEVENLABS_API_KEY{api_key_number} is invalid (should start with 'sk_')")
        
        return api_key
    
    def _get_audio_files(self, voice_dir_path: str) -> List[str]:
        """Get all audio files from the specified directory.
        
        Args:
            voice_dir_path: Path to directory containing audio files
            
        Returns:
            List[str]: List of audio file paths
            
        Raises:
            ValueError: If no audio files found or directory doesn't exist
        """
        if not os.path.exists(voice_dir_path):
            raise ValueError(f"Directory {voice_dir_path} does not exist")
        
        if not os.path.isdir(voice_dir_path):
            raise ValueError(f"{voice_dir_path} is not a directory")
        
        # Supported audio file extensions
        audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.ogg', '*.flac']
        audio_files = []
        
        for ext in audio_extensions:
            pattern = os.path.join(voice_dir_path, ext)
            audio_files.extend(glob.glob(pattern))
        
        if not audio_files:
            raise ValueError(f"No audio files found in {voice_dir_path}. Supported formats: {', '.join(audio_extensions)}")
        
        return audio_files
    
    async def clone_voice(
        self, 
        voice_dir_path: str, 
        api_key_number: int,
        voice_name: Optional[str] = None,
        voice_description: Optional[str] = None
    ) -> dict:
        """Clone a voice using ElevenLabs instant voice cloning API.
        
        Args:
            voice_dir_path: Path to directory containing audio files for cloning
            api_key_number: API key number to use (1-5)
            voice_name: Optional name for the cloned voice
            voice_description: Optional description for the cloned voice
            
        Returns:
            dict: Voice cloning result with voice_id and details
            
        Raises:
            Exception: If voice cloning fails
        """
        try:
            # Get API key
            api_key = self._get_api_key(api_key_number)
            
            # Get audio files
            audio_files = self._get_audio_files(voice_dir_path)
            
            print(f"🎙️ Starting voice cloning with {len(audio_files)} audio files from {voice_dir_path}")
            print(f"🔑 Using API key #{api_key_number}")
            
            # Initialize ElevenLabs client
            client = ElevenLabs(api_key=api_key)
            
            # Generate voice name if not provided
            if not voice_name:
                voice_name = f"Cloned_Voice_{os.path.basename(voice_dir_path)}"
            
            # Generate description if not provided
            if not voice_description:
                voice_description = f"Voice cloned from {voice_dir_path}"
            
            # Clone the voice using instant voice cloning
            voice = client.voices.clone(
                name=voice_name,
                description=voice_description,
                files=[open(file, "rb") for file in audio_files]
            )
            
            # Close all file handles
            for file in audio_files:
                try:
                    open(file, "rb").close()
                except:
                    pass
            
            print(f"✅ Voice cloned successfully! Voice ID: {voice.voice_id}")
            
            return {
                "voice_id": voice.voice_id,
                "voice_name": voice_name,
                "description": voice_description,
                "api_key_number": api_key_number,
                "audio_files_used": len(audio_files),
                "success": True
            }
            
        except Exception as e:
            print(f"❌ Voice cloning failed: {str(e)}")
            traceback.print_exc()
            raise Exception(f"Voice cloning failed: {str(e)}")
    
    async def get_voice_details(self, voice_id: str, api_key_number: int) -> dict:
        """Get details of a cloned voice.
        
        Args:
            voice_id: The voice ID to get details for
            api_key_number: API key number to use (1-5)
            
        Returns:
            dict: Voice details
        """
        try:
            api_key = self._get_api_key(api_key_number)
            client = ElevenLabs(api_key=api_key)
            
            voice = client.voices.get(voice_id=voice_id)
            
            return {
                "voice_id": voice.voice_id,
                "name": voice.name,
                "description": voice.description,
                "category": voice.category,
                "labels": voice.labels,
                "preview_url": voice.preview_url,
                "success": True
            }
            
        except Exception as e:
            print(f"❌ Failed to get voice details: {str(e)}")
            raise Exception(f"Failed to get voice details: {str(e)}")


# Dependency injection function
def get_voice_cloning_service() -> VoiceCloningService:
    return VoiceCloningService()
