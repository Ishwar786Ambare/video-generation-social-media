"""
Database models for storing news articles.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class NewsArticle(Base):
    """Model for storing news articles."""
    
    __tablename__ = 'news_articles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    content = Column(Text)
    source = Column(String(100))
    author = Column(String(200))
    url = Column(String(1000))
    published_at = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(50))
    used_in_video = Column(Boolean, default=False)
    video_id = Column(String(100))
    
    def __repr__(self):
        return f"<NewsArticle(title='{self.title}', source='{self.source}')>"
