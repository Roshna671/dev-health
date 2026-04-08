from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from models import CheckResult, CheckStatus

class TerminalReporter:
    def __init__(self):
        self.console = Console()

    def report(self, results):
        grouped_results = {}
        for result in results:
            grouped_results.setdefault(result.category, []).append(result)

        self.console.print(Panel(Text("DEV ENVIRONMENT HEALTH REPORT", justify="center", style="bold magenta")))

        pass_count = warn_count = fail_count = 0

        for category, checks in grouped_results.items():
            table = Table(title=f"Category: {category}")
            table.add_column("Status", justify="center")
            table.add_column("Check Name")
            table.add_column("Message")
            table.add_column("Fix Command")

            for check in checks:
                if check.status == CheckStatus.PASS:
                    status_icon = "✅"
                    pass_count += 1
                elif check.status == CheckStatus.WARN:
                    status_icon = "⚠️"
                    warn_count += 1
                else:
                    status_icon = "❌"
                    fail_count += 1

                table.add_row(status_icon, check.name, check.message, check.fix_cmd or "N/A")

            self.console.print(table)

        total = pass_count + warn_count + fail_count
        health_score = (pass_count / total) * 100 if total > 0 else 0
        score_color = "green" if health_score >= 80 else "yellow" if health_score >= 50 else "red"

        self.console.print(f"\n[bold]Summary:[/] {pass_count} passed, {warn_count} warnings, {fail_count} failed")
        self.console.print(f"[bold {score_color}]Health Score: {health_score:.1f}%[/]")

        if fail_count > 0:
            self.console.print("\n[bold red]Run \"devhealth fix\" to auto-resolve issues[/]")