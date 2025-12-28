"""
Instagram video uploader using instagrapi.
"""
from instagrapi import Client
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramUploader:
    """Uploads videos to Instagram."""
    
    def __init__(self, username: str, password: str):
        """Initialize Instagram uploader."""
        self.username = username
        self.password = password
        self.client = Client()
        self._login()
    
    def _login(self):
        """Login to Instagram."""
        try:
            # Try to load session
            session_file = f"credentials/instagram_{self.username}.json"
            if os.path.exists(session_file):
                self.client.load_settings(session_file)
                logger.info("Loaded Instagram session from file")
            
            # Login
            self.client.login(self.username, self.password)
            
            # Save session
            os.makedirs(os.path.dirname(session_file), exist_ok=True)
            self.client.dump_settings(session_file)
            
            logger.info(f"Logged in to Instagram as {self.username}")
        except Exception as e:
            logger.error(f"Error logging in to Instagram: {e}")
            raise
    
    def upload_video(self, video_path: str, caption: str) -> str:
        """
        Upload a video to Instagram as a post.
        
        Args:
            video_path: Path to video file
            caption: Video caption
        
        Returns:
            Media ID if successful
        """
        try:
            # Upload video
            media = self.client.video_upload(
                video_path,
                caption=caption
            )
            
            media_id = media.pk
            logger.info(f"Video uploaded to Instagram: {media_id}")
            return str(media_id)
        
        except Exception as e:
            logger.error(f"Error uploading to Instagram: {e}")
            return None
    
    def upload_reel(self, video_path: str, caption: str) -> str:
        """
        Upload a video to Instagram as a Reel.
        
        Args:
            video_path: Path to video file
            caption: Reel caption
        
        Returns:
            Media ID if successful
        """
        try:
            # Upload as reel
            media = self.client.clip_upload(
                video_path,
                caption=caption
            )
            
            media_id = media.pk
            logger.info(f"Reel uploaded to Instagram: {media_id}")
            return str(media_id)
        
        except Exception as e:
            logger.error(f"Error uploading reel to Instagram: {e}")
            return None
    
    def upload_igtv(self, video_path: str, title: str, caption: str) -> str:
        """
        Upload a video to Instagram as IGTV.
        
        Args:
            video_path: Path to video file
            title: IGTV title
            caption: IGTV caption
        
        Returns:
            Media ID if successful
        """
        try:
            # Upload as IGTV
            media = self.client.igtv_upload(
                video_path,
                title=title,
                caption=caption
            )
            
            media_id = media.pk
            logger.info(f"IGTV uploaded to Instagram: {media_id}")
            return str(media_id)
        
        except Exception as e:
            logger.error(f"Error uploading IGTV to Instagram: {e}")
            return None


if __name__ == "__main__":
    # Test Instagram uploader (requires valid credentials)
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m src.social_media.instagram_uploader <username> <password>")
        sys.exit(1)
    
    uploader = InstagramUploader(sys.argv[1], sys.argv[2])
    print("Instagram uploader initialized")
    print("To upload a video, call: uploader.upload_video('path/to/video.mp4', 'Caption')")
