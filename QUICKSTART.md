# Quick Start Guide

This guide will help you get started with the automated video generation system quickly.

## Step 1: Installation

```bash
# Clone the repository
git clone https://github.com/Ishwar786Ambare/video-generation-social-media.git
cd video-generation-social-media

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configuration

```bash
# Copy example configuration
cp config/config.example.json config/config.json

# Edit with your favorite editor
nano config/config.json
```

### Minimal Configuration (News Fetching Only)

For testing, you can start with just RSS feeds (no API keys needed):

```json
{
  "news_api": {
    "api_key": "",
    "sources": [],
    "categories": []
  },
  
  "rss_feeds": [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://rss.cnn.com/rss/edition.rss"
  ],
  
  "video": {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "duration_per_article": 10,
    "max_articles_per_video": 3
  },
  
  "youtube": {
    "enabled": false
  },
  
  "instagram": {
    "enabled": false
  },
  
  "facebook": {
    "enabled": false
  }
}
```

## Step 3: Test News Fetching

```bash
# Test RSS fetching
python -m src.news_fetcher.rss_fetcher
```

## Step 4: Generate Your First Video

```bash
# Run the full pipeline (without social media upload)
python main.py
```

This will:
1. Fetch news from RSS feeds
2. Store in database
3. Generate a video in `output/videos/`

## Step 5: Enable Social Media Upload (Optional)

### YouTube Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download credentials JSON and save as `credentials/youtube_credentials.json`
6. In `config/config.json`, set `"youtube.enabled": true`

### Instagram Setup

1. In `config/config.json`, add:
```json
{
  "instagram": {
    "username": "your_username",
    "password": "your_password",
    "enabled": true
  }
}
```

### Facebook Setup

1. Create a Facebook App at [developers.facebook.com](https://developers.facebook.com/)
2. Get App ID, App Secret, and Access Token
3. In `config/config.json`, add:
```json
{
  "facebook": {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "access_token": "your_access_token",
    "enabled": true
  }
}
```

## Step 6: Automate with Scheduling

```bash
# Run daily at 9:00 AM
python main.py --schedule --time "09:00"
```

## Troubleshooting

### Video Generation Fails

If you get errors about missing fonts or libraries:

```bash
# Ubuntu/Debian
sudo apt-get install imagemagick fonts-dejavu-core

# macOS
brew install imagemagick

# Windows
# Download and install ImageMagick from https://imagemagick.org/
```

### "No module named 'moviepy'"

Make sure you've activated your virtual environment and installed dependencies:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### News API Rate Limits

The free News API tier has limits. Consider:
- Reducing `max_articles` in config
- Using only RSS feeds for testing
- Upgrading to a paid News API plan

## Next Steps

- Customize video templates in `src/video_generator/`
- Add more RSS feeds in configuration
- Adjust video duration and styling
- Set up cron job or systemd service for production deployment
