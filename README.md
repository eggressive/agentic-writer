# Agentic-Writer: Automated Content Creation & Management

An intelligent AI agent system that handles the entire content lifecycle, from research to publication. Built with LangChain and powered by OpenAI's GPT models.

📚 **[View Complete Wiki Documentation](https://github.com/eggressive/agentic-writer/wiki)** | 🚀 **[Quick Start](https://github.com/eggressive/agentic-writer/wiki/Getting-Started)** | 📖 **[API Reference](https://github.com/eggressive/agentic-writer/wiki/API-Reference)**

## Features

✨ **Automated Research** - Intelligently searches and gathers information from multiple sources  
✍️ **Content Generation** - Creates well-structured, engaging articles with proper formatting  
🖼️ **Image Curation** - Finds and suggests relevant images from Unsplash  
📤 **Multi-Platform Publishing** - Publishes to file, Medium, and other platforms  
🔄 **End-to-End Pipeline** - Orchestrates the entire workflow automatically  

## Architecture

The system consists of four specialized agents:

1. **ResearchAgent** - Conducts web research, analyzes topics, and synthesizes findings
1. **WriterAgent** - Creates outlines, writes articles, generates metadata and tags
1. **ImageAgent** - Searches for relevant images and curates visual content
1. **PublisherAgent** - Handles publication to various platforms

All agents are coordinated by the `ContentCreationOrchestrator` which manages the workflow state and error handling.

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. Clone the repository:

```bash
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

1. Configure environment variables:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required configuration:

- `OPENAI_API_KEY` - Your OpenAI API key (required)

Optional configuration:

- `MEDIUM_ACCESS_TOKEN` - For publishing to Medium
- `UNSPLASH_ACCESS_KEY` - For image search functionality
- `OPENAI_MODEL` - Model to use (default: gpt-4-turbo-preview)
- `TEMPERATURE` - Model temperature (default: 0.7)

## Usage

### Command Line Interface

Create content on a topic:

```bash
python main.py create "Artificial Intelligence in Healthcare"
```

With options:

```bash
python main.py create "Sustainable Energy Solutions" \
  --style professional \
  --audience "business executives" \
  --platform file \
  --output-dir ./articles
```

Check configuration:

```bash
python main.py config
```

View version:

```bash
python main.py version
```

### Python API

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
    platforms=["file", "medium"],
    output_dir="./output"
)

# Print summary
print(orchestrator.get_summary(results))
```

## Project Structure

```text
agentic-writer/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── researcher.py      # Research agent
│   │   ├── writer.py          # Writing agent
│   │   ├── image_handler.py   # Image handling agent
│   │   └── publisher.py       # Publishing agent
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging utilities
│   ├── __init__.py
│   ├── orchestrator.py        # Main orchestration logic
│   └── cli.py                 # Command-line interface
├── tests/                     # Test suite
├── output/                    # Default output directory
├── main.py                    # Entry point
├── setup.py                   # Package setup
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── .gitignore
├── LICENSE
└── README.md
```

## Output

The agent creates two files per article:

1. **Markdown file** - The complete article with metadata
1. **JSON metadata file** - Structured data including tags, images, and statistics

Example output structure:

```text
output/
├── artificial_intelligence_in_healthcare.md
├── artificial_intelligence_in_healthcare_metadata.json
└── ...
```

## Features in Detail

### Research Agent

- Performs web searches using DuckDuckGo
- Analyzes topics and generates research questions
- Synthesizes findings from multiple sources
- Provides structured research data for writing

### Writer Agent

- Creates detailed article outlines
- Generates well-structured content (1200-1500 words)
- Produces engaging titles and meta descriptions
- Generates relevant tags automatically
- Supports multiple writing styles and audiences

### Image Agent

- Generates contextual image search queries
- Searches Unsplash for high-quality images
- Selects diverse, relevant images
- Provides image suggestions when API is unavailable

### Publisher Agent

- Saves articles as markdown files
- Exports metadata as JSON
- Ready for Medium API integration
- Extensible for additional platforms

## Development

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
ruff check src/ tests/
```

## Configuration Options

| Environment Variable | Description | Default | Required |
|---------------------|-------------|---------|----------|
| OPENAI_API_KEY | OpenAI API key | - | Yes |
| MEDIUM_ACCESS_TOKEN | Medium API token | - | No |
| UNSPLASH_ACCESS_KEY | Unsplash API key | - | No |
| OPENAI_MODEL | OpenAI model to use | gpt-4-turbo-preview | No |
| TEMPERATURE | Model temperature | 0.7 | No |
| LOG_LEVEL | Logging level | INFO | No |
| MAX_RESEARCH_SOURCES | Max sources to research | 5 | No |
| MAX_RETRIES | Max retry attempts | 3 | No |

## Error Handling

The system includes:

- Automatic retry logic with exponential backoff
- Comprehensive error logging
- Graceful degradation (continues without optional features)
- Detailed error messages for debugging

## Limitations

- Requires OpenAI API access (paid service)
- Medium publishing requires API token
- Image search requires Unsplash API key
- Web research depends on DuckDuckGo availability
- Generated content should be reviewed before publishing

## Documentation

This project includes comprehensive documentation:

- 📚 **[Complete Wiki](https://github.com/eggressive/agentic-writer/wiki)** - Full documentation with 10+ pages
- 🚀 **[Getting Started Guide](https://github.com/eggressive/agentic-writer/wiki/Getting-Started)** - 5-minute quick start
- 📦 **[Installation Guide](https://github.com/eggressive/agentic-writer/wiki/Installation)** - Detailed setup instructions
- 📖 **[Usage Guide](https://github.com/eggressive/agentic-writer/wiki/Usage-Guide)** - Complete usage documentation
- 🔧 **[API Reference](https://github.com/eggressive/agentic-writer/wiki/API-Reference)** - Python API documentation
- 🏗️ **[Architecture](https://github.com/eggressive/agentic-writer/wiki/Architecture)** - System design and components
- 🗺️ **[Roadmap](https://github.com/eggressive/agentic-writer/wiki/Roadmap)** - Future plans and features
- ❓ **[FAQ](https://github.com/eggressive/agentic-writer/wiki/FAQ)** - Frequently asked questions
- 🔍 **[Troubleshooting](https://github.com/eggressive/agentic-writer/wiki/Troubleshooting)** - Common issues and solutions
- 🤝 **[Contributing Guide](https://github.com/eggressive/agentic-writer/wiki/Contributing)** - How to contribute

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

We use [Conventional Commits](https://www.conventionalcommits.org/) and automated releases via [release-please](https://github.com/googleapis/release-please). This means:

- Use conventional commit format (e.g., `feat:`, `fix:`, `docs:`)
- Releases are automated based on your commits
- Version bumping and changelog generation happen automatically

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- Images from [Unsplash](https://unsplash.com/)
- Search via [DuckDuckGo](https://duckduckgo.com/)

## Future Enhancements

- [ ] Support for more LLM providers (Anthropic Claude, Google Gemini)
- [ ] WordPress integration
- [ ] Custom image generation with DALL-E
- [ ] Multi-language support
- [ ] SEO optimization suggestions
- [ ] Plagiarism checking
- [ ] Content scheduling
- [ ] Analytics integration
