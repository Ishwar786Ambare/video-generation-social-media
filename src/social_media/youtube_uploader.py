"""
YouTube Uploader Module
Upload videos to YouTube using Google API
"""

import os
import pickle
from typing import Optional, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YouTubeUploader:
    """Upload videos to YouTube"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, credentials_path: str = "credentials/youtube_credentials.json"):
        """
        Initialize YouTube Uploader
        
        Args:
            credentials_path: Path to OAuth2 credentials JSON file
        """
        self.credentials_path = credentials_path
        self.token_path = "credentials/youtube_token.pickle"
        self.youtube = None
    
    def authenticate(self):
        """Authenticate with YouTube API"""
        creds = None
        
        # Load saved credentials if available
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Please download OAuth2 credentials from Google Cloud Console"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        return self.youtube
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        category: str = "22",  # People & Blogs
        privacy_status: str = "private",
        tags: Optional[list] = None
    ) -> Dict:
        """
        Upload video to YouTube
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            category: YouTube category ID
            privacy_status: Privacy status (public, private, unlisted)
            tags: List of tags
            
        Returns:
            Response dict with video ID and details
        """
        if not self.youtube:
            self.authenticate()
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        # Execute upload
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        print(f"Uploading video: {title}")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"Upload progress: {progress}%")
        
        video_id = response['id']
        print(f"Video uploaded successfully! Video ID: {video_id}")
        print(f"Watch at: https://www.youtube.com/watch?v={video_id}")
        
        return response
    
    def update_video(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list] = None
    ) -> Dict:
        """
        Update video metadata
        
        Args:
            video_id: YouTube video ID
            title: New title
            description: New description
            tags: New tags
            
        Returns:
            Response dict
        """
        if not self.youtube:
            self.authenticate()
        
        # Get current video details
        video = self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        if not video['items']:
            raise ValueError(f"Video not found: {video_id}")
        
        snippet = video['items'][0]['snippet']
        
        # Update fields
        if title:
            snippet['title'] = title
        if description:
            snippet['description'] = description
        if tags:
            snippet['tags'] = tags
        
        # Execute update
        response = self.youtube.videos().update(
            part='snippet',
            body={
                'id': video_id,
                'snippet': snippet
            }
        ).execute()
        
        print(f"Video updated successfully: {video_id}")
        return response
