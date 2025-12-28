"""
Text-to-Speech Module
Converts text scripts to audio using edge_tts (Indian neural voices by default).
"""

import os
import asyncio
from typing import Optional
import edge_tts


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
        slow: Optional[bool] = None,
        voice_gender: str = "female"
    ) -> str:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert
            output_path: Path to save the audio file
            language: Language code (overrides default)
            slow: Slow speech flag (overrides default)
            voice_gender: Preferred gender for Indian neural voices ("female" or "male", defaults to "female")
            
        Returns:
            Path to the generated audio file using the selected language, speed, and voice gender.
        
        Examples:
            >>> tts = TextToSpeech()
            >>> tts.generate_speech("Hello", "out_female.mp3")
            'out_female.mp3'
            >>> tts.generate_speech("Hello", "out_male.mp3", voice_gender="male")
            'out_male.mp3'
        """
        lang = language or self.language
        is_slow = slow if slow is not None else self.slow
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Edge TTS with Indian neural voices (single, high-quality path)
        return self._generate_edge_voice(text, lang, output_path, is_slow, voice_gender)

    def _generate_edge_voice(self, text: str, language: str, output_path: str, slow: bool, voice_gender: str) -> str:
        """Generate speech using edge_tts Indian neural voices (hi/mr/en)."""

        voice_map = {
            "hi": {"female": "hi-IN-SwaraNeural", "male": "hi-IN-MadhurNeural"},
            "mr": {"female": "hi-IN-SwaraNeural", "male": "hi-IN-MadhurNeural"},
            "en": {"female": "en-IN-NeerjaNeural", "male": "en-IN-PrabhatNeural"},
        }

        gender = "male" if voice_gender.lower() == "male" else "female"
        voice = voice_map.get(language, voice_map["en"]).get(gender, "en-IN-NeerjaNeural")
        print(f"🎙️ Using Edge TTS voice '{voice}' (slow={slow})...")

        async def run_edge():
            communicate = edge_tts.Communicate(text, voice, rate="-20%" if slow else "+0%")
            await communicate.save(output_path)

        asyncio.run(run_edge())

        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print("✅ Edge TTS succeeded")
            return output_path

        raise RuntimeError(
            f"Edge TTS failed to generate valid output at {output_path}. "
            "Please verify the input text and voice settings."
        )
    
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
