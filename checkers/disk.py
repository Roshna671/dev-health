import shutil
from models import CheckResult, CheckStatus

class DiskChecker:
    def __init__(self, min_gb=2.0):
        self.min_gb = min_gb

    def check(self):
        total, used, free = shutil.disk_usage(".")
        free_gb = free / (1024 ** 3)

        if free_gb >= self.min_gb * 2:
            return [CheckResult(
                name="Disk Space",
                status=CheckStatus.PASS,
                message=f"Free disk space: {free_gb:.1f} GB (sufficient).",
                category="system"
            )]
        elif free_gb >= self.min_gb:
            return [CheckResult(
                name="Disk Space",
                status=CheckStatus.WARN,
                message=f"Free disk space: {free_gb:.1f} GB (low, consider cleanup).",
                category="system"
            )]
        else:
            return [CheckResult(
                name="Disk Space",
                status=CheckStatus.FAIL,
                message=f"Free disk space: {free_gb:.1f} GB (insufficient).",
                fix_cmd="Run: du -sh * | sort -rh to find large files",
                category="system"
            )]