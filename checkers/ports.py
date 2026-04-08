import socket
from models import CheckResult, CheckStatus

class PortChecker:
    def __init__(self, ports):
        self.ports = ports

    def check(self):
        results = []

        for port in self.ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(("localhost", port))
                if result == 0:
                    results.append(CheckResult(
                        name=f"Port {port}",
                        status=CheckStatus.FAIL,
                        message=f"Port {port} is in use — stop the process using it.",
                        fix_cmd=f"lsof -i :{port} to find the process, then kill it",
                        category="system"
                    ))
                else:
                    results.append(CheckResult(
                        name=f"Port {port}",
                        status=CheckStatus.PASS,
                        message=f"Port {port} is free.",
                        category="system"
                    ))

        return results