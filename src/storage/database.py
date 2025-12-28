"""
Database management for news articles.
"""
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from .models import Base, NewsArticle
from typing import List, Optional
import os


class Database:
    """Manages database operations."""
    
    def __init__(self, db_path: str = "news_data/news.db"):
        """Initialize database connection."""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_article(self, article_data: dict) -> NewsArticle:
        """Add a news article to the database."""
        article = NewsArticle(**article_data)
        self.session.add(article)
        self.session.commit()
        return article
    
    def get_unused_articles(self, limit: int = 10) -> List[NewsArticle]:
        """Get articles that haven't been used in videos yet."""
        return self.session.query(NewsArticle).filter(
            NewsArticle.used_in_video == False
        ).order_by(desc(NewsArticle.published_at)).limit(limit).all()
    
    def mark_article_used(self, article_id: int, video_id: str = None):
        """Mark an article as used in a video."""
        article = self.session.query(NewsArticle).filter(
            NewsArticle.id == article_id
        ).first()
        if article:
            article.used_in_video = True
            article.video_id = video_id
            self.session.commit()
    
    def get_article_by_url(self, url: str) -> Optional[NewsArticle]:
        """Get an article by its URL."""
        return self.session.query(NewsArticle).filter(
            NewsArticle.url == url
        ).first()
    
    def get_recent_articles(self, limit: int = 50) -> List[NewsArticle]:
        """Get recent articles."""
        return self.session.query(NewsArticle).order_by(
            desc(NewsArticle.published_at)
        ).limit(limit).all()
    
    def close(self):
        """Close database session."""
        self.session.close()
