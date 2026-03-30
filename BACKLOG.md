# Backlog

Prioritized list of improvements for autonomous agents to pick up.
Check `gh issue list --label agent-ready` first — GitHub Issues take priority over this list.

Mark items as done with ~~strikethrough~~ when completed via PR.

## Priority 1 (High Impact)

1. ~~**Increase test coverage to 80%** — identify untested branches in `src/agents/` and `src/orchestrator.py`, add unit tests following existing mock patterns in `tests/conftest.py`~~
2. ~~**Add `--dry-run` CLI flag** — show what the pipeline would do without calling OpenAI or writing files; useful for validating config and arguments~~
3. ~~**Add retry logic to WriterAgent** — `ResearchAgent` uses `tenacity.retry` for web calls; `WriterAgent` has no retry on LLM failures, add the same pattern~~

## Priority 2 (Medium Impact)

1. ~~**Add input validation for CLI arguments** — validate topic length (non-empty, reasonable max), validate style values, surface clear error messages~~
1. **Add `health` CLI command** — verify API keys work (OpenAI, Unsplash, Medium) with lightweight API calls before running the full pipeline
1. ~~**Consolidate setup.py into pyproject.toml** — move package metadata, dependencies, and entry points from `setup.py` to `pyproject.toml` (PEP 621)~~

## Priority 3 (Incremental)

1. **Pin dependency versions** — replace `>=` with `~=` or exact pins in `requirements.txt` for reproducible builds
1. **Extract prompt templates** — move inline prompt strings from agents into `src/prompts/` directory for easier tuning without touching agent logic
1. **Add structured JSON logging option** — add `--log-format json` flag for machine-readable log output
1. **Add type stubs / py.typed marker** — enable downstream type checking for anyone importing the package
