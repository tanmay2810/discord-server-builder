import json
from pathlib import Path
from typing import Any, Dict


CONFIG_PATH = Path(__file__).with_name("server_config.json")
EXAMPLE_CONFIG_PATH = Path(__file__).with_name("server_config.example.json")


def load_server_config(path: str | Path | None = None) -> Dict[str, Any]:
    """Load the server configuration from server_config.json or fall back to the example file."""
    config_path = Path(path) if path else CONFIG_PATH

    if not config_path.exists():
        config_path = EXAMPLE_CONFIG_PATH

    with config_path.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)
