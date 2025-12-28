"""
News API client for fetching news articles.
"""
from newsapi import NewsApiClient
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsAPIFetcher:
    """Fetches news from NewsAPI.org"""
    
    def __init__(self, api_key: str):
        """Initialize NewsAPI client."""
        self.client = NewsApiClient(api_key=api_key)
    
    def fetch_top_headlines(self, sources: List[str] = None, 
                           category: str = 'general',
                           language: str = 'en',
                           page_size: int = 20) -> List[Dict]:
        """Fetch top headlines from NewsAPI."""
        try:
            if sources:
                response = self.client.get_top_headlines(
                    sources=','.join(sources),
                    language=language,
                    page_size=page_size
                )
            else:
                response = self.client.get_top_headlines(
                    category=category,
                    language=language,
                    page_size=page_size
                )
            
            if response['status'] == 'ok':
                articles = []
                for article in response['articles']:
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'author': article.get('author', ''),
                        'url': article.get('url', ''),
                        'published_at': self._parse_date(article.get('publishedAt')),
                        'category': category
                    })
                logger.info(f"Fetched {len(articles)} articles from NewsAPI")
                return articles
            else:
                logger.error(f"NewsAPI error: {response.get('message', 'Unknown error')}")
                return []
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
            return []
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse ISO 8601 date string."""
        if not date_str:
            return datetime.utcnow()
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()


if __name__ == "__main__":
    # Test the NewsAPI fetcher
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.news_fetcher.news_api_client <API_KEY>")
        sys.exit(1)
    
    fetcher = NewsAPIFetcher(sys.argv[1])
    articles = fetcher.fetch_top_headlines(category='technology')
    print(f"Fetched {len(articles)} articles")
    for article in articles[:5]:
        print(f"- {article['title']}")
