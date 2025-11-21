# Troubleshooting Guide

Solutions to common issues and problems with Agentic-Writer.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Runtime Errors](#runtime-errors)
- [API Issues](#api-issues)
- [Performance Problems](#performance-problems)
- [Output Issues](#output-issues)
- [Platform-Specific Issues](#platform-specific-issues)

## Installation Issues

### "pip: command not found"

**Problem**: pip is not installed or not in PATH

**Solutions**:

```bash
# Option 1: Use python -m pip
python -m pip install -r requirements.txt

# Option 2: Install pip
# On Ubuntu/Debian:
sudo apt install python3-pip

# On macOS:
python -m ensurepip --upgrade

# On Windows:
# Download get-pip.py and run:
python get-pip.py
```

### "Permission denied" during installation

**Problem**: Insufficient permissions to install packages

**Solutions**:

```bash
# Option 1: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Option 2: Install with --user flag
pip install --user -r requirements.txt

# Option 3: Use sudo (not recommended)
sudo pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'langchain'"

**Problem**: Dependencies not installed

**Solutions**:

```bash
# Install dependencies
pip install -r requirements.txt

# If using virtual environment, ensure it's activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Force reinstall if needed
pip install --force-reinstall -r requirements.txt
```

### SSL Certificate Errors

**Problem**: SSL certificate verification fails

**Solutions**:

```bash
# Update certificates
pip install --upgrade certifi

# On macOS, run certificate installation
/Applications/Python\ 3.11/Install\ Certificates.command

# Temporary workaround (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Package Version Conflicts

**Problem**: Conflicting package versions

**Solutions**:

```bash
# Use fresh virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Update pip and setuptools
pip install --upgrade pip setuptools wheel

# Check for conflicts
pip check
```

## Configuration Issues

### "OPENAI_API_KEY is required but not set"

**Problem**: OpenAI API key not configured

**Solutions**:

1. **Create `.env` file**:

```bash
cp .env.example .env
```

1. **Add your API key**:

```bash
# Edit .env file
OPENAI_API_KEY=sk-your-actual-key-here
```

1. **Verify**:

```bash
python main.py config
```

**Common mistakes**:

- ❌ Extra spaces: `OPENAI_API_KEY = sk-...`
- ❌ Quotes: `OPENAI_API_KEY="sk-..."`
- ✅ Correct: `OPENAI_API_KEY=sk-...`

### ".env file not found"

**Problem**: `.env` file doesn't exist

**Solutions**:

```bash
# Copy from example
cp .env.example .env

# Or create manually
cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
LOG_LEVEL=INFO
EOF
```

### "Invalid API key"

**Problem**: API key is incorrect or expired

**Solutions**:

1. **Verify key format**: Should start with `sk-`
2. **Check for typos**: Copy-paste carefully
3. **Generate new key**: [OpenAI Platform](https://platform.openai.com/api-keys)
4. **Check account status**: Ensure account is active and has credits

### Environment Variables Not Loading

**Problem**: Configuration not reading from `.env`

**Solutions**:

```bash
# Ensure .env is in project root
ls -la .env

# Check file contents
cat .env

# Verify working directory
pwd

# Run from project root
cd /path/to/agentic-writer
python main.py config
```

## Runtime Errors

### "openai.error.RateLimitError"

**Problem**: Exceeded OpenAI API rate limits

**Solutions**:

1. **Wait and retry**: Rate limits reset over time
2. **Upgrade account**: Get higher limits
3. **Use slower model**: Switch to `gpt-3.5-turbo`
4. **Reduce frequency**: Space out requests

```bash
# Edit .env
OPENAI_MODEL=gpt-3.5-turbo
```

### "openai.error.AuthenticationError"

**Problem**: API authentication failed

**Solutions**:

1. **Verify API key**: Check it's correct
2. **Check account**: Ensure account is active
3. **Verify credits**: Check you have available credits
4. **Test key**:

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### "Connection timeout" or "Network error"

**Problem**: Network connectivity issues

**Solutions**:

1. **Check internet**: Ensure you're online
2. **Check firewall**: Allow outbound HTTPS
3. **Verify proxy**: Configure if behind proxy
4. **Try again**: Temporary network issues
5. **Check status**:
   - [OpenAI Status](https://status.openai.com/)
   - [DuckDuckGo Status](https://duckduckgo.com/)

### "DuckDuckGo search failed"

**Problem**: Web search not working

**Solutions**:

1. **Check internet connection**
2. **Retry**: Automatic retry should handle temporary issues
3. **Check MAX_RETRIES**: Increase if needed

```bash
# Edit .env
MAX_RETRIES=5
```

1. **Network restrictions**: Ensure DuckDuckGo isn't blocked

### "No research results found"

**Problem**: Research agent can't find information

**Solutions**:

1. **Broader topic**: Make topic less specific
2. **Check spelling**: Fix typos in topic
3. **Verify network**: Ensure web search works
4. **Try different topic**: Some topics have limited information

### Import Errors

**Problem**: Cannot import modules

**Solutions**:

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python version
python --version  # Should be 3.8+

# Verify installation
python -c "from src.orchestrator import ContentCreationOrchestrator; print('OK')"

# Check PYTHONPATH
echo $PYTHONPATH

# Run from project root
cd /path/to/agentic-writer
```

## API Issues

### OpenAI API Issues

#### "Model not found"

**Problem**: Specified model doesn't exist or isn't accessible

**Solutions**:

```bash
# Use available model
OPENAI_MODEL=gpt-4-turbo-preview
# or
OPENAI_MODEL=gpt-3.5-turbo
```

#### "Insufficient quota"

**Problem**: No credits remaining

**Solutions**:

1. Add credits to OpenAI account
2. Check billing settings
3. Wait for free tier reset (if applicable)

#### "Too many requests"

**Problem**: Rate limiting

**Solutions**:

1. Wait 60 seconds and retry
2. Reduce MAX_RESEARCH_SOURCES
3. Upgrade API tier

### Unsplash API Issues

#### "Unsplash API key invalid"

**Problem**: Invalid or missing Unsplash key

**Solutions**:

1. **Optional**: Unsplash is optional, system works without it
2. **Get key**: [Unsplash Developers](https://unsplash.com/developers)
3. **Add to .env**:

```bash
UNSPLASH_ACCESS_KEY=your-access-key
```

#### "Rate limit exceeded" (Unsplash)

**Problem**: 50 requests/hour limit reached

**Solutions**:

1. **Wait**: Limit resets hourly
2. **Continue**: System works without images
3. **Upgrade**: Apply for higher limits

### Medium API Issues

#### "Medium publishing failed"

**Problem**: Medium API error

**Solutions**:

1. **Verify token**: Check MEDIUM_ACCESS_TOKEN
2. **Token format**: Should be long alphanumeric string
3. **Token validity**: Tokens don't expire but check permissions
4. **Fallback**: Use file publishing only

## Performance Problems

### "Content creation is too slow"

**Problem**: Takes longer than 2-5 minutes

**Solutions**:

1. **Use faster model**:

```bash
OPENAI_MODEL=gpt-3.5-turbo
```

1. **Reduce research sources**:

```bash
MAX_RESEARCH_SOURCES=3
```

1. **Check internet speed**: Slow connection affects performance

2. **Skip images**: Don't configure Unsplash

3. **Check system load**: Close other applications

### "High memory usage"

**Problem**: Using too much RAM

**Solutions**:

1. **Normal usage**: 100-200 MB is normal
2. **Close other apps**: Free up memory
3. **Upgrade RAM**: If system has <2GB
4. **Check for leaks**: Restart if memory grows continuously

### "Process hangs or freezes"

**Problem**: System stops responding

**Solutions**:

1. **Wait longer**: Some operations take time
2. **Check logs**: Enable DEBUG logging

```bash
python main.py create "topic" --log-level DEBUG
```

1. **Kill and retry**: Ctrl+C to stop, try again
2. **Check API status**: Verify services are up
3. **Network issues**: Check connectivity

## Output Issues

### "No output files generated"

**Problem**: Files not created

**Solutions**:

1. **Check permissions**: Ensure write access to output directory

```bash
ls -ld output/
chmod 755 output/
```

1. **Verify path**: Check output directory exists

```bash
mkdir -p output
```

1. **Check errors**: Look for error messages in output

2. **Absolute paths**: Use full path

```bash
python main.py create "topic" --output-dir /full/path/to/output
```

### "Article is too short"

**Problem**: Generated article is shorter than expected

**Solutions**:

1. **Topic complexity**: Some topics yield shorter content
2. **Model selection**: Use GPT-4 for better quality
3. **Research depth**: Increase MAX_RESEARCH_SOURCES
4. **Wait for update**: Configurable length coming in future release

### "Poor content quality"

**Problem**: Generated content isn't good enough

**Solutions**:

1. **Use better model**:

```bash
OPENAI_MODEL=gpt-4-turbo-preview
```

1. **Adjust temperature**:

```bash
TEMPERATURE=0.7  # Balance
# or
TEMPERATURE=0.3  # More focused
```

1. **Better topic**: More specific topics = better content

2. **Define audience**: Be specific about target audience

3. **Review prompts**: Check agent prompts in source

### "Images not included"

**Problem**: No images in output

**Solutions**:

1. **Normal**: Images optional, system works without them
2. **Add Unsplash key**: Configure UNSPLASH_ACCESS_KEY
3. **Check logs**: See if there were errors
4. **Verify quota**: Check Unsplash rate limits

### "Metadata file missing"

**Problem**: Only .md file created, no .json

**Solutions**:

1. **Check for errors**: Look at log output
2. **Verify permissions**: Ensure write access
3. **Check disk space**: Ensure sufficient space
4. **Report bug**: If persistent, open issue

## Platform-Specific Issues

### Windows Issues

#### PowerShell Execution Policy

**Problem**: Cannot run activation script

**Solution**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Path issues

**Problem**: Scripts not found

**Solution**:

```cmd
# Use full path
python C:\path\to\agentic-writer\main.py create "topic"

# Or add to PATH
```

#### Unicode errors

**Problem**: Encoding issues with special characters

**Solution**:

```cmd
# Set UTF-8
chcp 65001

# Or in Python
$env:PYTHONIOENCODING="utf-8"
```

### macOS Issues

#### Certificate errors

**Problem**: SSL verification fails

**Solution**:

```bash
/Applications/Python\ 3.11/Install\ Certificates.command
```

#### Permission denied

**Problem**: Cannot execute scripts

**Solution**:

```bash
chmod +x main.py example.py verify_installation.py
```

### Linux Issues

#### Python3 vs Python

**Problem**: Wrong Python version

**Solution**:

```bash
# Use python3 explicitly
python3 -m pip install -r requirements.txt
python3 main.py create "topic"

# Or create alias
alias python=python3
```

#### Missing system packages

**Problem**: System dependencies missing

**Solution**:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

## Debugging Tips

### Enable Debug Logging

```bash
# Via CLI
python main.py create "topic" --log-level DEBUG

# Via .env
LOG_LEVEL=DEBUG
```

### Check Configuration

```bash
python main.py config
```

### Verify Installation

```bash
python verify_installation.py
```

### Test Imports

```bash
python -c "from src.orchestrator import ContentCreationOrchestrator; print('OK')"
```

### Check API Connectivity

```bash
# Test OpenAI API
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Test internet
ping google.com
```

### Review Logs

Check terminal output for error messages and stack traces.

## Getting Help

If you've tried these solutions and still have issues:

### 1. Search Existing Issues

[GitHub Issues](https://github.com/eggressive/agentic-writer/issues)

### 2. Check Documentation

- [Installation Guide](Installation.md)
- [Usage Guide](Usage-Guide.md)
- [FAQ](FAQ.md)

### 3. Report a Bug

Include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- System info (OS, Python version)
- Error messages and logs
- Configuration (redact API keys!)

### 4. Ask in Discussions

[GitHub Discussions](https://github.com/eggressive/agentic-writer/discussions)

## Common Error Messages

### "Config validation failed"

**Cause**: Missing required configuration
**Fix**: Add OPENAI_API_KEY to .env

### "Unable to create output directory"

**Cause**: Permission issues
**Fix**: Check write permissions

### "Research failed after X retries"

**Cause**: Network or API issues
**Fix**: Check internet, verify API keys, try again

### "Article generation failed"

**Cause**: OpenAI API error
**Fix**: Check API key, credits, rate limits

### "Platform 'X' not supported"

**Cause**: Invalid platform name
**Fix**: Use 'file' or 'medium'

## Prevention Tips

1. **Use virtual environments**: Avoid package conflicts
2. **Keep dependencies updated**: Regular `pip install --upgrade`
3. **Monitor API usage**: Track OpenAI spending
4. **Test configuration**: Run `verify_installation.py`
5. **Backup .env**: Keep secure copy of configuration
6. **Read error messages**: They usually indicate the problem
7. **Check logs**: Enable DEBUG when troubleshooting

---

**Still stuck?** [Open an issue](https://github.com/eggressive/agentic-writer/issues) or [ask in discussions](https://github.com/eggressive/agentic-writer/discussions).
