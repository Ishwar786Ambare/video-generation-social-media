# Frequently Asked Questions (FAQ)

## General Questions

### Q: What does this system do?
A: This is an automated pipeline that:
1. Fetches news articles from various sources (News API, RSS feeds)
2. Stores them in a database
3. Generates videos with text overlays and voice narration
4. Uploads videos to YouTube, Instagram, and Facebook automatically

### Q: Do I need programming knowledge to use this?
A: Basic knowledge helps, but you can follow the QUICKSTART guide step by step. You'll need to:
- Run Python commands
- Edit JSON configuration files
- Obtain API keys from various services

### Q: Is this free to use?
A: The software is free (MIT License), but some services have costs:
- **Free**: RSS feeds, gTTS (text-to-speech), basic infrastructure
- **Free Tier**: NewsAPI (100 requests/day), YouTube API, Facebook API
- **Paid**: Instagram (account only), NewsAPI premium features

### Q: Can I customize the videos?
A: Yes! You can customize:
- Video resolution and FPS
- Background colors
- Text styles and fonts
- Duration per article
- Voice language and speed
- Transition effects (in code)

### Q: Which platforms are supported?
A: Currently:
- YouTube ✓
- Instagram (Posts, Reels, IGTV) ✓
- Facebook (Profile, Page) ✓
- TikTok - Planned for future
- Twitter/X - Can be added

### Q: Can I run this on a schedule?
A: Yes! Multiple options:
- Built-in scheduler: `python main.py --schedule --time "09:00"`
- Cron (Linux/Mac)
- Task Scheduler (Windows)
- Cloud cron jobs (GCP Cloud Scheduler, AWS EventBridge)

## Technical Questions

### Q: What are the system requirements?
A: Minimum:
- Python 3.7+
- 2GB RAM
- 1GB disk space (more for videos)
- Internet connection

Recommended:
- Python 3.9+
- 4GB+ RAM (video processing is memory-intensive)
- 10GB+ disk space
- Linux or macOS (Windows works but may need tweaks)

### Q: Can I run this on a Raspberry Pi?
A: Possibly, but:
- Video generation will be slow
- Need 2GB+ RAM model
- Consider using lower resolution (720p)
- May need to install additional codecs

### Q: Can I deploy to the cloud?
A: Yes! Works on:
- AWS EC2
- Google Cloud Compute Engine
- Azure VMs
- DigitalOcean Droplets
- Heroku (with buildpacks)

### Q: How do I handle large volumes?
A: For scaling:
1. Use PostgreSQL instead of SQLite
2. Add Redis for caching
3. Separate services (fetch, generate, upload)
4. Use task queues (Celery, RabbitMQ)
5. Deploy multiple workers

### Q: Can I use different news sources?
A: Yes! Add RSS feeds to config:
```json
{
  "rss_feeds": [
    "http://feeds.your-source.com/news.xml",
    "https://another-source.com/rss"
  ]
}
```

## API & Authentication Questions

### Q: Do I need all the API keys?
A: No! Minimum setup:
- **Just testing**: Use only RSS feeds (no API keys needed)
- **Production**: Add NewsAPI key for better articles
- **Social media**: Only enable the platforms you want to use

### Q: How often should I rotate API keys?
A: Recommended:
- YouTube/Facebook tokens: Every 60 days
- Instagram password: Every 90 days
- NewsAPI key: Annually (or when compromised)

### Q: Can I use environment variables instead of config file?
A: Yes, modify `src/utils/config.py` to read from environment:
```python
import os
api_key = os.getenv('NEWS_API_KEY', self.get('news_api.api_key'))
```

### Q: What are the API rate limits?
A:
- **NewsAPI Free**: 100 requests/day
- **YouTube**: 10,000 units/day (~6 videos)
- **Facebook**: 75 videos/day per page
- **Instagram**: Unofficial, ~3-5 posts/day recommended

## Video Generation Questions

### Q: How long does video generation take?
A: Typical:
- 30-second video: 10-30 seconds
- 1-minute video: 30-60 seconds
- 5-minute video: 2-5 minutes

Depends on:
- CPU speed
- Video resolution
- Number of articles
- Audio generation time

### Q: Can I add my own images?
A: Yes! Modify `src/video_generator/image_processor.py`:
- Add image loading from URL or file
- Use as backgrounds
- Create custom templates

### Q: Can I use a different voice?
A: Yes! Options:
1. **Change language**: Edit `config.json` → `tts.language`
2. **Use different TTS engine**: Modify `text_to_speech.py`
   - Amazon Polly
   - Microsoft Azure TTS
   - IBM Watson TTS
3. **Record your own**: Replace TTS with audio files

### Q: How do I add video transitions?
A: Edit `src/video_generator/video_creator.py`:
```python
from moviepy.video.fx.all import fadein, fadeout
clip = clip.fx(fadein, 1).fx(fadeout, 1)
```

### Q: Can I add background music?
A: Yes! Modify `video_creator.py`:
```python
from moviepy.editor import AudioFileClip, CompositeAudioClip

music = AudioFileClip("music.mp3").volumex(0.3)
final_audio = CompositeAudioClip([narration, music])
```

## Social Media Questions

