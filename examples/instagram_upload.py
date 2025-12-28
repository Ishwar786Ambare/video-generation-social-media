"""
Example: Instagram Upload
Demonstrates how to upload a video to Instagram
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator
from src.social_media import InstagramUploader


def main():
    # Step 1: Generate video
    print("Step 1: Generating video...")
    generator = VideoGenerator(output_dir="output_videos")
    
    script = """
    Hello Instagram! This is an automated video upload demonstration.
    We're using Python to create and publish content automatically.
    Perfect for maintaining a consistent posting schedule.
    """
    
    # Instagram prefers square or vertical videos
    video_path = generator.generate_video(
        script=script,
        title="instagram_auto_upload_demo",
        platform="instagram"
    )
    
    print(f"✅ Video generated: {video_path}")
    
    # Step 2: Upload to Instagram
    print("\nStep 2: Uploading to Instagram...")
    
    # Set your Instagram credentials as environment variables
    # export IG_USERNAME="your_username"
    # export IG_PASSWORD="your_password"
    
    try:
        uploader = InstagramUploader()
        
        caption = """
        🎥 Automated Video Upload Demo
        
        This video was generated and uploaded automatically using Python! 🐍
        
        Perfect for content creators who want to automate their workflow.
        
        #automation #python #contentcreation #socialmedia
        """
        
        # Upload as regular post
        media = uploader.upload_video(
            video_path=video_path,
            caption=caption
        )
        
        # Or upload as Reel (uncomment to use)
        # media = uploader.upload_reel(
        #     video_path=video_path,
        #     caption=caption
        # )
        
        print(f"\n✅ Upload successful!")
        print(f"Media ID: {media.pk}")
        print(f"View at: https://www.instagram.com/p/{media.code}/")
    
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\nTo upload to Instagram, you need to:")
        print("1. Set environment variables:")
        print("   export IG_USERNAME='your_username'")
        print("   export IG_PASSWORD='your_password'")
        print("\n⚠️  Note: Use an app-specific password if you have 2FA enabled")


if __name__ == "__main__":
    main()
