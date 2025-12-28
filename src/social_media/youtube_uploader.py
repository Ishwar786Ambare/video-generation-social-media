"""
YouTube video uploader using YouTube Data API.
"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubeUploader:
    """Uploads videos to YouTube."""
    
    def __init__(self, credentials_file: str = 'credentials/youtube_credentials.json'):
        """Initialize YouTube uploader."""
        self.credentials_file = credentials_file
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API."""
        creds = None
        token_file = 'credentials/youtube_token.pickle'
        
        # Load saved credentials
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    logger.error(f"Credentials file not found: {self.credentials_file}")
                    logger.info("Please download OAuth 2.0 credentials from Google Cloud Console")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        logger.info("Authenticated with YouTube API")
    
    def upload_video(self, video_path: str, title: str, description: str,
                    tags: list = None, category: str = '25', privacy: str = 'public') -> str:
        """
        Upload a video to YouTube.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category: Video category ID (25 = News & Politics)
            privacy: Privacy status (public, private, unlisted)
        
        Returns:
            Video ID if successful
        """
        if not self.youtube:
            logger.error("Not authenticated with YouTube")
            return None
        
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or ['news', 'daily news', 'automated'],
                    'categoryId': category
                },
                'status': {
                    'privacyStatus': privacy,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            media = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024*1024
            )
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            logger.info(f"Video uploaded successfully: https://youtube.com/watch?v={video_id}")
            return video_id
        
        except Exception as e:
            logger.error(f"Error uploading to YouTube: {e}")
            return None


if __name__ == "__main__":
    # Test YouTube uploader (requires valid credentials)
    uploader = YouTubeUploader()
    print("YouTube uploader initialized")
    print("To upload a video, call: uploader.upload_video('path/to/video.mp4', 'Title', 'Description')")
