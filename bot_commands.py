import discord
from discord.ext import commands

from config import load_server_config
from server_builder import build_server


def create_bot_commands(bot: commands.Bot):
    @bot.command(name="setup")
    async def setup(ctx):
        await ctx.send("Setting up the server...")
        await build_server(ctx.guild)
        await ctx.send("Server setup complete.")

    @bot.command(name="reset")
    async def reset(ctx):
        guild = ctx.guild
        if guild is None:
            return

        for channel in list(guild.channels):
            if channel.name in {"📜・logs", "🎫・open-ticket", "👋・welcome", "📖・rules", "📢・announcements", "👋・goodbye", "📈・invite-tracker", "💬・general-chat", "🌸・introductions", "🖼️・media", "😂・memes", "🤖・bot-commands", "🎮・gaming-chat", "🎮・gaming-vc", "🌸・anime-chat", "🌸・anime-vc", "🎵・music-chat", "🎧・music-lounge", "🎤・karaoke-room", "☕・chill-lounge", "🔊・squad-room", "👥・duo-room", "👥・trio-room", "🌙・late-night-talks"}:
                try:
                    await channel.delete(reason="Reset command")
                except Exception:
                    pass

        for role in list(guild.roles):
            if role.name != "@everyone":
                try:
                    await role.delete(reason="Reset command")
                except Exception:
                    pass

        await ctx.send("Server cleanup complete.")
