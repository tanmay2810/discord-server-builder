import discord

from server_setup_helpers import ensure_intents, get_token


class ServerBuilderBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(intents=ensure_intents(), *args, **kwargs)

    async def on_ready(self):
        print("=" * 60)
        print(f"🤖 Eldian Bot Online as {self.user}")
        print(f"🌐 Connected to {len(self.guilds)} servers")

        for guild in self.guilds:
            print(f"   • {guild.name} ({guild.id})")

        print("🚀 Eldian Bot is ready.")

    async def on_member_join(self, member):
        welcome_channel = discord.utils.get(member.guild.text_channels, name="👋・welcome")
        if welcome_channel:
            await welcome_channel.send(
                f"Welcome {member.mention} to {member.guild.name}! Please read the rules and choose your roles."
            )


if __name__ == "__main__":
    bot = ServerBuilderBot()
    bot.run(get_token())