import discord
from discord.ext import commands

from admin_commands import register_admin_commands
from admin_logger import AdminLogger
from invite_tracking import handle_member_join, track_invites
from onboarding_dm import send_onboarding_dm
from reaction_roles import handle_reaction_add, handle_reaction_remove
from server_builder import build_server
from server_setup_helpers import ensure_intents, get_token
from welcome_message import send_welcome_message
from emoji_manager import upload_server_emojis
from soundboard import register_soundboard_commands


class ServerBuilderBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=ensure_intents())
        self.admin_logger = AdminLogger(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print("=" * 50)
        print(f"🤖 Bot Online as {self.user}")
        print("=" * 50)

        for guild in self.guilds:
            print(f"Connected to {guild.name}")
            await build_server(guild)
            await track_invites(guild)
            
            # Upload emojis from emojies/ folder
            emoji_results = await upload_server_emojis(guild)
            if emoji_results["uploaded"] > 0:
                print(f"📁 Uploaded {emoji_results['uploaded']} emojis")
            
            print("✅ Server Build Completed")

        print("🚀 AI Builder Ready")

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
