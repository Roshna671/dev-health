import shutil
import subprocess
from models import CheckResult, CheckStatus

class ToolChecker:
    def __init__(self, tools: list):
        self.tools = tools

    def check(self):
        results = []

        for tool in self.tools:
            if shutil.which(tool):
                if tool == "docker":
                    try:
                        docker_info = subprocess.run(["docker", "info"], capture_output=True, text=True)
                        if docker_info.returncode == 0:
                            results.append(CheckResult(
                                name=f"{tool} Tool",
                                status=CheckStatus.PASS,
                                message=f"{tool} is installed and running.",
                                category="tooling"
                            ))
                        else:
                            results.append(CheckResult(
                                name=f"{tool} Tool",
                                status=CheckStatus.FAIL,
                                message=f"{tool} is installed but the daemon is not running.",
                                fix_cmd="Start the Docker daemon",
                                category="tooling"
                            ))
                    except Exception as e:
                        results.append(CheckResult(
                            name=f"{tool} Tool",
                            status=CheckStatus.FAIL,
                            message=f"Failed to check Docker daemon: {str(e)}",
                            category="tooling"
                        ))
                else:
                    results.append(CheckResult(
                        name=f"{tool} Tool",
                        status=CheckStatus.PASS,
                        message=f"{tool} is installed.",
                        category="tooling"
                    ))
            else:
                fix_cmd = ""
                if tool == "git":
                    fix_cmd = "brew install git"
                elif tool == "docker":
                    fix_cmd = "Install from https://docker.com"

                results.append(CheckResult(
                    name=f"{tool} Tool",
                    status=CheckStatus.FAIL,
                    message=f"{tool} is not installed.",
                    fix_cmd=fix_cmd,
                    category="tooling"
                ))

        return results