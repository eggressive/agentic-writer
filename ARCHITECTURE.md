# Agentic-Writer Architecture

This document describes the architecture and design of the Automated Content Creation & Management system.

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Content Creation Pipeline                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Orchestrator   │
                    │   (Coordinator)  │
                    └──────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐        ┌─────────┐
    │ Stage 1 │         │ Stage 2 │        │ Stage 3 │
    │Research │───────▶ │ Writing │──────▶ │ Images │
    └─────────┘         └─────────┘        └─────────┘
          │                                       │
          │                                       ▼
          │                                 ┌─────────┐
          │                                 │ Stage 4 │
          └───────────────────────────────▶│ Publish │
                                            └─────────┘
```

## Components

### 1. Orchestrator (`orchestrator.py`)

**Role**: Coordinates all agents and manages the pipeline flow

**Responsibilities**:

- Initialize and configure all agents
- Execute the 4-stage pipeline sequentially
- Handle errors and retries
- Collect and aggregate results
- Generate execution summaries

**Key Methods**:

- `create_content()`: Main pipeline execution
- `get_summary()`: Generate human-readable summary

### 2. Research Agent (`agents/researcher.py`)

**Role**: Gather and synthesize information on topics

**Capabilities**:
- Web search using DuckDuckGo
- Topic analysis and research question generation
- Multi-source information synthesis
- Automatic retry with exponential backoff

**Pipeline**:

```text
Topic Input
    │
    ▼
Analyze Topic ──▶ Generate Research Questions
    │
    ▼
Web Search ──▶ Gather Sources (up to 5)
    │
    ▼
Synthesize ──▶ Research Summary
```

**Output**:
- Topic analysis
- Search results (list)
- Research synthesis
- Source count

### 3. Writer Agent (`agents/writer.py`)

**Role**: Create well-structured articles from research

**Capabilities**:
- Outline generation
- Full article writing (1200-1500 words)
- Title generation
- Meta description creation
- Tag generation

**Pipeline**:
```
Research Data
    │
    ▼
Create Outline
    │
    ▼
Write Article ──▶ Introduction
    │           ├─▶ Main Sections
    │           └─▶ Conclusion
    ▼
Generate Metadata ──▶ Title, Tags, Description
```

**Output**:
- Article title
- Full content (markdown)
- Outline structure
- Meta description
- Tags (5-8)
- Word count

### 4. Image Agent (`agents/image_handler.py`)

**Role**: Find and curate relevant images

**Capabilities**:
- Generate contextual image queries
- Search Unsplash API
- Select diverse, high-quality images
- Provide image suggestions

**Pipeline**:
```
Article Content
    │
    ▼
Generate Queries ──▶ 3-5 specific searches
    │
    ▼
Search Unsplash ──▶ Fetch images
    │
    ▼
Select Best ──▶ Diverse, relevant images (up to 3)
```

**Output**:
- Image URLs
- Image descriptions
- Author attribution
- Download links

### 5. Publisher Agent (`agents/publisher.py`)

**Role**: Publish content to various platforms

**Capabilities**:
- Save to file system (markdown + JSON)
- Medium API integration (prepared)
- Extensible for additional platforms

**Pipeline**:
```
Article Data
    │
    ├─▶ File Platform ──▶ Save .md + _metadata.json
    │
    └─▶ Medium Platform ──▶ Publish to Medium (optional)
