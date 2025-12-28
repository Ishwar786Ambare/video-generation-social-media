"""
Complete Automation Script
Demonstrates full workflow: generate and upload to all platforms
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator
from src.social_media import YouTubeUploader, FacebookUploader, InstagramUploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """
    Complete automation workflow:
    1. Generate a video
    2. Upload to YouTube
    3. Upload to Facebook
    4. Upload to Instagram
    """
    
    print("=" * 60)
    print("AUTOMATED VIDEO GENERATION & UPLOAD")
    print("=" * 60)
    
    # Step 1: Generate Video
    print("\n[1/4] Generating video...")
    print("-" * 60)
    
    generator = VideoGenerator(output_dir="output_videos")
    
    script = """
    Welcome to our automated content creation system!
    This video was generated and uploaded completely automatically.
    Using Python, we can create engaging videos at scale.
    Subscribe for more automation tips and tricks.
    Thanks for watching!
    """
    
    # Generate for multiple platforms
    videos = {}
    
    # YouTube version (16:9)
    print("Generating YouTube version (1920x1080)...")
    videos['youtube'] = generator.generate_video(
        script=script,
        title="automated_video_youtube",
        platform="youtube",
        resolution=(1920, 1080)
    )
    print(f"✅ YouTube video: {videos['youtube']}")
    
    # Facebook version (16:9)
    print("\nGenerating Facebook version (1280x720)...")
    videos['facebook'] = generator.generate_video(
        script=script,
        title="automated_video_facebook",
        platform="facebook",
        resolution=(1280, 720)
    )
    print(f"✅ Facebook video: {videos['facebook']}")
    
    # Instagram version (1:1)
    print("\nGenerating Instagram version (1080x1080)...")
    videos['instagram'] = generator.generate_video(
        script=script,
        title="automated_video_instagram",
        platform="instagram",
        resolution=(1080, 1080)
    )
    print(f"✅ Instagram video: {videos['instagram']}")
    
    # Step 2: Upload to YouTube (optional)
    print("\n[2/4] Uploading to YouTube...")
    print("-" * 60)
    try:
        yt_uploader = YouTubeUploader()
        yt_response = yt_uploader.upload_video(
            video_path=videos['youtube'],
            title="Automated Video Generation Demo",
            description="""
            This video was created using automated video generation with Python!
            
            Learn more about video automation at our channel.
            
            #automation #python #videocreation
            """,
            tags=["automation", "python", "tutorial", "video creation"],
            privacy_status="private"  # Change to "public" when ready
        )
        print(f"✅ YouTube upload successful!")
        print(f"   Video ID: {yt_response['id']}")
        print(f"   URL: https://www.youtube.com/watch?v={yt_response['id']}")
    except Exception as e:
        print(f"⚠️  YouTube upload skipped: {e}")
        print("   Set up credentials to enable YouTube uploads")
    
    # Step 3: Upload to Facebook (optional)
    print("\n[3/4] Uploading to Facebook...")
    print("-" * 60)
    try:
        fb_uploader = FacebookUploader()
        fb_response = fb_uploader.upload_video(
            video_path=videos['facebook'],
            title="Automated Video Generation Demo",
            description="""
            Check out this video created with automated video generation!
            
            Learn how to automate your content creation with Python.
            
            #automation #python #socialmedia
            """,
            published=True
        )
        print(f"✅ Facebook upload successful!")
        print(f"   Video ID: {fb_response.get('id')}")
    except Exception as e:
        print(f"⚠️  Facebook upload skipped: {e}")
        print("   Set FB_ACCESS_TOKEN environment variable to enable")
    
    # Step 4: Upload to Instagram (optional)
    print("\n[4/4] Uploading to Instagram...")
    print("-" * 60)
    try:
        ig_uploader = InstagramUploader()
        
        caption = """
        🎬 Automated Video Creation! 
        
        This video was generated completely automatically using Python! 🐍
        
        Perfect for content creators who want to scale their production.
        
        #automation #python #contentcreation #videoproduction #socialmedia #tech
        """
        
        ig_media = ig_uploader.upload_video(
            video_path=videos['instagram'],
            caption=caption
        )
        print(f"✅ Instagram upload successful!")
        print(f"   Media ID: {ig_media.pk}")
        print(f"   URL: https://www.instagram.com/p/{ig_media.code}/")
    except Exception as e:
        print(f"⚠️  Instagram upload skipped: {e}")
        print("   Set IG_USERNAME and IG_PASSWORD environment variables to enable")
    
    # Summary
    print("\n" + "=" * 60)
    print("AUTOMATION COMPLETE!")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"   Videos generated: {len(videos)}")
    print(f"   YouTube: {videos['youtube']}")
    print(f"   Facebook: {videos['facebook']}")
    print(f"   Instagram: {videos['instagram']}")
    print("\n💡 Next steps:")
    print("   1. Review generated videos in output_videos/")
    print("   2. Set up API credentials for uploads")
    print("   3. Customize scripts for your content")
    print("   4. Schedule automatic runs with cron/Task Scheduler")
    print("\n🎉 Happy automating!")


if __name__ == "__main__":
    main()
