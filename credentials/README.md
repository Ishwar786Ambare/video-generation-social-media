# Credentials Directory

This directory stores authentication credentials for social media APIs.

## Required Files

### YouTube Credentials

**File:** `youtube_credentials.json`

Get your credentials:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the credentials JSON file
6. Save it here as `youtube_credentials.json`

### Instagram Credentials

Instagram credentials are stored in `config/config.json`:
```json
{
  "instagram": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

A session file will be automatically created at:
- `instagram_<username>.json`

### Facebook Credentials

Facebook credentials are stored in `config/config.json`:
```json
{
  "facebook": {
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "access_token": "your_access_token"
  }
}
```

To get Facebook credentials:
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Get your App ID and App Secret
4. Generate a User Access Token with video upload permissions

## Security Notes

⚠️ **IMPORTANT:** Never commit credentials to git!

- All credential files are already in `.gitignore`
- Keep your API keys and passwords secure
- Rotate credentials regularly
- Use environment variables in production

## Auto-Generated Files

The following files will be created automatically:

- `youtube_token.pickle` - YouTube session token
- `instagram_<username>.json` - Instagram session
