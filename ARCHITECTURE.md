# System Architecture

## Overview

The Automated Video Generation System is designed as a modular pipeline that fetches news, generates videos, and uploads to social media platforms.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Orchestrator                         │
│                      (main.py)                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │  1. News Fetching                      │
    │  ┌──────────────┐  ┌──────────────┐  │
    │  │ News API     │  │ RSS Feeds    │  │
    │  │ Client       │  │ Parser       │  │
    │  └──────────────┘  └──────────────┘  │
    └────────────────┬───────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │  2. Storage Layer                      │
    │  ┌──────────────────────────────────┐ │
    │  │  SQLite Database                 │ │
    │  │  - Articles                      │ │
    │  │  - Metadata                      │ │
    │  │  - Usage tracking                │ │
    │  └──────────────────────────────────┘ │
    └────────────────┬───────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │  3. Video Generation                   │
    │  ┌──────────────┐  ┌──────────────┐  │
    │  │ Image        │  │ Text-to-     │  │
    │  │ Processor    │  │ Speech       │  │
    │  └──────────────┘  └──────────────┘  │
    │  ┌──────────────────────────────────┐ │
    │  │  Video Creator (MoviePy)         │ │
    │  │  - Combine images                │ │
    │  │  - Add audio                     │ │
    │  │  - Apply effects                 │ │
    │  └──────────────────────────────────┘ │
    └────────────────┬───────────────────────┘
                     │
                     ▼
    ┌────────────────────────────────────────┐
    │  4. Social Media Upload                │
    │  ┌──────────┐ ┌───────────┐ ┌────────┐│
    │  │ YouTube  │ │ Instagram │ │Facebook││
    │  │ Uploader │ │ Uploader  │ │Uploader││
    │  └──────────┘ └───────────┘ └────────┘│
    └────────────────────────────────────────┘
```

## Component Details

### 1. News Fetching Layer

**News API Client** (`src/news_fetcher/news_api_client.py`)
- Fetches news from NewsAPI.org
- Supports filtering by source, category, language
- Handles API rate limiting
- Parses and normalizes article data

**RSS Fetcher** (`src/news_fetcher/rss_fetcher.py`)
- Parses RSS/Atom feeds
- Supports multiple feed sources
- Extracts title, description, content, metadata
- No API key required

### 2. Storage Layer

**Database** (`src/storage/database.py`)
- SQLAlchemy-based ORM
- SQLite database for simplicity
- Tracks article usage to avoid duplicates
- Supports queries for unused articles

**Models** (`src/storage/models.py`)
- NewsArticle model with fields:
  - title, description, content
  - source, author, url
  - published_at, fetched_at
  - category, used_in_video, video_id

### 3. Video Generation Layer

**Image Processor** (`src/video_generator/image_processor.py`)
- Creates background images
- Generates text overlays
- Handles text wrapping
- Supports custom fonts and colors

**Text-to-Speech** (`src/video_generator/text_to_speech.py`)
- Uses Google Text-to-Speech (gTTS)
- Generates narration from article text
- Supports multiple languages
- Creates MP3 audio files

**Video Creator** (`src/video_generator/video_creator.py`)
- Uses MoviePy for video composition
- Combines images and audio
- Supports transitions and effects
- Outputs MP4 files

### 4. Social Media Upload Layer

**YouTube Uploader** (`src/social_media/youtube_uploader.py`)
- Uses YouTube Data API v3
- OAuth 2.0 authentication
- Supports metadata (title, description, tags)
- Handles resumable uploads

**Instagram Uploader** (`src/social_media/instagram_uploader.py`)
- Uses instagrapi library
- Supports posts, reels, and IGTV
- Session management
- Caption and hashtag support

**Facebook Uploader** (`src/social_media/facebook_uploader.py`)
- Uses Facebook Graph API
- Supports chunked uploads for large files
- Page posting support
- Video metadata

### 5. Configuration & Utilities

**Config Manager** (`src/utils/config.py`)
- JSON-based configuration
- Centralized settings management
- Environment-specific configs
- Credential management

## Data Flow

1. **Fetch**: News articles are fetched from APIs/RSS feeds
2. **Store**: Articles are stored in SQLite database
3. **Select**: Unused articles are selected for video
4. **Generate**: Video is created with images and audio
5. **Upload**: Video is uploaded to social media platforms
6. **Track**: Articles are marked as used in database

## Deployment Options

### Local Execution
```bash
python main.py
```

### Scheduled Execution
```bash
python main.py --schedule --time "09:00"
```

### Cron Job (Linux/Mac)
```bash
0 9 * * * cd /path/to/project && /path/to/venv/bin/python main.py
```

### systemd Service (Linux)
```ini
[Unit]
Description=Automated Video Generation

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/python main.py --schedule --time "09:00"
Restart=always

[Install]
WantedBy=multi-user.target
```

### Task Scheduler (Windows)
Use Windows Task Scheduler to run `python main.py` daily

## Scalability Considerations

### Current Design (Single Machine)
- Handles moderate workloads
- ~10-50 videos per day
- SQLite database sufficient

### Future Enhancements for Scale
- PostgreSQL/MySQL for database
- Redis for caching
- Celery for task queue
- S3 for video storage
- Kubernetes for orchestration
- Separate workers for generation and upload

## Security Best Practices

1. **Credentials**: Never commit to git
2. **API Keys**: Use environment variables
3. **Passwords**: Use secure storage (keyring)
4. **Permissions**: Run with minimal privileges
5. **Updates**: Keep dependencies updated
6. **Monitoring**: Log all API calls
7. **Rate Limiting**: Respect API limits

## Error Handling

- All modules include try-catch blocks
- Logging at INFO and ERROR levels
- Graceful degradation (skip failed uploads)
- Database transactions for consistency

## Monitoring & Logging

Logs are written to console with timestamps:
```
2024-01-01 09:00:00 - INFO - Fetching news...
2024-01-01 09:00:05 - INFO - Fetched 20 articles
2024-01-01 09:00:10 - INFO - Generating video...
```

For production, redirect to file:
```bash
python main.py >> logs/output.log 2>&1
```
