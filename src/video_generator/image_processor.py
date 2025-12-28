"""
Image processing for video backgrounds and text overlays.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles image generation and text overlay."""
    
    def __init__(self, width: int = 1920, height: int = 1080):
        """Initialize image processor with dimensions."""
        self.width = width
        self.height = height
    
    def create_background(self, color: tuple = (0, 51, 102), output_path: str = None) -> str:
        """Create a solid color background image."""
        if output_path is None:
            output_path = "temp/background.png"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create image with solid color
        img = Image.new('RGB', (self.width, self.height), color)
        img.save(output_path)
        
        logger.info(f"Created background image: {output_path}")
        return output_path
    
    def create_text_image(self, text: str, output_path: str = None,
                         font_size: int = 60, text_color: tuple = (255, 255, 255),
                         bg_color: tuple = (0, 51, 102), max_width: int = None) -> str:
        """Create an image with text overlay."""
        if output_path is None:
            output_path = "temp/text_image.png"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create image
        img = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fallback to default if not available
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Wrap text if max_width is specified
        if max_width is None:
            max_width = self.width - 200  # Leave margin
        
        wrapped_text = self._wrap_text(text, font, max_width, draw)
        
        # Get text bounding box
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position to center text
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Draw text
        draw.multiline_text((x, y), wrapped_text, fill=text_color, font=font, align='center')
        
        img.save(output_path)
        logger.info(f"Created text image: {output_path}")
        return output_path
    
    def _wrap_text(self, text: str, font, max_width: int, draw) -> str:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test image processor
    processor = ImageProcessor()
    processor.create_background(output_path="temp/test_bg.png")
    processor.create_text_image(
        "Breaking News: Test Article Headline Here",
        output_path="temp/test_text.png"
    )
    print("Generated test images in temp/")
