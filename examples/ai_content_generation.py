"""
AI-Powered Video Generation Example
Demonstrates how to use Groq AI to generate video content automatically
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.video_generator import VideoGenerator
from src.video_generator.content_generator import ContentGenerator


def main():
    """Generate a video using AI-powered content generation"""
    
    # Load environment variables
    load_dotenv()
    
    # Example 1: Generate video from a topic
    print("=" * 60)
    print("Example 1: AI-Generated Video from Topic")
    print("=" * 60)
    
    # Initialize video generator with AI enabled
    generator = VideoGenerator(enable_ai=True)
    
    # Generate a complete video from just a topic
    result = generator.generate_video_from_topic(
        topic="The benefits of meditation for mental health",
        title="meditation_benefits",
        duration=60,  # 60 seconds
        style="informative",
        platform="youtube"
    )
    
    print(f"\n✓ Video created: {result['video_path']}")
    print(f"\n📝 Generated Script:\n{result['script'][:200]}...")
    print(f"\n📄 Generated Description:\n{result['description'][:200]}...")
    
    # Example 2: Generate video ideas
    print("\n" + "=" * 60)
    print("Example 2: Generate Video Ideas")
    print("=" * 60)
    
    content_gen = ContentGenerator()
    ideas = content_gen.generate_video_ideas(
        niche="productivity and time management",
        count=5,
        platform="youtube"
    )
    
    print("\n💡 Video Ideas:")
    for idx, idea in enumerate(ideas, 1):
        print(f"\n{idx}. {idea['title']}")
        print(f"   {idea['description']}")
    
    # Example 3: Generate custom script and enhance it
    print("\n" + "=" * 60)
    print("Example 3: Generate and Enhance Script")
    print("=" * 60)
    
    # Generate initial script
    initial_script = content_gen.generate_script(
        topic="5 morning habits for success",
        duration=90,
        style="motivational",
        platform="instagram"
    )
    
    print(f"\n📝 Initial Script:\n{initial_script[:300]}...")
    
    # Enhance the script for more engagement
    enhanced_script = content_gen.enhance_script(
        script=initial_script,
        enhancement_type="engagement"
    )
    
    print(f"\n✨ Enhanced Script:\n{enhanced_script[:300]}...")
    
    # Generate video with the enhanced script
    video_path = generator.generate_video(
        script=enhanced_script,
        title="morning_habits_success",
        platform="instagram"
    )
    
    print(f"\n✓ Video created: {video_path}")
    
    # Example 4: Batch generate videos from AI ideas
    print("\n" + "=" * 60)
    print("Example 4: Batch Generate from AI Ideas")
    print("=" * 60)
    
    # Get video ideas
    ideas = content_gen.generate_video_ideas(
        niche="technology tips",
        count=3,
        platform="facebook"
    )
    
    # Generate scripts for each idea
    batch_configs = []
    for idx, idea in enumerate(ideas[:2], 1):  # Generate first 2 for demo
        print(f"\nGenerating content for: {idea['title']}")
        script = content_gen.generate_script(
            topic=idea['title'],
            duration=45,
            style="educational",
            platform="facebook"
        )
        
        batch_configs.append({
            "script": script,
            "title": f"tech_tip_{idx}",
            "platform": "facebook"
        })
    
    # Batch generate videos
    videos = generator.batch_generate(batch_configs, platform="facebook")
    
    print(f"\n✓ Generated {len(videos)} videos:")
    for video in videos:
        print(f"  - {video}")
    
    print("\n" + "=" * 60)
    print("✓ All examples completed successfully!")
    print("=" * 60)
    
    print("\n💡 Tips:")
    print("  1. Set your GROQ_API_KEY in .env file")
    print("  2. Adjust duration and style based on your platform")
    print("  3. Use enhance_script() to refine generated content")
    print("  4. Generate multiple ideas and pick the best ones")
    print("  5. Combine AI-generated scripts with custom images for better results")


if __name__ == "__main__":
    main()
