"""Setup configuration for the content creation agent."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentic-v",
    version="0.1.0",
    author="Dimitar",
    description="Automated content creation and management using LangChain agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eggressive/agentic-v",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-community>=0.0.20",
        "langchain-core>=0.1.0",
        "openai>=1.10.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "duckduckgo-search>=4.0.0",
        "pillow>=10.0.0",
        "medium-api>=0.6.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "tenacity>=8.2.0",
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "content-agent=src.cli:cli",
        ],
    },
)
