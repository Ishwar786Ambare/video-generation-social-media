"""
Example: Facebook Upload
Demonstrates how to upload a video to Facebook
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator
from src.social_media import FacebookUploader


def main():
    # Step 1: Generate video
    print("Step 1: Generating video...")
    generator = VideoGenerator(output_dir="output_videos")
    
    script = """
    Hello Facebook! This is an automated video upload demonstration.
    We're using Python and the Facebook Graph API to automate video publishing.
    This makes content creation much more efficient.
    """
    
    video_path = generator.generate_video(
        script=script,
        title="facebook_auto_upload_demo",
        platform="facebook"
    )
    
    print(f"✅ Video generated: {video_path}")
    
    # Step 2: Upload to Facebook
    print("\nStep 2: Uploading to Facebook...")
    
    # Set your Facebook access token as environment variable
    # export FB_ACCESS_TOKEN="your_access_token_here"
    
    try:
        uploader = FacebookUploader()
        
        response = uploader.upload_video(
            video_path=video_path,
            title="Automated Video Upload Demo",
            description="This video was generated and uploaded automatically using Python!",
            # page_id="YOUR_PAGE_ID",  # Optional: specify to upload to a page
            published=True
        )
        
        print(f"\n✅ Upload successful!")
        print(f"Video ID: {response.get('id')}")
    
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\nTo upload to Facebook, you need to:")
        print("1. Create a Facebook App in Meta for Developers")
        print("2. Get a User Access Token or Page Access Token")
        print("3. Set FB_ACCESS_TOKEN environment variable")
        print("   export FB_ACCESS_TOKEN='your_token_here'")


if __name__ == "__main__":
    main()
