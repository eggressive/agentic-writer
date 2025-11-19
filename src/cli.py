"""Command-line interface for the content creation agent."""

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from .orchestrator import ContentCreationOrchestrator
from .utils import Config, setup_logger


console = Console()


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
def create(topic, style, audience, platform, output_dir, log_level):
    """Create and publish content on a given TOPIC.

    Example:
        content-agent create "Artificial Intelligence in Healthcare" --style professional
    """
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
            f"  Medium: {'[green]✓ Set[/green]' if cfg.medium_access_token else '[yellow]○ Optional[/yellow]'}"
        )
        console.print(
            f"  Unsplash: {'[green]✓ Set[/green]' if cfg.unsplash_access_key else '[yellow]○ Optional[/yellow]'}"
        )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@cli.command()
def version():
    """Display version information."""
    from . import __version__

    console.print(
        f"[bold cyan]Content Creation Agent[/bold cyan] version [yellow]{__version__}[/yellow]"
    )


if __name__ == "__main__":
    cli()
