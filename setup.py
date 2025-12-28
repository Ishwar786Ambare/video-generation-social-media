#!/usr/bin/env python3
"""
Setup script to help configure the system.
"""
import os
import json
import shutil


def setup_config():
    """Setup configuration file."""
    config_path = "config/config.json"
    example_path = "config/config.example.json"
    
    if os.path.exists(config_path):
        print(f"✓ Configuration file already exists: {config_path}")
        overwrite = input("  Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("  Keeping existing configuration.")
            return
    
    # Copy example config
    shutil.copy(example_path, config_path)
    print(f"✓ Created configuration file: {config_path}")
    print("  Please edit this file with your API keys and preferences.")


def setup_directories():
    """Create necessary directories."""
    directories = [
        "config",
        "credentials",
        "news_data",
        "output/videos",
        "temp"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    
    required_packages = [
        'feedparser',
        'newsapi',
        'moviepy',
        'PIL',
        'gtts',
        'google',
        'instagrapi',
        'facebook',
        'sqlalchemy',
        'schedule'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print("\n⚠ Some dependencies are missing.")
        print("  Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies are installed!")
        return True


def test_news_fetch():
    """Test news fetching."""
    print("\nTesting news fetching...")
    
    try:
        from src.news_fetcher.rss_fetcher import RSSFetcher
        
        feeds = ["http://feeds.bbci.co.uk/news/rss.xml"]
        fetcher = RSSFetcher(feeds)
        articles = fetcher.fetch_feed(feeds[0], max_entries=3)
        
        if articles:
            print(f"✓ Successfully fetched {len(articles)} articles")
            print(f"  First article: {articles[0]['title'][:50]}...")
            return True
        else:
            print("✗ No articles fetched")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run setup."""
    print("=" * 60)
    print("Automated Video Generation - Setup")
    print("=" * 60)
    
    print("\n1. Setting up directories...")
    setup_directories()
    
    print("\n2. Setting up configuration...")
    setup_config()
    
    print("\n3. Checking dependencies...")
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n⚠ Please install dependencies before continuing.")
        print("  Run: pip install -r requirements.txt")
        return
    
    print("\n4. Testing news fetching...")
    test_news_fetch()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Edit config/config.json with your API keys")
    print("2. (Optional) Set up social media credentials in credentials/")
    print("3. Run: python main.py")
    print("\nFor more help, see QUICKSTART.md")


if __name__ == "__main__":
    main()
