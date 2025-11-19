# Architecture

Comprehensive overview of the Agentic-Writer system architecture, design patterns, and implementation details.

## Table of Contents

- [System Overview](#system-overview)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Agent Architecture](#agent-architecture)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [External Integrations](#external-integrations)
- [Error Handling](#error-handling)
- [Performance](#performance)
- [Security](#security)

## System Overview

Agentic-Writer is built on a multi-agent architecture where specialized agents work together under a central orchestrator to handle the complete content creation lifecycle.

### High-Level Architecture

```
┌────────────────────────────────────────────────────┐
│              User Interface Layer                  │
│        (CLI / Python API / Future: Web UI)         │
└────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────┐
│           ContentCreationOrchestrator              │
│         (Coordination & State Management)          │
└────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Research   │─▶│   Writer    │─▶│   Image     │
│   Agent     │  │   Agent     │  │   Agent     │
└─────────────┘  └─────────────┘  └─────────────┘
                                          │
                                          ▼
                                  ┌─────────────┐
                                  │  Publisher  │
                                  │   Agent     │
                                  └─────────────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │   Output Layer        │
                              │  (File, Medium, etc.) │
                              └───────────────────────┘
```

### Pipeline Flow

```
Input Topic
    │
    ├─▶ [Stage 1: Research] ──▶ Web Search + Analysis
    │                             │
    │                             ▼
    ├─▶ [Stage 2: Writing] ──▶ Article Generation
    │                             │
    │                             ▼
    ├─▶ [Stage 3: Images] ──▶ Image Curation
    │                             │
    │                             ▼
    └─▶ [Stage 4: Publishing] ──▶ Multi-Platform Output
```

## Core Components

### 1. ContentCreationOrchestrator

**Location**: `src/orchestrator.py`

**Responsibilities**:
- Initialize and configure all agents
- Execute 4-stage pipeline sequentially
- Manage state and data flow between agents
- Handle errors and retries
- Generate execution summaries

**Key Methods**:

```python
class ContentCreationOrchestrator:
    def __init__(self, config: Config):
        """Initialize orchestrator with configuration."""
        
    def create_content(
        self,
        topic: str,
        style: str,
        target_audience: str,
        platforms: List[str],
        output_dir: str
    ) -> Dict[str, Any]:
        """Execute full content creation pipeline."""
        
    def get_summary(self, results: Dict[str, Any]) -> str:
        """Generate human-readable summary."""
```

### 2. ResearchAgent

**Location**: `src/agents/researcher.py`

**Responsibilities**:
- Analyze topics and generate research questions
- Search the web using DuckDuckGo
- Synthesize information from multiple sources
- Handle search failures with retries

**Pipeline**:

```
Topic Input
    │
    ▼
Analyze Topic ──▶ Generate Research Questions
    │
    ▼
Web Search (DuckDuckGo)
    │
    ├─▶ Source 1
    ├─▶ Source 2
    ├─▶ Source 3
    └─▶ ... (up to max_sources)
    │
    ▼
Synthesize Findings ──▶ Research Summary
```

**Key Methods**:

```python
class ResearchAgent:
    def research(self, topic: str) -> Dict[str, Any]:
        """Conduct full research pipeline."""
        
    def analyze_topic(self, topic: str) -> str:
        """Analyze topic and generate focus areas."""
        
    def search_web(self, topic: str) -> List[Dict]:
        """Search DuckDuckGo for information."""
        
    def synthesize_research(
        self, 
        topic: str, 
        results: List[Dict]
    ) -> str:
        """Synthesize research into coherent summary."""
```

### 3. WriterAgent

**Location**: `src/agents/writer.py`

**Responsibilities**:
- Create detailed article outlines
- Generate full articles (1200-1500 words)
- Create titles and meta descriptions
- Generate relevant tags
- Support multiple writing styles

**Pipeline**:

```
Research Data + Style + Audience
    │
    ▼
Create Outline ──▶ Structure with sections
    │
    ▼
Write Article
    ├─▶ Introduction (engaging hook)
    ├─▶ Main Sections (detailed content)
    └─▶ Conclusion (summary + CTA)
    │
    ▼
Generate Metadata
    ├─▶ Title
    ├─▶ Meta Description
    └─▶ Tags (5-8)
```

**Key Methods**:

```python
class WriterAgent:
    def write_article(
        self,
        research_data: Dict[str, Any],
        style: str,
        target_audience: str
    ) -> Dict[str, Any]:
        """Generate complete article with metadata."""
        
    def create_outline(self, research: str, style: str) -> str:
        """Create detailed article outline."""
        
    def generate_title(self, content: str) -> str:
        """Generate engaging title."""
        
    def generate_meta_description(self, content: str) -> str:
        """Create SEO-friendly meta description."""
        
    def generate_tags(self, content: str) -> List[str]:
        """Generate relevant tags."""
```

### 4. ImageAgent

**Location**: `src/agents/image_handler.py`

**Responsibilities**:
- Generate contextual image search queries
- Search Unsplash for relevant images
- Select diverse, high-quality images
- Provide fallback suggestions

**Pipeline**:

```
Article Content + Title
    │
    ▼
Generate Search Queries ──▶ 3-5 specific queries
    │
    ▼
Search Unsplash (if API key available)
    │
    ├─▶ Query 1 results
    ├─▶ Query 2 results
    └─▶ Query 3 results
    │
    ▼
Select Best Images ──▶ Up to 3 diverse images
                       (different authors)
```

**Key Methods**:

```python
class ImageAgent:
    def find_images(
        self,
        article_content: str,
        article_title: str
    ) -> Dict[str, Any]:
        """Find relevant images for article."""
        
    def generate_image_queries(
        self,
        content: str,
        title: str
    ) -> List[str]:
        """Generate contextual search queries."""
        
    def search_unsplash(self, query: str) -> List[Dict]:
        """Search Unsplash API."""
        
    def select_diverse_images(
        self,
        all_images: List[Dict]
    ) -> List[Dict]:
        """Select diverse images from different authors."""
```

### 5. PublisherAgent

**Location**: `src/agents/publisher.py`

**Responsibilities**:
- Save articles as markdown files
- Export metadata as JSON
- Publish to Medium (if configured)
- Support extensible platform integration

**Pipeline**:

```
Article + Images + Metadata
    │
    ├─▶ File Platform
    │   ├─▶ Save markdown (.md)
    │   └─▶ Save metadata (.json)
    │
    └─▶ Medium Platform (if token available)
        └─▶ Publish via API
```

**Key Methods**:

```python
class PublisherAgent:
    def publish(
        self,
        article: Dict[str, Any],
        images: Dict[str, Any],
        platforms: List[str],
        output_dir: str
    ) -> Dict[str, Dict[str, Any]]:
        """Publish to specified platforms."""
        
    def publish_to_file(
        self,
        article: Dict,
        images: Dict,
        output_dir: str
    ) -> Dict:
        """Save to file system."""
        
    def publish_to_medium(
        self,
        article: Dict,
        images: Dict
    ) -> Dict:
        """Publish to Medium."""
```

## Data Flow

### Stage 1: Research Output

```json
{
  "topic": "The Future of AI",
  "analysis": "Topic analysis with focus areas...",
  "search_results": [
    {
      "title": "Source Title",
      "body": "Source content...",
      "href": "https://example.com"
    }
  ],
  "synthesis": "Comprehensive research summary...",
  "sources_count": 5
}
```

### Stage 2: Writing Output

```json
{
  "title": "The Future of AI: Opportunities and Challenges",
  "content": "# Article Title\n\n## Introduction\n...",
  "outline": "1. Introduction\n2. Current State\n...",
  "meta_description": "Explore the future of AI...",
  "tags": ["AI", "technology", "future", "innovation"],
  "word_count": 1342,
  "topic": "The Future of AI"
}
```

### Stage 3: Images Output

```json
{
  "images": [
    {
      "url": "https://images.unsplash.com/...",
      "description": "AI concept visualization",
      "author": "Photographer Name",
      "author_url": "https://unsplash.com/@photographer"
    }
  ]
}
```

### Stage 4: Publishing Output

```json
{
  "file": {
    "success": true,
    "platform": "file",
    "markdown_file": "output/the_future_of_ai.md",
    "metadata_file": "output/the_future_of_ai_metadata.json"
  },
  "medium": {
    "success": true,
    "platform": "medium",
    "url": "https://medium.com/@user/article-id"
  }
}
```

## Agent Architecture

### Base Agent Pattern

All agents follow a similar structure:

```python
class Agent:
    """Base agent pattern."""
    
    def __init__(self, llm: ChatOpenAI, **kwargs):
        """Initialize with LLM and config."""
        self.llm = llm
        self.logger = logging.getLogger(__name__)
        
    def process(self, input_data: Dict) -> Dict:
        """Main processing method."""
        try:
            result = self._perform_task(input_data)
            return {"success": True, "data": result}
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return {"success": False, "error": str(e)}
```

### LLM Integration

All agents share a single ChatOpenAI instance:

```python
llm = ChatOpenAI(
    model=config.openai_model,
    temperature=config.temperature,
    api_key=config.openai_api_key
)

# Shared across all agents
researcher = ResearchAgent(llm=llm)
writer = WriterAgent(llm=llm)
image_handler = ImageAgent(llm=llm)
```

### Prompt Structure

Agents use structured prompts with LangChain:

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}..."),
    ("human", "{task_description}\n\nInput: {input_data}")
])

chain = prompt | self.llm
result = chain.invoke({
    "role": "research assistant",
    "task_description": "Analyze this topic",
    "input_data": topic
})
```

## Technology Stack

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **langchain** | ≥0.1.0 | AI agent framework |
| **langchain-core** | ≥0.1.0 | Core utilities |
| **langchain-openai** | ≥0.0.2 | OpenAI integration |
| **openai** | ≥1.10.0 | OpenAI API client |
| **pydantic** | ≥2.0.0 | Data validation |
| **click** | ≥8.1.0 | CLI framework |
| **rich** | ≥13.0.0 | Terminal UI |
| **tenacity** | ≥8.2.0 | Retry logic |
| **duckduckgo-search** | ≥4.1.0 | Web search |

### Development Tools

- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatting
- **ruff** - Linting

## Design Patterns

### 1. Orchestrator Pattern

Central coordinator manages agent workflow:

```python
class ContentCreationOrchestrator:
    def create_content(self, ...):
        # Stage 1: Research
        research = self.researcher.research(topic)
        
        # Stage 2: Writing
        article = self.writer.write_article(research, ...)
        
        # Stage 3: Images
        images = self.image_handler.find_images(article, ...)
        
        # Stage 4: Publishing
        results = self.publisher.publish(article, images, ...)
        
        return self._aggregate_results(...)
```

### 2. Agent Pattern

Specialized agents with single responsibilities:

- **ResearchAgent** - Research only
- **WriterAgent** - Writing only
- **ImageAgent** - Images only
- **PublisherAgent** - Publishing only

### 3. Configuration Pattern

Centralized configuration with Pydantic:

```python
class Config(BaseModel):
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    # ...
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load from environment variables."""
```

### 4. Retry Pattern

Automatic retries with exponential backoff:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def search_web(self, topic: str):
    """Search with automatic retry."""
```

## External Integrations

### 1. OpenAI API

**Purpose**: LLM for all text generation

**Authentication**: API key

**Usage**:
- Topic analysis
- Content generation
- Metadata creation
- Image query generation

**Rate Limits**: Tier-based (varies by account)

### 2. DuckDuckGo Search

**Purpose**: Web research

**Authentication**: None required

**Usage**:
- Topic research
- Information gathering

**Rate Limits**: Reasonable use (no official limit)

### 3. Unsplash API

**Purpose**: Image search

**Authentication**: Access key (optional)

**Usage**:
- Image search
- High-quality photos

**Rate Limits**: 50 requests/hour (free tier)

### 4. Medium API

**Purpose**: Content publishing

**Authentication**: Access token (optional)

**Usage**:
- Article publishing
- Author posting

**Rate Limits**: Platform-specific

## Error Handling

### Retry Logic

```python
@retry(
    stop=stop_after_attempt(config.max_retries),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def api_call():
    """Automatic retry on failure."""
```

### Graceful Degradation

```python
def find_images(self, ...):
    if not self.unsplash_access_key:
        # Continue without images
        return {"images": []}
        
    try:
        return self._search_unsplash(...)
    except Exception:
        # Return empty list on failure
        return {"images": []}
```

### Error Propagation

```
Agent Error
    │
    ├─▶ Log error
    │
    ├─▶ Retry (if applicable)
    │   ├─▶ Success → Continue
    │   └─▶ Failure → Propagate
    │
    └─▶ Orchestrator catches
        └─▶ Handle gracefully or abort
```

## Performance

### Execution Time

- **Research**: 10-30 seconds
- **Writing**: 30-60 seconds
- **Images**: 5-15 seconds
- **Publishing**: <5 seconds
- **Total**: 2-5 minutes typical

### Resource Usage

- **Memory**: 100-200 MB
- **CPU**: Low (I/O bound)
- **Network**: Moderate (API calls)
- **Disk**: Minimal (output files)

### Optimization Opportunities

1. **Parallel Execution** - Run independent agents concurrently
2. **Caching** - Cache research results
3. **Batch API Calls** - Reduce API overhead
4. **Faster Models** - Use gpt-3.5-turbo for speed

## Security

### API Key Management

- ✅ Environment variables (.env)
- ✅ Never committed to version control
- ✅ Validated before use
- ✅ Secure storage recommendations

### Input Validation

- ✅ Sanitize user inputs
- ✅ Validate file paths
- ✅ Check API responses
- ✅ Prevent injection attacks

### Output Safety

- ✅ Sanitize generated content
- ✅ Validate URLs
- ✅ Check file permissions
- ✅ Prevent directory traversal

### CodeQL Scanning

- ✅ Automated security scans
- ✅ No known vulnerabilities
- ✅ Regular updates

## Extensibility

### Adding New Agents

1. Create agent class in `src/agents/`
2. Implement required interface
3. Register in `__init__.py`
4. Integrate into orchestrator
5. Add tests
6. Update documentation

### Adding Publishing Platforms

1. Add method to `PublisherAgent`
2. Handle authentication
3. Implement publishing logic
4. Update configuration
5. Add tests

### Supporting More LLMs

1. Create provider wrapper
2. Implement common interface
3. Update configuration
4. Test with all agents

## Future Architecture Improvements

See [Roadmap](Roadmap.md) for details:

- [ ] Async/await for parallel execution
- [ ] Caching layer for research
- [ ] Web UI dashboard
- [ ] API endpoint wrapper
- [ ] Queue-based processing
- [ ] Database integration
- [ ] Microservices architecture

---

**Want to contribute?** See the [Contributing Guide](Contributing.md).

**Have questions?** Check the [FAQ](FAQ.md) or [open an issue](https://github.com/eggressive/agentic-writer/issues).
