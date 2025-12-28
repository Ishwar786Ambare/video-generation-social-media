# API Documentation

## Video Generator API

### VideoGenerator Class

Main class for generating videos from text scripts.

#### Constructor

```python
VideoGenerator(output_dir: str = "output_videos")
```

**Parameters:**
- `output_dir` (str): Directory where generated videos will be saved. Default: "output_videos"

**Example:**
```python
from src.video_generator import VideoGenerator

generator = VideoGenerator(output_dir="my_videos")
```

#### Methods

##### generate_video()

Generate a single video from script and optional media.

```python
generate_video(
    script: str,
    title: str,
    images: Optional[List[str]] = None,
    background_music: Optional[str] = None,
    platform: str = "youtube",
    **kwargs
) -> str
```

**Parameters:**
- `script` (str): Text script to convert to speech
- `title` (str): Video title (used for filename)
- `images` (List[str], optional): List of image file paths
- `background_music` (str, optional): Path to background music file
- `platform` (str): Target platform ("youtube", "facebook", "instagram")
- `**kwargs`: Additional platform-specific parameters
  - `resolution` (tuple): Video resolution (width, height)
  - `fps` (int): Frames per second
  - `aspect_ratio` (str): Aspect ratio string

**Returns:**
- `str`: Path to the generated video file

**Example:**
```python
video_path = generator.generate_video(
    script="Hello world!",
    title="my_video",
    images=["img1.jpg", "img2.jpg"],
    background_music="music.mp3",
    platform="youtube",
    resolution=(1920, 1080),
    fps=30
)
```

##### batch_generate()

Generate multiple videos in batch.

```python
batch_generate(
    videos_config: List[Dict],
    platform: str = "youtube"
) -> List[str]
```

**Parameters:**
- `videos_config` (List[Dict]): List of video configurations
- `platform` (str): Default platform for all videos

**Config Dictionary Format:**
```python
{
    "title": "video_name",
    "script": "Video narration text",
    "images": ["img1.jpg", "img2.jpg"],  # optional
    "background_music": "music.mp3",     # optional
    "settings": {                         # optional
        "resolution": (1920, 1080),
        "fps": 30
    }
}
```

**Returns:**
- `List[str]`: List of paths to generated videos

**Example:**
```python
configs = [
    {"title": "vid1", "script": "First video"},
    {"title": "vid2", "script": "Second video"}
]
paths = generator.batch_generate(configs, platform="youtube")
```

---

## Text-to-Speech API

### TextToSpeech Class

Handles conversion of text to speech audio.

#### Constructor

```python
TextToSpeech(language: str = "en", slow: bool = False)
```

**Parameters:**
- `language` (str): Language code (e.g., "en", "es", "fr", "de")
- `slow` (bool): Use slower speech speed

#### Methods

##### generate_speech()

Convert text to audio file.

```python
generate_speech(
    text: str,
    output_path: str,
    language: Optional[str] = None,
    slow: Optional[bool] = None
) -> str
```

**Parameters:**
- `text` (str): Text to convert
- `output_path` (str): Path to save audio file
- `language` (str, optional): Override default language
- `slow` (bool, optional): Override default speed

**Returns:**
- `str`: Path to generated audio file

---

## Social Media APIs

### YouTubeUploader Class

Upload and manage videos on YouTube.

#### Constructor

```python
YouTubeUploader(credentials_path: str = "credentials/youtube_credentials.json")
```

**Parameters:**
- `credentials_path` (str): Path to OAuth2 credentials JSON

#### Methods

##### authenticate()

Authenticate with YouTube API.

```python
authenticate() -> Resource
```

**Returns:**
- YouTube API service resource

##### upload_video()

Upload video to YouTube.

```python
upload_video(
    video_path: str,
    title: str,
    description: str = "",
    category: str = "22",
    privacy_status: str = "private",
    tags: Optional[list] = None
) -> Dict
```

**Parameters:**
- `video_path` (str): Path to video file
- `title` (str): Video title
- `description` (str): Video description
- `category` (str): YouTube category ID
- `privacy_status` (str): "public", "private", or "unlisted"
- `tags` (list): List of video tags

**Returns:**
- `Dict`: Response with video ID and metadata

**Category IDs:**
- "1": Film & Animation
- "2": Autos & Vehicles
- "10": Music
- "15": Pets & Animals
- "17": Sports
- "19": Travel & Events
- "20": Gaming
- "22": People & Blogs
- "23": Comedy
- "24": Entertainment
- "25": News & Politics
- "26": Howto & Style
- "27": Education
- "28": Science & Technology

##### update_video()

Update video metadata.

```python
update_video(
    video_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[list] = None
) -> Dict
```

---

### FacebookUploader Class

Upload and manage videos on Facebook.

#### Constructor

