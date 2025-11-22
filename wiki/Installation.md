# Installation Guide

Detailed installation instructions for Agentic-Writer across different platforms and environments.

## Table of Contents

- [System Requirements](#system-requirements)
- [Python Installation](#python-installation)
- [Quick Installation](#quick-installation)
- [Development Installation](#development-installation)
- [Docker Installation](#docker-installation-future)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Configuration](#configuration)
- [Verification](#verification)
- [Platform-Specific Instructions](#platform-specific-instructions)

## System Requirements

### Minimum Requirements

- **Operating System**: Linux, macOS, or Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: 512 MB (1 GB recommended)
- **Disk Space**: 200 MB for installation
- **Internet**: Required for API calls

### Recommended Requirements

- **Python**: 3.10 or higher
- **RAM**: 2 GB
- **Disk Space**: 500 MB
- **Network**: Stable broadband connection

## Python Installation

### Check Python Version

```bash
python --version
# or
python3 --version
```

You should see: `Python 3.8.x` or higher

### Installing Python

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### macOS

Using Homebrew:

```bash
brew install python@3.11
```

Or download from [python.org](https://www.python.org/downloads/macos/)

#### Windows

1. Download installer from [python.org](https://www.python.org/downloads/windows/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

Verify installation:

```cmd
python --version
pip --version
```

## Quick Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
OPENAI_API_KEY=sk-your-key-here
```

### Step 4: Verify Installation

```bash
python verify_installation.py
```

✅ You're ready to go!

## Development Installation

For contributors and developers who want to modify the code:

### 1. Fork and Clone

```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/agentic-writer.git
cd agentic-writer
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on Linux/macOS:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### 3. Install in Editable Mode

```bash
pip install -e .
```

This installs the package in development mode, so changes to the code are immediately reflected.

### 4. Install Development Dependencies

```bash
pip install pytest pytest-cov black ruff
```

### 5. Setup Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

### 6. Run Tests

```bash
pytest tests/ -v --cov=src
```

## Docker Installation (Future)

Docker support is planned for future releases. Check the [Roadmap](Roadmap.md) for updates.

### Proposed Docker Setup

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

## Virtual Environment Setup

### Why Use Virtual Environments?

Virtual environments isolate your project dependencies from system-wide Python packages, preventing conflicts.

### Using venv (Recommended)

#### Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Virtual Environment

**Linux/macOS:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Deactivate

```bash
deactivate
```

### Using virtualenv

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Using conda

```bash
conda create -n agentic-writer python=3.11
conda activate agentic-writer
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional - for enhanced features
MEDIUM_ACCESS_TOKEN=your-medium-token
UNSPLASH_ACCESS_KEY=your-unsplash-key

# Model Configuration
OPENAI_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7

# System Settings
LOG_LEVEL=INFO
MAX_RESEARCH_SOURCES=5
MAX_RETRIES=3
```

### Getting API Keys

#### OpenAI API Key (Required)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (you won't see it again!)
6. Add to `.env`: `OPENAI_API_KEY=sk-...`

#### Unsplash API Key (Optional)

1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Register as a developer
3. Create a new application
4. Copy the "Access Key"
5. Add to `.env`: `UNSPLASH_ACCESS_KEY=...`

#### Medium Access Token (Optional)

1. Log in to [Medium](https://medium.com/)
2. Go to [Settings](https://medium.com/me/settings)
3. Navigate to "Integration tokens"
4. Create a new token
5. Add to `.env`: `MEDIUM_ACCESS_TOKEN=...`

## Verification

### Verify Installation Script

```bash
python verify_installation.py
```

Expected output:

```text
✓ Python version: 3.11.x
✓ All required packages installed
✓ Configuration loaded successfully
✓ OpenAI API key found
✓ All checks passed!
```

### Manual Verification

#### Check Python Version

```bash
python --version
```

#### Check Installed Packages

```bash
pip list | grep -E "langchain|openai|click|rich"
```

#### Test Import

```bash
python -c "from src.orchestrator import ContentCreationOrchestrator; print('✓ Import successful')"
```

#### Verify Configuration

```bash
python main.py config
```

#### Run Tests

```bash
pytest tests/ -v
```

## Platform-Specific Instructions

### Linux

#### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# Clone and setup
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Fedora/RHEL

```bash
# Install system dependencies
sudo dnf install python3 python3-pip git

# Clone and setup
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Arch Linux

```bash
# Install system dependencies
sudo pacman -S python python-pip git

# Clone and setup
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS

#### Using Homebrew

```bash
# Install Python
brew install python@3.11

# Clone and setup
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Common macOS Issues

**SSL Certificate Error:**

```bash
# Run Python's certificate installation
/Applications/Python\ 3.11/Install\ Certificates.command
```

### Windows

#### Using Command Prompt

```cmd
REM Clone repository
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer

REM Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt
```

#### Using PowerShell

```powershell
# Clone repository
git clone https://github.com/eggressive/agentic-writer.git
cd agentic-writer

# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Common Windows Issues

**PowerShell Execution Policy:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Long Path Support:**
Enable in Windows 10/11 Settings → System → About → Advanced system settings

## Troubleshooting Installation

### "pip: command not found"

**Solution**: Ensure Python and pip are installed:

```bash
python -m ensurepip --upgrade
```

### "Permission denied" errors

**Solution**: Use virtual environment or install with `--user`:

```bash
pip install --user -r requirements.txt
```

### SSL/Certificate errors

**Solution**: Update certificates:

```bash
pip install --upgrade certifi
```

### Package conflicts

**Solution**: Use a fresh virtual environment:

```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "ModuleNotFoundError"

**Solution**: Reinstall dependencies:

```bash
pip install --force-reinstall -r requirements.txt
```

## Updating

### Update from Git

```bash
cd agentic-writer
git pull origin main
pip install --upgrade -r requirements.txt
```

### Update Specific Package

```bash
pip install --upgrade langchain openai
```

## Uninstallation

### Remove Virtual Environment

```bash
deactivate  # if activated
rm -rf venv
```

### Remove Project

```bash
cd ..
rm -rf agentic-writer
```

### Remove Dependencies (if installed globally)

```bash
pip uninstall -r requirements.txt -y
```

## Next Steps

After successful installation:

1. 📖 Read the [Getting Started](Getting-Started.md) guide
2. 🎯 Try the [Usage Guide](Usage-Guide.md) examples
3. 🏗️ Understand the [Architecture](Architecture.md)
4. 🤝 See how to [Contribute](Contributing.md)

## Need Help?

- 📚 Check the [FAQ](FAQ.md)
- 🔍 Review [Troubleshooting](Troubleshooting.md)
- 🐛 [Report an issue](https://github.com/eggressive/agentic-writer/issues)
- 💬 [Ask in discussions](https://github.com/eggressive/agentic-writer/discussions)

---

**Installation successful?** Continue to [Getting Started](Getting-Started.md) to create your first article!