### Q: Why isn't my YouTube upload working?
A: Common issues:
1. API not enabled → Enable in Google Cloud Console
2. Wrong credentials file → Check path in config
3. Quota exceeded → Wait until next day
4. Video too large → Reduce resolution or duration

### Q: Instagram says "Challenge Required"?
A: This means:
- Instagram detected automation
- Complete the challenge via email/SMS
- Reduce posting frequency
- Add delays between posts
- Make account look more human (follow, like, etc.)

### Q: Can I post to multiple Facebook pages?
A: Yes! Modify the upload function:
```python
pages = ['page_id_1', 'page_id_2']
for page_id in pages:
    uploader.upload_video(video_path, title, description, page_id)
```

### Q: How do I schedule posts for specific times?
A: Currently posts immediately. For scheduling:
1. Use Facebook/YouTube built-in scheduling
2. Or delay the upload:
   ```python
   import time
   from datetime import datetime
   
   target_time = datetime(2024, 1, 15, 14, 30)
   wait_seconds = (target_time - datetime.now()).total_seconds()
   time.sleep(wait_seconds)
   uploader.upload_video(...)
   ```

## Error Messages

### Error: "ModuleNotFoundError: No module named 'moviepy'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError: config/config.json"
**Solution**: Copy example config
```bash
cp config/config.example.json config/config.json
```

### Error: "OSError: decoder jpeg not available"
**Solution**: Install Pillow properly
```bash
pip uninstall Pillow
pip install Pillow
```

### Error: "InvalidToken" from YouTube
**Solution**: Re-authenticate
```bash
rm credentials/youtube_token.pickle
python main.py  # Will prompt for login
```

### Error: "No unused articles available"
**Solution**: Fetch news first
```bash
python -c "from src.news_fetcher.rss_fetcher import RSSFetcher; f = RSSFetcher(['http://feeds.bbci.co.uk/news/rss.xml']); f.fetch_all()"
```

### Error: "Rate limit exceeded" from NewsAPI
**Solution**:
- Wait until tomorrow (free tier resets daily)
- Reduce `max_articles` in config
- Use only RSS feeds
- Upgrade to paid plan

## Best Practices

### Q: How often should I post?
A: Recommended:
- **YouTube**: Daily is fine (within quota)
- **Instagram**: 1-2 times per day max
- **Facebook**: 1-3 times per day

### Q: What's the ideal video length?
A: Platform-specific:
- **YouTube**: 3-10 minutes (better engagement)
- **Instagram Reels**: 15-60 seconds
- **Facebook**: 1-3 minutes

### Q: How do I avoid copyright issues?
A:
1. Use only news sources that allow redistribution
2. Add commentary/transformation (fair use)
3. Credit sources in description
4. Use royalty-free background music
5. Avoid showing full articles

### Q: How can I increase video quality?
A:
1. Use higher resolution: `"width": 1920, "height": 1080`
2. Better fonts: Install custom fonts
3. Add images from articles (if available)
4. Use professional TTS (Google Cloud TTS)
5. Add background music
6. Create custom templates

### Q: Should I run this 24/7?
A: No, recommended:
- Run once or twice daily
- Use scheduling (cron, systemd)
- Monitor for errors
- Keep logs
- Alert on failures

## Customization

### Q: Can I add my logo/watermark?
A: Yes! Modify `image_processor.py`:
```python
from PIL import Image
logo = Image.open('logo.png')
img.paste(logo, (x, y), logo)
```

### Q: Can I create videos in different languages?
A: Yes! Change in config:
```json
{
  "tts": {
    "language": "es"  // Spanish
  }
}
```

Supported languages: en, es, fr, de, it, pt, ru, ja, ko, zh, and more.

### Q: How do I add hashtags?
A: Edit upload templates in config:
```json
{
  "youtube": {
    "description_template": "Daily news\n\n#news #breakingnews #dailynews"
  },
  "instagram": {
    "caption_template": "📰 Daily News\n\n#news #daily #trending"
  }
}
```

## Troubleshooting

### Videos are not generating
1. Check logs for errors
2. Verify temp directory exists and is writable
3. Test image processor:
   ```bash
   python -m src.video_generator.image_processor
   ```
4. Check disk space
5. Ensure moviepy dependencies installed

### Audio is missing from videos
1. Check if audio file was created in temp/
2. Verify gTTS is working:
   ```bash
   python -c "from gtts import gTTS; tts = gTTS('test'); tts.save('test.mp3')"
   ```
3. Check MoviePy audio codec installation
4. Try different audio format

### Uploads are failing
1. Verify API credentials
2. Check internet connection
3. Test file size (too large?)
4. Verify API quotas not exceeded
5. Check platform-specific requirements

## Getting Help

- **GitHub Issues**: https://github.com/Ishwar786Ambare/video-generation-social-media/issues
- **Documentation**: See README.md, QUICKSTART.md, API_SETUP.md
- **Examples**: Run `python examples.py`
- **Logs**: Check console output for error messages

## Contributing

Want to add features? PRs welcome!
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

Popular feature requests:
- TikTok integration
- Advanced video templates
- AI-powered content generation
- Analytics dashboard
- Multi-language support
- Cloud deployment scripts