```

**Output**:
- File paths (for file platform)
- Publication URLs (for online platforms)
- Success/failure status

## Data Flow

### Input Data
```json
{
  "topic": "The Future of AI",
  "style": "professional",
  "target_audience": "business executives",
  "platforms": ["file", "medium"],
  "output_dir": "output"
}
```

### Stage 1: Research Output
```json
{
  "topic": "The Future of AI",
  "analysis": "Detailed topic analysis...",
  "search_results": [
    {
      "title": "Source 1",
      "body": "Content...",
      "href": "https://..."
    }
  ],
  "synthesis": "Comprehensive research summary...",
  "sources_count": 5
}
```

### Stage 2: Writing Output
```json
{
  "title": "The Future of AI: Trends and Predictions",
  "content": "# The Future of AI\n\n...",
  "outline": "1. Introduction\n2. Current State...",
  "meta_description": "Explore the future of AI...",
  "tags": ["AI", "machine learning", "technology"],
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
      "author_url": "https://unsplash.com/@..."
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

## Configuration System

### Config Object (`utils/config.py`)
```python
Config(
    openai_api_key: str,           # Required
    medium_access_token: Optional[str],
    unsplash_access_key: Optional[str],
    openai_model: str = "gpt-4-turbo-preview",
    temperature: float = 0.7,
    log_level: str = "INFO",
    max_research_sources: int = 5,
    max_retries: int = 3
)
```

### Loading Priority
1. Environment variables (.env file)
2. Default values

## CLI System

### Command Structure
```
main.py
  ├─ create <topic> [options]
  │   ├─ --style TEXT
  │   ├─ --audience TEXT
  │   ├─ --platform TEXT
  │   └─ --output-dir TEXT
  ├─ config
  └─ version
```

### CLI Implementation
- Built with **Click** for command parsing
- **Rich** for beautiful terminal output
- Progress spinners during execution
- Colored status messages

## Error Handling

### Retry Strategy
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
```

### Error Propagation
```
Agent Error
    │
    ▼
Retry (up to 3 times)
    │
    ├─▶ Success ──▶ Continue Pipeline
    │
    └─▶ Failure ──▶ Log Error ──▶ Graceful Degradation or Abort
```

### Logging Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General informational messages (default)
- **WARNING**: Warning messages (recoverable errors)
- **ERROR**: Error messages (failures)

## LLM Integration

### Model Configuration
```python
ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.7,
    api_key=config.openai_api_key
)
```

### Prompt Structure
All agents use structured prompts:
```python
ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a [role]..."),
    HumanMessage(content="[task details]...")
])
```

## External APIs

### 1. DuckDuckGo Search
- **Purpose**: Web research
- **Library**: `duckduckgo-search`
- **Rate Limits**: None specified
- **Fallback**: Graceful degradation

### 2. Unsplash API
- **Purpose**: Image search
- **Auth**: Client ID (optional)
- **Rate Limits**: 50 requests/hour (free tier)
- **Fallback**: Return empty list or suggestions

### 3. OpenAI API
- **Purpose**: LLM for all text generation
- **Auth**: API key (required)
- **Rate Limits**: Tier-based
- **Fallback**: Retry with exponential backoff

### 4. Medium API
- **Purpose**: Content publishing
- **Auth**: Access token (optional)
- **Rate Limits**: Platform-specific
- **Fallback**: File-only publishing

## Extensibility

### Adding New Agents
1. Create agent class in `src/agents/`
2. Implement required interface
3. Register in `__init__.py`
4. Integrate into orchestrator
5. Add tests

### Adding New Publishing Platforms
1. Add method to `PublisherAgent`
2. Handle authentication
3. Implement publishing logic
4. Update `publish()` method
5. Add tests

### Adding New LLM Providers
1. Create provider wrapper
2. Implement common interface
3. Update config for provider selection
4. Test with all agents

## Testing Strategy

### Unit Tests
- Configuration validation
- Logging functionality
- Publisher file operations
- Error handling

### Integration Tests
- End-to-end pipeline
- Agent interactions
- External API mocking

### Test Coverage
```
src/
├── agents/       (mocked API calls)
├── utils/        (100% coverage target)
└── orchestrator  (integration tests)
```

## Performance Considerations

### Execution Time
- Research: 10-30 seconds
- Writing: 30-60 seconds
- Images: 5-15 seconds
- Publishing: <5 seconds
- **Total**: 2-5 minutes typical

### Optimization Opportunities
1. Parallel agent execution (where possible)
2. Caching research results
3. Batch API calls
4. Use faster models for drafts

### Resource Usage
- Memory: ~100-200 MB
- CPU: Low (mostly I/O bound)
- Network: Moderate (API calls)

## Security Considerations

### API Key Management
- Never commit keys to version control
- Use environment variables
- Validate keys before use
- Support key rotation

### Input Validation
- Sanitize user inputs
- Validate file paths
- Check API responses
- Handle malicious content

### Output Safety
- Sanitize generated content
- Validate URLs
- Check file permissions
- Prevent directory traversal

## Monitoring & Observability

### Logging
```
[timestamp] - [component] - [level] - [message]
```

### Metrics
- Pipeline success rate
- Average execution time
- API call counts
- Error rates

### Debugging
- Enable DEBUG logging
- Check API responses
- Review generated prompts
- Validate configurations

## Deployment

### Standalone Script
```bash
python main.py create "topic"
```

### Package Installation
```bash
pip install -e .
content-agent create "topic"
```

### Docker (Future)
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## Future Enhancements

### Planned Features
- [ ] More LLM providers (Claude, Gemini)
- [ ] WordPress integration
- [ ] Content scheduling
- [ ] SEO optimization
- [ ] Multi-language support
- [ ] Custom image generation (DALL-E)
- [ ] Plagiarism checking
- [ ] Analytics integration

### Architecture Improvements
- [ ] Async/await for parallel execution
- [ ] Database for caching
- [ ] Web UI dashboard
- [ ] API endpoint wrapper
- [ ] Queue-based job processing

## Conclusion

The architecture is designed to be:
- **Modular**: Each agent is independent
- **Extensible**: Easy to add new features
- **Robust**: Comprehensive error handling
- **Maintainable**: Clear separation of concerns
- **Testable**: Well-structured for testing

This design supports the current requirements while allowing for future growth and adaptation.
