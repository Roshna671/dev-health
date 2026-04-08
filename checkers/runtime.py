import subprocess
from packaging import version
from models import CheckResult, CheckStatus

class RuntimeChecker:
    def __init__(self, min_python: str, min_node: str):
        self.min_python = min_python
        self.min_node = min_node

    def check(self):
        results = []

        # Check Python version
        try:
            python_version_output = subprocess.run(["python3", "--version"], capture_output=True, text=True, check=True)
            python_version = python_version_output.stdout.strip().split()[1]
            if version.parse(python_version) >= version.parse(self.min_python):
                results.append(CheckResult(
                    name="Python Version",
                    status=CheckStatus.PASS,
                    message=f"Python version {python_version} meets the requirement.",
                    category="runtime"
                ))
            else:
                results.append(CheckResult(
                    name="Python Version",
                    status=CheckStatus.FAIL,
                    message=f"Python version {python_version} is below the required {self.min_python}.",
                    fix_cmd="pyenv install 3.11.4",
                    category="runtime"
                ))
        except Exception as e:
            results.append(CheckResult(
                name="Python Version",
                status=CheckStatus.FAIL,
                message=f"Failed to check Python version: {str(e)}",
                category="runtime"
            ))

        # Check Node.js version
        try:
            node_version_output = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
            node_version = node_version_output.stdout.strip().lstrip("v")
            if version.parse(node_version) >= version.parse(self.min_node):
                results.append(CheckResult(
                    name="Node.js Version",
                    status=CheckStatus.PASS,
                    message=f"Node.js version {node_version} meets the requirement.",
                    category="runtime"
                ))
            else:
                results.append(CheckResult(
                    name="Node.js Version",
                    status=CheckStatus.FAIL,
                    message=f"Node.js version {node_version} is below the required {self.min_node}.",
                    fix_cmd="nvm install 18",
                    category="runtime"
                ))
        except FileNotFoundError:
            results.append(CheckResult(
                name="Node.js Version",
                status=CheckStatus.WARN,
                message="Node.js is not installed.",
                fix_cmd="nvm install 18",
                category="runtime"
            ))
        except Exception as e:
            results.append(CheckResult(
                name="Node.js Version",
                status=CheckStatus.FAIL,
                message=f"Failed to check Node.js version: {str(e)}",
                category="runtime"
            ))

        return results