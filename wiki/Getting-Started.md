# Getting Started with Agentic-Writer

This guide will help you get up and running with Agentic-Writer in just a few minutes.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **pip** package manager
- An **OpenAI API key** (required) - [Get one here](https://platform.openai.com/api-keys)
- *Optional*: Unsplash API key for image search
- *Optional*: Medium API token for publishing to Medium

## Quick Start (5 Minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

### Step 3: Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional - for enhanced features
MEDIUM_ACCESS_TOKEN=your-medium-token
UNSPLASH_ACCESS_KEY=your-unsplash-key
```

### Step 4: Verify Installation

Run the verification script:

```bash
python verify_installation.py
```

You should see:
```
✓ All checks passed!
✓ Configuration is valid
✓ All dependencies are installed
```

### Step 5: Check Configuration

```bash
python main.py config
```

Expected output:
```
╭───────────────────────╮
│ Current Configuration │
╰───────────────────────╯

OpenAI Model: gpt-4-turbo-preview
Temperature: 0.7
Max Research Sources: 5
Log Level: INFO

API Keys Status:
  OpenAI: ✓ Set
  Medium: ○ Optional
  Unsplash: ○ Optional
```

### Step 6: Create Your First Article

```bash
python main.py create "The Future of Artificial Intelligence"
```

The system will:
1. 🔍 Research the topic (10-30 seconds)
2. ✍️ Write a comprehensive article (30-60 seconds)
3. 🖼️ Find relevant images (5-15 seconds)
4. 📤 Save to `output/` directory (<5 seconds)

### Step 7: View Your Article

```bash
cat output/the_future_of_artificial_intelligence.md
```

## Your First Article - Detailed Example

Let's create an article with custom options:

```bash
python main.py create "Introduction to Machine Learning" \
  --style casual \
  --audience "beginners with no technical background" \
  --platform file \
  --output-dir ./my-articles
```

**What this does:**
- **Topic**: "Introduction to Machine Learning"
- **Style**: Casual, conversational tone
- **Audience**: Written for beginners
- **Platform**: Saves to file system
- **Output**: Saves to `./my-articles/` directory

## Understanding the Output

Each content creation produces two files:

### 1. Markdown Article (`.md`)

```markdown
# Introduction to Machine Learning

**Topic:** Introduction to Machine Learning
**Word Count:** 1342
**Tags:** machine learning, AI, data science, beginners, technology

**Meta Description:** A beginner-friendly introduction to machine learning concepts and applications...

---

[Full article content with proper markdown formatting]
```

### 2. Metadata JSON (`_metadata.json`)

```json
{
  "title": "Introduction to Machine Learning",
  "topic": "Introduction to Machine Learning",
  "word_count": 1342,
  "tags": ["machine learning", "AI", "data science", "beginners", "technology"],
  "meta_description": "A beginner-friendly introduction...",
  "images": [
    {
      "url": "https://images.unsplash.com/...",
      "description": "AI and machine learning visualization",
      "author": "Photographer Name",
      "author_url": "https://unsplash.com/@photographer"
    }
  ],
  "sources_count": 5
}
```

## Common Use Cases

### 1. Blog Post Generation

```bash
python main.py create "10 Benefits of Remote Work" \
  --style professional \
  --audience "business professionals"
```

### 2. Technical Tutorial

```bash
python main.py create "Getting Started with Docker" \
  --style technical \
  --audience "software developers"
```

### 3. Educational Content

```bash
python main.py create "Understanding Climate Change" \
  --style accessible \
  --audience "high school students"
```

### 4. Business Article

```bash
python main.py create "Digital Marketing Trends 2024" \
  --style professional \
  --audience "marketing executives"
```

## Using the Python API

For more control, use the Python API directly:

```python
from src.orchestrator import ContentCreationOrchestrator
from src.utils import Config, setup_logger

# Setup logging
logger = setup_logger(level="INFO")

# Load and validate configuration
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

# Check status
if results["status"] == "completed":
    print("✓ Article created successfully!")
    article = results["article"]
    print(f"Title: {article['title']}")
    print(f"Words: {article['word_count']}")
    print(f"Tags: {', '.join(article['tags'])}")
else:
    print(f"✗ Failed: {results.get('error', 'Unknown error')}")
```

## Next Steps

Now that you're set up, explore these resources:

1. **[Usage Guide](Usage-Guide.md)** - Learn all the command options, features, and see real-world examples
2. **[Architecture](Architecture.md)** - Understand how the system works
3. **[API Reference](API-Reference.md)** - Dive into the Python API
4. **[FAQ](FAQ.md)** - Find answers to common questions

## Troubleshooting Quick Fixes

### "OPENAI_API_KEY is required but not set"
**Solution**: Add your API key to the `.env` file

### "No module named 'langchain'"
**Solution**: Run `pip install -r requirements.txt`

### Rate limiting errors
**Solution**: Wait a few minutes or use `gpt-3.5-turbo` model

### Slow execution
**Solution**: Normal! Content creation takes 2-5 minutes

For more issues, see the [Troubleshooting Guide](Troubleshooting.md).

## Getting Help

- 📖 Read the [FAQ](FAQ.md)
- 🐛 [Report an issue](https://github.com/eggressive/agentic-writer/issues)
- 💬 [Start a discussion](https://github.com/eggressive/agentic-writer/discussions)
- 📧 Contact the maintainers

## What's Next?

- ⭐ Star the repository on [GitHub](https://github.com/eggressive/agentic-writer)
- 🔔 Watch for updates and new features
- 🤝 Contribute improvements (see [Contributing Guide](Contributing.md))
- 📢 Share your experience and feedback

---

**Ready to dive deeper?** Continue to the [Usage Guide](Usage-Guide.md) for comprehensive documentation.
