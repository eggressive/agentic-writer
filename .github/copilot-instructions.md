# Copilot Instructions

## Quick mental model
- `main.py` only wires CLI to `src/cli.py`; every workflow spins up `ContentCreationOrchestrator` (`src/orchestrator.py`) that runs the four agents sequentially (research → writing → images → publishing).
- Each agent sits in `src/agents/` and receives the shared `ChatOpenAI` instance plus its own knobs (research source cap, Unsplash key, Medium token) so changes stay localized.
- Results flow through a single `results` dict; `get_summary()` formats the same schema for CLI panels and tests—preserve keys if you change stage outputs.
- Logging goes through `logging.getLogger(__name__)` inside modules and `utils.logger.setup_logger()` for the CLI/example so that Rich progress bars stay clean.

## Configuration & secrets
- `.env.example` documents every knob; `Config.from_env()` (Pydantic model in `src/utils/config.py`) is the single source of truth and `validate_required()` must run before touching OpenAI.
- Only `OPENAI_API_KEY` is mandatory; `MEDIUM_ACCESS_TOKEN` and `UNSPLASH_ACCESS_KEY` are optional but code should continue gracefully (see `PublisherAgent.publish_to_medium()` and `ImageAgent.search_unsplash()`).
- When adding config, extend the Pydantic model, expose it via CLI options if end-users must tweak it, and surface it inside `Config`-backed help text (`content config`).

## Agent patterns
- Research (`researcher.py`) always: `analyze_topic()` → `search_web()` (DuckDuckGo + `tenacity.retry`) → `synthesize_research()`; respect `max_sources` and keep retries on the HTTP call path.
- Writer (`writer.py`) assumes 1.2–1.5k words, Markdown formatting, and splits responsibilities into outline/meta/tags helpers—reuse those helpers or extend them rather than folding logic into `write_article()`.
- Image agent (`image_handler.py`) first creates 3–5 queries via LLM, then talks to Unsplash only if a key exists, and caps selection to 3 diverse authors; without a key we fall back to textual suggestions—don’t short-circuit this flow.
- Publisher (`publisher.py`) always writes both `*.md` and `*_metadata.json`, normalizes filenames, and returns per-platform result dicts; new platforms should follow the same `{success, platform, ...}` contract so orchestration summaries keep working.

## LLM usage
- All prompts use `ChatPromptTemplate.from_messages` + `llm.invoke`; keep prompts declarative strings and avoid manual JSON unless parsing is in place.
- A single `ChatOpenAI` instance (temperature + model from config) is reused across agents—if you need a different model, accept it via config rather than re-instantiating inside agents.

## Developer workflows
- Install deps: `pip install -r requirements.txt`; sanity-check env + imports + smoke tests via `python verify_installation.py` (runs pytest without coverage).
- Primary run path: `python main.py create "Topic" --style professional --audience "execs" --platform file --platform medium --output-dir output/whitepapers`.
- CLI uses Click + Rich progress bars; whenever you add stages emit lightweight status strings so panels stay readable.
- Logging levels are user-set via `--log-level` or `LOG_LEVEL`; only INFO and above should hit stdout during normal runs.

## Testing & quality
- Pytest is configured via `pytest.ini` to collect from `tests/`, enforce verbose mode, and always emit coverage (`pytest` or `python -m pytest` already includes `--cov=src --cov-report=term-missing --cov-report=html`).
- Unit tests cover utils + publisher; integration tests (`tests/test_integration.py`) rely on `unittest.mock.patch` to fake `ChatOpenAI` and DuckDuckGo—follow that pattern for anything touching external APIs.
- Formatting/linting: `black src tests` and `ruff check src tests --fix`; keep type hints (project already uses them everywhere) and prefer explicit return dicts over loosely shaped objects.

## Extending the system
- New agents belong in `src/agents/`, exported via `src/agents/__init__.py`, registered in `ContentCreationOrchestrator.__init__`, and reflected in `ARCHITECTURE.md`.
- When altering pipeline outputs, update `orchestrator.get_summary()`, CLI summary panels, and the metadata JSON schema simultaneously to avoid drift.
- Any feature that calls an external service must surface credentials through `Config`, document them in `.env.example`, and add at least a mocked regression test.
- File outputs live under `output/` by default; keep filenames deterministic (slugified title) so downstream automation can locate artifacts.
