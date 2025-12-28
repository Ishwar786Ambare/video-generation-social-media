#!/usr/bin/env python3
"""
Example script showing how to use individual components.
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.news_fetcher.rss_fetcher import RSSFetcher
from src.storage.database import Database
from src.video_generator.video_creator import VideoCreator


def example_fetch_and_store():
    """Example: Fetch news and store in database."""
    print("=" * 50)
    print("Example 1: Fetching and Storing News")
    print("=" * 50)
    
    # Initialize RSS fetcher
    feeds = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "http://rss.cnn.com/rss/edition.rss"
    ]
    fetcher = RSSFetcher(feeds)
    
    # Fetch articles
    articles = fetcher.fetch_all(max_per_feed=5)
    print(f"\nFetched {len(articles)} articles")
    
    # Store in database
    db = Database("news_data/news.db")
    
    for article in articles:
        # Check if already exists
        if not db.get_article_by_url(article['url']):
            db.add_article(article)
            print(f"Stored: {article['title'][:50]}...")
    
    db.close()
    print("\nDone!")


def example_generate_video():
    """Example: Generate video from database articles."""
    print("\n" + "=" * 50)
    print("Example 2: Generating Video from Articles")
    print("=" * 50)
    
    # Get articles from database
    db = Database("news_data/news.db")
    articles = db.get_unused_articles(limit=3)
    
    if not articles:
        print("\nNo unused articles found. Run example_fetch_and_store() first.")
        db.close()
        return
    
    print(f"\nUsing {len(articles)} articles for video")
    
    # Convert to dict format
    article_dicts = []
    for article in articles:
        article_dicts.append({
            'title': article.title,
            'description': article.description[:100] if article.description else '',
            'source': article.source
        })
        print(f"- {article.title[:50]}...")
    
    # Create video
    creator = VideoCreator()
    output_path = "output/videos/example_video.mp4"
    
    print("\nGenerating video (this may take a minute)...")
    video_path = creator.create_news_video(
        article_dicts,
        output_path,
        duration_per_article=8
    )
    
    # Mark articles as used
    for article in articles:
        db.mark_article_used(article.id, video_path)
    
    db.close()
    
    print(f"\nVideo created: {video_path}")
    print("You can now play this video with your media player!")


def example_simple_video():
    """Example: Create a simple test video."""
    print("\n" + "=" * 50)
    print("Example 3: Creating a Simple Test Video")
    print("=" * 50)
    
    creator = VideoCreator()
    
    title = "Welcome to Automated News Videos"
    description = "This is a test video created with Python. The system can automatically generate videos from news articles and upload them to social media platforms."
    
    output_path = "output/videos/test_simple.mp4"
    
    print("\nGenerating simple test video...")
    video_path = creator.create_simple_video(
        title,
        description,
        output_path,
        duration=15
    )
    
    print(f"\nTest video created: {video_path}")


def main():
    """Run examples."""
    print("Automated Video Generation - Examples")
    print("=" * 50)
    
    # Create output directories
    os.makedirs("news_data", exist_ok=True)
    os.makedirs("output/videos", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    
    while True:
        print("\nChoose an example to run:")
        print("1. Fetch news and store in database")
        print("2. Generate video from stored articles")
        print("3. Create a simple test video")
        print("4. Run all examples")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-4): ").strip()
        
        if choice == '1':
            example_fetch_and_store()
        elif choice == '2':
            example_generate_video()
        elif choice == '3':
            example_simple_video()
        elif choice == '4':
            example_fetch_and_store()
            example_generate_video()
            example_simple_video()
            print("\nAll examples completed!")
            break
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
