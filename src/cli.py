"""Command-line interface for the content creation agent."""

from __future__ import annotations

from typing import Optional

import click
import openai
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .orchestrator import ContentCreationOrchestrator
from .utils import Config, setup_logger

console = Console()

VALID_STYLES = {
    "professional",
    "casual",
    "technical",
    "academic",
    "conversational",
    "formal",
    "informal",
}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
MAX_TOPIC_LENGTH = 500
MIN_TOPIC_LENGTH = 3


def validate_create_inputs(topic: str, style: Optional[str], log_level: str) -> None:
    """Validate inputs for the create command.

    Args:
        topic: The content topic provided by the user.
        style: Optional writing style.
        log_level: Logging verbosity level.

    Raises:
        click.BadParameter: If any argument fails validation.
    """
    stripped = topic.strip()
    if not stripped:
        raise click.BadParameter(
            "Topic cannot be empty or whitespace.", param_hint="'TOPIC'"
        )
    if len(stripped) < MIN_TOPIC_LENGTH:
        raise click.BadParameter(
            f"Topic must be at least {MIN_TOPIC_LENGTH} characters.",
            param_hint="'TOPIC'",
        )
    if len(stripped) > MAX_TOPIC_LENGTH:
        raise click.BadParameter(
            f"Topic must be at most {MAX_TOPIC_LENGTH} characters.",
            param_hint="'TOPIC'",
        )

    if style is not None and style.lower() not in VALID_STYLES:
        valid = ", ".join(sorted(VALID_STYLES))
        raise click.BadParameter(
            f"Invalid style '{style}'. Valid styles: {valid}.",
            param_hint="'--style'",
        )

    if log_level.upper() not in VALID_LOG_LEVELS:
        valid = ", ".join(sorted(VALID_LOG_LEVELS))
        raise click.BadParameter(
            f"Invalid log level '{log_level}'. Valid levels: {valid}.",
            param_hint="'--log-level'",
        )


@click.group()
def cli():
    """Automated Content Creation & Management Agent.

    This tool helps you research topics, write articles, find images,
    and publish content automatically using AI agents.
    """
    pass


