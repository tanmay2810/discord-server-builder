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


def is_builder_enabled(guild_id: int) -> bool:
    """Check if the server builder is explicitly enabled for a guild.

    Unknown guilds default to builder_enabled = False.
    """
    config = load_server_config()
    servers = config.get("servers", {})
    guild_config = servers.get(str(guild_id))
    if guild_config is None:
        return False
    return bool(guild_config.get("builder_enabled", False))


def get_guild_config(guild_id: int) -> Dict[str, Any]:
    """Get the per-guild configuration for a specific guild ID.

    Returns an empty dict for unknown guilds.
    """
    config = load_server_config()
    servers = config.get("servers", {})
    return servers.get(str(guild_id), {})