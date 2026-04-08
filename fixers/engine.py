import subprocess
from rich.console import Console
from rich.prompt import Confirm
from models import CheckResult, CheckStatus

class FixEngine:
    def __init__(self):
        self.console = Console()

    def show_fixes(self, results):
        for result in results:
            if result.status in [CheckStatus.FAIL, CheckStatus.WARN] and result.fix_cmd:
                self.console.print(f"[bold]{result.name}[/]: {result.message}")
                self.console.print(f"Fix Command: [italic]{result.fix_cmd}[/]")
                if Confirm.ask("Do you want to run this fix?"):
                    self.run_fix(result.fix_cmd)

    def run_fix(self, fix_cmd):
        if not self.is_safe_fix(fix_cmd):
            self.console.print(f"[bold red]Skipping unsafe fix command: {fix_cmd}[/]")
            return

        self.console.print(f"[bold]Running:[/] {fix_cmd}")
        try:
            subprocess.run(fix_cmd, shell=True, check=True)
            self.console.print(f"[bold green]Success:[/] {fix_cmd}")
        except subprocess.CalledProcessError as e:
            self.console.print(f"[bold red]Failed:[/] {fix_cmd} (Error: {e})")

    def auto_fix(self, results):
        for result in results:
            if result.status == CheckStatus.FAIL and result.fix_cmd and self.is_safe_fix(result.fix_cmd):
                self.run_fix(result.fix_cmd)

    def is_safe_fix(self, fix_cmd):
        unsafe_keywords = ["rm", "kill", "sudo", "drop", "delete"]
        return not any(keyword in fix_cmd for keyword in unsafe_keywords)