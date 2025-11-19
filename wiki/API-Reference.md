# API Reference

Complete Python API documentation for Agentic-Writer.

## Table of Contents

- [Core Classes](#core-classes)
- [Configuration](#configuration)
- [Agents](#agents)
- [Utilities](#utilities)
- [CLI](#cli)
- [Types and Schemas](#types-and-schemas)
- [Examples](#examples)

## Core Classes

### ContentCreationOrchestrator

**Location**: `src/orchestrator.py`

Main orchestrator class that coordinates all agents.

#### Constructor

```python
ContentCreationOrchestrator(config: Config)
```

**Parameters**:
- `config` (Config): Configuration object with API keys and settings

**Example**:
```python
from src.orchestrator import ContentCreationOrchestrator
from src.utils import Config

config = Config.from_env()
orchestrator = ContentCreationOrchestrator(config)
```

#### Methods

##### create_content()

```python
create_content(
    topic: str,
    style: str = "professional",
    target_audience: str = "general audience",
    platforms: List[str] = ["file"],
    output_dir: str = "output"
) -> Dict[str, Any]
```

Execute the complete content creation pipeline.

**Parameters**:
- `topic` (str): The topic to write about
- `style` (str): Writing style - "professional", "casual", "technical", or "accessible"
- `target_audience` (str): Description of target audience
- `platforms` (List[str]): Publishing platforms - ["file"], ["medium"], or both
- `output_dir` (str): Directory to save output files

**Returns**:
```python
{
    "status": "completed" | "failed",
    "research": Dict[str, Any],
    "article": Dict[str, Any],
    "images": Dict[str, Any],
    "publication": Dict[str, Dict[str, Any]],
    "error": Optional[str]
}
```

**Example**:
```python
results = orchestrator.create_content(
    topic="Machine Learning Basics",
    style="accessible",
    target_audience="beginners",
    platforms=["file"],
    output_dir="./articles"
)

if results["status"] == "completed":
    print(f"Title: {results['article']['title']}")
```

##### get_summary()

```python
get_summary(results: Dict[str, Any]) -> str
```

Generate human-readable summary of results.

**Parameters**:
- `results` (Dict): Results from `create_content()`

**Returns**:
- `str`: Formatted summary string

**Example**:
```python
summary = orchestrator.get_summary(results)
print(summary)
```

## Configuration

### Config

**Location**: `src/utils/config.py`

Configuration management using Pydantic.

#### Class Definition

```python
class Config(BaseModel):
    openai_api_key: str
    medium_access_token: Optional[str] = None
    unsplash_access_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    log_level: str = "INFO"
    max_research_sources: int = 5
    max_retries: int = 3
```

#### Class Methods

##### from_env()

```python
@classmethod
def from_env(cls) -> "Config"
```

Load configuration from environment variables.

**Returns**:
- `Config`: Configuration object

**Example**:
```python
from src.utils import Config

config = Config.from_env()
print(f"Model: {config.openai_model}")
```

##### validate_required()

```python
def validate_required(self) -> None
```

Validate that required configuration is present.

**Raises**:
- `ValueError`: If required configuration is missing

**Example**:
```python
try:
    config.validate_required()
    print("Configuration valid!")
except ValueError as e:
    print(f"Error: {e}")
```

## Agents

### ResearchAgent

**Location**: `src/agents/researcher.py`

Conducts web research and synthesizes information.

#### Constructor

```python
ResearchAgent(llm: ChatOpenAI, max_sources: int = 5)
```

**Parameters**:
- `llm` (ChatOpenAI): Language model instance
- `max_sources` (int): Maximum number of sources to research

#### Methods

##### research()

```python
research(topic: str) -> Dict[str, Any]
```

Conduct full research pipeline.

**Parameters**:
- `topic` (str): Topic to research

**Returns**:
```python
{
    "topic": str,
    "analysis": str,
    "search_results": List[Dict[str, str]],
    "synthesis": str,
    "sources_count": int
}
```

**Example**:
```python
from src.agents import ResearchAgent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.7)
researcher = ResearchAgent(llm=llm, max_sources=5)

results = researcher.research("Artificial Intelligence")
print(results["synthesis"])
```

##### analyze_topic()

```python
analyze_topic(topic: str) -> str
```

Analyze topic and identify key areas.

**Parameters**:
- `topic` (str): Topic to analyze

**Returns**:
- `str`: Topic analysis

##### search_web()

```python
search_web(topic: str) -> List[Dict[str, str]]
```

Search the web using DuckDuckGo.

**Parameters**:
- `topic` (str): Search query

**Returns**:
```python
[
    {
        "title": str,
        "body": str,
        "href": str
    }
]
```

##### synthesize_research()

```python
synthesize_research(topic: str, results: List[Dict]) -> str
```

Synthesize research findings.

**Parameters**:
- `topic` (str): Original topic
- `results` (List[Dict]): Search results

**Returns**:
- `str`: Research synthesis

### WriterAgent

**Location**: `src/agents/writer.py`

Generates articles and metadata.

#### Constructor

```python
WriterAgent(llm: ChatOpenAI)
```

**Parameters**:
- `llm` (ChatOpenAI): Language model instance

#### Methods

##### write_article()

```python
write_article(
    research_data: Dict[str, Any],
    style: str = "professional",
    target_audience: str = "general audience"
) -> Dict[str, Any]
```

Generate complete article with metadata.

**Parameters**:
- `research_data` (Dict): Results from ResearchAgent
- `style` (str): Writing style
- `target_audience` (str): Target audience description

**Returns**:
```python
{
    "title": str,
    "content": str,
    "outline": str,
    "meta_description": str,
    "tags": List[str],
    "word_count": int,
    "topic": str
}
```

**Example**:
```python
from src.agents import WriterAgent

writer = WriterAgent(llm=llm)
article = writer.write_article(
    research_data=research_results,
    style="casual",
    target_audience="beginners"
)

print(f"Title: {article['title']}")
print(f"Words: {article['word_count']}")
```

##### create_outline()

```python
create_outline(research: str, style: str) -> str
```

Create article outline.

##### generate_title()

```python
generate_title(content: str) -> str
```

Generate engaging title.

##### generate_meta_description()

```python
generate_meta_description(content: str) -> str
```

Create meta description.

##### generate_tags()

```python
generate_tags(content: str) -> List[str]
```

Generate relevant tags.

### ImageAgent

**Location**: `src/agents/image_handler.py`

Finds and curates relevant images.

#### Constructor

```python
ImageAgent(llm: ChatOpenAI, unsplash_access_key: Optional[str] = None)
```

**Parameters**:
- `llm` (ChatOpenAI): Language model instance
- `unsplash_access_key` (Optional[str]): Unsplash API key

#### Methods

##### find_images()

```python
find_images(article_content: str, article_title: str) -> Dict[str, Any]
```

Find relevant images for article.

**Parameters**:
- `article_content` (str): Article content
- `article_title` (str): Article title

**Returns**:
```python
{
    "images": [
        {
            "url": str,
            "description": str,
            "author": str,
            "author_url": str
        }
    ]
}
```

**Example**:
```python
from src.agents import ImageAgent

image_handler = ImageAgent(
    llm=llm,
    unsplash_access_key="your-key"
)

images = image_handler.find_images(
    article_content=article["content"],
    article_title=article["title"]
)

for img in images["images"]:
    print(f"Image: {img['url']}")
```

##### generate_image_queries()

```python
generate_image_queries(content: str, title: str) -> List[str]
```

Generate search queries for images.

##### search_unsplash()

```python
search_unsplash(query: str) -> List[Dict]
```

Search Unsplash for images.

### PublisherAgent

**Location**: `src/agents/publisher.py`

Publishes content to various platforms.

#### Constructor

```python
PublisherAgent(medium_access_token: Optional[str] = None)
```

**Parameters**:
- `medium_access_token` (Optional[str]): Medium API token

#### Methods

##### publish()

```python
publish(
    article: Dict[str, Any],
    images: Dict[str, Any],
    platforms: List[str],
    output_dir: str = "output"
) -> Dict[str, Dict[str, Any]]
```

Publish to specified platforms.

**Parameters**:
- `article` (Dict): Article data from WriterAgent
- `images` (Dict): Images from ImageAgent
- `platforms` (List[str]): Target platforms
- `output_dir` (str): Output directory

**Returns**:
```python
{
    "file": {
        "success": bool,
        "platform": str,
        "markdown_file": str,
        "metadata_file": str
    },
    "medium": {
        "success": bool,
        "platform": str,
        "url": str,
        "error": Optional[str]
    }
}
```

**Example**:
```python
from src.agents import PublisherAgent

publisher = PublisherAgent(
    medium_access_token="your-token"
)

results = publisher.publish(
    article=article,
    images=images,
    platforms=["file", "medium"],
    output_dir="./output"
)

for platform, result in results.items():
    if result["success"]:
        print(f"{platform}: ✓ Success")
```

##### publish_to_file()

```python
publish_to_file(
    article: Dict,
    images: Dict,
    output_dir: str
) -> Dict
```

Save to file system.

##### publish_to_medium()

```python
publish_to_medium(article: Dict, images: Dict) -> Dict
```

Publish to Medium.

## Utilities

### Logger

**Location**: `src/utils/logger.py`

#### setup_logger()

```python
setup_logger(
    name: str = "agentic_writer",
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger
```

Setup configured logger.

**Parameters**:
- `name` (str): Logger name
- `level` (str): Log level (DEBUG, INFO, WARNING, ERROR)
- `log_file` (Optional[str]): Path to log file

**Returns**:
- `logging.Logger`: Configured logger

**Example**:
```python
from src.utils import setup_logger

logger = setup_logger(
    name="my_app",
    level="DEBUG",
    log_file="app.log"
)

logger.info("Application started")
logger.debug("Debug information")
```

## CLI

### Main CLI

**Location**: `src/cli.py`

#### run_cli()

```python
def run_cli() -> None
```

Main CLI entry point.

**Usage**:
```bash
python main.py create "topic" [options]
python main.py config
python main.py version
```

## Types and Schemas

### Research Result Schema

```python
{
    "topic": str,
    "analysis": str,
    "search_results": [
        {
            "title": str,
            "body": str,
            "href": str
        }
    ],
    "synthesis": str,
    "sources_count": int
}
```

### Article Schema

```python
{
    "title": str,
    "content": str,  # Markdown formatted
    "outline": str,
    "meta_description": str,
    "tags": List[str],  # 5-8 tags
    "word_count": int,  # 1200-1500
    "topic": str
}
```

### Images Schema

```python
{
    "images": [
        {
            "url": str,
            "description": str,
            "author": str,
            "author_url": str
        }
    ]
}
```

### Publication Result Schema

```python
{
    "platform_name": {
        "success": bool,
        "platform": str,
        "markdown_file": Optional[str],
        "metadata_file": Optional[str],
        "url": Optional[str],
        "error": Optional[str]
    }
}
```

## Examples

### Complete Example

```python
from src.orchestrator import ContentCreationOrchestrator
from src.utils import Config, setup_logger

# Setup
logger = setup_logger(level="INFO")
config = Config.from_env()
config.validate_required()

# Create orchestrator
orchestrator = ContentCreationOrchestrator(config)

# Create content
results = orchestrator.create_content(
    topic="The Future of AI",
    style="professional",
    target_audience="business leaders",
    platforms=["file", "medium"],
    output_dir="./articles"
)

# Handle results
if results["status"] == "completed":
    print("✓ Success!")
    print(orchestrator.get_summary(results))
    
    article = results["article"]
    print(f"\nTitle: {article['title']}")
    print(f"Words: {article['word_count']}")
    print(f"Tags: {', '.join(article['tags'])}")
    
    # Access files
    pub = results["publication"]["file"]
    print(f"\nMarkdown: {pub['markdown_file']}")
    print(f"Metadata: {pub['metadata_file']}")
else:
    print(f"✗ Failed: {results.get('error')}")
```

### Using Individual Agents

```python
from src.agents import ResearchAgent, WriterAgent, ImageAgent, PublisherAgent
from src.utils import Config
from langchain_openai import ChatOpenAI

# Setup
config = Config.from_env()
llm = ChatOpenAI(
    model=config.openai_model,
    temperature=config.temperature,
    api_key=config.openai_api_key
)

# Research
researcher = ResearchAgent(llm, max_sources=5)
research = researcher.research("Machine Learning")

# Write
writer = WriterAgent(llm)
article = writer.write_article(
    research_data=research,
    style="technical",
    target_audience="developers"
)

# Images
image_handler = ImageAgent(llm, config.unsplash_access_key)
images = image_handler.find_images(
    article_content=article["content"],
    article_title=article["title"]
)

# Publish
publisher = PublisherAgent(config.medium_access_token)
results = publisher.publish(
    article=article,
    images=images,
    platforms=["file"],
    output_dir="./output"
)
```

### Custom Configuration

```python
from src.utils import Config

# Create custom config
config = Config(
    openai_api_key="sk-...",
    openai_model="gpt-3.5-turbo",
    temperature=0.5,
    max_research_sources=3,
    max_retries=5,
    log_level="DEBUG"
)

# Use config
orchestrator = ContentCreationOrchestrator(config)
```

### Batch Processing

```python
topics = [
    "AI in Healthcare",
    "Blockchain Technology",
    "Renewable Energy"
]

for topic in topics:
    print(f"Processing: {topic}")
    
    results = orchestrator.create_content(
        topic=topic,
        style="professional",
        target_audience="general audience",
        platforms=["file"],
        output_dir=f"./articles/{topic.replace(' ', '_').lower()}"
    )
    
    if results["status"] == "completed":
        print(f"✓ {topic} completed")
    else:
        print(f"✗ {topic} failed: {results.get('error')}")
```

### Error Handling

```python
try:
    results = orchestrator.create_content(
        topic="Your Topic",
        style="professional",
        target_audience="general audience"
    )
    
    if results["status"] == "completed":
        print("Success!")
    else:
        print(f"Failed: {results.get('error')}")
        
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

**More examples?** Check out the [Usage Guide](Usage-Guide.md) and [examples.py](https://github.com/eggressive/agentic-writer/blob/main/example.py).

**Need help?** See the [FAQ](FAQ.md) or [open an issue](https://github.com/eggressive/agentic-writer/issues).
