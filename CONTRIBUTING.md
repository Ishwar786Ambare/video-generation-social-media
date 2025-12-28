# Contributing to Video Generation Social Media

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Follow the project's coding standards

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, package versions)
- **Error messages or logs**

Example:
```markdown
## Bug: Video generation fails with certain characters

**Environment:**
- OS: Ubuntu 20.04
- Python: 3.9.5
- moviepy: 1.0.3

**Steps to reproduce:**
1. Create script with special characters: "Hello! @#$%"
2. Run generate_video()
3. Error occurs

**Error message:**
```
UnicodeEncodeError: ...
```

**Expected:** Video should be generated
**Actual:** Error is raised
```

### Suggesting Features

Feature suggestions are welcome! Include:

- **Clear use case**
- **Why it's valuable**
- **Proposed implementation** (if you have ideas)
- **Examples** of similar features elsewhere

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow coding standards
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   python -m pytest tests/
   python -m py_compile src/**/*.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add amazing feature for video filters"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Describe what changes you made
   - Reference any related issues
   - Include screenshots/examples if relevant

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ishwar786Ambare/video-generation-social-media.git
   cd video-generation-social-media
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   ```

4. **Install FFmpeg**
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from ffmpeg.org

## Coding Standards

### Python Style

Follow PEP 8 guidelines:

- **Indentation:** 4 spaces
- **Line length:** 79-100 characters
- **Naming:**
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Documentation

- **Docstrings** for all public modules, classes, and functions
- Use **Google style** docstrings
- Include **type hints** where appropriate

Example:
```python
def generate_video(
    script: str,
    title: str,
    platform: str = "youtube"
) -> str:
    """
    Generate a video from text script.
    
    Args:
        script: Text to convert to speech
        title: Video filename
        platform: Target platform
        
    Returns:
        Path to generated video file
        
    Raises:
        ValueError: If script is empty
        FileNotFoundError: If resources not found
    """
    pass
```

### Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good code coverage
- Test edge cases

### Commit Messages

Use clear, descriptive commit messages:

```
Add video filter feature

- Implement blur and sharpen filters
- Add filter parameter to generate_video()
- Update documentation with examples
- Add tests for filter functionality
```

## Project Structure

```
video-generation-social-media/
├── src/
│   ├── video_generator/    # Core video generation
│   └── social_media/        # Platform uploaders
├── examples/                # Example scripts
├── docs/                    # Documentation
├── tests/                   # Test files
├── requirements.txt         # Dependencies
└── README.md               # Main documentation
```

## Areas for Contribution

### High Priority
- [ ] Add subtitle/caption generation
- [ ] Implement video templates
- [ ] Add more TTS engine options
- [ ] Improve error handling
- [ ] Add comprehensive test suite

### Medium Priority
- [ ] Support for more video formats
- [ ] Advanced video effects (transitions, filters)
- [ ] Batch upload to multiple platforms
- [ ] Video analytics dashboard
- [ ] Configuration file support

### Documentation
- [ ] More examples and tutorials
- [ ] Video walkthroughs
- [ ] API reference improvements
- [ ] Troubleshooting guides
- [ ] Best practices guide

### Nice to Have
- [ ] GUI interface
- [ ] Web-based editor
- [ ] Cloud deployment guide
- [ ] Docker support
- [ ] CI/CD pipeline

## Questions?

- Open a GitHub issue
- Check existing documentation
- Review closed issues/PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for making this project better! 🙌
