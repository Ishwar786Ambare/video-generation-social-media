"""
Content Generator Module
Uses Groq AI to generate video scripts and content
"""

import os
from typing import Optional, Dict, List
from dotenv import load_dotenv
from groq import Groq


class ContentGenerator:
    """Handles AI-powered content generation using Groq"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Content Generator with Groq
        
        Args:
            api_key: Groq API key (if not provided, reads from GROQ_API_KEY env variable)
            model: Groq model to use (if not provided, reads from GROQ_MODEL env variable)
        """
        load_dotenv()
        
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key not found. Please set GROQ_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client = Groq(api_key=self.api_key)
    
    def generate_script(
        self,
        topic: str,
        duration: int = 60,
        style: str = "informative",
        platform: str = "youtube",
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        Generate a video script for the given topic
        
        Args:
            topic: Main topic or theme for the video
            duration: Target duration in seconds
            style: Writing style (informative, entertaining, educational, promotional)
            platform: Target platform (youtube, facebook, instagram)
            additional_instructions: Any additional instructions for content generation
            
        Returns:
            Generated script text
        """
        # Calculate approximate word count (average speaking rate: 150 words/minute)
        word_count = int((duration / 60) * 150)
        
        # Platform-specific guidance
        platform_guidance = {
            "youtube": "engaging and detailed, suitable for longer-form content",
            "facebook": "conversational and shareable, with hooks to drive engagement",
            "instagram": "concise, visually-oriented, and attention-grabbing"
        }
        
        # Build the prompt
        prompt = f"""Generate a {style} video script about: {topic}

Target platform: {platform.upper()}
Target duration: {duration} seconds (approximately {word_count} words)
Style: {platform_guidance.get(platform.lower(), 'engaging and informative')}

Requirements:
- Write a compelling script that's {style} and {platform_guidance.get(platform.lower(), 'engaging')}
- Keep it around {word_count} words for a {duration}-second video
- Make it natural for text-to-speech narration (avoid special characters, write numbers as words)
- Include a strong hook at the beginning
- End with a clear call-to-action or conclusion
- Write in a conversational tone
"""
        
        if additional_instructions:
            prompt += f"\n\nAdditional instructions: {additional_instructions}"
        
        prompt += "\n\nProvide ONLY the script text, no titles, labels, or formatting."
        
        # Generate content using Groq
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional video script writer who creates engaging, "
                               "natural-sounding scripts optimized for text-to-speech narration and "
                               "social media content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        script = response.choices[0].message.content.strip()
        return script
    
    def generate_video_ideas(
        self,
        niche: str,
        count: int = 5,
        platform: str = "youtube"
    ) -> List[Dict[str, str]]:
        """
        Generate video topic ideas for a given niche
        
        Args:
            niche: The niche or category for video ideas
            count: Number of ideas to generate
            platform: Target platform
            
        Returns:
            List of dictionaries containing title and description for each idea
        """
        prompt = f"""Generate {count} compelling video ideas for the {niche} niche on {platform}.

For each idea, provide:
1. A catchy, engaging title
2. A brief description (1-2 sentences)

Format your response as a numbered list with this exact format:
1. TITLE: [title here]
   DESC: [description here]

2. TITLE: [title here]
   DESC: [description here]

Make the titles attention-grabbing and optimized for {platform}."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative content strategist specializing in social media "
                               "video content that drives engagement and views."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=1500
        )
        
        ideas_text = response.choices[0].message.content.strip()
        return self._parse_video_ideas(ideas_text)
    
    def generate_description(
        self,
        script: str,
        platform: str = "youtube",
        include_hashtags: bool = True
    ) -> str:
        """
        Generate a video description based on the script
        
        Args:
            script: The video script
            platform: Target platform
            include_hashtags: Whether to include relevant hashtags
            
        Returns:
            Generated description text
        """
        prompt = f"""Based on this video script, write an engaging description for {platform}:

Script:
{script[:500]}...

Requirements:
- Write a compelling description that summarizes the video
- Make it SEO-friendly and engaging
- Include a call-to-action
"""
        
        if include_hashtags:
            prompt += "- Include 5-10 relevant hashtags at the end\n"
        
        prompt += f"\nOptimize for {platform} best practices."
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a social media marketing expert who writes compelling "
                               "video descriptions that drive engagement and discoverability."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        description = response.choices[0].message.content.strip()
        return description
    
    def _parse_video_ideas(self, ideas_text: str) -> List[Dict[str, str]]:
        """
        Parse the generated video ideas into structured format
        
        Args:
            ideas_text: Raw text containing video ideas
            
        Returns:
            List of dictionaries with title and description
        """
        ideas = []
        lines = ideas_text.split('\n')
        current_title = None
        
        for line in lines:
            line = line.strip()
            if 'TITLE:' in line:
                current_title = line.split('TITLE:')[1].strip()
            elif 'DESC:' in line and current_title:
                description = line.split('DESC:')[1].strip()
                ideas.append({
                    "title": current_title,
                    "description": description
                })
                current_title = None
        
        return ideas
    
    def enhance_script(
        self,
        script: str,
        enhancement_type: str = "engagement"
    ) -> str:
        """
        Enhance an existing script
        
        Args:
            script: Original script to enhance
            enhancement_type: Type of enhancement (engagement, clarity, emotion, brevity)
            
        Returns:
            Enhanced script
        """
        enhancement_prompts = {
            "engagement": "Make this script more engaging and attention-grabbing while keeping the core message",
            "clarity": "Improve the clarity and simplicity of this script while maintaining its purpose",
            "emotion": "Add more emotional appeal and storytelling elements to this script",
            "brevity": "Make this script more concise while preserving all key points"
        }
        
        prompt = f"""{enhancement_prompts.get(enhancement_type, enhancement_prompts['engagement'])}:

Original Script:
{script}

Provide the enhanced script, maintaining suitability for text-to-speech narration."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert video script editor who improves scripts while "
                               "maintaining their natural flow for voice narration."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        enhanced_script = response.choices[0].message.content.strip()
        return enhanced_script
