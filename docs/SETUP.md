# Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **FFmpeg** (required for video processing)
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

3. **pip** (Python package manager)
   ```bash
   pip --version
   ```

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ishwar786Ambare/video-generation-social-media.git
cd video-generation-social-media
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "from src.video_generator import VideoGenerator; print('Installation successful!')"
```

## Platform-Specific Setup

### YouTube Setup

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "Create Project"
   - Name your project

2. **Enable YouTube Data API v3**
   - In your project, go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

3. **Create OAuth2 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the JSON file

4. **Save Credentials**
   ```bash
   mkdir -p credentials
   # Move downloaded file to credentials/youtube_credentials.json
   ```

5. **First-Time Authorization**
   - Run any YouTube upload example
   - A browser window will open for authorization
   - Grant the requested permissions
   - Token will be saved for future use

### Facebook Setup

1. **Create Facebook App**
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Click "My Apps" > "Create App"
   - Choose "Business" type
   - Fill in app details

2. **Get Access Token**
   - In your app dashboard, go to Tools > Graph API Explorer
   - Select your app
   - Add permissions: `pages_manage_posts`, `pages_read_engagement`
   - Generate Access Token

3. **Set Environment Variable**
   ```bash
   export FB_ACCESS_TOKEN="your_access_token_here"
   ```

4. **For Page Uploads (Optional)**
   - Get your Page ID from your Facebook Page settings
   - Use it in the `page_id` parameter

### Instagram Setup

1. **Prepare Account**
   - Use a regular Instagram account (business or personal)
   - If 2FA is enabled, generate an app-specific password

2. **Set Credentials**
   ```bash
   export IG_USERNAME="your_instagram_username"
   export IG_PASSWORD="your_instagram_password"
   ```

3. **Important Notes**
   - Instagram may ask for verification on first login
   - Login manually from the same IP first to avoid challenges
   - Keep your account secure and follow Instagram's ToS

## Environment Variables Setup

Create a `.env` file in the project root:

```bash
# YouTube
YOUTUBE_CREDENTIALS_PATH=credentials/youtube_credentials.json

# Facebook
FB_ACCESS_TOKEN=your_facebook_access_token_here

# Instagram
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
```

Load environment variables in your scripts:

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Now you can access variables
fb_token = os.getenv('FB_ACCESS_TOKEN')
```

## Directory Structure

After setup, your project should look like:

```
video-generation-social-media/
├── src/
│   ├── video_generator/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── text_to_speech.py
│   │   └── video_composer.py
│   └── social_media/
│       ├── __init__.py
│       ├── youtube_uploader.py
│       ├── facebook_uploader.py
│       └── instagram_uploader.py
├── examples/
│   ├── basic_video_generation.py
│   ├── youtube_upload.py
│   ├── facebook_upload.py
│   └── instagram_upload.py
├── credentials/
│   └── youtube_credentials.json
├── output_videos/
├── requirements.txt
├── .env
└── README.md
```

## Testing Your Setup

### Test Video Generation

```bash
python examples/basic_video_generation.py
```

This should create a video in the `output_videos/` directory.

### Test Platform Uploads

```bash
# Test YouTube (requires credentials)
python examples/youtube_upload.py

# Test Facebook (requires access token)
python examples/facebook_upload.py

# Test Instagram (requires credentials)
python examples/instagram_upload.py
```

## Troubleshooting Setup

### FFmpeg Issues

**Error:** `MoviePy requires FFmpeg`

**Solution:** Ensure FFmpeg is installed and in your system PATH
```bash
ffmpeg -version
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'moviepy'`

**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt
```

### YouTube Authentication Issues

**Error:** `Credentials file not found`

**Solution:** 
1. Verify file exists at `credentials/youtube_credentials.json`
2. Check file permissions
3. Verify JSON format is valid

### Facebook Token Issues

**Error:** `Invalid access token`

**Solution:**
1. Generate a new access token
2. Ensure required permissions are granted
3. Check token hasn't expired

### Instagram Login Issues

**Error:** `Challenge required`

**Solution:**
1. Login to Instagram from the same IP manually
2. Complete any security verifications
3. Use app-specific password if 2FA is enabled

## Next Steps

Once setup is complete:

1. ✅ Run the examples to familiarize yourself with the API
2. ✅ Review the [API Reference](README.md#api-reference)
3. ✅ Create your first automated video workflow
4. ✅ Explore batch generation features
5. ✅ Customize for your specific use case

## Getting Help

If you encounter issues during setup:

1. Check this guide again carefully
2. Review error messages
3. Check the [Troubleshooting](README.md#troubleshooting) section
4. Open an issue on GitHub with details

Happy coding! 🚀
