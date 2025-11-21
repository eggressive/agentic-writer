# Agentic-Writer Wiki

This directory contains the complete documentation for the Agentic-Writer project. These markdown files are designed to be used with GitHub Wiki or as standalone documentation.

## Wiki Structure

### Core Pages

1. **[Home.md](Home.md)** - Wiki homepage with overview and quick links
2. **[Getting-Started.md](Getting-Started.md)** - Quick start guide for new users
3. **[Installation.md](Installation.md)** - Detailed installation instructions for all platforms

### Usage Documentation

1. **[Usage-Guide.md](Usage-Guide.md)** - Comprehensive usage guide with examples
2. **[API-Reference.md](API-Reference.md)** - Complete Python API documentation

### Technical Documentation

1. **[Architecture.md](Architecture.md)** - System architecture and design
2. **[Roadmap.md](Roadmap.md)** - Project roadmap and future plans

### Support Documentation

1. **[FAQ.md](FAQ.md)** - Frequently asked questions
2. **[Troubleshooting.md](Troubleshooting.md)** - Common issues and solutions
3. **[Contributing.md](Contributing.md)** - How to contribute to the project

## Using This Wiki

### For GitHub Wiki

To populate the GitHub Wiki with these pages:

**Important:** The wiki repository doesn't exist until you create the first page via the web interface.

1. **Initialize the wiki:**
   - Go to <https://github.com/eggressive/agentic-writer/wiki>
   - Click "Create the first page"
   - Create a page titled "Home" with content from `wiki/Home.md`
   - This creates the wiki repository

2. **Clone the wiki repository** (now it exists):

   ```bash
   git clone https://github.com/eggressive/agentic-writer.wiki.git
   ```

3. **Copy all markdown files:**

   ```bash
   cp wiki/*.md agentic-writer.wiki/
   cd agentic-writer.wiki
   git add .
   git commit -m "Add comprehensive wiki documentation"
   git push
   ```

**Alternative:** Use the web interface to create all pages manually. See [WIKI-SETUP.md](../WIKI-SETUP.md) for detailed instructions.

### As Standalone Documentation

These files can also be read directly from the repository or locally:

```bash
# View in terminal
cat wiki/Home.md

# Or use a markdown viewer
# macOS:
open -a "Typora" wiki/Home.md
# Linux:
xdg-open wiki/Home.md
# Windows:
start wiki/Home.md
```

### Building a Documentation Site

These markdown files can be used with documentation generators:

#### Using MkDocs

```bash
pip install mkdocs mkdocs-material

# Create mkdocs.yml
cat > mkdocs.yml << EOF
site_name: Agentic-Writer Documentation
theme:
  name: material
nav:
  - Home: wiki/Home.md
  - Getting Started: wiki/Getting-Started.md
  - Installation: wiki/Installation.md
  - Usage Guide: wiki/Usage-Guide.md
  - Architecture: wiki/Architecture.md
  - API Reference: wiki/API-Reference.md
  - Contributing: wiki/Contributing.md
  - Roadmap: wiki/Roadmap.md
  - FAQ: wiki/FAQ.md
  - Troubleshooting: wiki/Troubleshooting.md
EOF

# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

#### Using Docsify

```bash
# Install docsify-cli
npm i docsify-cli -g

# Initialize
docsify init ./docs

