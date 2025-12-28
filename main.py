"""
Main orchestration script for automated video generation and social media posting.
"""
import argparse
import logging
import os
import schedule
import time
from datetime import datetime
from typing import List, Dict

from src.utils.config import Config
from src.news_fetcher.news_api_client import NewsAPIFetcher
from src.news_fetcher.rss_fetcher import RSSFetcher
from src.storage.database import Database
from src.video_generator.video_creator import VideoCreator
from src.social_media.youtube_uploader import YouTubeUploader
from src.social_media.instagram_uploader import InstagramUploader
from src.social_media.facebook_uploader import FacebookUploader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VideoGenerationPipeline:
    """Main pipeline for automated video generation and posting."""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize the pipeline."""
        self.config = Config(config_path)
        self.db = Database(self.config.get('database.path', 'news_data/news.db'))
        
        # Initialize video settings
        video_settings = self.config.get_video_settings()
        self.video_creator = VideoCreator(
            width=video_settings.get('width', 1920),
            height=video_settings.get('height', 1080),
            fps=video_settings.get('fps', 30)
        )
        
        # Initialize social media uploaders (lazy loading)
        self._youtube_uploader = None
        self._instagram_uploader = None
        self._facebook_uploader = None
    
    def fetch_news(self):
        """Fetch news from all configured sources."""
        logger.info("Fetching news from sources...")
        all_articles = []
        
        # Fetch from News API
        news_api_key = self.config.get_news_api_key()
        if news_api_key:
            try:
                fetcher = NewsAPIFetcher(news_api_key)
                categories = self.config.get_news_categories()
                
                for category in categories:
                    articles = fetcher.fetch_top_headlines(
                        category=category,
                        page_size=self.config.get('news_api.max_articles', 20) // len(categories)
                    )
                    all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error fetching from News API: {e}")
        
        # Fetch from RSS feeds
        rss_feeds = self.config.get_rss_feeds()
        if rss_feeds:
            try:
                fetcher = RSSFetcher(rss_feeds)
                articles = fetcher.fetch_all(max_per_feed=5)
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error fetching from RSS feeds: {e}")
        
        # Store articles in database
        stored_count = 0
        for article in all_articles:
            # Check if article already exists
            if not self.db.get_article_by_url(article['url']):
                self.db.add_article(article)
                stored_count += 1
        
        logger.info(f"Fetched {len(all_articles)} articles, stored {stored_count} new articles")
        return stored_count
    
    def generate_video(self) -> str:
        """Generate video from unused news articles."""
        logger.info("Generating video...")
        
        # Get unused articles
        max_articles = self.config.get('video.max_articles_per_video', 5)
        articles = self.db.get_unused_articles(limit=max_articles)
        
        if not articles:
            logger.warning("No unused articles available for video generation")
            return None
        
        # Convert to dict format
        article_dicts = []
        for article in articles:
            article_dicts.append({
                'title': article.title,
                'description': article.description,
                'source': article.source
            })
        
        # Generate output path
        output_dir = self.config.get('output.video_directory', 'output/videos')
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"{output_dir}/news_video_{timestamp}.mp4"
        
        # Create video
        duration_per_article = self.config.get('video.duration_per_article', 10)
        video_path = self.video_creator.create_news_video(
            article_dicts,
            output_path,
            duration_per_article=duration_per_article
        )
        
        # Mark articles as used
        for article in articles:
            self.db.mark_article_used(article.id, video_path)
        
        logger.info(f"Video generated: {video_path}")
        return video_path
    
    def upload_to_social_media(self, video_path: str):
        """Upload video to all enabled social media platforms."""
        logger.info("Uploading to social media platforms...")
        
        date_str = datetime.now().strftime('%B %d, %Y')
        
        # Upload to YouTube
        if self.config.get('youtube.enabled', False):
            try:
                if not self._youtube_uploader:
                    creds_file = self.config.get_youtube_credentials()
                    self._youtube_uploader = YouTubeUploader(creds_file)
                
                title = self.config.get('youtube.title_template', 'Daily News - {date}').format(date=date_str)
                description = self.config.get('youtube.description_template', 'Daily news summary')
                tags = self.config.get('youtube.tags', ['news'])
                
                video_id = self._youtube_uploader.upload_video(
                    video_path,
                    title=title,
                    description=description,
                    tags=tags,
                    category=self.config.get('youtube.category', '25'),
                    privacy=self.config.get('youtube.privacy', 'public')
                )
                
                if video_id:
                    logger.info(f"Uploaded to YouTube: {video_id}")
            except Exception as e:
                logger.error(f"Error uploading to YouTube: {e}")
        
        # Upload to Instagram
        if self.config.get('instagram.enabled', False):
            try:
                if not self._instagram_uploader:
                    creds = self.config.get_instagram_credentials()
                    self._instagram_uploader = InstagramUploader(
                        creds['username'],
                        creds['password']
                    )
                
                caption = self.config.get('instagram.caption_template', 'Daily News').format(
                    date=date_str,
                    topics='Top Stories'
                )
                
                upload_as = self.config.get('instagram.upload_as', 'reel')
                if upload_as == 'reel':
                    media_id = self._instagram_uploader.upload_reel(video_path, caption)
                elif upload_as == 'igtv':
                    media_id = self._instagram_uploader.upload_igtv(
                        video_path,
                        title=f"Daily News - {date_str}",
                        caption=caption
                    )
                else:
                    media_id = self._instagram_uploader.upload_video(video_path, caption)
                
                if media_id:
                    logger.info(f"Uploaded to Instagram: {media_id}")
            except Exception as e:
                logger.error(f"Error uploading to Instagram: {e}")
        
        # Upload to Facebook
        if self.config.get('facebook.enabled', False):
            try:
                if not self._facebook_uploader:
                    creds = self.config.get_facebook_credentials()
                    self._facebook_uploader = FacebookUploader(
                        creds['app_id'],
                        creds['app_secret'],
                        creds['access_token']
                    )
                
                title = self.config.get('facebook.title_template', 'Daily News - {date}').format(date=date_str)
                description = self.config.get('facebook.description_template', 'Daily news summary')
                page_id = self.config.get('facebook.page_id')
                
                video_id = self._facebook_uploader.upload_video(
                    video_path,
                    title=title,
                    description=description,
                    page_id=page_id if page_id else None
                )
                
                if video_id:
                    logger.info(f"Uploaded to Facebook: {video_id}")
            except Exception as e:
                logger.error(f"Error uploading to Facebook: {e}")
    
    def run(self):
        """Run the complete pipeline."""
        logger.info("Starting video generation pipeline...")
        
        try:
            # Step 1: Fetch news
            self.fetch_news()
            
            # Step 2: Generate video
            video_path = self.generate_video()
            
            if not video_path:
                logger.warning("No video generated, skipping upload")
                return
            
            # Step 3: Upload to social media
            self.upload_to_social_media(video_path)
            
            logger.info("Pipeline completed successfully!")
        
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
        
        finally:
            self.db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Automated video generation for social media'
    )
    parser.add_argument(
        '--config',
        default='config/config.json',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Run on a schedule'
    )
    parser.add_argument(
        '--time',
        default='09:00',
        help='Time to run daily (HH:MM format)'
    )
    
    args = parser.parse_args()
    
    # Create pipeline
    pipeline = VideoGenerationPipeline(args.config)
    
    if args.schedule:
        # Schedule daily execution
        logger.info(f"Scheduling daily execution at {args.time}")
        schedule.every().day.at(args.time).do(pipeline.run)
        
        logger.info("Scheduler started. Press Ctrl+C to exit.")
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        # Run once
        pipeline.run()


if __name__ == "__main__":
    main()