@cli.command()
@click.argument("topic")
@click.option(
    "--style",
    default=None,
    help="Writing style (e.g., professional, casual, technical)",
)
@click.option("--audience", default=None, help="Target audience description")
@click.option(
    "--platform", multiple=True, default=["file"], help="Publishing platform(s)"
)
@click.option("--output-dir", default="output", help="Output directory for files")
@click.option("--log-level", default="INFO", help="Logging level")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Validate config and show what would run without calling APIs",
)
def create(topic, style, audience, platform, output_dir, log_level, dry_run):
    """Create and publish content on a given TOPIC.

    Example:
        content-agent create "Artificial Intelligence in Healthcare" --style professional
    """
    validate_create_inputs(topic, style, log_level)
    topic = topic.strip()
    log_level = log_level.upper()

    # Setup
    logger = setup_logger(level=log_level)

    console.print(
        Panel.fit(
            f"[bold cyan]Automated Content Creation Agent[/bold cyan]\n"
            f"Topic: [yellow]{topic}[/yellow]",
            border_style="cyan",
        )
    )

    try:
        # Load configuration
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Loading configuration...", total=None)
            config = Config.from_env()
            config.validate_required()
            progress.update(task, completed=True)

        console.print("[green]✓[/green] Configuration loaded")

        if dry_run:
            console.print(
                Panel(
                    f"[bold]Topic:[/bold] {topic}\n"
                    f"[bold]Style:[/bold] {style or '(default)'}\n"
                    f"[bold]Audience:[/bold] {audience or '(default)'}\n"
                    f"[bold]Platforms:[/bold] {', '.join(platform)}\n"
                    f"[bold]Output Dir:[/bold] {output_dir}\n"
                    f"[bold]Model:[/bold] {config.openai_model}\n"
                    f"[bold]Pipeline:[/bold] audience → research → write → images → publish",
                    title="Dry Run",
                    border_style="yellow",
                )
            )
            console.print("[yellow]Dry run complete — no APIs called.[/yellow]")
            return

        # Initialize orchestrator
        orchestrator = ContentCreationOrchestrator(config)
        console.print("[green]✓[/green] Agents initialized")

        # Run content creation pipeline
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Research
            task1 = progress.add_task("[cyan]Researching topic...", total=None)

            # Execute pipeline
            results = orchestrator.create_content(
                topic=topic,
                style=style,
                target_audience=audience,
                platforms=list(platform),
                output_dir=output_dir,
            )

            progress.update(task1, completed=True)

        # Display results
        if results.get("status") == "completed":
            console.print(
                "\n[bold green]✓ Content creation completed successfully![/bold green]\n"
            )

            # Display summary
            summary = orchestrator.get_summary(results)
            console.print(Panel(summary, title="Summary", border_style="green"))

            # Display article preview
            article = results.get("article", {})
            console.print(f"\n[bold]Title:[/bold] {article.get('title')}")
            console.print(f"[bold]Word Count:[/bold] {article.get('word_count')}")
            console.print(f"[bold]Tags:[/bold] {', '.join(article.get('tags', []))}")

            # Display publication info
            pub_results = results.get("publication", {})
            if "file" in pub_results and pub_results["file"].get("success"):
                file_path = pub_results["file"].get("markdown_file")
                console.print(
                    f"\n[bold green]Article saved to:[/bold green] {file_path}"
                )
        else:
            console.print(
                f"\n[bold red]✗ Content creation failed:[/bold red] {results.get('error')}"
            )

    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {str(e)}")
        console.print(
            "\nPlease ensure you have set the required environment variables."
        )
        console.print("Copy .env.example to .env and fill in your API keys.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        logger.exception("Content creation failed")


@cli.command()
def config():
    """Display current configuration."""
    try:
        cfg = Config.from_env()

        console.print(
            Panel.fit(
                "[bold cyan]Current Configuration[/bold cyan]", border_style="cyan"
            )
        )

        console.print(f"\n[bold]OpenAI Model:[/bold] {cfg.openai_model}")
        console.print(f"[bold]Temperature:[/bold] {cfg.temperature}")
        console.print(f"[bold]Max Research Sources:[/bold] {cfg.max_research_sources}")
        console.print(f"[bold]Log Level:[/bold] {cfg.log_level}")

        console.print("\n[bold]API Keys Status:[/bold]")
        console.print(
            f"  OpenAI: {'[green]✓ Set[/green]' if cfg.openai_api_key else '[red]✗ Not set[/red]'}"
        )
        console.print(
            f"  Unsplash: {'[green]✓ Set[/green]' if cfg.unsplash_access_key else '[yellow]○ Optional[/yellow]'}"
        )

        console.print("\n[bold]Publishing Platforms:[/bold]")
        console.print(
            f"  Medium: {'[green]✓ Set[/green]' if cfg.medium_access_token else '[yellow]○ Optional[/yellow]'}"
        )
        ghost_ready = bool(cfg.ghost_api_url and cfg.ghost_admin_api_key)
        console.print(
            f"  Ghost: {'[green]✓ Set[/green]' if ghost_ready else '[yellow]○ Optional[/yellow]'}"
        )
        wp_ready = bool(
            cfg.wordpress_url and cfg.wordpress_username and cfg.wordpress_app_password
        )
        console.print(
            f"  WordPress: {'[green]✓ Set[/green]' if wp_ready else '[yellow]○ Optional[/yellow]'}"
        )
        hn_ready = bool(cfg.hashnode_api_key and cfg.hashnode_publication_id)
        console.print(
            f"  Hashnode: {'[green]✓ Set[/green]' if hn_ready else '[yellow]○ Optional[/yellow]'}"
        )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@cli.command()
def health():
    """Verify that configured API keys are working.

    Makes lightweight API calls to OpenAI (required), Unsplash (optional),
    and Medium (optional) to confirm credentials are valid before running
    the full pipeline.

    Exits with code 1 if any configured service fails its check.
    """
    cfg = Config.from_env()

    console.print(
        Panel.fit("[bold cyan]API Health Check[/bold cyan]", border_style="cyan")
    )

    results: list[tuple[str, str, str]] = []  # (service, status, message)

    # --- OpenAI (required) ---
    if not cfg.openai_api_key:
        results.append(("OpenAI", "error", "API key not set"))
    else:
        try:
            client = openai.OpenAI(api_key=cfg.openai_api_key)
            client.models.list()
            results.append(("OpenAI", "ok", ""))
        except openai.AuthenticationError:
            results.append(("OpenAI", "error", "Invalid API key"))
        except Exception as e:
            results.append(("OpenAI", "error", str(e)))

    # --- Unsplash (optional) ---
    if not cfg.unsplash_access_key:
        results.append(("Unsplash", "skip", "Not configured (optional)"))
    else:
        try:
            resp = requests.get(
                "https://api.unsplash.com/photos",
                params={"per_page": 1},
                headers={"Authorization": f"Client-ID {cfg.unsplash_access_key}"},
                timeout=10,
            )
            if resp.status_code == 200:
                results.append(("Unsplash", "ok", ""))
            elif resp.status_code == 401:
                results.append(("Unsplash", "error", "Invalid API key (HTTP 401)"))
            else:
                results.append(("Unsplash", "error", f"HTTP {resp.status_code}"))
        except Exception as e:
            results.append(("Unsplash", "error", str(e)))

    # --- Medium (optional) ---
    if not cfg.medium_access_token:
        results.append(("Medium", "skip", "Not configured (optional)"))
    else:
        try:
            resp = requests.get(
                "https://api.medium.com/v1/me",
                headers={"Authorization": f"Bearer {cfg.medium_access_token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                results.append(("Medium", "ok", ""))
            elif resp.status_code == 401:
                results.append(("Medium", "error", "Invalid token (HTTP 401)"))
            else:
                results.append(("Medium", "error", f"HTTP {resp.status_code}"))
        except Exception as e:
            results.append(("Medium", "error", str(e)))

    # Display results
    console.print()
    any_error = False
    for service, status, message in results:
        if status == "ok":
            console.print(f"  [bold]{service}[/bold]  [green]✓ OK[/green]")
        elif status == "skip":
            console.print(f"  [bold]{service}[/bold]  [yellow]○ {message}[/yellow]")
        else:
            console.print(f"  [bold]{service}[/bold]  [red]✗ {message}[/red]")
            any_error = True

    console.print()
    if any_error:
        console.print("[bold red]✗ One or more health checks failed.[/bold red]")
        raise SystemExit(1)
    else:
        console.print("[bold green]✓ All configured services are healthy.[/bold green]")


@cli.command()
def version():
    """Display version information."""
    from . import __version__

    console.print(
        f"[bold cyan]Content Creation Agent[/bold cyan] version [yellow]{__version__}[/yellow]"
    )


if __name__ == "__main__":
    cli()
