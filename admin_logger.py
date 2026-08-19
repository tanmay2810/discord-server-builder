import discord
from datetime import datetime


class AdminLogger:
    def __init__(self, bot):
        self.bot = bot

    async def log(self, guild: discord.Guild, action: str, details: str):
        log_channel = discord.utils.get(guild.text_channels, name="📜・logs")
        if log_channel is None:
            return

        message = (
            f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC] "
            f"{action}: {details} "
            f"(Guild: {guild.name} ID: {guild.id})"
        )
        await log_channel.send(message)