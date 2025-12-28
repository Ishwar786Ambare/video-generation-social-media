"""
Text-to-Speech Module
Converts text scripts to audio using gTTS
"""

import os
from typing import Optional
from gtts import gTTS


class TextToSpeech:
    """Handles text-to-speech conversion"""
    
    def __init__(self, language: str = "en", slow: bool = False):
        """
        Initialize Text-to-Speech converter
        
        Args:
            language: Language code (e.g., 'en', 'es', 'fr')
            slow: Whether to use slow speech speed
        """
        self.language = language
        self.slow = slow
    
    def generate_speech(
        self,
        text: str,
        output_path: str,
        language: Optional[str] = None,
        slow: Optional[bool] = None
    ) -> str:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert
            output_path: Path to save the audio file
            language: Language code (overrides default)
            slow: Slow speech flag (overrides default)
            
        Returns:
            Path to the generated audio file
        """
        lang = language or self.language
        is_slow = slow if slow is not None else self.slow
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate speech
        tts = gTTS(text=text, lang=lang, slow=is_slow)
        tts.save(output_path)
        
        return output_path
    
    def generate_multiple(
        self,
        text_segments: list,
        output_dir: str,
        prefix: str = "segment"
    ) -> list:
        """
        Generate multiple audio files from text segments
        
        Args:
            text_segments: List of text strings
            output_dir: Directory to save audio files
            prefix: Prefix for output filenames
            
        Returns:
            List of paths to generated audio files
        """
        audio_files = []
        
        for idx, text in enumerate(text_segments):
            output_path = os.path.join(output_dir, f"{prefix}_{idx}.mp3")
            audio_path = self.generate_speech(text, output_path)
            audio_files.append(audio_path)
        
        return audio_files
