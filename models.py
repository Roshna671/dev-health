from dataclasses import dataclass, field
from enum import Enum

class CheckStatus(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"

@dataclass
class CheckResult:
    name: str
    status: CheckStatus
    message: str
    fix_cmd: str = field(default="")
    category: str = field(default="general")