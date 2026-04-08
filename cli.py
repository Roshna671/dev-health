import typer
from rich.console import Console
from config import load_config
from checkers.runtime import RuntimeChecker
from checkers.tools import ToolChecker
from checkers.envvars import EnvVarChecker
from checkers.deps import DepsChecker
from checkers.ports import PortChecker
from checkers.disk import DiskChecker
from reporters.terminal import TerminalReporter
from fixers.engine import FixEngine

app = typer.Typer()
console = Console()

@app.command()
def check(fix: bool = typer.Option(False, help="Run fix engine after checks"),
          export: str = typer.Option(None, help="Export results as JSON")):
    config = load_config()
    results = []

    console.print("[bold magenta]Running checks...[/]")
    with console.status("Checking..."):
        results.extend(RuntimeChecker(config.python_version, config.node_version).check())
        results.extend(ToolChecker(config.required_tools).check())
        results.extend(EnvVarChecker(config.required_env_vars).check())
        results.extend(DepsChecker().check())
        results.extend(PortChecker(config.required_ports_free).check())
        results.extend(DiskChecker(config.min_disk_gb).check())

    reporter = TerminalReporter()
    reporter.report(results)

    if export:
        import json
        with open(export, "w") as file:
            json.dump([result.__dict__ for result in results], file, indent=4)
        console.print(f"[bold green]Results exported to {export}[/]")

    if fix:
        engine = FixEngine()
        engine.auto_fix(results)

@app.command()
def fix():
    check(fix=True)

@app.command()
def export():
    check(export="health_report.json")

if __name__ == "__main__":
    app()