# GitHub Wiki Setup Guide

This guide explains how to populate your GitHub Wiki with the comprehensive documentation created in the `wiki/` directory.

## Quick Setup

### Method 1: GitHub Web Interface (Recommended)

This is the easiest method since the wiki repository doesn't exist until you create the first page.

1. **Enable Wiki on GitHub**
   - Go to https://github.com/eggressive/agentic-writer
   - Navigate to Settings → Features
   - Enable "Wikis" if not already enabled

2. **Create the First Page**
   - Go to https://github.com/eggressive/agentic-writer/wiki
   - Click "Create the first page"
   - For the first page, use the title "Home"
   - Copy and paste the content from `wiki/Home.md`
   - Click "Save Page"

3. **Add Remaining Pages**
   - Click "New Page" for each additional page
   - Use the following titles (without the .md extension):
     - Getting-Started
     - Installation
     - Usage-Guide
     - Architecture
     - API-Reference
     - Roadmap
     - FAQ
     - Troubleshooting
     - Contributing
   - Copy the content from the corresponding `wiki/*.md` files
   - Save each page

4. **Verify**
   - All 10 wiki pages should now be visible
   - Navigation between pages should work

### Method 2: Clone and Copy (After Wiki is Initialized)

**Note:** This method only works after you've created at least one page via the web interface (Method 1, step 2).

1. **Initialize Wiki First**
   - Follow Method 1 to create the first page (Home)
   - This creates the wiki repository

2. **Clone the Wiki Repository**
   ```bash
   git clone https://github.com/eggressive/agentic-writer.wiki.git
   ```

3. **Copy Wiki Files**
   ```bash
   # From your project directory
   cp wiki/*.md agentic-writer.wiki/
   ```

4. **Commit and Push**
   ```bash
   cd agentic-writer.wiki
   git add .
   git commit -m "Add comprehensive wiki documentation"
   git push
   ```

5. **Verify**
   - Visit https://github.com/eggressive/agentic-writer/wiki
   - You should see all 10 wiki pages

## Wiki Pages Overview

The wiki contains 10 comprehensive pages:

| Page | File | Purpose |
|------|------|---------|
| **Home** | Home.md | Welcome page with overview and quick links |
| **Getting Started** | Getting-Started.md | 5-minute quick start guide |
| **Installation** | Installation.md | Platform-specific installation instructions |
| **Usage Guide** | Usage-Guide.md | Complete usage documentation |
| **Architecture** | Architecture.md | System architecture and design |
| **API Reference** | API-Reference.md | Full Python API documentation |
| **Roadmap** | Roadmap.md | Project roadmap and future plans |
| **FAQ** | FAQ.md | Frequently asked questions |
| **Troubleshooting** | Troubleshooting.md | Common issues and solutions |
| **Contributing** | Contributing.md | Contribution guide |

## Sidebar Configuration

Create a `_Sidebar.md` file in the wiki for navigation:

```markdown
### 📚 Documentation

**Getting Started**
- [Home](Home)
- [Getting Started](Getting-Started)
- [Installation](Installation)

**Usage**
- [Usage Guide](Usage-Guide)
- [API Reference](API-Reference)

**Technical**
- [Architecture](Architecture)
- [Roadmap](Roadmap)

**Support**
- [FAQ](FAQ)
- [Troubleshooting](Troubleshooting)
- [Contributing](Contributing)

---

**Quick Links**
- [GitHub Repo](https://github.com/eggressive/agentic-writer)
- [Issues](https://github.com/eggressive/agentic-writer/issues)
- [Discussions](https://github.com/eggressive/agentic-writer/discussions)
```

## Footer Configuration

Create a `_Footer.md` file for consistent footer:

```markdown
---

**Agentic-Writer** | [GitHub](https://github.com/eggressive/agentic-writer) | [Issues](https://github.com/eggressive/agentic-writer/issues) | [License](https://github.com/eggressive/agentic-writer/blob/main/LICENSE)

© 2024 Agentic-Writer Contributors
```

