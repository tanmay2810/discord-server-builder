"""
Resource Registry — Tracks Discord resources created by Eldian Bot per guild.

This module provides a safe ownership mechanism so that /reset only deletes
resources that Eldian Bot itself created. Resources are keyed by Guild ID.

Data is stored in: data/registries/<guild_id>.json
"""

import json
from pathlib import Path

REGISTRY_DIR = Path(__file__).resolve().parent / "data" / "registries"


def _registry_path(guild_id: int) -> Path:
    return REGISTRY_DIR / f"{guild_id}.json"


def _load(guild_id: int) -> dict:
    path = _registry_path(guild_id)
    if not path.exists():
        return {"roles": [], "channels": [], "categories": []}
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            # Ensure all keys exist even if the file is malformed/partial
            return {
                "roles": data.get("roles", []),
                "channels": data.get("channels", []),
                "categories": data.get("categories", []),
            }
    except (json.JSONDecodeError, OSError):
        return {"roles": [], "channels": [], "categories": []}


def _save(guild_id: int, data: dict) -> None:
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    with _registry_path(guild_id).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def add_owned_role(guild_id: int, role_id: int) -> None:
    data = _load(guild_id)
    if role_id not in data["roles"]:
        data["roles"].append(role_id)
        _save(guild_id, data)


def add_owned_channel(guild_id: int, channel_id: int) -> None:
    data = _load(guild_id)
    if channel_id not in data["channels"]:
        data["channels"].append(channel_id)
        _save(guild_id, data)


def add_owned_category(guild_id: int, category_id: int) -> None:
    data = _load(guild_id)
    if category_id not in data["categories"]:
        data["categories"].append(category_id)
        _save(guild_id, data)


def get_owned_role_ids(guild_id: int) -> list[int]:
    return _load(guild_id)["roles"]


def get_owned_channel_ids(guild_id: int) -> list[int]:
    return _load(guild_id)["channels"]


def get_owned_category_ids(guild_id: int) -> list[int]:
    return _load(guild_id)["categories"]


def clear_registry(guild_id: int) -> None:
    """Delete the registry file for a guild after a successful reset."""
    path = _registry_path(guild_id)
    if path.exists():
        try:
            path.unlink()
        except OSError:
            pass