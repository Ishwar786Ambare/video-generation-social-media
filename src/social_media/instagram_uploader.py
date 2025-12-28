"""
Instagram Uploader Module
Upload videos to Instagram using Instagrapi
"""

import os
from typing import Optional, Dict
from instagrapi import Client
from instagrapi.types import Media


class InstagramUploader:
    """Upload videos to Instagram"""
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize Instagram Uploader
        
        Args:
            username: Instagram username (or set IG_USERNAME env var)
            password: Instagram password (or set IG_PASSWORD env var)
        """
        self.username = username or os.getenv('IG_USERNAME')
        self.password = password or os.getenv('IG_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError(
                "Instagram credentials required. "
                "Set IG_USERNAME and IG_PASSWORD environment variables "
                "or pass username and password parameters"
            )
        
        self.client = Client()
        self.logged_in = False
    
    def login(self):
        """Login to Instagram"""
        if not self.logged_in:
            print("Logging in to Instagram...")
            self.client.login(self.username, self.password)
            self.logged_in = True
            print("Successfully logged in!")
    
    def upload_video(
        self,
        video_path: str,
        caption: str = "",
        thumbnail_path: Optional[str] = None
    ) -> Media:
        """
        Upload video to Instagram feed
        
        Args:
            video_path: Path to video file
            caption: Video caption
            thumbnail_path: Optional custom thumbnail path
            
        Returns:
            Media object with upload details
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.login()
        
        print(f"Uploading video to Instagram: {video_path}")
        
        # Upload video
        if thumbnail_path and os.path.exists(thumbnail_path):
            media = self.client.video_upload(
                video_path,
                caption=caption,
                thumbnail=thumbnail_path
            )
        else:
            media = self.client.video_upload(
                video_path,
                caption=caption
            )
        
        print(f"Video uploaded successfully! Media ID: {media.pk}")
        print(f"Video code: {media.code}")
        print(f"View at: https://www.instagram.com/p/{media.code}/")
        
        return media
    
    def upload_reel(
        self,
        video_path: str,
        caption: str = "",
        thumbnail_path: Optional[str] = None
    ) -> Media:
        """
        Upload video as Instagram Reel
        
        Args:
            video_path: Path to video file
            caption: Reel caption
            thumbnail_path: Optional custom thumbnail path
            
        Returns:
            Media object with upload details
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.login()
        
        print(f"Uploading reel to Instagram: {video_path}")
        
        # Upload as reel
        if thumbnail_path and os.path.exists(thumbnail_path):
            media = self.client.clip_upload(
                video_path,
                caption=caption,
                thumbnail=thumbnail_path
            )
        else:
            media = self.client.clip_upload(
                video_path,
                caption=caption
            )
        
        print(f"Reel uploaded successfully! Media ID: {media.pk}")
        print(f"Reel code: {media.code}")
        print(f"View at: https://www.instagram.com/reel/{media.code}/")
        
        return media
    
    def upload_story(
        self,
        video_path: str,
        caption: str = ""
    ) -> Media:
        """
        Upload video as Instagram Story
        
        Args:
            video_path: Path to video file
            caption: Story caption/text
            
        Returns:
            Media object with upload details
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.login()
        
        print(f"Uploading story to Instagram: {video_path}")
        
        # Upload as story
        media = self.client.video_upload_to_story(
            video_path,
            caption=caption
        )
        
        print(f"Story uploaded successfully! Media ID: {media.pk}")
        
        return media
    
    def upload_igtv(
        self,
        video_path: str,
        title: str,
        caption: str = "",
        thumbnail_path: Optional[str] = None
    ) -> Media:
        """
        Upload video as IGTV
        
        Args:
            video_path: Path to video file
            title: IGTV title
            caption: IGTV caption
            thumbnail_path: Optional custom thumbnail path
            
        Returns:
            Media object with upload details
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.login()
        
        print(f"Uploading IGTV to Instagram: {video_path}")
        
        # Upload as IGTV
        if thumbnail_path and os.path.exists(thumbnail_path):
            media = self.client.igtv_upload(
                video_path,
                title=title,
                caption=caption,
                thumbnail=thumbnail_path
            )
        else:
            media = self.client.igtv_upload(
                video_path,
                title=title,
                caption=caption
            )
        
        print(f"IGTV uploaded successfully! Media ID: {media.pk}")
        print(f"IGTV code: {media.code}")
        
        return media
    
    def get_media_info(self, media_id: str) -> Dict:
        """
        Get information about uploaded media
        
        Args:
            media_id: Instagram media ID
            
        Returns:
            Dict with media information
        """
        self.login()
        
        media = self.client.media_info(int(media_id))
        return {
            'id': media.pk,
            'code': media.code,
            'likes': media.like_count,
            'comments': media.comment_count,
            'views': media.view_count if hasattr(media, 'view_count') else 0,
            'caption': media.caption_text
        }
