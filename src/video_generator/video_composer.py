"""
Video Composer Module
Combines audio, images, and music into final video
"""

import os
from typing import List, Optional, Tuple
from moviepy.editor import (
    ImageClip, AudioFileClip, CompositeVideoClip,
    concatenate_videoclips, CompositeAudioClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class VideoComposer:
    """Composes videos from various media elements"""
    
    def __init__(self):
        """Initialize Video Composer"""
        pass
    
    def create_video(
        self,
        audio_path: str,
        images: List[str],
        output_path: str,
        background_music: Optional[str] = None,
        resolution: Tuple[int, int] = (1920, 1080),
        fps: int = 30,
        **kwargs
    ) -> str:
        """
        Create video from audio and images
        
        Args:
            audio_path: Path to audio file
            images: List of image paths
            output_path: Path to save the video
            background_music: Optional background music path
            resolution: Video resolution (width, height)
            fps: Frames per second
            **kwargs: Additional parameters
            
        Returns:
            Path to the generated video
        """
        # Load audio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        # Create video clips from images
        if images:
            video_clips = self._create_image_clips(
                images, duration, resolution, fps
            )
        else:
            # Create a default background if no images provided
            video_clips = [self._create_default_background(
                duration, resolution, fps
            )]
        
        # Combine video clips
        final_video = concatenate_videoclips(video_clips, method="compose")
        
        # Set audio
        if background_music:
            # Mix narration with background music
            bg_music = AudioFileClip(background_music).volumex(0.3)
            bg_music = bg_music.set_duration(duration)
            final_audio = CompositeAudioClip([audio, bg_music])
            final_video = final_video.set_audio(final_audio)
        else:
            final_video = final_video.set_audio(audio)
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write video file
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        # Clean up
        audio.close()
        final_video.close()
        if background_music:
            bg_music.close()
        
        return output_path
    
    def _create_image_clips(
        self,
        images: List[str],
        total_duration: float,
        resolution: Tuple[int, int],
        fps: int
    ) -> List[ImageClip]:
        """
        Create video clips from images
        
        Args:
            images: List of image paths
            total_duration: Total duration for all clips
            resolution: Target resolution
            fps: Frames per second
            
        Returns:
            List of ImageClip objects
        """
        clips = []
        duration_per_image = total_duration / len(images)
        
        for img_path in images:
            # Resize image to match resolution
            img = self._resize_image(img_path, resolution)
            
            # Create clip
            clip = ImageClip(img).set_duration(duration_per_image)
            clip = clip.set_fps(fps)
            clips.append(clip)
        
        return clips
    
    def _resize_image(
        self,
        image_path: str,
        target_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Resize image to target size maintaining aspect ratio
        
        Args:
            image_path: Path to image
            target_size: Target (width, height)
            
        Returns:
            Numpy array of resized image
        """
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        # Calculate scaling to fit within target size
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create a new image with target size and paste resized image
        new_img = Image.new('RGB', target_size, (0, 0, 0))
        paste_x = (target_size[0] - img.width) // 2
        paste_y = (target_size[1] - img.height) // 2
        new_img.paste(img, (paste_x, paste_y))
        
        return np.array(new_img)
    
    def _create_default_background(
        self,
        duration: float,
        resolution: Tuple[int, int],
        fps: int
    ) -> ImageClip:
        """
        Create a default background when no images are provided
        
        Args:
            duration: Clip duration
            resolution: Video resolution
            fps: Frames per second
            
        Returns:
            ImageClip with default background
        """
        # Create a gradient background
        img = Image.new('RGB', resolution, (30, 30, 50))
        draw = ImageDraw.Draw(img)
        
        # Add some visual interest with a gradient
        for i in range(resolution[1]):
            color_value = int(30 + (i / resolution[1]) * 40)
            draw.line([(0, i), (resolution[0], i)], 
                     fill=(color_value, color_value, color_value + 20))
        
        clip = ImageClip(np.array(img)).set_duration(duration)
        clip = clip.set_fps(fps)
        
        return clip
    
    def add_subtitles(
        self,
        video_path: str,
        subtitles: List[dict],
        output_path: str
    ) -> str:
        """
        Add subtitles to video
        
        Args:
            video_path: Path to input video
            subtitles: List of subtitle dicts with 'text', 'start', 'end'
            output_path: Path to save output video
            
        Returns:
            Path to video with subtitles
        """
        # This is a placeholder for subtitle functionality
        # In production, you'd use libraries like moviepy's TextClip
        print("Subtitle feature - requires additional implementation")
        return video_path
