# Quick Start Guide

Get started with automated video generation in 5 minutes!

## 1. Install Dependencies

```bash
# Install FFmpeg first (required)
# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Then install Python dependencies
pip install -r requirements.txt
```

## 2. Generate Your First Video

Create a file `test_video.py`:

```python
from src.video_generator import VideoGenerator

# Initialize generator
generator = VideoGenerator(output_dir="output_videos")

# Define your script
script = """
Welcome to automated video generation!
This is a quick demonstration of the system.
You can create videos from text in seconds.
Thanks for watching!
"""

# Generate video
video_path = generator.generate_video(
    script=script,
    title="my_first_video",
    platform="youtube"
)

print(f"✅ Success! Video saved to: {video_path}")
```

Run it:
```bash
python test_video.py
```

## 3. Upload to YouTube (Optional)

### Setup YouTube API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable YouTube Data API v3
3. Create OAuth credentials → Download JSON
4. Save as `credentials/youtube_credentials.json`

### Upload Code
```python
from src.social_media import YouTubeUploader

uploader = YouTubeUploader()
uploader.upload_video(
    video_path="output_videos/my_first_video.mp4",
    title="My First Automated Video",
    description="Created with Python!",
    tags=["automation", "python"],
    privacy_status="private"  # Start with private!
)
```

## 4. Explore Examples

```bash
# See all examples
ls examples/

# Run basic generation
python examples/basic_video_generation.py

# Run batch generation
python examples/batch_generation.py
```

## 5. Customize

### Different Platforms
```python
# YouTube (16:9, 1080p)
generator.generate_video(script, title, platform="youtube")

# Facebook (16:9, 720p)
generator.generate_video(script, title, platform="facebook")

# Instagram (1:1, 1080x1080)
generator.generate_video(script, title, platform="instagram")
```

### Add Images
```python
generator.generate_video(
    script=script,
    title="video_with_images",
    images=["image1.jpg", "image2.jpg", "image3.jpg"],
    platform="youtube"
)
```

### Add Background Music
```python
generator.generate_video(
    script=script,
    title="video_with_music",
    background_music="background.mp3",
    platform="youtube"
)
```

## Next Steps

- 📖 Read the [Complete Tutorial](docs/TUTORIAL.md)
- 📚 Check the [API Documentation](docs/API.md)
- ⚙️ Follow the [Setup Guide](docs/SETUP.md)
- 🔍 Browse [Examples](examples/)

## Common Issues

**FFmpeg not found?**
```bash
# Check if installed
ffmpeg -version

# If not, install it (see step 1)
```

**Import errors?**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt
```

**No audio in video?**
- Check your script isn't empty
- Verify internet connection (gTTS needs it)

**Upload fails?**
- Check credentials are properly set up
- Verify API permissions
- Check environment variables

## Getting Help

- Check [Troubleshooting](README.md#troubleshooting)
- Review [Documentation](docs/)
- Open an issue on GitHub

---

Happy automating! 🎬
