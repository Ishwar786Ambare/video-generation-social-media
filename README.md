# 🎬 Automated Video Generation for Social Media

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Groq](https://img.shields.io/badge/AI-Groq-brightgreen.svg)](https://groq.com/)

A comprehensive Python toolkit for **automated video generation and distribution** across YouTube, Facebook, and Instagram. Create engaging videos from text scripts with AI-powered content generation, text-to-speech, image composition, and automated uploads to social media platforms.

## ✨ Features

- 🤖 **AI Content Generation**: Generate video scripts and ideas using Groq AI (replaces Gemini)
- 🎤 **Text-to-Speech**: Convert scripts to natural-sounding audio using gTTS
- 🎨 **Video Composition**: Combine images, audio, and background music
- 📱 **Multi-Platform Support**: Upload to YouTube, Facebook, and Instagram
- ⚙️ **Platform Optimization**: Automatic resolution and format adjustments
- 🔄 **Batch Processing**: Generate multiple videos at once
- 💡 **Smart Content**: AI-powered script enhancement and video ideas
- 🎯 **Easy Configuration**: Simple, intuitive API

## 🆕 NEW: Groq AI Integration

This project now uses **Groq AI** for lightning-fast content generation! No more Gemini dependency.

- ⚡ Super fast inference speeds
- 🎯 High-quality content generation
- 💰 Generous free tier
- 🔧 Easy to configure

See the [Groq Guide](docs/GROQ_GUIDE.md) for detailed setup instructions.

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [AI Content Generation](#ai-content-generation)
- [Video Generation](#video-generation)
- [Social Media Upload](#social-media-upload)
  - [YouTube](#youtube-upload)
  - [Facebook](#facebook-upload)
  - [Instagram](#instagram-upload)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (required for video processing)
- Groq API Key (free at https://console.groq.com/)

#### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add to PATH.

### Install Package

1. Clone the repository:
```bash
git clone https://github.com/Ishwar786Ambare/video-generation-social-media.git
cd video-generation-social-media
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys (especially GROQ_API_KEY)
```

## 🎯 Quick Start

### Option 1: AI-Powered Video Generation (NEW!)

```python
from src.video_generator import VideoGenerator

# Initialize with AI enabled
generator = VideoGenerator(enable_ai=True)

# Generate video from just a topic - AI does the rest!
result = generator.generate_video_from_topic(
    topic="The benefits of morning exercise",
    title="morning_exercise",
    duration=60,
    style="informative",
    platform="youtube"
)

print(f"Video: {result['video_path']}")
print(f"AI-Generated Script: {result['script']}")
print(f"AI-Generated Description: {result['description']}")
```

### Option 2: Traditional Manual Script

```python
from src.video_generator import VideoGenerator

# Initialize generator
generator = VideoGenerator(output_dir="output_videos")

# Define your script
script = """
Welcome to automated video generation!
This is a demo of creating videos with Python.
It's simple, fast, and powerful.
"""

# Generate video
video_path = generator.generate_video(
    script=script,
    title="my_first_video",
    platform="youtube"
)

print(f"Video created: {video_path}")
```

## 🤖 AI Content Generation

### Generate Video Ideas

```python
from src.video_generator.content_generator import ContentGenerator

content_gen = ContentGenerator()

# Get AI-generated video ideas
ideas = content_gen.generate_video_ideas(
    niche="productivity tips",
    count=5,
    platform="youtube"
)

for idea in ideas:
    print(f"{idea['title']}: {idea['description']}")
```

### Generate Custom Scripts

```python
# Generate a script from a topic
script = content_gen.generate_script(
    topic="5 morning habits for success",
    duration=90,
    style="motivational",
    platform="instagram"
)

# Enhance existing scripts
enhanced = content_gen.enhance_script(
    script=script,
    enhancement_type="engagement"  # engagement, clarity, emotion, brevity
)
```

For more AI features, see [docs/GROQ_GUIDE.md](docs/GROQ_GUIDE.md)

## 🎬 Video Generation

### Basic Video Generation

```python
from src.video_generator import VideoGenerator

generator = VideoGenerator()

video_path = generator.generate_video(
    script="Your video script here",
    title="video_title",
    platform="youtube"  # or "facebook", "instagram"
)
```

### Video with Images

```python
video_path = generator.generate_video(
    script="Your narration script",
    title="image_slideshow",
    images=[
        "path/to/image1.jpg",
        "path/to/image2.jpg",
        "path/to/image3.jpg"
    ],
    platform="youtube"
)
```

### Video with Background Music

```python
video_path = generator.generate_video(
    script="Your script",
    title="video_with_music",
    images=["image1.jpg", "image2.jpg"],
    background_music="path/to/music.mp3",
    platform="youtube"
)
```

### Platform-Specific Settings

```python
# YouTube - 16:9, 1080p
video_path = generator.generate_video(
    script="YouTube video",
    title="yt_video",
    platform="youtube",
    resolution=(1920, 1080),
    fps=30
)

# Instagram - Square, 1080x1080
video_path = generator.generate_video(
    script="Instagram video",
    title="ig_video",
    platform="instagram",
    resolution=(1080, 1080)
)

# Facebook - 16:9, 720p
video_path = generator.generate_video(
    script="Facebook video",
    title="fb_video",
    platform="facebook",
    resolution=(1280, 720)
)
```

### Batch Generation

```python
videos_config = [
    {
        "title": "video_1",
        "script": "First video script",
        "images": ["img1.jpg"]
    },
    {
        "title": "video_2",
        "script": "Second video script",
        "images": ["img2.jpg"]
    }
]

video_paths = generator.batch_generate(
    videos_config=videos_config,
    platform="youtube"
)
```

## 📤 Social Media Upload

### YouTube Upload

#### Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials
5. Download credentials JSON file
6. Save as `credentials/youtube_credentials.json`

#### Upload Code

```python
from src.social_media import YouTubeUploader

uploader = YouTubeUploader(
    credentials_path="credentials/youtube_credentials.json"
)

response = uploader.upload_video(
    video_path="output_videos/my_video.mp4",
    title="My Awesome Video",
    description="Video description here",
    tags=["python", "automation", "tutorial"],
    privacy_status="public"  # or "private", "unlisted"
)

print(f"Video ID: {response['id']}")
print(f"Watch at: https://www.youtube.com/watch?v={response['id']}")
```

### Facebook Upload

#### Setup

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app
3. Get User Access Token or Page Access Token
4. Set environment variable:
```bash
export FB_ACCESS_TOKEN="your_access_token_here"
```

#### Upload Code

```python
from src.social_media import FacebookUploader

uploader = FacebookUploader()  # Reads from FB_ACCESS_TOKEN env var

response = uploader.upload_video(
    video_path="output_videos/my_video.mp4",
    title="My Video Title",
    description="Video description",
    page_id="YOUR_PAGE_ID",  # Optional: for page uploads
    published=True
)

print(f"Video ID: {response['id']}")
```

### Instagram Upload

#### Setup

Set your Instagram credentials:
```bash
export IG_USERNAME="your_username"
export IG_PASSWORD="your_password"
```

**Note:** If you have 2FA enabled, use an app-specific password.

#### Upload Code

```python
from src.social_media import InstagramUploader

uploader = InstagramUploader()

# Upload as feed video
media = uploader.upload_video(
    video_path="output_videos/my_video.mp4",
    caption="Check out this automated video! #automation #python"
)

# Upload as Reel
media = uploader.upload_reel(
    video_path="output_videos/my_video.mp4",
    caption="My awesome reel! 🎬"
)

# Upload as Story
media = uploader.upload_story(
    video_path="output_videos/my_video.mp4",
    caption="Story time! 📱"
)

print(f"View at: https://www.instagram.com/p/{media.code}/")
```

## 📚 Examples

Check the `examples/` directory for complete working examples:

- `basic_video_generation.py` - Simple video creation
- `video_with_images.py` - Video with image slideshow
- `youtube_upload.py` - Complete YouTube workflow
- `facebook_upload.py` - Complete Facebook workflow
- `instagram_upload.py` - Complete Instagram workflow
- `batch_generation.py` - Generate multiple videos

Run any example:
```bash
python examples/basic_video_generation.py
```

## 📖 API Reference

### VideoGenerator

```python
VideoGenerator(output_dir="output_videos")
```

**Methods:**

- `generate_video(script, title, images=None, background_music=None, platform="youtube", **kwargs)` - Generate a single video
- `batch_generate(videos_config, platform="youtube")` - Generate multiple videos

### YouTubeUploader

```python
YouTubeUploader(credentials_path="credentials/youtube_credentials.json")
```

**Methods:**

- `authenticate()` - Authenticate with YouTube API
- `upload_video(video_path, title, description="", category="22", privacy_status="private", tags=None)` - Upload video
- `update_video(video_id, title=None, description=None, tags=None)` - Update video metadata

### FacebookUploader

```python
FacebookUploader(access_token=None)
```

**Methods:**

- `upload_video(video_path, title, description="", page_id=None, published=True)` - Upload video
- `upload_video_resumable(video_path, title, description="", page_id=None)` - Upload large videos
- `get_video_insights(video_id)` - Get video analytics
- `delete_video(video_id)` - Delete video

### InstagramUploader

```python
InstagramUploader(username=None, password=None)
```

**Methods:**

- `login()` - Login to Instagram
- `upload_video(video_path, caption="", thumbnail_path=None)` - Upload feed video
- `upload_reel(video_path, caption="", thumbnail_path=None)` - Upload Reel
- `upload_story(video_path, caption="")` - Upload Story
- `upload_igtv(video_path, title, caption="", thumbnail_path=None)` - Upload IGTV
- `get_media_info(media_id)` - Get media statistics

## ⚙️ Configuration

### Platform Settings

Each platform has optimized default settings:

| Platform  | Resolution  | Aspect Ratio | FPS |
|-----------|-------------|--------------|-----|
| YouTube   | 1920x1080   | 16:9         | 30  |
| Facebook  | 1280x720    | 16:9         | 30  |
| Instagram | 1080x1080   | 1:1          | 30  |

### Environment Variables

Create a `.env` file in the project root:

```bash
# YouTube
YOUTUBE_CREDENTIALS_PATH=credentials/youtube_credentials.json

# Facebook
FB_ACCESS_TOKEN=your_facebook_access_token

# Instagram
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🔧 Troubleshooting

### Common Issues

**1. FFmpeg not found**
```
Error: MoviePy requires FFmpeg
```
Solution: Install FFmpeg (see Installation section)

**2. YouTube authentication fails**
```
Error: Credentials file not found
```
Solution: Download OAuth2 credentials from Google Cloud Console

**3. Instagram login fails**
```
Error: Challenge required
```
Solution: Login manually from the same IP first, or use app-specific password with 2FA

**4. Facebook upload fails**
```
Error: Invalid access token
```
Solution: Generate a new access token with proper permissions

### Getting Help

- Check the [examples/](examples/) directory for working code
- Review error messages carefully
- Ensure all API credentials are properly configured

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

- Use this tool responsibly and comply with each platform's Terms of Service
- Respect rate limits and API quotas
- Don't spam or post inappropriate content
- YouTube, Facebook, and Instagram are trademarks of their respective owners

## 🙏 Acknowledgments

- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [gTTS](https://github.com/pndurette/gTTS) - Text-to-speech
- [Instagrapi](https://github.com/adw0rd/instagrapi) - Instagram API
- Google YouTube Data API
- Facebook Graph API

## 📞 Support

For questions and support, please open an issue on GitHub.

---

**Happy video generating! 🎬**