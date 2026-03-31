"""Setup configuration for the content creation agent."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentic-writer",
    version="0.12.1",
    author="Dimitar",
    description="Automated content creation and management using LangChain agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eggressive/agentic-writer",
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
        "langchain~=1.2.13",
        "langchain-openai~=1.1.12",
        "langchain-community~=0.4.1",
        "langchain-core~=1.2.23",
        "openai~=2.30.0",
        "requests~=2.32.5",
        "beautifulsoup4~=4.14.3",
        "ddgs~=9.12.0",
        "pillow~=12.1.1",
        "medium-api~=0.6.1",
        "python-dotenv~=1.2.2",
        "pydantic~=2.12.5",
        "tenacity~=9.1.4",
        "click~=8.3.1",
        "rich~=14.3.3",
    ],
    extras_require={
        "dev": [
            "pytest~=9.0.2",
            "pytest-cov~=7.1.0",
            "black~=26.3.1",
            "ruff~=0.15.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "content-agent=src.cli:cli",
        ],
    },
)