# Copy wiki files
cp wiki/*.md docs/

# Serve
docsify serve docs
```

## Page Organization

### Navigation Flow

```text
Home
 ├─→ Getting Started (Quick 5-min setup)
 │    └─→ Installation (Detailed setup)
 │         └─→ Usage Guide (How to use)
 │              ├─→ API Reference (Python API)
 │              └─→ Examples
 │
 ├─→ Architecture (How it works)
 │    └─→ Technical deep dive
 │
 ├─→ Support
 │    ├─→ FAQ (Common questions)
 │    └─→ Troubleshooting (Problem solving)
 │
 └─→ Community
      ├─→ Contributing (How to help)
      └─→ Roadmap (Future plans)
```

### Reading Paths

**For New Users**:

1. Home
2. Getting Started
3. Installation
4. Usage Guide
5. FAQ

**For Developers**:

1. Home
2. Architecture
3. API Reference
4. Contributing

**For Troubleshooting**:

1. Troubleshooting
2. FAQ
3. GitHub Issues

## Maintaining the Wiki

### Updating Documentation

When updating the wiki:

1. **Edit markdown files** in this directory
2. **Test links** - ensure all internal links work
3. **Update README.md** if structure changes
4. **Sync to GitHub Wiki** if applicable
5. **Announce changes** in release notes

### Link Format

Internal links should use relative paths:

```markdown
See the [Installation Guide](Installation.md) for details.
Check our [Roadmap](Roadmap.md) for future plans.
```

External links use full URLs:

```markdown
Report issues on [GitHub](https://github.com/eggressive/agentic-writer/issues).
```

### Adding New Pages

To add a new wiki page:

1. **Create markdown file** in this directory
2. **Follow naming convention**: `Page-Name.md` (Title Case with hyphens)
3. **Add to Home.md** in Quick Links section
4. **Update this README.md** with page description
5. **Cross-link** from related pages

### Style Guide

**Headings**:

- Use `#` for page title (only one per page)
- Use `##` for major sections
- Use `###` for subsections
- Use `####` rarely, for deep nesting

**Code Blocks**:

```python
# Use language identifiers
def example():
    pass
```

```bash
# For shell commands
python main.py create "topic"
```

**Lists**:

- Use `-` for unordered lists
- Use `1.` for ordered lists
- Indent with 2 spaces for nested lists

**Links**:

- Use descriptive text: `[Installation Guide](Installation.md)`
- Not: `[click here](Installation.md)`

**Emphasis**:

- **Bold** for important terms: `**important**`
- *Italic* for emphasis: `*emphasis*`
- `Code` for technical terms: `` `code` ``

## Page Summaries

### Home.md

Welcome page with project overview, quick links, features, architecture diagram, and current status.

### Getting-Started.md

5-minute quick start guide covering installation, configuration, and creating your first article.

### Installation.md

Comprehensive installation guide for all platforms (Linux, macOS, Windows) with troubleshooting.

### Usage-Guide.md

Complete usage documentation covering CLI, Python API, configuration, and best practices.

### API-Reference.md

Full Python API documentation with classes, methods, parameters, return types, and examples.

### Architecture.md

System architecture overview including components, data flow, design patterns, and technical details.

### Roadmap.md

Project roadmap with current version, planned features, release schedule, and community requests.

### FAQ.md

Frequently asked questions covering general topics, installation, usage, troubleshooting, and licensing.

### Troubleshooting.md

Common issues and solutions organized by category with step-by-step fixes.

### Contributing.md

Comprehensive guide for contributors covering setup, workflow, code standards, and PR process.

## Statistics

- **Total Pages**: 10
- **Total Words**: ~50,000+
- **Code Examples**: 100+
- **Internal Links**: 50+
- **Topics Covered**: Installation, Usage, API, Architecture, Support, Contributing

## Quick Search

Looking for something specific?

- **Installation issues** → [Installation.md](Installation.md), [Troubleshooting.md](Troubleshooting.md)
- **Usage examples** → [Usage-Guide.md](Usage-Guide.md), [Getting-Started.md](Getting-Started.md)
- **API documentation** → [API-Reference.md](API-Reference.md)
- **How it works** → [Architecture.md](Architecture.md)
- **Future plans** → [Roadmap.md](Roadmap.md)
- **Common questions** → [FAQ.md](FAQ.md)
- **Problems** → [Troubleshooting.md](Troubleshooting.md)
- **Contributing** → [Contributing.md](Contributing.md)

## Feedback

Found an issue with the documentation?

- 📝 [Edit on GitHub](https://github.com/eggressive/agentic-writer/tree/main/wiki)
- 🐛 [Report an issue](https://github.com/eggressive/agentic-writer/issues)
- 💬 [Discuss](https://github.com/eggressive/agentic-writer/discussions)

## License

This documentation is part of the Agentic-Writer project and is licensed under the MIT License.

---

**Start here**: [Home.md](Home.md) | **Get started**: [Getting-Started.md](Getting-Started.md) | **Need help?**: [FAQ.md](FAQ.md)
