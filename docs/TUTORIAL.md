# Complete Tutorial: Automated Video Generation for Social Media

## Introduction

This tutorial will guide you through creating an automated video generation and upload system for YouTube, Facebook, and Instagram using Python. By the end, you'll be able to generate professional videos from text scripts and automatically distribute them across multiple platforms.

## What You'll Learn

1. How to convert text to speech
2. How to compose videos from audio and images
3. How to optimize videos for different platforms
4. How to automate uploads to YouTube, Facebook, and Instagram
5. How to batch process multiple videos

## Prerequisites

- Python 3.8 or higher
- Basic Python programming knowledge
- FFmpeg installed on your system
- API credentials for platforms you want to use

## Part 1: Basic Video Generation

### Step 1: Setup

First, ensure you have the package installed:

```bash
pip install -r requirements.txt
```

### Step 2: Your First Video

Create a simple video from text:

```python
from src.video_generator import VideoGenerator

# Initialize the generator
generator = VideoGenerator(output_dir="my_videos")

# Write your script
script = """
Hello and welcome to my channel!
In this video, we'll explore automated video creation.
This is an exciting way to scale your content production.
Thanks for watching!
"""

# Generate the video
video_path = generator.generate_video(
    script=script,
    title="my_first_video",
    platform="youtube"
)

print(f"Video created at: {video_path}")
```

**What's happening:**
1. Text is converted to speech using gTTS
2. A video background is generated
3. Audio is synchronized with video
4. Final video is saved as MP4

### Step 3: Adding Images

Enhance your video with images:

```python
# Prepare your images
images = [
    "intro_slide.jpg",
    "feature1.png",
    "feature2.png",
    "outro_slide.jpg"
]

# Generate video with images
video_path = generator.generate_video(
    script=script,
    title="video_with_images",
    images=images,
    platform="youtube"
)
```

**Tips:**
- Images will display for equal durations
- Images are automatically resized to match video resolution
- Use high-quality images (1920x1080 or higher)

### Step 4: Background Music

Add background music for professional touch:

```python
video_path = generator.generate_video(
    script=script,
    title="video_with_music",
    images=images,
    background_music="background.mp3",
    platform="youtube"
)
```

**Notes:**
- Background music volume is automatically reduced (30%)
- Music is looped/trimmed to match video duration
- Use royalty-free music to avoid copyright issues

## Part 2: Platform-Specific Optimization

### YouTube Videos

YouTube prefers 16:9 aspect ratio, high resolution:

```python
video_path = generator.generate_video(
    script=script,
    title="youtube_video",
    platform="youtube",
    resolution=(1920, 1080),  # Full HD
    fps=30
)
```

**Best practices:**
- Use 1080p or 4K resolution
- Keep 16:9 aspect ratio
- Add engaging thumbnails after upload

### Facebook Videos

Facebook works well with 720p:

```python
video_path = generator.generate_video(
    script=script,
    title="facebook_video",
    platform="facebook",
    resolution=(1280, 720),
    fps=30
)
```

**Best practices:**
- 720p is often sufficient
- Consider both 16:9 and 1:1 formats
- Add captions for better engagement

### Instagram Videos

Instagram prefers square or vertical formats:

```python
# Square format (feed)
video_path = generator.generate_video(
    script=script,
    title="instagram_feed",
    platform="instagram",
    resolution=(1080, 1080)  # Square
)

# Vertical format (Reels/Stories)
video_path = generator.generate_video(
    script=script,
    title="instagram_reel",
    platform="instagram",
    resolution=(1080, 1920)  # 9:16
)
```

**Best practices:**
- Keep videos under 60 seconds for feed
- Use 9:16 for Reels and Stories
- Make content mobile-friendly

## Part 3: Uploading to Social Media

### YouTube Upload

#### Setup YouTube API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth2 credentials (Desktop app)
5. Download credentials JSON
6. Save as `credentials/youtube_credentials.json`

#### Upload Code

