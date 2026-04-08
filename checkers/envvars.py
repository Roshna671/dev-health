import os
from models import CheckResult, CheckStatus

class EnvVarChecker:
    def __init__(self, required_vars, env_file=".env"):
        self.required_vars = required_vars
        self.env_file = env_file

    def check(self):
        results = []

        # Check if .env file exists
        if not os.path.exists(self.env_file):
            results.append(CheckResult(
                name=".env File",
                status=CheckStatus.WARN,
                message=".env file is missing.",
                fix_cmd=f"Create a {self.env_file} file",
                category="environment"
            ))

        for var in self.required_vars:
            value = os.environ.get(var)
            if value is None:
                results.append(CheckResult(
                    name=f"Environment Variable: {var}",
                    status=CheckStatus.FAIL,
                    message=f"{var} is missing.",
                    fix_cmd=f"Add {var} to your .env file",
                    category="environment"
                ))
            elif value.lower() in ["changeme", "your-key-here", "xxx", "placeholder"]:
                results.append(CheckResult(
                    name=f"Environment Variable: {var}",
                    status=CheckStatus.WARN,
                    message=f"{var} looks like a placeholder value.",
                    category="environment"
                ))
            else:
                results.append(CheckResult(
                    name=f"Environment Variable: {var}",
                    status=CheckStatus.PASS,
                    message=f"{var} is set.",
                    category="environment"
                ))

        return results