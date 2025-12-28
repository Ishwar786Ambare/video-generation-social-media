# Project Overview: Automated Video Generation for Social Media

## 🎯 Project Purpose

This repository provides a **complete toolkit** for automated video generation and distribution across YouTube, Facebook, and Instagram. It enables content creators to:

- Generate professional videos from text scripts
- Optimize videos for different platforms automatically
- Upload to multiple social media platforms programmatically
- Scale content production efficiently

## 📦 What's Included

### Core Modules

#### 1. Video Generator (`src/video_generator/`)
- **core.py**: Main VideoGenerator class with platform-specific settings
- **text_to_speech.py**: Convert text to natural speech using gTTS
- **video_composer.py**: Compose videos from audio, images, and music

#### 2. Social Media Integrations (`src/social_media/`)
- **youtube_uploader.py**: Upload to YouTube via Data API v3 with OAuth2
- **facebook_uploader.py**: Upload to Facebook via Graph API
- **instagram_uploader.py**: Upload to Instagram (Feed, Reels, Stories, IGTV)

### Documentation

1. **README.md** - Main documentation with features and quick examples
2. **QUICKSTART.md** - 5-minute getting started guide
3. **docs/SETUP.md** - Detailed setup for all platforms
4. **docs/API.md** - Complete API reference
5. **docs/TUTORIAL.md** - Step-by-step tutorial
6. **CONTRIBUTING.md** - Contribution guidelines
7. **CHANGELOG.md** - Version history

### Examples (`examples/`)

1. **basic_video_generation.py** - Simple text-to-video
2. **video_with_images.py** - Add image slideshow
3. **batch_generation.py** - Generate multiple videos
4. **youtube_upload.py** - YouTube workflow
5. **facebook_upload.py** - Facebook workflow
6. **instagram_upload.py** - Instagram workflow
7. **complete_automation.py** - Full automation pipeline

## 🚀 Key Features

### Video Generation
- ✅ Text-to-speech using gTTS
- ✅ Image slideshow composition
- ✅ Background music integration
- ✅ Platform-specific optimization
- ✅ Batch processing
- ✅ Custom resolutions and FPS

### Social Media Upload
- ✅ YouTube: OAuth2 authentication, metadata management
- ✅ Facebook: Profile and page uploads, analytics
- ✅ Instagram: Feed, Reels, Stories, IGTV support

### Platform Optimization
- YouTube: 1920x1080, 16:9, 30 FPS
- Facebook: 1280x720, 16:9, 30 FPS
- Instagram: 1080x1080, 1:1, 30 FPS

## 🛠️ Technology Stack

### Core Dependencies
- **moviepy** - Video editing and composition
- **Pillow** - Image processing
- **gTTS** - Text-to-speech
- **numpy** - Numerical operations

### API Integrations
- **google-api-python-client** - YouTube Data API
- **google-auth-oauthlib** - OAuth2 authentication
- **instagrapi** - Instagram API client
- **requests** - HTTP client for Facebook Graph API

### Utilities
- **python-dotenv** - Environment variable management
- **FFmpeg** - Video encoding (external dependency)

## 📋 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
sudo apt install ffmpeg  # Ubuntu/Debian
```

### 2. Generate Your First Video
```python
from src.video_generator import VideoGenerator

generator = VideoGenerator()
video = generator.generate_video(
    script="Welcome to automated video generation!",
    title="my_first_video",
    platform="youtube"
)
```

### 3. Upload to YouTube
```python
from src.social_media import YouTubeUploader

uploader = YouTubeUploader()
uploader.upload_video(
    video_path=video,
    title="My First Video",
    description="Created with Python!"
)
```

## 🎨 Use Cases

### Content Creators
- Automate daily video posts
- Create consistent content schedules
- Scale video production

### Marketing Teams
- Generate promotional videos at scale
- Multi-platform distribution
- A/B testing with variations

### Educators
- Create course materials
- Generate video tutorials
- Automate lesson publishing

### News & Media
- Quick video updates
- Breaking news videos
- Social media content

## 🔒 Security

### ✅ Security Measures
- Updated Pillow to 10.2.0 (fixes CVE)
- Removed unmaintained dependencies
- Environment variable for credentials
- .gitignore for sensitive files
- No hardcoded secrets

### 🔐 Credentials Management
- YouTube: OAuth2 credentials in `credentials/`
- Facebook: Access token via environment variable
- Instagram: Credentials via environment variables
- Example: `.env.example` template provided

## 📊 Project Statistics

- **Total Files**: 25
- **Python Modules**: 10
- **Example Scripts**: 7
- **Documentation Pages**: 7
- **Dependencies**: 14 packages
- **Supported Platforms**: 3 (YouTube, Facebook, Instagram)

## 🔄 Workflow Example

```python
# 1. Generate video for multiple platforms
generator = VideoGenerator()

videos = {
    'youtube': generator.generate_video(script, "yt", platform="youtube"),
    'facebook': generator.generate_video(script, "fb", platform="facebook"),
    'instagram': generator.generate_video(script, "ig", platform="instagram")
}

# 2. Upload to all platforms
yt_uploader.upload_video(videos['youtube'], title, description)
fb_uploader.upload_video(videos['facebook'], title, description)
ig_uploader.upload_video(videos['instagram'], caption)

# 3. Monitor results
# Check analytics via platform APIs
```

## 🎓 Learning Path

### Beginner
1. Read QUICKSTART.md
2. Run basic_video_generation.py
3. Experiment with different scripts

### Intermediate
1. Review docs/TUTORIAL.md
2. Try platform-specific uploads
3. Use batch generation

### Advanced
1. Study docs/API.md
2. Customize VideoGenerator
3. Build automation pipelines
4. Integrate with scheduling systems

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for:
- Code style guidelines
- Development setup
- Pull request process
- Feature priorities

## 📝 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- MoviePy team for video editing tools
- Google for YouTube Data API
- Meta for Facebook Graph API
- Instagrapi for Instagram access

## 📞 Support

- 📖 Documentation: `docs/` directory
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📧 Contact: Via GitHub

## 🔮 Future Roadmap

### Planned Features
- [ ] Subtitle/caption generation
- [ ] Video template system
- [ ] Additional TTS engines (AWS Polly, Azure)
- [ ] Advanced video effects
- [ ] Scheduling system
- [ ] Analytics dashboard
- [ ] GUI interface
- [ ] Docker support

### Community Suggestions
Open an issue to suggest new features!

## 📈 Version History

- **v1.0.0** (2024-12-28) - Initial release
  - Core video generation
  - Social media integrations
  - Complete documentation
  - Security fixes applied

---

**Built with ❤️ for content creators worldwide**

For detailed documentation, see [README.md](README.md)