```python
from src.social_media import YouTubeUploader

# Initialize uploader
uploader = YouTubeUploader(
    credentials_path="credentials/youtube_credentials.json"
)

# Upload video
response = uploader.upload_video(
    video_path="my_videos/youtube_video.mp4",
    title="My Automated Video",
    description="This video was created using Python automation!",
    tags=["automation", "python", "tutorial"],
    category="22",  # People & Blogs
    privacy_status="public"  # or "private", "unlisted"
)

print(f"Video uploaded! ID: {response['id']}")
print(f"Watch at: https://www.youtube.com/watch?v={response['id']}")
```

#### Update Video Metadata

```python
uploader.update_video(
    video_id=response['id'],
    title="Updated Title",
    description="Updated description",
    tags=["new", "tags"]
)
```

### Facebook Upload

#### Setup Facebook API

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app (Business type)
3. Generate User Access Token or Page Access Token
4. Grant permissions: `pages_manage_posts`, `pages_read_engagement`
5. Set access token as environment variable

```bash
export FB_ACCESS_TOKEN="your_access_token"
```

#### Upload Code

```python
from src.social_media import FacebookUploader

# Initialize uploader (uses FB_ACCESS_TOKEN env var)
uploader = FacebookUploader()

# Upload to profile
response = uploader.upload_video(
    video_path="my_videos/facebook_video.mp4",
    title="My Automated Video",
    description="Check out this automated video!",
    published=True
)

# Upload to page
response = uploader.upload_video(
    video_path="my_videos/facebook_video.mp4",
    title="My Automated Video",
    description="Check out this automated video!",
    page_id="YOUR_PAGE_ID",
    published=True
)

print(f"Video uploaded! ID: {response['id']}")
```

#### Get Video Analytics

```python
insights = uploader.get_video_insights(video_id)
print(f"Video insights: {insights}")
```

### Instagram Upload

#### Setup Instagram

Set your credentials as environment variables:

```bash
export IG_USERNAME="your_username"
export IG_PASSWORD="your_password"
```

**Note:** If 2FA is enabled, use an app-specific password.

#### Upload Code

```python
from src.social_media import InstagramUploader

# Initialize uploader
uploader = InstagramUploader()

# Upload to feed
media = uploader.upload_video(
    video_path="my_videos/instagram_feed.mp4",
    caption="""
    🎬 Check out this automated video!
    
    Created with Python automation 🐍
    
    #automation #python #socialmedia #contentcreation
    """
)

print(f"Posted! View at: https://www.instagram.com/p/{media.code}/")
```

#### Upload as Reel

```python
media = uploader.upload_reel(
    video_path="my_videos/instagram_reel.mp4",
    caption="Amazing automated content! 🚀 #reels #automation"
)
```

#### Upload as Story

```python
media = uploader.upload_story(
    video_path="my_videos/instagram_story.mp4",
    caption="Check this out! 👀"
)
```

## Part 4: Batch Processing

### Generate Multiple Videos

```python
from src.video_generator import VideoGenerator

generator = VideoGenerator()

# Define multiple video configurations
videos_config = [
    {
        "title": "monday_motivation",
        "script": "Happy Monday! Start your week strong with these tips...",
        "images": ["monday1.jpg", "monday2.jpg"],
        "platform": "youtube"
    },
    {
        "title": "tuesday_tutorial",
        "script": "Welcome to Tuesday's tutorial. Today we'll learn...",
        "images": ["tutorial1.jpg", "tutorial2.jpg"],
        "platform": "youtube"
    },
    {
        "title": "wednesday_wisdom",
        "script": "Wednesday wisdom: Here are three key insights...",
        "images": ["wisdom1.jpg", "wisdom2.jpg"],
        "platform": "youtube"
    }
]

# Generate all videos
video_paths = generator.batch_generate(videos_config)

print(f"Generated {len(video_paths)} videos!")
```

### Automated Upload Pipeline

