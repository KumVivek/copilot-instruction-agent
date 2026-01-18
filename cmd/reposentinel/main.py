"""Main entry point for RepoSentinel."""
import sys
import os
import logging
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from core.config import Config
from core.logger import setup_logger
from core.profiler.detect import detect_stack
from core.analyzers.runner import run_analyzers
from core.risk.scorer import score
from core.rules.builder import build_rules
from llm.client import LLMClient
from core.report.writer import write_report
from core.instructions.generator import InstructionGenerator

console = Console()

def main(repo: Optional[str] = None, skip_llm: bool = False) -> int:
    """Main entry point for RepoSentinel.
    
    Args:
        repo: Optional repository path. If not provided, uses current directory.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Get repository path
        if not repo:
            if len(sys.argv) > 1:
                repo = sys.argv[1]
            else:
                repo = str(Path.cwd())
        
        # Validate repository path
        repo_path = Path(repo)
        if not repo_path.exists():
            console.print(f"[red]Error: Repository path does not exist: {repo}[/red]")
            return 1
        
        if not repo_path.is_dir():
            console.print(f"[red]Error: Repository path is not a directory: {repo}[/red]")
            return 1
        
        # Load configuration
        config = Config()
        
        # Setup logging
        log_level = config.get("logging.level", "INFO")
        use_rich = config.get("logging.format", "rich") == "rich"
        logger = setup_logger("reposentinel", log_level, use_rich)
        
        logger.info(f"Starting RepoSentinel analysis for: {repo}")
        
        # Display banner
        console.print(Panel.fit(
            "[bold blue]RepoSentinel[/bold blue]\n"
            "Production-grade repo intelligence engine",
            border_style="blue"
        ))
        
        # Run analysis with progress indicators
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Detect stack
            task1 = progress.add_task("Detecting technology stack...", total=None)
            try:
                stack = detect_stack(repo)
                progress.update(task1, completed=True)
                console.print(f"[green]✓[/green] Detected: {stack['language']} "
                            f"(confidence: {stack['confidence']:.0%})")
            except Exception as e:
                progress.update(task1, completed=True)
                logger.error(f"Stack detection failed: {e}")
                console.print(f"[red]✗[/red] Stack detection failed: {e}")
                return 1
            
            # Run analyzers
            task2 = progress.add_task("Running code analyzers...", total=None)
            try:
                findings = run_analyzers(repo, stack)
                progress.update(task2, completed=True)
                console.print(f"[green]✓[/green] Found {len(findings)} issue(s)")
            except Exception as e:
                progress.update(task2, completed=True)
                logger.error(f"Analysis failed: {e}", exc_info=True)
                console.print(f"[red]✗[/red] Analysis failed: {e}")
                return 1
            
            # Calculate risk scores
            task3 = progress.add_task("Calculating risk scores...", total=None)
            try:
                risk = score(findings, config)
                progress.update(task3, completed=True)
                console.print(f"[green]✓[/green] Calculated risk for {len(risk)} category/categories")
            except Exception as e:
                progress.update(task3, completed=True)
                logger.error(f"Risk scoring failed: {e}", exc_info=True)
                console.print(f"[red]✗[/red] Risk scoring failed: {e}")
                return 1
            
            # Build rules
            task4 = progress.add_task("Building rules from findings and best practices...", total=None)
            try:
                language = stack.get("language", "")
                rules = build_rules(findings, risk, config, language)
                progress.update(task4, completed=True)
                console.print(f"[green]✓[/green] Generated {len(rules)} rule(s)")
            except Exception as e:
                progress.update(task4, completed=True)
                logger.error(f"Rule building failed: {e}", exc_info=True)
                console.print(f"[red]✗[/red] Rule building failed: {e}")
                return 1
            
            # Generate Copilot instructions (categorized)
            if skip_llm:
                logger.info("Skipping LLM generation (--skip-llm flag set)")
                categorized_instructions = None
                console.print(f"[yellow]⚠[/yellow] Skipped AI-generated instructions")
            else:
                task5 = progress.add_task("Generating categorized Copilot instructions...", total=None)
                try:
                    llm = LLMClient(config)
                    categorized_instructions = llm.generate_instructions(stack, rules, findings)
                    progress.update(task5, completed=True)
                    console.print(f"[green]✓[/green] Generated {len(categorized_instructions)} instruction file(s)")
                except RuntimeError as e:
                    progress.update(task5, completed=True)
                    error_msg = str(e)
                    if "quota" in error_msg.lower() or "api key" in error_msg.lower():
                        console.print(f"[yellow]⚠[/yellow] {error_msg}")
                        console.print("[yellow]Continuing without AI-generated instructions...[/yellow]")
                        categorized_instructions = None
                    else:
                        logger.error(f"Instruction generation failed: {e}", exc_info=True)
                        console.print(f"[red]✗[/red] Instruction generation failed: {e}")
                        return 1
                except Exception as e:
                    progress.update(task5, completed=True)
                    logger.error(f"Instruction generation failed: {e}", exc_info=True)
                    console.print(f"[red]✗[/red] Instruction generation failed: {e}")
                    return 1
        
        # Write outputs to the analyzed repository
        try:
            # Resolve repository path
            repo = Path(repo).resolve()
            github_dir = repo / ".github"
            github_dir.mkdir(parents=True, exist_ok=True)
            
            if categorized_instructions:
                # Write categorized instruction files
                category_titles = {
                    "design": "Design & Architecture",
                    "api": "API Development",
                    "security": "Security",
                    "data-access": "Data Access",
                    "caching": "Caching",
                    "testing": "Testing",
                    "logging": "Logging",
                }
                
                for category, content in categorized_instructions.items():
                    filename = f"copilot-instructions-{category}.md"
                    instruction_file = github_dir / filename
                    
                    with open(instruction_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    title = category_titles.get(category, category.title())
                    logger.info(f"{title} instructions written to {instruction_file}")
                    console.print(f"[green]✓[/green] {title}: {instruction_file}")
            else:
                # Generate basic categorized instructions without AI
                generator = InstructionGenerator(stack.get("language", ""))
                basic_instructions = generator.generate_all_instructions(stack, findings, rules)
                
                category_titles = {
                    "design": "Design & Architecture",
                    "api": "API Development",
                    "security": "Security",
                    "data-access": "Data Access",
                    "caching": "Caching",
                    "testing": "Testing",
                    "logging": "Logging",
                }
                
                for category, content in basic_instructions.items():
                    filename = f"copilot-instructions-{category}.md"
                    instruction_file = github_dir / filename
                    
                    with open(instruction_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    
                    title = category_titles.get(category, category.title())
                    logger.info(f"Basic {title} instructions written to {instruction_file}")
                    console.print(f"[yellow]ℹ[/yellow] {title} (basic): {instruction_file}")
            
            # Write report to the analyzed repository
            write_report(stack, findings, risk, config, str(repo))
            report_path = config.get("output.report_path", "analysis-report.md")
            report_file = repo / report_path
            console.print(f"[green]✓[/green] Analysis report: {report_file}")
            
        except Exception as e:
            logger.error(f"Failed to write outputs: {e}", exc_info=True)
            console.print(f"[red]✗[/red] Failed to write outputs: {e}")
            return 1
        
        # Display summary
        console.print("\n[bold]Summary:[/bold]")
        summary_table = Table(show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Language", stack.get("language", "Unknown"))
        summary_table.add_row("Findings", str(len(findings)))
        summary_table.add_row("Rules Generated", str(len(rules)))
        summary_table.add_row("Risk Categories", str(len(risk)))
        
        critical_count = sum(1 for score_val in risk.values() if score_val <= 5)
        summary_table.add_row("Critical Categories", str(critical_count))
        
        console.print(summary_table)
        
        logger.info("Analysis completed successfully")
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Analysis interrupted by user[/yellow]")
        return 130
    except Exception as e:
        logger.exception("Unexpected error occurred")
        console.print(f"[red]Unexpected error: {e}[/red]")
        return 1

def _generate_basic_instructions(stack: Dict[str, Any], rules: List[str]) -> str:
    """Generate basic instructions without AI."""
    language = stack.get("language", "Unknown")
    rules_text = "\n".join(f"- {rule}" for rule in rules) if rules else "No specific rules generated."
    
    return f"""# GitHub Copilot Instructions

## Technology Stack
- **Language**: {language}
- **Confidence**: {stack.get('confidence', 0):.0%}

## Rules and Constraints

{rules_text}

## Notes

This file was generated automatically by RepoSentinel.
For AI-enhanced instructions, set your OPENAI_API_KEY and run without --skip-llm flag.
"""

def cli():
    """CLI entry point for setuptools."""
    parser = argparse.ArgumentParser(
        description="RepoSentinel - Generate GitHub Copilot guardrails",
        prog="reposentinel"
    )
    parser.add_argument(
        "repo",
        nargs="?",
        help="Path to repository to analyze (default: current directory)"
    )
    parser.add_argument(
        "--skip-llm",
        action="store_true",
        help="Skip AI-generated instructions (useful if API quota exceeded)"
    )
    
    args = parser.parse_args()
    repo = args.repo if args.repo else None
    sys.exit(main(repo, skip_llm=args.skip_llm))

if __name__ == "__main__":
    cli()
