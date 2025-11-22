# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