Complete automation: generate and upload:

```python
from src.video_generator import VideoGenerator
from src.social_media import YouTubeUploader, FacebookUploader, InstagramUploader

# Initialize
generator = VideoGenerator()
yt_uploader = YouTubeUploader()
fb_uploader = FacebookUploader()
ig_uploader = InstagramUploader()

# Generate video
video_path = generator.generate_video(
    script="Your daily content update!",
    title="daily_update",
    platform="youtube"
)

# Upload to all platforms
yt_response = yt_uploader.upload_video(
    video_path=video_path,
    title="Daily Update",
    description="Your daily dose of awesome content!"
)

fb_response = fb_uploader.upload_video(
    video_path=video_path,
    title="Daily Update",
    description="Your daily dose of awesome content!"
)

ig_media = ig_uploader.upload_video(
    video_path=video_path,
    caption="Daily Update! #content"
)

print("Video uploaded to all platforms! 🎉")
```

## Part 5: Advanced Techniques

### Custom Text-to-Speech

```python
from src.video_generator.text_to_speech import TextToSpeech

tts = TextToSpeech(language="en", slow=False)

# Generate audio
audio_path = tts.generate_speech(
    text="Your custom text",
    output_path="output/custom_audio.mp3",
    language="es"  # Spanish
)
```

### Custom Video Composition

```python
from src.video_generator.video_composer import VideoComposer

composer = VideoComposer()

video_path = composer.create_video(
    audio_path="audio.mp3",
    images=["img1.jpg", "img2.jpg"],
    output_path="custom_video.mp4",
    background_music="music.mp3",
    resolution=(1920, 1080),
    fps=60  # High frame rate
)
```

### Environment Variables Setup

Create a `.env` file:

```bash
# YouTube
YOUTUBE_CREDENTIALS_PATH=credentials/youtube_credentials.json

# Facebook
FB_ACCESS_TOKEN=your_token
FB_PAGE_ID=your_page_id

# Instagram
IG_USERNAME=your_username
IG_PASSWORD=your_password

# Settings
OUTPUT_DIR=output_videos
TTS_LANGUAGE=en
```

Load in your script:

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Use environment variables
output_dir = os.getenv('OUTPUT_DIR', 'output_videos')
```

## Best Practices

### 1. Content Quality
- Write clear, engaging scripts
- Use high-quality images (min 1080p)
- Use royalty-free music
- Test videos before mass deployment

### 2. Platform Compliance
- Follow each platform's Terms of Service
- Respect copyright laws
- Don't spam or post duplicate content
- Use appropriate content ratings

### 3. Optimization
- Use appropriate resolutions for each platform
- Optimize file sizes (compress if needed)
- Add relevant tags and descriptions
- Use eye-catching thumbnails

### 4. Security
- Never commit credentials to version control
- Use environment variables for secrets
- Rotate access tokens regularly
- Use app-specific passwords for Instagram

### 5. Scheduling
- Use cron jobs or task schedulers for automation
- Spread out uploads to avoid rate limits
- Monitor API quotas
- Handle errors gracefully

## Troubleshooting

### Video Generation Issues

**Problem:** FFmpeg not found
**Solution:** Install FFmpeg and add to system PATH

**Problem:** Poor audio quality
**Solution:** Use clearer scripts, adjust TTS settings

### Upload Issues

**Problem:** YouTube authentication fails
**Solution:** Re-download credentials, check OAuth permissions

**Problem:** Facebook upload rejected
**Solution:** Verify video format, check access token permissions

**Problem:** Instagram challenge required
**Solution:** Login manually first, use app-specific password

## Next Steps

1. Experiment with different video styles
2. Create templates for recurring content
3. Set up scheduled automation
4. Monitor analytics and engagement
5. Iterate based on performance data

## Resources

- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api)

## Conclusion

You now have a complete system for automated video generation and distribution! Start small, test thoroughly, and scale up your content creation workflow.

Happy automating! 🚀
