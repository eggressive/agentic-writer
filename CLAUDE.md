# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agentic-writer is a Python CLI tool that uses LangChain + OpenAI to automate article creation through a 5-stage agent pipeline: audience analysis → research → writing → image curation → publishing.

## Commands

```bash
# Install
pip install -r requirements.txt

# Run
python main.py create "Topic" --style professional --audience "execs" --platform file --output-dir output/
python main.py config    # Show current configuration
python main.py version   # Show version

# Tests (pytest.ini already includes --cov=src flags)
pytest                   # Full suite with coverage
pytest tests/test_writer.py -v  # Single test file
pytest -k "test_name"    # Single test by name
pytest -m "not functional"  # Skip functional tests

# Formatting & linting
black src/ tests/
ruff check src/ tests/ --fix

# Markdown linting
markdownlint-cli2 "**/*.md"
markdownlint-cli2 --fix "**/*.md"

# Verify installation
python verify_installation.py
```

## Architecture

**Entry flow:** `main.py` → `src/cli.py` (Click + Rich) → `ContentCreationOrchestrator` (`src/orchestrator.py`) → agents run sequentially.

**Orchestrator** initializes three `ChatOpenAI` instances with different temperatures:

- `llm_creative` (0.8): audience analysis, angle finding
- `llm_analytical` (0.2): research, fact-checking
- `llm_writer` (0.7): content generation

**Five agents** in `src/agents/`, each receives the shared LLM + config:

1. `AudienceStrategist` — generates reader personas (JSON with demographics, goals, pain_points, etc.)
2. `ResearchAgent` — `analyze_topic()` → `search_web()` (DuckDuckGo + tenacity retry) → `create_research_brief()`
3. `WriterAgent` — generates 1200-1500 word Markdown articles with metadata
4. `ImageAgent` — LLM-generated queries → Unsplash search (falls back to text suggestions without API key)
5. `PublisherAgent` — writes `.md` + `_metadata.json` files; Medium publishing support

**Data flow:** A single `results` dict flows through the orchestrator. Each stage adds a nested dict with `status` and stage-specific fields. `get_summary()` formats this for CLI display — preserve dict keys if changing stage outputs.

**Config:** `Config.from_env()` in `src/utils/config.py` (Pydantic model) is the single source of truth. Only `OPENAI_API_KEY` is required; `MEDIUM_ACCESS_TOKEN` and `UNSPLASH_ACCESS_KEY` are optional with graceful degradation.

## Code Style

- Black formatting with 88-char line limit, double quotes
- Ruff linting: E (pycodestyle), F (Pyflakes), I (isort) — configured in `pyproject.toml`
- Type hints used throughout
- Google-style docstrings for public functions/classes
- All prompts use `ChatPromptTemplate.from_messages` + `llm.invoke`

## Testing Patterns

- Tests mock `ChatOpenAI` via `unittest.mock.patch` — see `tests/conftest.py` for shared `mock_llm` fixture
- DuckDuckGo searches are also mocked
- File output tests use temp directories
- Any new external service needs a mocked regression test

## Preflight Checklist

Run these before every commit. CI will reject PRs that fail any of them.

```bash
black src/ tests/                                    # fix formatting
ruff check src/ tests/ --fix                         # fix lint issues
pytest --cov=src --cov-fail-under=60                 # run tests
```

## Merge Policy

Read `.github/merge-policy.yml` for the machine-readable contract defining risk tiers and required checks per tier. CI (`.github/workflows/ci.yml`) enforces: preflight (black + ruff) must pass before tests run.

## Harness Rules

- Every bug fix PR **must** include a regression test that reproduces the bug before the fix.
- Every feature PR **must** include tests covering the happy path and at least one error case.
- If a production issue is found without test coverage, add a test before fixing the bug.

## Autonomous Agent Workflow

When working autonomously (scheduled trigger, background agent), follow this loop:

1. **Find work:** `gh issue list --label agent-ready --state open` — pick the highest-priority issue
2. **No issues?** Read `BACKLOG.md` and pick the top unclaimed item
3. **Branch:** `git checkout -b {type}/{short-description}` (e.g., `feat/add-dry-run-flag`)
4. **Understand requirements:** Read the issue/backlog item and relevant source files
5. **Implement:** Make changes, following the patterns in this file
6. **Preflight:** Run the three commands above — fix any failures before proceeding
7. **Commit:** Use conventional commits (`feat:`, `fix:`, `refactor:`, etc.)
8. **Create PR:** `gh pr create` using the PR template (`.github/pull_request_template.md`)
9. **CI feedback:** If CI fails, read the logs, fix, and push again
10. **Done:** Move to the next task

## Conventions

- New agents go in `src/agents/`, export via `__init__.py`, register in orchestrator
- External service credentials must go through `Config`, documented in `.env.example`
- Publisher outputs both `.md` and `_metadata.json` with slugified filenames
- New platforms must follow `{success, platform, ...}` return dict contract
- Pipeline changes require updating `orchestrator.get_summary()`, CLI panels, and metadata schema together
- Commits follow Conventional Commits (release-please automation)