## Verifying the Wiki

After setup, verify:

1. ✅ All 10 pages are visible
2. ✅ Links between pages work
3. ✅ Code blocks are formatted correctly
4. ✅ Images (if any) display properly
5. ✅ Navigation is intuitive

## Updating the Wiki

When updating documentation:

1. **Edit files** in the `wiki/` directory
2. **Test locally** using a markdown viewer
3. **Commit changes** to the main repository
4. **Sync to wiki**:
   ```bash
   cd agentic-writer.wiki
   cp ../wiki/*.md .
   git add .
   git commit -m "Update wiki documentation"
   git push
   ```

## Alternative: MkDocs Site

If you prefer a documentation site over GitHub Wiki:

### Setup MkDocs

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Create configuration
cat > mkdocs.yml << EOF
site_name: Agentic-Writer Documentation
site_url: https://eggressive.github.io/agentic-writer/
repo_url: https://github.com/eggressive/agentic-writer
repo_name: eggressive/agentic-writer

theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - search.highlight

nav:
  - Home: wiki/Home.md
  - Getting Started: wiki/Getting-Started.md
  - Installation: wiki/Installation.md
  - Usage:
      - Usage Guide: wiki/Usage-Guide.md
      - API Reference: wiki/API-Reference.md
  - Technical:
      - Architecture: wiki/Architecture.md
      - Roadmap: wiki/Roadmap.md
  - Support:
      - FAQ: wiki/FAQ.md
      - Troubleshooting: wiki/Troubleshooting.md
      - Contributing: wiki/Contributing.md

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - admonition
  - toc:
      permalink: true
EOF

# Build and serve
mkdocs serve
```

### Deploy to GitHub Pages

```bash
# Build static site
mkdocs build

# Deploy to gh-pages branch
mkdocs gh-deploy
```

Access at: https://eggressive.github.io/agentic-writer/

## Alternative: Docsify

For a lightweight documentation site:

```bash
# Install Docsify
npm i docsify-cli -g

# Initialize
docsify init ./docs

# Copy wiki files
cp wiki/*.md docs/

# Configure sidebar
cat > docs/_sidebar.md << EOF
- [Home](/)
- [Getting Started](Getting-Started)
- [Installation](Installation)
- [Usage Guide](Usage-Guide)
- [API Reference](API-Reference)
- [Architecture](Architecture)
- [Roadmap](Roadmap)
- [FAQ](FAQ)
- [Troubleshooting](Troubleshooting)
- [Contributing](Contributing)
EOF

# Serve locally
docsify serve docs

# Deploy to GitHub Pages
# Push docs/ directory to gh-pages branch
```

## Maintenance

### Regular Updates

- Update wiki when adding features
- Keep installation instructions current
- Update roadmap with progress
- Add new FAQ entries based on issues
- Keep troubleshooting guide current

### Quality Checks

- ✅ Fix broken links
- ✅ Update outdated information
- ✅ Add new examples
- ✅ Improve clarity based on feedback
- ✅ Keep consistent formatting

## Statistics

Your new wiki includes:

- **10 comprehensive pages**
- **~50,000+ words** of documentation
- **100+ code examples**
- **50+ internal cross-links**
- **Platform-specific** instructions
- **Complete API** documentation

## Support

For wiki-related questions:

- 📝 Edit suggestions via Pull Requests
- 🐛 Report issues on [GitHub Issues](https://github.com/eggressive/agentic-writer/issues)
- 💬 Discuss in [GitHub Discussions](https://github.com/eggressive/agentic-writer/discussions)

## Next Steps

1. Choose your preferred method (Wiki, MkDocs, or Docsify)
2. Follow the setup instructions above
3. Verify all pages are accessible
4. Share the documentation with your users
5. Maintain and update regularly

---

**Questions?** Open an issue or discussion on GitHub!

**Found this helpful?** Star the repository and share with others!
