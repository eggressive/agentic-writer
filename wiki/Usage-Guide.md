# Usage Guide

Complete guide to using Agentic-Writer for automated content creation.

## Table of Contents

- [Command Line Interface](#command-line-interface)
- [Python API](#python-api)
- [Content Creation Options](#content-creation-options)
- [Writing Styles](#writing-styles)
- [Target Audiences](#target-audiences)
- [Publishing Platforms](#publishing-platforms)
- [Configuration](#configuration)
- [Output Format](#output-format)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)

## Command Line Interface

### Basic Command Structure

```bash
python main.py <command> [options]
```

### Available Commands

#### 1. Create Content

```bash
python main.py create "Your Topic Here" [options]
```

**Options:**
- `--style TEXT` - Writing style (default: professional)
- `--audience TEXT` - Target audience (default: general audience)
- `--platform TEXT` - Publishing platform(s) (default: file)
- `--output-dir TEXT` - Output directory (default: ./output)
- `--log-level TEXT` - Logging level (default: INFO)

#### 2. Check Configuration

```bash
python main.py config
```

Displays current configuration and API key status.

#### 3. Show Version

```bash
python main.py version
```

Displays version information.

### Command Examples

#### Simple Content Creation

```bash
python main.py create "The Future of AI"
```

Creates an article with default settings:
- Style: professional
- Audience: general audience
- Platform: file
- Output: ./output/

#### Custom Style and Audience

```bash
python main.py create "Introduction to Python" \
  --style casual \
  --audience "beginners"
```

#### Multiple Platforms

```bash
python main.py create "Remote Work Best Practices" \
  --platform file \
  --platform medium
```

#### Custom Output Directory

```bash
python main.py create "Machine Learning Basics" \
  --output-dir ./my-articles
```

#### All Options Combined

```bash
python main.py create "Sustainable Energy Solutions" \
  --style professional \
  --audience "business executives and decision makers" \
  --platform file \
  --platform medium \
  --output-dir ./energy-articles \
  --log-level DEBUG
```

## Python API

### Basic Usage

```python
from src.orchestrator import ContentCreationOrchestrator
from src.utils import Config

# Load configuration
config = Config.from_env()
config.validate_required()

# Initialize orchestrator
orchestrator = ContentCreationOrchestrator(config)

# Create content
results = orchestrator.create_content(
    topic="The Future of Quantum Computing",
    style="technical",
    target_audience="technology enthusiasts",
    platforms=["file"],
    output_dir="./articles"
)

# Check results
if results["status"] == "completed":
    print("Success!")
    print(f"Title: {results['article']['title']}")
```

### Configuration Management

```python
from src.utils import Config

# Load from environment
config = Config.from_env()

# Access configuration
print(f"Model: {config.openai_model}")
print(f"Temperature: {config.temperature}")
print(f"Max Sources: {config.max_research_sources}")

# Validate required keys
try:
    config.validate_required()
    print("Configuration valid!")
except ValueError as e:
    print(f"Configuration error: {e}")
```

### Individual Agent Usage

#### Research Agent

```python
from src.agents import ResearchAgent
from src.utils import Config
from langchain_openai import ChatOpenAI

config = Config.from_env()
llm = ChatOpenAI(
    model=config.openai_model,
    temperature=config.temperature,
    api_key=config.openai_api_key
)

researcher = ResearchAgent(
    llm=llm,
    max_sources=config.max_research_sources
)

research_results = researcher.research("Artificial Intelligence")
print(research_results["synthesis"])
```

#### Writer Agent

```python
from src.agents import WriterAgent

writer = WriterAgent(llm=llm)

article = writer.write_article(
    research_data=research_results,
    style="professional",
    target_audience="business professionals"
)

print(f"Title: {article['title']}")
print(f"Words: {article['word_count']}")
```

#### Image Agent

```python
from src.agents import ImageAgent

image_handler = ImageAgent(
    llm=llm,
    unsplash_access_key=config.unsplash_access_key
)

images = image_handler.find_images(
    article_content=article["content"],
    article_title=article["title"]
)

for img in images["images"]:
    print(f"Image: {img['url']}")
    print(f"By: {img['author']}")
```

#### Publisher Agent

```python
from src.agents import PublisherAgent

publisher = PublisherAgent(
    medium_access_token=config.medium_access_token
)

publication_results = publisher.publish(
    article=article,
    images=images,
    platforms=["file", "medium"],
    output_dir="./output"
)

for platform, result in publication_results.items():
    if result["success"]:
        print(f"{platform}: Published successfully!")
```

## Content Creation Options

### Writing Styles

Choose a style that matches your content goals:

#### Professional
```bash
--style professional
```
- Formal tone
- Business-appropriate language
- Structured and organized
- Ideal for: Business articles, reports, whitepapers

#### Casual
```bash
--style casual
```
- Conversational tone
- Friendly and approachable
- Easy to read
- Ideal for: Blog posts, personal stories, tutorials

#### Technical
```bash
--style technical
```
- Detailed explanations
- Technical terminology
- In-depth analysis
- Ideal for: Documentation, technical guides, research

#### Accessible
```bash
--style accessible
```
- Simple language
- Clear explanations
- Beginner-friendly
- Ideal for: Educational content, introductions

### Target Audiences

Define your audience for better-tailored content:

#### General Audience
```bash
--audience "general audience"
```
Suitable for most readers without specialized knowledge.

#### Professionals
```bash
--audience "business executives"
--audience "software developers"
--audience "marketing professionals"
```
Industry-specific language and examples.

#### Skill Levels
```bash
--audience "beginners"
--audience "intermediate users"
--audience "advanced practitioners"
```
Adjusted complexity and depth.

#### Demographics
```bash
--audience "high school students"
--audience "university graduates"
--audience "retirees"
```
Age-appropriate language and references.

### Publishing Platforms

Specify where to publish your content:

#### File System (Default)
```bash
--platform file
```
Saves markdown and JSON files locally.

#### Medium
```bash
--platform medium
```
Publishes to Medium (requires `MEDIUM_ACCESS_TOKEN`).

#### Multiple Platforms
```bash
--platform file --platform medium
```
Publishes to multiple destinations.

## Configuration

### Environment Variables

Set in `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key

# Model Settings
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo, gpt-4
TEMPERATURE=0.7                    # 0.0 to 1.0

# Optional APIs
MEDIUM_ACCESS_TOKEN=your-token
UNSPLASH_ACCESS_KEY=your-key

# System Settings
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
MAX_RESEARCH_SOURCES=5             # 1 to 10
MAX_RETRIES=3                      # 1 to 5
```

### Model Selection

#### GPT-4 Turbo (Recommended)
```bash
OPENAI_MODEL=gpt-4-turbo-preview
```
- Best quality
- Latest features
- Higher cost

#### GPT-4
```bash
OPENAI_MODEL=gpt-4
```
- High quality
- Reliable
- Moderate cost

#### GPT-3.5 Turbo
```bash
OPENAI_MODEL=gpt-3.5-turbo
```
- Good quality
- Fast
- Lower cost

### Temperature Settings

Controls creativity vs. consistency:

```bash
# Focused and factual (0.0-0.3)
TEMPERATURE=0.2

# Balanced - default (0.4-0.7)
TEMPERATURE=0.7

# Creative and varied (0.8-1.0)
TEMPERATURE=0.9
```

## Output Format

### Markdown File

`output/your_topic.md`:

```markdown
# Your Article Title

**Topic:** Original Topic
**Word Count:** 1342
**Tags:** tag1, tag2, tag3, tag4, tag5
**Meta Description:** Brief description...

---

## Introduction

[Article content in markdown format with proper headings, lists, etc.]

## Main Section 1

Content...

## Main Section 2

Content...

## Conclusion

Final thoughts...
```

### Metadata JSON

`output/your_topic_metadata.json`:

```json
{
  "title": "Your Article Title",
  "topic": "Original Topic",
  "word_count": 1342,
  "tags": [
    "tag1",
    "tag2",
    "tag3"
  ],
  "meta_description": "Brief description...",
  "images": [
    {
      "url": "https://images.unsplash.com/photo-...",
      "description": "Image description",
      "author": "Photographer Name",
      "author_url": "https://unsplash.com/@photographer"
    }
  ],
  "sources_count": 5
}
```

## Advanced Usage

### Custom Logging

```python
from src.utils import setup_logger

# Create custom logger
logger = setup_logger(
    name="my_app",
    level="DEBUG",
    log_file="my_app.log"
)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Batch Processing

```python
topics = [
    "AI in Healthcare",
    "Blockchain Technology",
    "Renewable Energy"
]

for topic in topics:
    results = orchestrator.create_content(
        topic=topic,
        style="professional",
        target_audience="general audience",
        platforms=["file"],
        output_dir=f"./articles/{topic.replace(' ', '_').lower()}"
    )
    print(f"Completed: {topic}")
```

### Custom Research Sources

```python
config = Config.from_env()
config.max_research_sources = 10  # More sources

orchestrator = ContentCreationOrchestrator(config)
```

### Error Handling

```python
try:
    results = orchestrator.create_content(
        topic="Your Topic",
        style="professional",
        target_audience="general audience",
        platforms=["file"],
        output_dir="./output"
    )
    
    if results["status"] == "completed":
        print("Success!")
    else:
        print(f"Failed: {results.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

### 1. Topic Selection

✅ **Good Topics:**
- "The Impact of AI on Healthcare Diagnostics"
- "Best Practices for Remote Team Management"
- "Understanding Kubernetes Architecture"

❌ **Avoid:**
- Vague topics: "AI stuff"
- Too broad: "Everything about computers"
- Too narrow: "Python list.append() function"

### 2. Audience Definition

✅ **Be Specific:**
- "software engineers with 3-5 years experience"
- "small business owners in retail"
- "college students studying data science"

❌ **Too Generic:**
- "people"
- "everyone"

### 3. Style Selection

Match style to purpose:
- **Blog posts** → casual or accessible
- **Business reports** → professional
- **Technical docs** → technical
- **Educational** → accessible

### 4. Review Before Publishing

Always review generated content:
- ✅ Check factual accuracy
- ✅ Verify tone and style
- ✅ Ensure logical flow
- ✅ Add personal insights
- ✅ Check for bias

### 5. Optimize Costs

- Use `gpt-3.5-turbo` for drafts
- Reduce `MAX_RESEARCH_SOURCES` if needed
- Cache configuration objects
- Batch similar requests

### 6. Output Organization

```bash
# Organize by topic
./articles/
  ├── ai/
  ├── technology/
  └── business/

# Or by date
./articles/
  ├── 2024-01/
  ├── 2024-02/
  └── 2024-03/
```

## Performance Tips

### Execution Time

Typical content creation takes 2-5 minutes:
- Research: 10-30 seconds
- Writing: 30-60 seconds
- Images: 5-15 seconds
- Publishing: <5 seconds

### Optimization

1. **Use faster models** for drafts:
   ```bash
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. **Reduce research sources**:
   ```bash
   MAX_RESEARCH_SOURCES=3
   ```

3. **Skip optional features**:
   - Don't configure Unsplash if images aren't needed
   - Use file-only publishing for speed

## Troubleshooting

### Slow Performance

**Issue**: Content creation takes too long

**Solutions:**
- Use `gpt-3.5-turbo` model
- Reduce `MAX_RESEARCH_SOURCES`
- Check internet connection
- Monitor OpenAI API status

### Poor Content Quality

**Issue**: Generated content isn't good enough

**Solutions:**
- Use `gpt-4-turbo-preview` or `gpt-4`
- Increase `TEMPERATURE` for creativity
- Provide more specific topic
- Define target audience clearly

### API Errors

**Issue**: OpenAI API errors

**Solutions:**
- Check API key validity
- Verify account has credits
- Check rate limits
- Review error messages

## Next Steps

- 📖 Learn about [Architecture](Architecture.md)
- 🔧 Explore [API Reference](API-Reference.md)
- 💡 See [Examples](Examples.md)
- 🐛 Check [Troubleshooting](Troubleshooting.md)

---

**Need more help?** Visit the [FAQ](FAQ.md) or [open an issue](https://github.com/eggressive/agentic-writer/issues).