```python
FacebookUploader(access_token: Optional[str] = None)
```

**Parameters:**
- `access_token` (str, optional): Facebook access token (or use FB_ACCESS_TOKEN env var)

#### Methods

##### upload_video()

Upload video to Facebook.

```python
upload_video(
    video_path: str,
    title: str,
    description: str = "",
    page_id: Optional[str] = None,
    published: bool = True
) -> Dict
```

**Parameters:**
- `video_path` (str): Path to video file
- `title` (str): Video title
- `description` (str): Video description
- `page_id` (str, optional): Facebook page ID for page uploads
- `published` (bool): Publish immediately or save as draft

**Returns:**
- `Dict`: Response with video ID

##### upload_video_resumable()

Upload large videos using resumable upload.

```python
upload_video_resumable(
    video_path: str,
    title: str,
    description: str = "",
    page_id: Optional[str] = None
) -> Dict
```

Use for videos larger than 1GB.

##### get_video_insights()

Get video analytics.

```python
get_video_insights(video_id: str) -> Dict
```

##### delete_video()

Delete a video.

```python
delete_video(video_id: str) -> bool
```

---

### InstagramUploader Class

Upload and manage videos on Instagram.

#### Constructor

```python
InstagramUploader(
    username: Optional[str] = None,
    password: Optional[str] = None
)
```

**Parameters:**
- `username` (str, optional): Instagram username (or use IG_USERNAME env var)
- `password` (str, optional): Instagram password (or use IG_PASSWORD env var)

#### Methods

##### login()

Login to Instagram.

```python
login()
```

Automatically called by upload methods.

##### upload_video()

Upload video to Instagram feed.

```python
upload_video(
    video_path: str,
    caption: str = "",
    thumbnail_path: Optional[str] = None
) -> Media
```

**Parameters:**
- `video_path` (str): Path to video file
- `caption` (str): Video caption
- `thumbnail_path` (str, optional): Custom thumbnail image

**Returns:**
- `Media`: Media object with upload details

##### upload_reel()

Upload video as Instagram Reel.

```python
upload_reel(
    video_path: str,
    caption: str = "",
    thumbnail_path: Optional[str] = None
) -> Media
```

##### upload_story()

Upload video as Instagram Story.

```python
upload_story(
    video_path: str,
    caption: str = ""
) -> Media
```

##### upload_igtv()

Upload video as IGTV.

```python
upload_igtv(
    video_path: str,
    title: str,
    caption: str = "",
    thumbnail_path: Optional[str] = None
) -> Media
```

##### get_media_info()

Get media statistics.

```python
get_media_info(media_id: str) -> Dict
```

**Returns:**
```python
{
    'id': '...',
    'code': '...',
    'likes': 100,
    'comments': 20,
    'views': 500,
    'caption': '...'
}
```

---

## Platform-Specific Settings

### Default Resolutions

| Platform  | Resolution  | Aspect Ratio |
|-----------|-------------|--------------|
| YouTube   | 1920x1080   | 16:9         |
| Facebook  | 1280x720    | 16:9         |
| Instagram | 1080x1080   | 1:1          |

### Recommended Video Specs

**YouTube:**
- Resolution: 1920x1080 (1080p) or 3840x2160 (4K)
- Aspect Ratio: 16:9
- Frame Rate: 24, 30, or 60 fps
- Format: MP4 (H.264 codec)

**Facebook:**
- Resolution: 1280x720 minimum
- Aspect Ratio: 16:9 (landscape) or 9:16 (vertical)
- Frame Rate: 30 fps
- Format: MP4 (H.264 codec)
- Max Duration: 240 minutes

**Instagram:**
- Feed: 1080x1080 (1:1) or 1080x1350 (4:5)
- Reels: 1080x1920 (9:16)
- Stories: 1080x1920 (9:16)
- Frame Rate: 30 fps
- Format: MP4 (H.264 codec)
- Max Duration: 60 seconds (Feed), 90 seconds (Reels)

---

## Error Handling

All methods may raise exceptions. Wrap calls in try-except:

```python
try:
    video_path = generator.generate_video(...)
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Error: {e}")
```

Common exceptions:
- `FileNotFoundError`: File or credentials not found
- `ValueError`: Invalid parameters
- `Exception`: API errors, upload failures

---

## Rate Limits

Be aware of platform rate limits:

- **YouTube**: 10,000 units/day (upload = 1,600 units)
- **Facebook**: Varies by app tier
- **Instagram**: No official limits, but avoid spam behavior

---

## Best Practices

1. **Always test with private/draft uploads first**
2. **Handle errors gracefully**
3. **Respect platform guidelines and ToS**
4. **Use appropriate video formats and resolutions**
5. **Keep credentials secure**
6. **Monitor API quotas**

---

For more examples, see the `examples/` directory.
