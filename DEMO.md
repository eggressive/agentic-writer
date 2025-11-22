# Agentic-Writer Demo Guide

This guide demonstrates how to use the Automated Content Creation & Management Agent.

## Prerequisites

1. **Python 3.8+** installed
1. **OpenAI API Key** (required)
1. Optional: Unsplash API key for image search
1. Optional: Medium API token for publishing to Medium

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

Add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Verify Configuration

```bash
python main.py config
```

You should see:

```text
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

## Usage Examples

### Example 1: Simple Content Creation

Create a basic article on a topic:

```bash
python main.py create "The Future of Renewable Energy"
```

This will:

1. Research the topic using DuckDuckGo search
1. Analyze and synthesize the findings
1. Write a comprehensive article (1200-1500 words)
1. Generate relevant tags and metadata
1. Save the article to `output/the_future_of_renewable_energy.md`

### Example 2: Content with Custom Style

Create content for a specific audience:

```bash
python main.py create "Introduction to Machine Learning" \
  --style casual \
  --audience "beginners with no technical background"
```

### Example 3: Professional Business Article

Create professional content for business executives:

```bash
python main.py create "Digital Transformation Strategies for SMEs" \
  --style professional \
  --audience "business executives and decision makers" \
  --output-dir ./business-articles
```

### Example 4: Technical Deep Dive

Create technical content:

```bash
python main.py create "Understanding Kubernetes Architecture" \
  --style technical \
  --audience "software engineers and DevOps professionals"
```

### Example 5: Multi-Platform Publishing

Publish to multiple platforms (when API tokens are configured):

```bash
python main.py create "Best Practices for Remote Team Management" \
  --platform file \
  --platform medium \
  --style professional
```

## Using the Python API

For more control, use the Python API directly:

```python
from src.orchestrator import ContentCreationOrchestrator
from src.utils import Config, setup_logger

# Setup
logger = setup_logger(level="INFO")
config = Config.from_env()
config.validate_required()

# Initialize orchestrator
orchestrator = ContentCreationOrchestrator(config)

# Create content
results = orchestrator.create_content(
    topic="Quantum Computing: A Beginner's Guide",
    style="accessible",
    target_audience="tech enthusiasts with basic science knowledge",
    platforms=["file"],
    output_dir="./articles"
)

# Check results
if results["status"] == "completed":
    print(orchestrator.get_summary(results))
    article = results["article"]
    print(f"Title: {article['title']}")
    print(f"Words: {article['word_count']}")
    print(f"Tags: {', '.join(article['tags'])}")
```

## Understanding the Output

Each content creation produces two files:

### 1. Markdown File (`.md`)

Example: `the_future_of_renewable_energy.md`

```markdown
# The Future of Renewable Energy

**Topic:** The Future of Renewable Energy

**Word Count:** 1342

**Tags:** renewable energy, sustainability, solar power, wind energy, green technology

**Meta Description:** Explore the future of renewable energy and its impact on sustainable development...

---

[Article content here]
```

### 2. Metadata File (`_metadata.json`)

Example: `the_future_of_renewable_energy_metadata.json`

```json
{
  "title": "The Future of Renewable Energy",
  "topic": "The Future of Renewable Energy",
  "word_count": 1342,
  "tags": ["renewable energy", "sustainability", "solar power", "wind energy", "green technology"],
  "meta_description": "Explore the future of renewable energy...",
  "images": [
    {
      "url": "https://images.unsplash.com/...",
      "description": "Solar panels in a field",
      "author": "Photographer Name"
    }
  ],
  "sources_count": 5
}
```

## Workflow Stages

The agent executes a 4-stage pipeline:

### Stage 1: Research 🔍

- Searches the web using DuckDuckGo
- Gathers information from multiple sources
- Analyzes the topic
- Synthesizes findings

### Stage 2: Writing ✍️

- Creates a detailed outline
- Writes engaging introduction
- Develops main content sections
- Crafts a compelling conclusion
- Generates title and metadata

### Stage 3: Images 🖼️

- Generates relevant image queries
- Searches Unsplash (if configured)
- Curates diverse images
- Provides image suggestions

### Stage 4: Publishing 📤

- Saves markdown file
- Exports metadata JSON
- Publishes to configured platforms

## Troubleshooting

### "OPENAI_API_KEY is required but not set"

Solution: Add your OpenAI API key to `.env`:

```bash
OPENAI_API_KEY=sk-your-key-here
```

### "No module named 'langchain'"

Solution: Install dependencies:

```bash
pip install -r requirements.txt
```

### Slow execution

The content creation process typically takes 2-5 minutes depending on:

- OpenAI API response time
- Web search results
- Article length and complexity

You can adjust the model for faster (but potentially lower quality) results:

```bash
OPENAI_MODEL=gpt-3.5-turbo
```

### Rate limiting errors

If you hit OpenAI rate limits:

1. Wait a few minutes
1. Reduce `MAX_RESEARCH_SOURCES` in `.env`
1. Use a lower tier model

## Advanced Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | Model to use | `gpt-4-turbo-preview` |
| `TEMPERATURE` | Creativity (0.0-1.0) | `0.7` |
| `MAX_RESEARCH_SOURCES` | Sources to research | `5` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MEDIUM_ACCESS_TOKEN` | Medium API token | - |
| `UNSPLASH_ACCESS_KEY` | Unsplash API key | - |

### Model Selection

Choose the right model for your needs:

- **gpt-4-turbo-preview**: Best quality, slower, more expensive
- **gpt-4**: High quality, balanced
- **gpt-3.5-turbo**: Faster, cheaper, good quality

### Adjusting Temperature

- **0.0-0.3**: Focused, factual, consistent
- **0.4-0.7**: Balanced (default: 0.7)
- **0.8-1.0**: Creative, varied, less predictable

## Tips for Best Results

1. **Be Specific**: Use clear, specific topics
   - ✅ "The Impact of AI on Healthcare Diagnostics"
   - ❌ "AI stuff"

1. **Define Your Audience**: Helps tailor content
   - "software developers"
   - "business executives"
   - "general public"

1. **Choose Appropriate Style**:
   - `professional` - Formal, business-oriented
   - `casual` - Conversational, accessible
   - `technical` - Detailed, for experts
   - `accessible` - Simple, for beginners

1. **Review Before Publishing**: Always review generated content before publishing

1. **Customize Settings**: Adjust temperature and model based on your needs

## Real-World Use Cases

### Content Marketing

Generate blog posts for company websites

### Educational Content

Create learning materials and tutorials

### Research Summaries

Synthesize information on complex topics

### Documentation

Write technical documentation and guides

### Newsletter Content

Create engaging newsletter articles

### Social Media

Generate long-form content for LinkedIn or Medium

## Next Steps

1. ⭐ **Star the repository** on GitHub
2. 🐛 **Report issues** if you encounter problems
3. 💡 **Suggest features** for future enhancements
4. 🤝 **Contribute** improvements or bug fixes

## Support

For questions or issues:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the main README.md

## License

MIT License - See LICENSE file for details
