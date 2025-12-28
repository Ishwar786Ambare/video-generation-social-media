"""
Video Generator Package
Automated video generation for social media platforms with AI-powered content generation
"""

__version__ = "2.0.0"
__author__ = "Video Generation Team"

from .core import VideoGenerator
from .text_to_speech import TextToSpeech
from .video_composer import VideoComposer
from .content_generator import ContentGenerator

__all__ = ['VideoGenerator', 'TextToSpeech', 'VideoComposer', 'ContentGenerator']
