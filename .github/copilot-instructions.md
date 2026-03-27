# Copilot Instructions

## Quick mental model

- `main.py` only wires CLI to `src/cli.py`; every workflow spins up `ContentCreationOrchestrator` (`src/orchestrator.py`) that runs five agents sequentially (audience analysis → research → writing → images → publishing).
- Each agent sits in `src/agents/` and receives a shared `ChatOpenAI` instance plus its own knobs (research source cap, Unsplash key, Medium token) so changes stay localized.
- The orchestrator initializes three `ChatOpenAI` instances with different temperatures:
  - `llm_creative` (0.8): audience analysis, angle finding
  - `llm_analytical` (0.2): research, fact-checking
  - `llm_writer` (0.7): content generation
- Results flow through a single `results` dict; `get_summary()` formats the same schema for CLI panels and tests — preserve keys if you change stage outputs.
- Logging goes through `logging.getLogger(__name__)` inside modules and `utils.logger.setup_logger()` for the CLI/example so that Rich progress bars stay clean.

## Configuration & secrets

- `.env.example` documents every knob; `Config.from_env()` (Pydantic model in `src/utils/config.py`) is the single source of truth and `validate_required()` must run before touching OpenAI.
- Only `OPENAI_API_KEY` is mandatory; `MEDIUM_ACCESS_TOKEN` and `UNSPLASH_ACCESS_KEY` are optional but code should continue gracefully (see `PublisherAgent.publish_to_medium()` and `ImageAgent.search_unsplash()`).
- When adding config, extend the Pydantic model, expose it via CLI options if end-users must tweak it, and surface it inside `Config`-backed help text (`content config`).

## Agent patterns

- Audience (`audience_strategist.py`): generates a detailed reader persona (JSON with demographics, goals, pain_points) that downstream agents use to tailor content.
- Research (`researcher.py`): `analyze_topic()` → `search_web()` (DuckDuckGo + `tenacity.retry`) → `create_research_brief()`; respect `max_sources` and keep retries on the HTTP call path.
- Writer (`writer.py`): assumes 1.2-1.5k words, Markdown formatting, uses `tenacity.retry` on LLM calls, and splits responsibilities into outline/meta/tags helpers — reuse those helpers or extend them rather than folding logic into `write_article()`.
- Image agent (`image_handler.py`): first creates 3-5 queries via LLM, then talks to Unsplash only if a key exists, and caps selection to 3 diverse authors; without a key we fall back to textual suggestions — don't short-circuit this flow.
- Publisher (`publisher.py`): always writes both `*.md` and `*_metadata.json`, normalizes filenames, and returns per-platform result dicts; new platforms should follow the same `{success, platform, ...}` contract so orchestration summaries keep working.

## LLM usage

- All prompts use `ChatPromptTemplate.from_messages` + `llm.invoke`; keep prompts declarative strings and avoid manual JSON unless parsing is in place.
- Three `ChatOpenAI` instances with different temperatures are created by the orchestrator — agents receive the appropriate one. If you need a different model, accept it via config rather than re-instantiating inside agents.

## CI pipeline & merge policy

- All PRs are validated by `.github/workflows/ci.yml`: preflight gate (black + ruff) must pass before the test gate (pytest with 60% coverage floor).
- `.github/merge-policy.yml` defines risk tiers (low/medium/high) by file pattern and required checks per tier.
- Preflight checklist (run before every commit):
  - `black src/ tests/`
  - `ruff check src/ tests/ --fix`
  - `markdownlint-cli2 "**/*.md"`
  - `pytest --cov=src --cov-fail-under=60`

## Testing & quality

- Pytest is configured via `pytest.ini` to collect from `tests/`, enforce verbose mode, and always emit coverage.
- Tests mock `ChatOpenAI` via `unittest.mock.patch` — see `tests/conftest.py` for the shared `mock_llm` fixture. DuckDuckGo searches are also mocked. Follow this pattern for anything touching external APIs.
- Formatting/linting: `black src/ tests/` and `ruff check src/ tests/ --fix`; keep type hints (project already uses them everywhere) and prefer explicit return dicts over loosely shaped objects.
- Harness rule: every bug fix must include a regression test; every feature must include happy-path + error-case tests.

## Code style

- Follow PEP 8 baseline with Black's 88-character line limit (not 79).
- Prefer double quotes for strings (enforced by Black).
- Ruff linting: E (pycodestyle), F (Pyflakes), I (isort); E501 ignored (line length handled by Black).
- Use type hints where they add clarity for function parameters and return values.
- Write docstrings for all public functions and classes using Google-style format.
- Commits follow Conventional Commits (release-please automation).

## Extending the system

- New agents belong in `src/agents/`, exported via `src/agents/__init__.py`, registered in `ContentCreationOrchestrator.__init__`.
- When altering pipeline outputs, update `orchestrator.get_summary()`, CLI summary panels, and the metadata JSON schema simultaneously to avoid drift.
- Any feature that calls an external service must surface credentials through `Config`, document them in `.env.example`, and add at least a mocked regression test.
- File outputs live under `output/` by default; keep filenames deterministic (slugified title) so downstream automation can locate artifacts.
