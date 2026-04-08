from pydantic import BaseModel
from typing import List, Optional
import yaml
import os

class DevHealthConfig(BaseModel):
    required_tools: List[str]
    required_env_vars: List[str]
    python_version: str
    node_version: Optional[str] = None
    required_ports_free: List[int]
    min_disk_gb: int = 2

def load_config() -> DevHealthConfig:
    config_path = ".envhealth.yml"
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config_data = yaml.safe_load(file)
        return DevHealthConfig(**config_data)
    else:
        return DevHealthConfig(
            required_tools=["git", "docker"],
            required_env_vars=["DATABASE_URL", "SECRET_KEY"],
            python_version="3.10",
            required_ports_free=[5432, 3000],
        )