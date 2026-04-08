import os
from importlib.metadata import version, PackageNotFoundError
from models import CheckResult, CheckStatus

class DepsChecker:
    def __init__(self, requirements_file="requirements.txt"):
        self.requirements_file = requirements_file

    def check(self):
        results = []

        if not os.path.exists(self.requirements_file):
            results.append(CheckResult(
                name="Dependencies",
                status=CheckStatus.WARN,
                message="requirements.txt file is missing.",
                fix_cmd="Create a requirements.txt file",
                category="dependencies"
            ))
            return results

        with open(self.requirements_file, "r") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            package, _, version_spec = line.partition("==")
            try:
                installed_version = version(package)
                if version_spec and installed_version != version_spec:
                    results.append(CheckResult(
                        name=f"Dependency: {package}",
                        status=CheckStatus.WARN,
                        message=f"{package} is installed but version {installed_version} does not match {version_spec}.",
                        fix_cmd="pip install -r requirements.txt",
                        category="dependencies"
                    ))
                else:
                    results.append(CheckResult(
                        name=f"Dependency: {package}",
                        status=CheckStatus.PASS,
                        message=f"{package} is installed and up-to-date.",
                        category="dependencies"
                    ))
            except PackageNotFoundError:
                results.append(CheckResult(
                    name=f"Dependency: {package}",
                    status=CheckStatus.FAIL,
                    message=f"{package} is not installed.",
                    fix_cmd="pip install -r requirements.txt",
                    category="dependencies"
                ))

        return results