"""
Facebook Uploader Module
Upload videos to Facebook using Graph API
"""

import os
import requests
from typing import Optional, Dict


class FacebookUploader:
    """Upload videos to Facebook"""
    
    API_VERSION = "v18.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Facebook Uploader
        
        Args:
            access_token: Facebook access token (or set FB_ACCESS_TOKEN env var)
        """
        self.access_token = access_token or os.getenv('FB_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError(
                "Facebook access token required. "
                "Set FB_ACCESS_TOKEN environment variable or pass access_token parameter"
            )
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        page_id: Optional[str] = None,
        published: bool = True
    ) -> Dict:
        """
        Upload video to Facebook page or profile
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            page_id: Facebook page ID (if uploading to page)
            published: Whether to publish immediately
            
        Returns:
            Response dict with video ID
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Determine upload endpoint
        if page_id:
            upload_url = f"{self.BASE_URL}/{page_id}/videos"
        else:
            upload_url = f"{self.BASE_URL}/me/videos"
        
        # Prepare upload parameters
        params = {
            'access_token': self.access_token,
            'title': title,
            'description': description,
            'published': str(published).lower()
        }
        
        print(f"Uploading video to Facebook: {title}")
        
        # Upload video
        with open(video_path, 'rb') as video_file:
            files = {'file': video_file}
            response = requests.post(upload_url, data=params, files=files)
        
        if response.status_code == 200:
            result = response.json()
            video_id = result.get('id')
            print(f"Video uploaded successfully! Video ID: {video_id}")
            return result
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            raise Exception(f"Upload failed: {error_msg}")
    
    def upload_video_resumable(
        self,
        video_path: str,
        title: str,
        description: str = "",
        page_id: Optional[str] = None
    ) -> Dict:
        """
        Upload large video using resumable upload
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            page_id: Facebook page ID
            
        Returns:
            Response dict with video ID
        """
        file_size = os.path.getsize(video_path)
        
        # Step 1: Initialize upload session
        if page_id:
            init_url = f"{self.BASE_URL}/{page_id}/videos"
        else:
            init_url = f"{self.BASE_URL}/me/videos"
        
        init_params = {
            'access_token': self.access_token,
            'upload_phase': 'start',
            'file_size': file_size
        }
        
        response = requests.post(init_url, data=init_params)
        if response.status_code != 200:
            raise Exception(f"Failed to initialize upload: {response.text}")
        
        upload_session_id = response.json()['upload_session_id']
        
        # Step 2: Upload video data
        with open(video_path, 'rb') as video_file:
            upload_params = {
                'access_token': self.access_token,
                'upload_phase': 'transfer',
                'upload_session_id': upload_session_id,
                'start_offset': 0
            }
            
            files = {'video_file_chunk': video_file}
            response = requests.post(init_url, data=upload_params, files=files)
            
            if response.status_code != 200:
                raise Exception(f"Failed to upload video: {response.text}")
        
        # Step 3: Finish upload
        finish_params = {
            'access_token': self.access_token,
            'upload_phase': 'finish',
            'upload_session_id': upload_session_id,
            'title': title,
            'description': description
        }
        
        response = requests.post(init_url, data=finish_params)
        if response.status_code == 200:
            result = response.json()
            print(f"Video uploaded successfully! Success: {result.get('success')}")
            return result
        else:
            raise Exception(f"Failed to finalize upload: {response.text}")
    
    def get_video_insights(self, video_id: str) -> Dict:
        """
        Get insights/analytics for a video
        
        Args:
            video_id: Facebook video ID
            
        Returns:
            Dict with video insights
        """
        url = f"{self.BASE_URL}/{video_id}/video_insights"
        params = {'access_token': self.access_token}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get insights: {response.text}")
    
    def delete_video(self, video_id: str) -> bool:
        """
        Delete a video
        
        Args:
            video_id: Facebook video ID
            
        Returns:
            True if successful
        """
        url = f"{self.BASE_URL}/{video_id}"
        params = {'access_token': self.access_token}
        
        response = requests.delete(url, params=params)
        if response.status_code == 200:
            print(f"Video deleted successfully: {video_id}")
            return True
        else:
            raise Exception(f"Failed to delete video: {response.text}")
