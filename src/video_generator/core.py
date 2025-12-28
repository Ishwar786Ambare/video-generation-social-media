"""
Core Video Generator Module
Handles the main video generation workflow
"""

import os
from typing import Dict, List, Optional
from .text_to_speech import TextToSpeech
from .video_composer import VideoComposer
from .content_generator import ContentGenerator


class VideoGenerator:
    """Main class for generating videos for social media"""
    
    def __init__(self, output_dir: str = "output_videos", enable_ai: bool = False):
        """
        Initialize the Video Generator
        
        Args:
            output_dir: Directory to save generated videos
            enable_ai: Enable AI-powered content generation with Groq
        """
        self.output_dir = output_dir
        self.tts = TextToSpeech()
        self.composer = VideoComposer()
        self.content_generator = None
        
        if enable_ai:
            try:
                self.content_generator = ContentGenerator()
            except ValueError as e:
                print(f"Warning: AI content generation disabled - {e}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_video(
        self,
        script: str,
        title: str,
        images: Optional[List[str]] = None,
        background_music: Optional[str] = None,
        platform: str = "youtube",
        **kwargs
    ) -> str:
        """
        Generate a video from script and images
        
        Args:
            script: Text script for the video
            title: Video title
            images: List of image paths to include
            background_music: Path to background music file
            platform: Target platform (youtube, facebook, instagram)
            **kwargs: Additional platform-specific parameters
            
        Returns:
            Path to the generated video file
        """
        print(f"Generating video for {platform}...")
        
        # Get platform-specific settings
        settings = self._get_platform_settings(platform, **kwargs)
        
        # Generate audio from script
        print("Generating audio from script...")
        audio_path = self.tts.generate_speech(
            text=script,
            output_path=os.path.join(self.output_dir, f"{title}_audio.mp3")
        )
        
        # Compose video
        print("Composing video...")
        video_path = self.composer.create_video(
            audio_path=audio_path,
            images=images or [],
            output_path=os.path.join(self.output_dir, f"{title}.mp4"),
            background_music=background_music,
            **settings
        )
        
        print(f"Video generated successfully: {video_path}")
        return video_path
    
    def _get_platform_settings(self, platform: str, **kwargs) -> Dict:
        """
        Get platform-specific video settings
        
        Args:
            platform: Target platform name
            **kwargs: Override settings
            
        Returns:
            Dictionary of settings
        """
        # Default settings for each platform
        platform_defaults = {
            "youtube": {
                "resolution": (1920, 1080),
                "fps": 30,
                "aspect_ratio": "16:9"
            },
            "facebook": {
                "resolution": (1280, 720),
                "fps": 30,
                "aspect_ratio": "16:9"
            },
            "instagram": {
                "resolution": (1080, 1080),
                "fps": 30,
                "aspect_ratio": "1:1"
            }
        }
        
        settings = platform_defaults.get(platform.lower(), platform_defaults["youtube"])
        settings.update(kwargs)
        return settings
    
    def generate_video_from_topic(
        self,
        topic: str,
        title: str,
        duration: int = 60,
        style: str = "informative",
        images: Optional[List[str]] = None,
        background_music: Optional[str] = None,
        platform: str = "youtube",
        **kwargs
    ) -> Dict[str, str]:
        """
        Generate a complete video from a topic using AI content generation
        
        Args:
            topic: Main topic for the video
            title: Video title
            duration: Target duration in seconds
            style: Content style (informative, entertaining, educational, promotional)
            images: List of image paths to include
            background_music: Path to background music file
            platform: Target platform (youtube, facebook, instagram)
            **kwargs: Additional platform-specific parameters
            
        Returns:
            Dictionary containing video_path, script, and description
            
        Raises:
            RuntimeError: If AI content generation is not enabled
        """
        if not self.content_generator:
            raise RuntimeError(
                "AI content generation is not enabled. Initialize VideoGenerator with enable_ai=True"
            )
        
        print(f"Generating script for topic: {topic}...")
        script = self.content_generator.generate_script(
            topic=topic,
            duration=duration,
            style=style,
            platform=platform
        )
        
        print(f"Generating description...")
        description = self.content_generator.generate_description(
            script=script,
            platform=platform
        )
        
        print(f"Creating video...")
        video_path = self.generate_video(
            script=script,
            title=title,
            images=images,
            background_music=background_music,
            platform=platform,
            **kwargs
        )
        
        return {
            "video_path": video_path,
            "script": script,
            "description": description
        }
    
    def batch_generate(
        self,
        videos_config: List[Dict],
        platform: str = "youtube"
    ) -> List[str]:
        """
        Generate multiple videos in batch
        
        Args:
            videos_config: List of video configurations
            platform: Target platform
            
        Returns:
            List of generated video paths
        """
        generated_videos = []
        
        for idx, config in enumerate(videos_config):
            print(f"\nGenerating video {idx + 1}/{len(videos_config)}...")
            video_path = self.generate_video(
                script=config.get("script", ""),
                title=config.get("title", f"video_{idx}"),
                images=config.get("images"),
                background_music=config.get("background_music"),
                platform=platform,
                **config.get("settings", {})
            )
            generated_videos.append(video_path)
        
        return generated_videos
