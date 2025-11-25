# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.4](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.8.3...agentic-writer-v0.8.4) (2025-11-25)


### Code Refactoring

* extract _build_persona_context helper to reduce duplication in WriterAgent ([#60](https://github.com/eggressive/agentic-writer/issues/60)) ([8d10783](https://github.com/eggressive/agentic-writer/commit/8d10783ac97f4a04b3e650f78960bf90b67710f3))

## [0.8.3](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.8.2...agentic-writer-v0.8.3) (2025-11-25)


### Bug Fixes

* empty persona context instruction in create_outline prompt ([#59](https://github.com/eggressive/agentic-writer/issues/59)) ([f1e0da4](https://github.com/eggressive/agentic-writer/commit/f1e0da41861a9603d3c12ea84ca7231a10f4db15))

## [0.8.2](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.8.1...agentic-writer-v0.8.2) (2025-11-25)


### Miscellaneous

* add tests for create_outline method with persona parameter ([#58](https://github.com/eggressive/agentic-writer/issues/58)) ([9b73356](https://github.com/eggressive/agentic-writer/commit/9b7335630d94d62464fb611593a0d080be158c6b))

## [0.8.1](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.8.0...agentic-writer-v0.8.1) (2025-11-25)


### Miscellaneous

* enhance create_outline method to include reader persona context ([#57](https://github.com/eggressive/agentic-writer/issues/57)) ([7c072da](https://github.com/eggressive/agentic-writer/commit/7c072da9f5be09307a312c548bd91e308386425d))

## [0.8.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.7.1...agentic-writer-v0.8.0) (2025-11-25)


### Features

* add audience strategist agent for reader persona generation ([#55](https://github.com/eggressive/agentic-writer/issues/55)) ([e8cbeb2](https://github.com/eggressive/agentic-writer/commit/e8cbeb2e5aa0fac6c5c4c7ed118ac9d2d86122c4))

## [0.7.1](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.7.0...agentic-writer-v0.7.1) (2025-11-24)


### Bug Fixes

* improve publisher.py test coverage from 66% to 100% ([#50](https://github.com/eggressive/agentic-writer/issues/50)) ([0821459](https://github.com/eggressive/agentic-writer/commit/082145958979996e1e4ee1ccfea5ee92076f47ca))

## [0.7.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.6.2...agentic-writer-v0.7.0) (2025-11-24)


### Features

* replace synthesize_research with create_research_brief for structured JSON output ([#46](https://github.com/eggressive/agentic-writer/issues/46)) ([6f0c222](https://github.com/eggressive/agentic-writer/commit/6f0c2224179d2c70223ad87ecc4cbda08834e103))

## [0.6.2](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.6.1...agentic-writer-v0.6.2) (2025-11-24)


### Miscellaneous

* add workflow to auto-approve release-please PRs ([#44](https://github.com/eggressive/agentic-writer/issues/44)) ([436457f](https://github.com/eggressive/agentic-writer/commit/436457f2a9c9efbe03c158dc1c2323ce565e16d1))

## [0.6.1](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.6.0...agentic-writer-v0.6.1) (2025-11-24)


### Miscellaneous

* **black:** add configuration files for VSCode and Black ([#41](https://github.com/eggressive/agentic-writer/issues/41)) ([17c7fb9](https://github.com/eggressive/agentic-writer/commit/17c7fb9c3b60666bd149c0f8f09f1324ef29b78a))

## [0.6.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.5.0...agentic-writer-v0.6.0) (2025-11-23)


### Features

* add CLI tests to achieve 99% coverage for src/cli.py ([#38](https://github.com/eggressive/agentic-writer/issues/38)) ([e3f9da9](https://github.com/eggressive/agentic-writer/commit/e3f9da9e477cd9fc95de1c04c85edb364ca7796f))

## [0.5.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.4.2...agentic-writer-v0.5.0) (2025-11-23)


### Features

* add tests for edge cases in researcher, writer, orchestrator, and image handler ([#36](https://github.com/eggressive/agentic-writer/issues/36)) ([f5d2e0d](https://github.com/eggressive/agentic-writer/commit/f5d2e0d783365304ed457041bf623d93f8ace95b))

## [0.4.2](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.4.1...agentic-writer-v0.4.2) (2025-11-23)


### Miscellaneous

* enhance unsplash api integration with download tracking and advanced search parameters ([#30](https://github.com/eggressive/agentic-writer/issues/30)) ([28afa50](https://github.com/eggressive/agentic-writer/commit/28afa50d9bcae52a15e1f12fac4f1607c0d698b9))

## [0.4.1](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.4.0...agentic-writer-v0.4.1) (2025-11-23)


### Miscellaneous

* replace deprecated duckduckgo-search with ddgs package ([#27](https://github.com/eggressive/agentic-writer/issues/27)) ([10693de](https://github.com/eggressive/agentic-writer/commit/10693de59039b102ace30835e634dd4dc63a9b4d))

## [0.4.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.3.1...agentic-writer-v0.4.0) (2025-11-23)


### Features

* add acceptance tests script and functional tests for article generation ([#24](https://github.com/eggressive/agentic-writer/issues/24)) ([54f245f](https://github.com/eggressive/agentic-writer/commit/54f245f847e766e3f8ca0b6e820a5e88a9354631))

## [0.3.1](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.3.0...agentic-writer-v0.3.1) (2025-11-23)


### Bug Fixes

* remove .md extensions from wiki links in Home.md ([#21](https://github.com/eggressive/agentic-writer/issues/21)) ([4ee8d93](https://github.com/eggressive/agentic-writer/commit/4ee8d93689094445488654c73b82d86fcdee9b20))

## [0.3.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.2.0...agentic-writer-v0.3.0) (2025-11-22)


### Features

* add markdownlint GitHub Action workflow ([#17](https://github.com/eggressive/agentic-writer/issues/17)) ([420c89d](https://github.com/eggressive/agentic-writer/commit/420c89dfa2f553ce9207f9879af012a7c572af3f))


### Bug Fixes

* **markdownlint:** add CHANGELOG.md to ignores list ([#19](https://github.com/eggressive/agentic-writer/issues/19)) ([cfc8135](https://github.com/eggressive/agentic-writer/commit/cfc8135f25976ce9e4c6055242831bcc72428116))

## [0.2.0](https://github.com/eggressive/agentic-writer/compare/agentic-writer-v0.1.0...agentic-writer-v0.2.0) (2025-11-22)

### Features

* add wiki documentation ([#6](https://github.com/eggressive/agentic-writer/issues/6)) ([626f839](https://github.com/eggressive/agentic-writer/commit/626f8390c1b14a50945b3e0e6235fcc3a48db1ed))

### Bug Fixes

* **ci:** add token parameter to release-please workflow ([#15](https://github.com/eggressive/agentic-writer/issues/15)) ([fc9f053](https://github.com/eggressive/agentic-writer/commit/fc9f05304b1bee7f18c152a461b99f6d77b80f6e))
* markdown docs ([#12](https://github.com/eggressive/agentic-writer/issues/12)) ([55c4d28](https://github.com/eggressive/agentic-writer/commit/55c4d28662f53420b62530cd50002a95ecf788d0))
* **release-please:** update release-please configuration ([#13](https://github.com/eggressive/agentic-writer/issues/13)) ([dcb3274](https://github.com/eggressive/agentic-writer/commit/dcb3274b09e63acc01c5e8e364f12dd41a8e1158))

### Code Refactoring

* update Home.md for improved documentation structure and clarity ([#9](https://github.com/eggressive/agentic-writer/issues/9)) ([5b7b00c](https://github.com/eggressive/agentic-writer/commit/5b7b00c93e70479abca9aaf8bf8db1bb7ba8eecf))

## [Unreleased]

### Added

* Automated release management with release-please
* Conventional Commits guidelines in CONTRIBUTING.md
* Release process documentation

## [0.1.0] - historical baseline

### Added

* Initial release of Agentic-Writer
* ResearchAgent for automated web research and topic analysis
* WriterAgent for content generation with multiple styles and audiences
* ImageAgent for image curation from Unsplash
* PublisherAgent for multi-platform publishing (file, Medium)
* ContentCreationOrchestrator for end-to-end workflow management
* Command-line interface with Click and Rich
* Python API for programmatic access
* Configuration management with Pydantic
* Comprehensive test suite with pytest
* Documentation including README, CONTRIBUTING, and wiki
* Support for OpenAI GPT models via LangChain
* Automatic retry logic with exponential backoff
* Logging utilities with configurable levels

[Unreleased]: https://github.com/eggressive/agentic-writer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/eggressive/agentic-writer/releases/tag/v0.1.0
