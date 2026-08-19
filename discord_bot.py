import discord

from config import load_server_config
from server_setup_helpers import ensure_intents, get_token


class ServerBuilderBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=ensure_intents(), *args, **kwargs)
        self.config = load_server_config()

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        for guild in self.guilds:
            print(f"Connected to {guild.name}")

    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name="👋・welcome")
        if welcome_channel:
            await welcome_channel.send(
                f"Welcome {member.mention} to {member.guild.name}! Please read the rules and choose your roles."
            )

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.lower() == ".setup":
            await self.setup_server(message.guild)

    async def setup_server(self, guild):
        from server_builder import build_server

        await build_server(guild)
        await guild.system_channel.send("Server setup complete.")


if __name__ == "__main__":
    bot = ServerBuilderBot()
    bot.run(get_token())
