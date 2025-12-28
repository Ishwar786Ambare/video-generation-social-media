# Getting Started with Groq AI Integration

This project now uses **Groq AI** for intelligent content generation instead of Gemini!

## 🚀 Quick Setup

### 1. Get Your Groq API Key

1. Visit [https://console.groq.com/](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key

### 2. Configure Your Environment

Create a `.env` file in the project root (or copy from `.env.example`):

```env
# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 📝 Features

The Groq integration provides:

- **🎬 AI Script Generation**: Generate video scripts from topics
- **💡 Video Ideas**: Get creative content ideas for your niche
- **📄 Description Generator**: Create SEO-friendly descriptions
- **✨ Script Enhancement**: Improve existing scripts
- **🎯 Platform Optimization**: Content tailored for YouTube, Instagram, Facebook

## 🎯 Usage Examples

### Example 1: Generate Video from Topic

```python
from src.video_generator import VideoGenerator

# Initialize with AI enabled
generator = VideoGenerator(enable_ai=True)

# Generate complete video from a topic
result = generator.generate_video_from_topic(
    topic="The benefits of meditation",
    title="meditation_guide",
    duration=60,  # seconds
    style="informative",
    platform="youtube"
)

print(f"Video: {result['video_path']}")
print(f"Script: {result['script']}")
print(f"Description: {result['description']}")
```

### Example 2: Generate Video Ideas

```python
from src.video_generator.content_generator import ContentGenerator

content_gen = ContentGenerator()

ideas = content_gen.generate_video_ideas(
    niche="productivity",
    count=5,
    platform="youtube"
)

for idea in ideas:
    print(f"{idea['title']}: {idea['description']}")
```

### Example 3: Custom Script Generation

```python
from src.video_generator.content_generator import ContentGenerator

content_gen = ContentGenerator()

# Generate script
script = content_gen.generate_script(
    topic="5 morning habits for success",
    duration=90,
    style="motivational",
    platform="instagram"
)

# Enhance the script
enhanced = content_gen.enhance_script(
    script=script,
    enhancement_type="engagement"  # or "clarity", "emotion", "brevity"
)
```

### Example 4: Complete Workflow

```python
from src.video_generator import VideoGenerator
from src.video_generator.content_generator import ContentGenerator

# Initialize
generator = VideoGenerator(enable_ai=True)
content_gen = ContentGenerator()

# Step 1: Get video ideas
ideas = content_gen.generate_video_ideas(niche="tech tips", count=3)

# Step 2: Pick an idea and generate script
script = content_gen.generate_script(
    topic=ideas[0]['title'],
    duration=60,
    platform="youtube"
)

# Step 3: Generate description
description = content_gen.generate_description(script)

# Step 4: Create video
video_path = generator.generate_video(
    script=script,
    title="tech_tip_1",
    platform="youtube"
)
```

## 🎨 Available Models

Groq supports several high-performance models:

- `llama-3.3-70b-versatile` (default) - Best for general content
- `llama-3.1-70b-versatile` - Great for creative content
- `mixtral-8x7b-32768` - Fast and efficient
- `gemma2-9b-it` - Good for shorter content

Change the model in your `.env` file or when initializing:

```python
content_gen = ContentGenerator(model="mixtral-8x7b-32768")
```

## 🎬 Content Styles

When generating scripts, you can choose from:

- `informative` - Educational and fact-based
- `entertaining` - Fun and engaging
- `educational` - Tutorial-style content
- `promotional` - Marketing and sales-focused
- `motivational` - Inspirational content

## 📱 Platform Optimization

Content is automatically optimized for:

- **YouTube**: Longer, detailed content
- **Instagram**: Short, visual-focused content
- **Facebook**: Shareable, conversational content

## 🔧 Advanced Features

### Enhancement Types

```python
enhanced = content_gen.enhance_script(
    script=original_script,
    enhancement_type="engagement"  # engagement, clarity, emotion, brevity
)
```

### Custom Instructions

```python
script = content_gen.generate_script(
    topic="Your topic",
    additional_instructions="Include 3 specific examples and end with a question"
)
```

## 📚 Full Example

Run the complete example:

```bash
python examples/ai_content_generation.py
```

## ⚙️ Configuration Options

In your `.env` file:

```env
# Required
GROQ_API_KEY=your_key_here

# Optional (with defaults)
GROQ_MODEL=llama-3.3-70b-versatile
OUTPUT_DIR=output_videos
TTS_LANGUAGE=en
```

## 🆘 Troubleshooting

### API Key Error
```
ValueError: Groq API key not found
```
**Solution**: Make sure your `.env` file contains `GROQ_API_KEY`

### Import Error
```
ImportError: No module named 'groq'
```
**Solution**: Run `pip install groq==0.13.0`

### Enable AI
```
RuntimeError: AI content generation is not enabled
```
**Solution**: Initialize with `VideoGenerator(enable_ai=True)`

## 📖 More Examples

Check out the `examples/` directory:

- `ai_content_generation.py` - Comprehensive AI usage examples
- `basic_video_generation.py` - Simple video creation
- `batch_generation.py` - Multiple videos at once

## 🎉 Benefits of Groq

- ⚡ **Super Fast**: Fastest inference speeds
- 💰 **Cost Effective**: Generous free tier
- 🎯 **High Quality**: State-of-the-art models
- 🔧 **Easy to Use**: Simple API
- 🌍 **No Gemini Required**: Completely independent

Enjoy creating amazing videos with AI-powered content! 🚀
