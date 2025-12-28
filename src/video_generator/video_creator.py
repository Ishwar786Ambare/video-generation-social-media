"""
Video creation using MoviePy.
"""
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip, 
    concatenate_videoclips, TextClip
)
from .image_processor import ImageProcessor
from .text_to_speech import TextToSpeech
import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoCreator:
    """Creates videos from news articles."""
    
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30):
        """Initialize video creator."""
        self.width = width
        self.height = height
        self.fps = fps
        self.image_processor = ImageProcessor(width, height)
        self.tts = TextToSpeech()
    
    def _ensure_directories(self, *dirs):
        """Ensure directories exist."""
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
    
    def create_news_video(self, articles: List[Dict], output_path: str,
                         duration_per_article: int = 10) -> str:
        """Create a video from news articles."""
        try:
            self._ensure_directories(os.path.dirname(output_path), "temp")
            
            clips = []
            
            for i, article in enumerate(articles):
                # Create text image for this article
                title = article.get('title', 'No title')
                description = article.get('description', '')
                
                # Truncate if too long
                if len(title) > 100:
                    title = title[:97] + "..."
                
                text = f"{title}"
                if description and len(description) < 150:
                    text += f"\n\n{description}"
                
                # Create image with text
                image_path = f"temp/article_{i}.png"
                self.image_processor.create_text_image(
                    text,
                    output_path=image_path,
                    font_size=50
                )
                
                # Create clip from image
                clip = ImageClip(image_path).set_duration(duration_per_article)
                clips.append(clip)
            
            # Concatenate all clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Generate audio narration
            audio_path = "temp/narration.mp3"
            self.tts.generate_from_articles(articles, audio_path)
            
            # Add audio to video
            if os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                # Trim or loop audio to match video duration
                if audio.duration < final_clip.duration:
                    # Video is longer, use video duration
                    final_clip = final_clip.set_audio(audio)
                else:
                    # Audio is longer, extend video or trim audio
                    final_clip = final_clip.set_audio(audio.subclip(0, final_clip.duration))
            
            # Write final video
            final_clip.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            final_clip.close()
            if os.path.exists(audio_path):
                audio.close()
            
            logger.info(f"Created video: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise
    
    def create_simple_video(self, title: str, description: str, output_path: str,
                           duration: int = 30) -> str:
        """Create a simple video with title and description."""
        try:
            self._ensure_directories(os.path.dirname(output_path), "temp")
            
            # Create background image
            bg_path = "temp/simple_bg.png"
            self.image_processor.create_background(output_path=bg_path)
            
            # Create text image
            text_path = "temp/simple_text.png"
            text = f"{title}\n\n{description}"
            self.image_processor.create_text_image(text, output_path=text_path)
            
            # Create video clip
            clip = ImageClip(text_path).set_duration(duration)
            
            # Generate audio
            audio_path = "temp/simple_audio.mp3"
            full_text = f"{title}. {description}"
            self.tts.generate_speech(full_text, audio_path)
            
            # Add audio
            if os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                clip = clip.set_audio(audio)
            
            # Write video
            clip.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            clip.close()
            if os.path.exists(audio_path):
                audio.close()
            
            logger.info(f"Created simple video: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating simple video: {e}")
            raise


if __name__ == "__main__":
    # Test video creator
    creator = VideoCreator()
    
    test_articles = [
        {
            'title': 'Breaking News: Technology Advances',
            'description': 'New developments in artificial intelligence are changing the world.'
        },
        {
            'title': 'Sports Update: Major Victory',
            'description': 'Local team wins championship in thrilling finale.'
        }
    ]
    
    output = "temp/test_video.mp4"
    creator.create_news_video(test_articles, output, duration_per_article=5)
    print(f"Created test video: {output}")
