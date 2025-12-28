"""
Example: Batch Video Generation
Generate multiple videos at once
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator


def main():
    # Initialize video generator
    generator = VideoGenerator(output_dir="output_videos")
    
    # Define multiple video configurations
    videos_config = [
        {
            "title": "video_1_intro",
            "script": "Welcome to our first automated video. This demonstrates batch processing.",
            "platform": "youtube"
        },
        {
            "title": "video_2_features",
            "script": "In this video, we showcase the amazing features of our automation system.",
            "platform": "facebook"
        },
        {
            "title": "video_3_conclusion",
            "script": "Thank you for watching our automated video series. Stay tuned for more!",
            "platform": "instagram"
        }
    ]
    
    # Generate all videos
    print("Starting batch video generation...")
    video_paths = generator.batch_generate(
        videos_config=videos_config,
        platform="youtube"  # Default platform
    )
    
    print(f"\n✅ Generated {len(video_paths)} videos successfully!")
    for idx, path in enumerate(video_paths, 1):
        print(f"{idx}. {path}")


if __name__ == "__main__":
    main()
