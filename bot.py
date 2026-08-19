import discord
from discord.ext import commands

from admin_commands import register_admin_commands
from admin_logger import AdminLogger
from invite_tracking import handle_member_join
from onboarding_dm import send_onboarding_dm
from reaction_roles import handle_reaction_add, handle_reaction_remove
from server_setup_helpers import ensure_intents, get_token
from welcome_message import send_welcome_message
from soundboard import register_soundboard_commands


class ServerBuilderBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=ensure_intents())
        self.admin_logger = AdminLogger(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print("=" * 60)
        print(f"🤖 Eldian Bot Online as {self.user}")
        print(f"🌐 Connected to {len(self.guilds)} servers")

        for guild in self.guilds:
            print(f"   • {guild.name} ({guild.id})")

        print("🚀 Eldian Bot is ready.")

    async def on_member_join(self, member):
        await send_welcome_message(member)
        await send_onboarding_dm(member)
        await handle_member_join(member)
        await self.admin_logger.log(member.guild, "Member joined", f"{member} joined the server.")

    async def on_raw_reaction_add(self, payload):
        await handle_reaction_add(self, payload)

    async def on_raw_reaction_remove(self, payload):
        await handle_reaction_remove(self, payload)


def run_bot():
    bot = ServerBuilderBot()
    register_admin_commands(bot)
    register_soundboard_commands(bot)
    bot.run(get_token())