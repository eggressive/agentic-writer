#!/usr/bin/env python3
"""Verify that the content creation agent is properly installed."""

import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return True, f"{version.major}.{version.minor}.{version.micro}"
    return False, f"{version.major}.{version.minor}.{version.micro}"


def check_dependencies():
    """Check if all required dependencies are installed."""
    dependencies = [
        "langchain",
        "langchain_openai",
        "langchain_core",
        "openai",
        "requests",
        "beautifulsoup4",
        "duckduckgo_search",
        "PIL",
        "dotenv",
        "pydantic",
        "tenacity",
        "click",
        "rich",
        "pytest",
    ]

    results = {}
    for dep in dependencies:
        try:
            if dep == "PIL":
                __import__("PIL")
            elif dep == "dotenv":
                __import__("dotenv")
            elif dep == "beautifulsoup4":
                __import__("bs4")
            elif dep == "duckduckgo_search":
                __import__("duckduckgo_search")
            else:
                __import__(dep)
            results[dep] = (True, "✓")
        except ImportError:
            results[dep] = (False, "✗")

    return results


def check_modules():
    """Check if project modules can be imported."""
    modules = [
        "src.utils.config",
        "src.utils.logger",
        "src.agents.researcher",
        "src.agents.writer",
        "src.agents.image_handler",
        "src.agents.publisher",
        "src.orchestrator",
        "src.cli",
    ]

    results = {}
    for module in modules:
        try:
            __import__(module)
            results[module] = (True, "✓")
        except ImportError as e:
            results[module] = (False, f"✗ {str(e)}")

    return results


def check_configuration():
    """Check if configuration can be loaded."""
    try:
        from src.utils.config import Config

        config = Config.from_env()

        status = {
            "Config loads": True,
            "OPENAI_API_KEY": bool(config.openai_api_key),
            "MEDIUM_TOKEN": bool(config.medium_access_token),
            "UNSPLASH_KEY": bool(config.unsplash_access_key),
        }
        return status
    except Exception as e:
        return {"Error": str(e)}


def run_tests():
    """Run pytest tests."""
    try:
        import pytest

        result = pytest.main(["-v", "--no-cov", "tests/"])
        return result == 0
    except Exception as e:
        return False, str(e)


def main():
    """Run all verification checks."""
    console.print(
        Panel.fit(
            "[bold cyan]Agentic-Writer Installation Verification[/bold cyan]",
            border_style="cyan",
        )
    )

    # Python version
    console.print("\n[bold]1. Checking Python Version...[/bold]")
    py_ok, py_version = check_python_version()
    if py_ok:
        console.print(f"   [green]✓[/green] Python {py_version} (>= 3.8 required)")
    else:
        console.print(
            f"   [red]✗[/red] Python {py_version} (>= 3.8 required but found {py_version})"
        )

    # Dependencies
    console.print("\n[bold]2. Checking Dependencies...[/bold]")
    deps = check_dependencies()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Package", style="cyan")
    table.add_column("Status", style="green")

    all_deps_ok = True
    for dep, (ok, status) in deps.items():
        table.add_row(
            dep, f"[green]{status}[/green]" if ok else f"[red]{status}[/red]"
        )
        if not ok:
            all_deps_ok = False

    console.print(table)

    if all_deps_ok:
        console.print("   [green]✓[/green] All dependencies installed")
    else:
        console.print(
            "   [red]✗[/red] Some dependencies missing. Run: pip install -r requirements.txt"
        )

    # Project modules
    console.print("\n[bold]3. Checking Project Modules...[/bold]")
    modules = check_modules()
    all_modules_ok = True
    for module, (ok, status) in modules.items():
        if ok:
            console.print(f"   [green]{status}[/green] {module}")
        else:
            console.print(f"   [red]{status}[/red] {module}")
            all_modules_ok = False

    if all_modules_ok:
        console.print("   [green]✓[/green] All project modules can be imported")
    else:
        console.print("   [red]✗[/red] Some modules failed to import")

    # Configuration
    console.print("\n[bold]4. Checking Configuration...[/bold]")
    config_status = check_configuration()
    for key, value in config_status.items():
        if isinstance(value, bool):
            if value:
                console.print(f"   [green]✓[/green] {key}")
            else:
                if "API_KEY" in key.upper():
                    console.print(f"   [yellow]○[/yellow] {key} (required for running)")
                else:
                    console.print(f"   [yellow]○[/yellow] {key} (optional)")
        else:
            console.print(f"   [red]✗[/red] {key}: {value}")

    # Tests
    console.print("\n[bold]5. Running Tests...[/bold]")
    console.print("   Running pytest...")
    tests_ok = run_tests()

    if tests_ok:
        console.print("   [green]✓[/green] All tests passed")
    else:
        console.print("   [red]✗[/red] Some tests failed")

    # Summary
    console.print("\n" + "=" * 60)
    if py_ok and all_deps_ok and all_modules_ok:
        console.print(
            "[bold green]✓ Installation verified successfully![/bold green]\n"
        )
        console.print("Next steps:")
        console.print("1. Add your OPENAI_API_KEY to .env file")
        console.print('2. Run: python main.py create "Your Topic"')
        console.print("3. Check the output/ directory for your article\n")
    else:
        console.print("[bold red]✗ Installation verification failed[/bold red]\n")
        console.print("Please address the issues above and try again.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
