"""
Example: Video Generation with Images
Demonstrates how to create a video with images and background music
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
    Welcome to our product showcase.
    Today we're presenting our latest features and updates.
    These improvements will enhance your experience significantly.
    Let's dive into what's new and exciting.
    """
    
    # List of image paths (you would provide your own images)
    # For demo purposes, these paths should be replaced with actual images
    images = [
        # "path/to/image1.jpg",
        # "path/to/image2.jpg",
        # "path/to/image3.jpg",
    ]
    
    # Background music path (optional)
    # background_music = "path/to/music.mp3"
    
    # Generate video
    video_path = generator.generate_video(
        script=script,
        title="product_showcase",
        images=images if images else None,
        # background_music=background_music,
        platform="youtube"
    )
    
    print(f"\n✅ Video generated successfully!")
    print(f"📁 Location: {video_path}")


if __name__ == "__main__":
    main()
