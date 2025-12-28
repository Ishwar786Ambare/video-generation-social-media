"""
Text-to-speech generation for video narration.
"""
from gtts import gTTS
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextToSpeech:
    """Generates speech audio from text."""
    
    def __init__(self, language: str = 'en', slow: bool = False):
        """Initialize TTS engine."""
        self.language = language
        self.slow = slow
    
    def generate_speech(self, text: str, output_path: str) -> str:
        """Generate speech audio file from text."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generate speech
            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            tts.save(output_path)
            
            logger.info(f"Generated speech audio: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            raise
    
    def generate_from_articles(self, articles: list, output_path: str) -> str:
        """Generate speech from multiple news articles."""
        text_parts = []
        
        for i, article in enumerate(articles):
            # Add intro for each article
            text_parts.append(f"News story {i + 1}.")
            text_parts.append(article.get('title', ''))
            
            # Add description if available
            description = article.get('description', '')
            if description:
                text_parts.append(description)
        
        full_text = ' '.join(text_parts)
        return self.generate_speech(full_text, output_path)


if __name__ == "__main__":
    # Test text-to-speech
    tts = TextToSpeech()
    test_text = "This is a test of the text to speech system. It will generate audio for news videos."
    output = "temp/test_speech.mp3"
    tts.generate_speech(test_text, output)
    print(f"Generated test audio: {output}")
