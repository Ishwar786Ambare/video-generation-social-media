"""
Facebook video uploader using Facebook Graph API.
"""
import facebook
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookUploader:
    """Uploads videos to Facebook."""
    
    def __init__(self, app_id: str, app_secret: str, access_token: str):
        """Initialize Facebook uploader."""
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.graph = facebook.GraphAPI(access_token=access_token)
    
    def upload_video(self, video_path: str, title: str, description: str,
                    page_id: str = None) -> str:
        """
        Upload a video to Facebook.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            page_id: Facebook page ID (if posting to a page)
        
        Returns:
            Video ID if successful
        """
        try:
            # Determine upload endpoint
            if page_id:
                endpoint = f"{page_id}/videos"
            else:
                endpoint = "me/videos"
            
            # Prepare video file
            with open(video_path, 'rb') as video_file:
                # Upload video
                response = self.graph.put_video(
                    video=video_file,
                    title=title,
                    description=description
                )
            
            video_id = response.get('id')
            logger.info(f"Video uploaded to Facebook: {video_id}")
            return video_id
        
        except Exception as e:
            logger.error(f"Error uploading to Facebook: {e}")
            return None
    
    def upload_video_chunked(self, video_path: str, title: str, description: str,
                            page_id: str = None) -> str:
        """
        Upload a large video to Facebook using chunked upload.
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            page_id: Facebook page ID (if posting to a page)
        
        Returns:
            Video ID if successful
        """
        try:
            file_size = os.path.getsize(video_path)
            
            # Determine upload endpoint
            if page_id:
                endpoint = f"https://graph-video.facebook.com/v18.0/{page_id}/videos"
            else:
                endpoint = "https://graph-video.facebook.com/v18.0/me/videos"
            
            # Start upload session
            start_params = {
                'access_token': self.access_token,
                'upload_phase': 'start',
                'file_size': file_size
            }
            
            response = requests.post(endpoint, params=start_params)
            response_data = response.json()
            
            if 'error' in response_data:
                logger.error(f"Error starting upload: {response_data['error']}")
                return None
            
            upload_session_id = response_data.get('upload_session_id')
            
            # Upload video in chunks
            chunk_size = 1024 * 1024 * 10  # 10 MB chunks
            with open(video_path, 'rb') as video_file:
                start_offset = 0
                while start_offset < file_size:
                    chunk = video_file.read(chunk_size)
                    transfer_params = {
                        'access_token': self.access_token,
                        'upload_phase': 'transfer',
                        'upload_session_id': upload_session_id,
                        'start_offset': start_offset
                    }
                    
                    files = {'video_file_chunk': chunk}
                    response = requests.post(endpoint, params=transfer_params, files=files)
                    
                    start_offset += len(chunk)
                    progress = (start_offset / file_size) * 100
                    logger.info(f"Upload progress: {progress:.1f}%")
            
            # Finish upload
            finish_params = {
                'access_token': self.access_token,
                'upload_phase': 'finish',
                'upload_session_id': upload_session_id,
                'title': title,
                'description': description
            }
            
            response = requests.post(endpoint, params=finish_params)
            response_data = response.json()
            
            if 'error' in response_data:
                logger.error(f"Error finishing upload: {response_data['error']}")
                return None
            
            video_id = response_data.get('id')
            logger.info(f"Video uploaded to Facebook: {video_id}")
            return video_id
        
        except Exception as e:
            logger.error(f"Error uploading to Facebook: {e}")
            return None


if __name__ == "__main__":
    # Test Facebook uploader (requires valid credentials)
    import sys
    if len(sys.argv) < 4:
        print("Usage: python -m src.social_media.facebook_uploader <app_id> <app_secret> <access_token>")
        sys.exit(1)
    
    uploader = FacebookUploader(sys.argv[1], sys.argv[2], sys.argv[3])
    print("Facebook uploader initialized")
    print("To upload a video, call: uploader.upload_video('path/to/video.mp4', 'Title', 'Description')")
