"""
Video Generator Package
Automated video generation for social media platforms
"""

__version__ = "1.0.0"
__author__ = "Video Generation Team"

from .core import VideoGenerator
from .text_to_speech import TextToSpeech
from .video_composer import VideoComposer

__all__ = ['VideoGenerator', 'TextToSpeech', 'VideoComposer']
