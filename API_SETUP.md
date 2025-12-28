# API Setup Guides

Detailed instructions for setting up each API used in the system.

## 1. NewsAPI Setup

### Free Tier
- **Limit**: 100 requests/day
- **Coverage**: Headlines from 70+ sources
- **Best for**: Testing and small projects

### Steps:
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Sign up with your email
4. Verify your email
5. Copy your API key
6. Add to `config/config.json`:
```json
{
  "news_api": {
    "api_key": "your_api_key_here"
  }
}
```

### Testing:
```bash
python -c "from newsapi import NewsApiClient; client = NewsApiClient(api_key='YOUR_KEY'); print(client.get_top_headlines(language='en', page_size=5))"
```

## 2. YouTube Data API v3

### Prerequisites
- Google Account
- Google Cloud Project

### Setup Steps:

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com/
   - Click "Select Project" → "New Project"
   - Name: "Video Generation Project"
   - Click "Create"

2. **Enable YouTube Data API**
   - In Google Cloud Console, go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click on it and press "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - User Type: External
     - App name: "Video Generation Bot"
     - Support email: Your email
     - Developer contact: Your email
     - Save and continue
   - Application type: "Desktop app"
   - Name: "Video Generator"
   - Click "Create"

4. **Download Credentials**
   - Click the download button (⬇️) next to your credential
   - Save as `credentials/youtube_credentials.json`

5. **Configure Scopes**
   - In OAuth consent screen, add scope:
     - `https://www.googleapis.com/auth/youtube.upload`

6. **First Run Authentication**
   - First time you run, a browser will open
   - Sign in with your Google account
   - Grant permissions
   - A token will be saved for future use

### Quotas
- **Free Tier**: 10,000 units/day
- **Video Upload**: 1,600 units per video
- **~6 videos per day** on free tier

### Testing:
```bash
python -m src.social_media.youtube_uploader
```

## 3. Instagram API (instagrapi)

### Important Notes
- Uses unofficial API (no official API for posting)
- Use a dedicated account (not your personal one)
- Risk of temporary bans if overused
- Enable 2FA for security

### Setup Steps:

1. **Create Instagram Account**
   - Create a new Instagram account (or use existing)
   - **Important**: Don't use your personal account
   - Complete profile setup
   - Post 1-2 manual posts first (looks more human)

2. **Configure Account**
   - Enable 2-Factor Authentication (recommended)
   - Add profile picture and bio
   - Verify email and phone

3. **Add Credentials**
   Edit `config/config.json`:
   ```json
   {
     "instagram": {
       "username": "your_username",
       "password": "your_password",
       "enabled": true,
       "upload_as": "reel"
     }
   }
   ```

### Rate Limits (Unofficial)
- **Recommended**: 1-3 posts per day
- **Safe**: Wait 2-3 hours between posts
- **Avoid**: Posting same content repeatedly

### Video Requirements
- **Format**: MP4
- **Duration**: 3-60 seconds (Reels), up to 60 minutes (IGTV)
- **Aspect Ratio**: 9:16 (vertical) for Reels, 16:9 (horizontal) for IGTV
- **Size**: Max 650MB (Reels), max 3.6GB (IGTV)

### Testing:
```bash
python -m src.social_media.instagram_uploader your_username your_password
```

## 4. Facebook Graph API

### Prerequisites
- Facebook Account
- Facebook Page (for page posting)

### Setup Steps:

1. **Create Facebook App**
   - Go to https://developers.facebook.com/
   - Click "My Apps" → "Create App"
   - Use case: "Other"
   - App Type: "Business"
   - App name: "Video Generator"
   - Contact email: Your email
   - Click "Create App"

2. **Get App Credentials**
   - In Dashboard, copy:
     - App ID
     - App Secret (click "Show")

3. **Generate Access Token**
   
   **Option A: Graph API Explorer (Short-lived)**
   - Go to https://developers.facebook.com/tools/explorer/
   - Select your app
   - Get Token → "Get User Access Token"
   - Select permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `publish_video`
   - Generate token
   
   **Option B: Long-lived Token (Recommended)**
   - Get short-lived token from Option A
   - Exchange for long-lived:
   ```bash
   curl "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
   ```

4. **Get Page ID** (if posting to page)
   - Go to your Facebook Page
   - Settings → About
   - Scroll to "Page ID"
   - Or use Graph API Explorer: `/me/accounts`

5. **Add to Configuration**
   Edit `config/config.json`:
   ```json
   {
     "facebook": {
       "app_id": "your_app_id",
       "app_secret": "your_app_secret",
       "access_token": "your_access_token",
       "page_id": "your_page_id",
       "enabled": true
     }
   }
   ```

### Rate Limits
- **Page**: 75 video posts per user per day
- **Profile**: 50 posts per day
- **Size**: Max 10GB per video

### Video Requirements
- **Format**: MP4, MOV
- **Duration**: 1 second to 240 minutes
- **Size**: Max 10GB
- **Codec**: H.264

### Testing:
```bash
python -m src.social_media.facebook_uploader YOUR_APP_ID YOUR_APP_SECRET YOUR_ACCESS_TOKEN
```

## 5. Optional: Google Text-to-Speech (Advanced)

For better voice quality, you can use Google Cloud TTS instead of gTTS.

### Setup:
1. Go to https://console.cloud.google.com/
2. Enable "Cloud Text-to-Speech API"
3. Create service account key
4. Download JSON credentials
5. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

### Update Code:
Modify `src/video_generator/text_to_speech.py` to use Google Cloud TTS.

## Troubleshooting

### YouTube: "Access Not Configured"
- Make sure YouTube Data API v3 is enabled in Google Cloud Console
- Wait a few minutes after enabling

### Instagram: "Challenge Required"
- Instagram detected unusual activity
- Complete the challenge (email/SMS verification)
- Wait 24 hours before retrying
- Reduce posting frequency

### Facebook: "Invalid Access Token"
- Token expired (short-lived tokens expire in hours)
- Generate a long-lived token
- Or re-generate token

### News API: "Rate Limit Exceeded"
- Free tier: 100 requests/day
- Reduce `max_articles` in config
- Upgrade to paid plan
- Or rely only on RSS feeds

## Security Reminders

- **Never commit credentials** to git
- **Rotate tokens** regularly
- **Use environment variables** in production
- **Enable 2FA** where possible
- **Monitor API usage** for unusual activity
- **Keep dependencies updated**

## Getting Help

- **YouTube API**: https://developers.google.com/youtube/v3
- **Instagram**: https://github.com/adw0rd/instagrapi
- **Facebook Graph**: https://developers.facebook.com/docs/graph-api
- **NewsAPI**: https://newsapi.org/docs
