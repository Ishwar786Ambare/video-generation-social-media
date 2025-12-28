"""
Example: Basic Video Generation
Demonstrates how to generate a simple video with text-to-speech
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator


def main():
    # Initialize video generator
    generator = VideoGenerator(output_dir="output_videos")
    
    # Define video script
    script = """
    Welcome to our automated video generation tutorial.
    In this video, we'll demonstrate how to create engaging content
    for social media platforms using Python.
    This is a powerful way to automate your content creation workflow
    and save hours of manual work.
    """
    
    # Generate video
    video_path = generator.generate_video(
        script=script,
        title="intro_video",
        platform="youtube"
    )
    
    print(f"\n✅ Video generated successfully!")
    print(f"📁 Location: {video_path}")


if __name__ == "__main__":
    main()
