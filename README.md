# Automated Video Generation for Social Media

A comprehensive Python-based system for automatically generating and publishing news videos to YouTube, Instagram, and Facebook.

## Features

- **Automated News Fetching**: Collects daily news from multiple sources (RSS feeds, News API)
- **Content Storage**: Stores news articles in a database for processing
- **Video Generation**: Automatically creates videos with:
  - Background images
  - Text overlays with news headlines and content
  - Text-to-speech narration
  - Professional transitions and effects
- **Multi-Platform Upload**: Automatically uploads videos to:
  - YouTube
  - Instagram
  - Facebook
- **Scheduled Automation**: Run the entire pipeline on a schedule

## Project Structure

```
video-generation-social-media/
├── src/
│   ├── news_fetcher/
│   │   ├── __init__.py
│   │   ├── news_api_client.py
│   │   └── rss_fetcher.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── video_generator/
│   │   ├── __init__.py
│   │   ├── video_creator.py
│   │   ├── image_processor.py
│   │   └── text_to_speech.py
│   ├── social_media/
│   │   ├── __init__.py
│   │   ├── youtube_uploader.py
│   │   ├── instagram_uploader.py
│   │   └── facebook_uploader.py
│   └── utils/
│       ├── __init__.py
│       └── config.py
├── config/
│   └── config.example.json
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ishwar786Ambare/video-generation-social-media.git
cd video-generation-social-media
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up configuration:
```bash
cp config/config.example.json config/config.json
```

5. Edit `config/config.json` with your API credentials and preferences.

## Configuration

### News API Setup

1. Get a free API key from [NewsAPI.org](https://newsapi.org/)
2. Add it to your `config/config.json`:
```json
{
  "news_api": {
    "api_key": "your_newsapi_key_here",
    "sources": ["bbc-news", "cnn", "google-news"],
    "categories": ["technology", "business", "general"]
  }
}
```

### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download the credentials JSON file and save as `credentials/youtube_credentials.json`

### Instagram Setup

1. Add your Instagram credentials to `config/config.json`:
```json
{
  "instagram": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

### Facebook Setup

1. Create a Facebook App at [Facebook Developers](https://developers.facebook.com/)
2. Get your App ID and App Secret
3. Add to `config/config.json`:
```json
{
  "facebook": {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "access_token": "your_access_token"
  }
}
```

## Usage

### Run Once

Generate and upload videos immediately:

```bash
python main.py
```

### Scheduled Execution

Run automatically every day at a specific time:

```bash
python main.py --schedule --time "09:00"
```

### Test Individual Components

Test news fetching:
```bash
python -m src.news_fetcher.news_api_client
```

Test video generation:
```bash
python -m src.video_generator.video_creator
```

## How It Works

1. **News Fetching**: The system fetches the latest news articles from configured sources (News API, RSS feeds)

2. **Content Storage**: News articles are stored in a SQLite database with metadata (title, description, source, published date)

3. **Video Generation**:
   - Selects top news articles from the database
   - Generates background images or uses stock images
   - Creates text overlays with headlines and summaries
   - Generates voiceover using text-to-speech
   - Combines everything into a video using MoviePy

4. **Social Media Upload**:
   - Uploads the generated video to YouTube with appropriate title, description, and tags
   - Posts to Instagram (as IGTV or Reel)
   - Shares on Facebook page

5. **Automation**: The entire pipeline can run on a schedule (daily, hourly, etc.)

## Customization

### Video Settings

Edit `config/config.json` to customize:
- Video resolution (1920x1080 for YouTube, 1080x1920 for Instagram Stories)
- Video duration
- Font styles and sizes
- Background colors/images
- Transition effects

### News Sources

Add or remove news sources in the configuration:
```json
{
  "rss_feeds": [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://rss.cnn.com/rss/edition.rss"
  ]
}
```

### Voice Settings

Configure text-to-speech:
```json
{
  "tts": {
    "engine": "gtts",
    "language": "en",
    "speed": 1.0
  }
}
```

## Dependencies

- **feedparser**: Parse RSS feeds
- **newsapi-python**: NewsAPI client
- **moviepy**: Video creation and editing
- **Pillow**: Image processing
- **gTTS**: Google Text-to-Speech
- **google-api-python-client**: YouTube API
- **instagrapi**: Instagram API
- **facebook-sdk**: Facebook Graph API
- **sqlalchemy**: Database ORM
- **schedule**: Task scheduling

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've installed all requirements: `pip install -r requirements.txt`

2. **API Rate Limits**: If you hit rate limits, reduce the frequency of fetching news or upgrade your API plan

3. **Video Generation Errors**: Ensure you have enough disk space and memory for video processing

4. **Upload Failures**: Check your API credentials and ensure you have necessary permissions

## Security Notes

- Never commit API keys or credentials to the repository
- Use environment variables or secure configuration files
- Keep `config/config.json` and all credential files in `.gitignore`
- Regularly rotate your API keys and passwords

## Future Enhancements

- Support for TikTok uploads
- Advanced video templates with animations
- AI-powered content summarization
- Multi-language support
- Analytics dashboard
- Webhook notifications
- Cloud deployment (AWS, GCP, Azure)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.