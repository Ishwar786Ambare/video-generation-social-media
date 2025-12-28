"""
RSS feed parser for fetching news from RSS sources.
"""
import feedparser
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSFetcher:
    """Fetches news from RSS feeds."""
    
    def __init__(self, feed_urls: List[str]):
        """Initialize with list of RSS feed URLs."""
        self.feed_urls = feed_urls
    
    def fetch_all(self, max_per_feed: int = 10) -> List[Dict]:
        """Fetch articles from all configured RSS feeds."""
        all_articles = []
        
        for url in self.feed_urls:
            articles = self.fetch_feed(url, max_per_feed)
            all_articles.extend(articles)
        
        logger.info(f"Fetched {len(all_articles)} articles from {len(self.feed_urls)} RSS feeds")
        return all_articles
    
    def fetch_feed(self, feed_url: str, max_entries: int = 10) -> List[Dict]:
        """Fetch articles from a single RSS feed."""
        try:
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {feed_url}")
            
            articles = []
            for entry in feed.entries[:max_entries]:
                articles.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', entry.get('description', '')),
                    'content': entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '',
                    'source': feed.feed.get('title', 'RSS Feed'),
                    'author': entry.get('author', ''),
                    'url': entry.get('link', ''),
                    'published_at': self._parse_date(entry),
                    'category': 'rss'
                })
            
            logger.info(f"Fetched {len(articles)} articles from {feed_url}")
            return articles
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_url}: {e}")
            return []
    
    def _parse_date(self, entry: Dict) -> datetime:
        """Parse published date from RSS entry."""
        date_fields = ['published_parsed', 'updated_parsed']
        
        for field in date_fields:
            if hasattr(entry, field):
                time_struct = getattr(entry, field)
                if time_struct:
                    try:
                        return datetime(*time_struct[:6])
                    except (ValueError, TypeError, AttributeError):
                        pass
        
        return datetime.utcnow()


if __name__ == "__main__":
    # Test the RSS fetcher
    test_feeds = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "http://rss.cnn.com/rss/edition.rss"
    ]
    
    fetcher = RSSFetcher(test_feeds)
    articles = fetcher.fetch_all(max_per_feed=5)
    print(f"Fetched {len(articles)} articles")
    for article in articles[:5]:
        print(f"- {article['title']}")
