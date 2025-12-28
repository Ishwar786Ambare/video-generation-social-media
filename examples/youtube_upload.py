"""
Example: YouTube Upload
Demonstrates how to upload a video to YouTube
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator
from src.social_media import YouTubeUploader


def main():
    # Step 1: Generate video
    print("Step 1: Generating video...")
    generator = VideoGenerator(output_dir="output_videos")
    
    script = """
    Hello YouTube! This is an automated video upload demonstration.
    We're using Python to generate and upload videos automatically.
    This can save hours of manual work in your content creation workflow.
    """
    
    video_path = generator.generate_video(
        script=script,
        title="youtube_auto_upload_demo",
        platform="youtube"
    )
    
    print(f"✅ Video generated: {video_path}")
    
    # Step 2: Upload to YouTube
    print("\nStep 2: Uploading to YouTube...")
    
    # Note: You need to set up OAuth2 credentials first
    # Download credentials from Google Cloud Console
    uploader = YouTubeUploader(
        credentials_path="credentials/youtube_credentials.json"
    )
    
    try:
        response = uploader.upload_video(
            video_path=video_path,
            title="Automated Video Upload Demo",
            description="This video was generated and uploaded automatically using Python!",
            tags=["automation", "python", "tutorial"],
            privacy_status="private"  # Change to "public" when ready
        )
        
        print(f"\n✅ Upload successful!")
        print(f"Video ID: {response['id']}")
    
    except FileNotFoundError as e:
        print(f"\n⚠️  {e}")
        print("\nTo upload to YouTube, you need to:")
        print("1. Create a project in Google Cloud Console")
        print("2. Enable YouTube Data API v3")
        print("3. Create OAuth2 credentials")
        print("4. Download credentials JSON file")
        print("5. Save it as credentials/youtube_credentials.json")


if __name__ == "__main__":
    main()
