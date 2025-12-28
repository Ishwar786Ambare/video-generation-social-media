"""
Quick test to verify Groq integration is working
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_setup():
    """Test if Groq is properly configured"""
    
    print("=" * 60)
    print("Testing Groq AI Integration")
    print("=" * 60)
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        print("\n📝 To fix this:")
        print("1. Create a .env file in the project root")
        print("2. Add: GROQ_API_KEY=your_api_key_here")
        print("3. Get your API key from: https://console.groq.com/")
        return False
    
    if api_key == "your_groq_api_key_here":
        print("⚠️  GROQ_API_KEY is set to the example value")
        print("\n📝 Please update your .env file with your actual API key")
        print("   Get it from: https://console.groq.com/")
        return False
    
    print("✓ GROQ_API_KEY found")
    print(f"  Key starts with: {api_key[:10]}...")
    
    # Test Groq connection
    try:
        from src.video_generator.content_generator import ContentGenerator
        
        print("\n✓ ContentGenerator module loaded")
        
        # Initialize content generator
        content_gen = ContentGenerator()
        print("✓ ContentGenerator initialized")
        
        # Test a simple generation
        print("\n🤖 Testing AI content generation...")
        script = content_gen.generate_script(
            topic="Welcome to AI-powered video generation",
            duration=10,
            style="informative",
            platform="youtube"
        )
        
        print("✓ AI generation successful!")
        print(f"\n📝 Generated script preview:")
        print("-" * 60)
        print(script[:200] + "...")
        print("-" * 60)
        
        print("\n🎉 SUCCESS! Groq integration is working perfectly!")
        print("\n💡 Next steps:")
        print("   - Run: python examples/ai_content_generation.py")
        print("   - Check: docs/GROQ_GUIDE.md for more examples")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n📝 Run: pip install groq==0.13.0")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📝 Please check:")
        print("   1. Your API key is correct")
        print("   2. You have internet connection")
        print("   3. Your Groq account is active")
        return False


if __name__ == "__main__":
    success = test_groq_setup()
    
    if not success:
        print("\n" + "=" * 60)
        print("Setup incomplete. Please follow the instructions above.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("All systems ready! Start creating amazing videos! 🚀")
        print("=" * 60)
