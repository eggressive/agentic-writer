# CI Autofix Prompt (Reference)

This is the prompt used by the `ci-autofix` remote trigger (`trig_01SfFsnvVFjnye1ymJcju1a8`).
Kept here for version control. The live copy is in the trigger configuration.

To update the trigger prompt, use `claude /schedule` or the RemoteTrigger API.

---

## Step 1: Find failed CI runs on open PRs

Check all open PRs (excluding those with `skip-autofix` label) for failed CI checks.
If none found, exit immediately.

## Step 2: Check recency and avoid rework

- Only process failures from the last 2 hours
- Skip PRs with 2+ existing `<!-- ci-autofix -->` comments (needs human review)

## Step 3: Diagnose the failure

Check out PR branch, read `gh run view --log-failed`. Categorize:
- **Formatting/lint**: Auto-fixable with `black`/`ruff --fix`
- **Test failure**: Read failing test + source, identify root cause
- **Import/coverage**: Fix imports or add targeted tests
- **Workflow YAML / credentials**: Do NOT fix, comment "needs human review"

## Step 4: Fix (up to 3 attempts)

Each attempt: apply fix, run full preflight (`black --check`, `ruff check`, `pytest --cov-fail-under=60`).
Track approaches to avoid repeating failed strategies.

## Step 5: Commit and push

Conventional commit: `fix(ci): <description>`. Never force-push.

## Step 6: Comment on PR

Leave `<!-- ci-autofix -->` marker comment with outcome.
If all 3 attempts fail, document what was tried and flag for human review.

## Rules

- One PR per run (most recent failure)
- Only modify `src/` and `tests/`
- Follow code style (Black 88 chars, ruff, type hints)
- Never touch workflows, credentials, or CI config
