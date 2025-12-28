"""
Configuration management for the video generation system.
"""
import json
import os
from typing import Dict, Any


class Config:
    """Manages application configuration."""
    
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Please copy config/config.example.json to config/config.json"
            )
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def get_news_api_key(self) -> str:
        """Get News API key."""
        return self.get('news_api.api_key', '')
    
    def get_news_sources(self) -> list:
        """Get news sources."""
        return self.get('news_api.sources', [])
    
    def get_news_categories(self) -> list:
        """Get news categories."""
        return self.get('news_api.categories', ['general'])
    
    def get_rss_feeds(self) -> list:
        """Get RSS feed URLs."""
        return self.get('rss_feeds', [])
    
    def get_video_settings(self) -> Dict[str, Any]:
        """Get video generation settings."""
        return self.get('video', {
            'width': 1920,
            'height': 1080,
            'fps': 30,
            'duration': 60,
            'background_color': [0, 51, 102]
        })
    
    def get_tts_settings(self) -> Dict[str, Any]:
        """Get text-to-speech settings."""
        return self.get('tts', {
            'engine': 'gtts',
            'language': 'en',
            'speed': 1.0
        })
    
    def get_youtube_credentials(self) -> str:
        """Get YouTube credentials file path."""
        return self.get('youtube.credentials_file', 'credentials/youtube_credentials.json')
    
    def get_instagram_credentials(self) -> Dict[str, str]:
        """Get Instagram credentials."""
        return {
            'username': self.get('instagram.username', ''),
            'password': self.get('instagram.password', '')
        }
    
    def get_facebook_credentials(self) -> Dict[str, str]:
        """Get Facebook credentials."""
        return {
            'app_id': self.get('facebook.app_id', ''),
            'app_secret': self.get('facebook.app_secret', ''),
            'access_token': self.get('facebook.access_token', '')
        }
