import os

import discord
from dotenv import load_dotenv

from config import load_server_config

load_dotenv()


def get_token() -> str:
    token = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
    if not token:
        raise RuntimeError("No Discord token found. Add DISCORD_TOKEN to your .env file.")
    return token


def ensure_intents() -> discord.Intents:
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.message_content = True
    return intents


async def safe_delete_role(guild: discord.Guild, role_name: str) -> None:
    role = discord.utils.get(guild.roles, name=role_name)
    if role is not None:
        try:
            await role.delete(reason="Cleanup")
        except Exception:
            pass


async def ensure_server_defaults(guild: discord.Guild) -> None:
    config = load_server_config()
    for category_name in config.get("categories", []):
        if not any(category.name == category_name for category in guild.categories):
            await guild.create_category(category_name)


async def ensure_bot_role(guild: discord.Guild, role_name: str = "🤖 Bots") -> None:
    if not discord.utils.get(guild.roles, name=role_name):
        await guild.create_role(name=role_name)


async def set_channel_overwrites(channel: discord.abc.GuildChannel, overwrite_map: dict[str, dict]) -> None:
    for target_name, permissions in overwrite_map.items():
        target = discord.utils.get(channel.guild.roles, name=target_name)
        if target is None:
            continue
        await channel.set_permissions(target, **permissions)
