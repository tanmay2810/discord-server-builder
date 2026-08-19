import discord

from config import is_builder_enabled
from admin_logger import AdminLogger

SERVER_CHANNELS = {
    "📜・logs",
    "🎫・open-ticket",
    "👋・welcome",
    "📖・rules",
    "📢・announcements",
    "👋・goodbye",
    "📈・invite-tracker",
    "💬・general-chat",
    "🌸・introductions",
    "🖼️・media",
    "😂・memes",
    "🤖・bot-commands",
    "🎮・gaming-chat",
    "🎮・gaming-vc",
    "🌸・anime-chat",
    "🌸・anime-vc",
    "🎵・music-chat",
    "🎧・music-lounge",
    "🎤・karaoke-room",
    "☕・chill-lounge",
    "🔊・squad-room",
    "👥・duo-room",
    "👥・trio-room",
    "🌙・late-night-talks",
}

# Roles allowed to run administrative commands
ADMIN_ROLE_NAMES = {"👑 Founder", "⚜️ Owner", "🛡️ Admin"}


def _has_admin_permission(interaction: discord.Interaction) -> bool:
    """Check if the user has administrative permission.

    Allows users with Administrator permission or one of the admin roles.
    """
    if interaction.user is None:
        return False

    if isinstance(interaction.user, discord.Member):
        if interaction.user.guild_permissions.administrator:
            return True
        role_names = {role.name for role in interaction.user.roles}
        return bool(role_names & ADMIN_ROLE_NAMES)

    return False


async def safe_server_reset(guild: discord.Guild):
    for channel in list(guild.channels):
        if channel.name in SERVER_CHANNELS:
            try:
                await channel.delete(reason="Reset command")
            except Exception:
                pass

    for role in list(guild.roles):
        if not role.is_default():
            try:
                await role.delete(reason="Reset command")
            except Exception:
                pass


async def register_admin_commands(bot):
    admin_logger = AdminLogger(bot)

    @bot.tree.command(name="wizard", description="Start the setup wizard for this server")
    async def wizard(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Server Setup Wizard",
            description="Use the commands below to configure and manage your server.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="/setup", value="Creates the main server structure.", inline=False)
        embed.add_field(name="/setup-emojis", value="Uploads emojis from the emojies/ folder.", inline=False)
        embed.add_field(name="/status", value="Shows server and bot status.", inline=False)
        embed.add_field(name="/reset", value="Removes generated roles and channels.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="setup", description="Build the Discord server structure")
    async def setup(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        guild = interaction.guild
        guild_id = guild.id

        if not _has_admin_permission(interaction):
            await interaction.response.send_message(
                "❌ You need Administrator permission or an admin role to use this command.",
                ephemeral=True,
            )
            return

        if not is_builder_enabled(guild_id):
            await interaction.response.send_message(
                "❌ The server builder is not enabled for this server. "
                "Ask the bot owner to enable it in server_config.json.",
                ephemeral=True,
            )
            return

        from server_builder import build_server

        await interaction.response.defer(thinking=True)

        try:
            await build_server(guild)
            await admin_logger.log(
                guild,
                "Server setup",
                f"Server structure created by {interaction.user}",
            )
            print(f"[SETUP] Guild={guild.name} ID={guild_id}")
            print(f"[USER] {interaction.user} ID={interaction.user.id}")
            await interaction.followup.send("✅ Server setup completed.")
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ The bot does not have permission to modify this server. "
                "Check that the bot has Manage Roles, Manage Channels, and Manage Emojis permissions.",
                ephemeral=True,
            )
        except discord.HTTPException as e:
            await interaction.followup.send(f"❌ Discord API error: {e}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Setup failed: {e}", ephemeral=True)

    @bot.tree.command(name="setup-emojis", description="Upload emojis from the emojies/ folder to this server")
    async def setup_emojis(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        guild = interaction.guild
        guild_id = guild.id

        if not _has_admin_permission(interaction):
            await interaction.response.send_message(
                "❌ You need Administrator permission or an admin role to use this command.",
                ephemeral=True,
            )
            return

        if not is_builder_enabled(guild_id):
            await interaction.response.send_message(
                "❌ The server builder is not enabled for this server. "
                "Ask the bot owner to enable it in server_config.json.",
                ephemeral=True,
            )
            return

        from emoji_manager import upload_server_emojis

        await interaction.response.defer(thinking=True)

        try:
            results = await upload_server_emojis(guild)
            await admin_logger.log(
                guild,
                "Emoji upload",
                f"Uploaded {results['uploaded']} emojis by {interaction.user}",
            )
            print(f"[EMOJIS] Guild={guild.name} ID={guild_id}")
            print(f"[USER] {interaction.user} ID={interaction.user.id}")
            await interaction.followup.send(
                f"✅ Emoji upload complete. Uploaded: {results['uploaded']}, Failed: {results['failed']}."
            )
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ The bot does not have permission to manage emojis in this server.",
                ephemeral=True,
            )
        except discord.HTTPException as e:
            await interaction.followup.send(f"❌ Discord API error: {e}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Emoji upload failed: {e}", ephemeral=True)

    @bot.tree.command(name="reset", description="Delete generated roles and channels")
    async def reset(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        guild = interaction.guild
        guild_id = guild.id

        if not _has_admin_permission(interaction):
            await interaction.response.send_message(
                "❌ You need Administrator permission or an admin role to use this command.",
                ephemeral=True,
            )
            return

        if not is_builder_enabled(guild_id):
            await interaction.response.send_message(
                "❌ The server builder is not enabled for this server. "
                "Ask the bot owner to enable it in server_config.json.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(thinking=True)

        try:
            await safe_server_reset(guild)
            await admin_logger.log(
                guild,
                "Server reset",
                f"Server structure reset by {interaction.user}",
            )
            print(f"[RESET] Guild={guild.name} ID={guild_id}")
            print(f"[USER] {interaction.user} ID={interaction.user.id}")
            await interaction.followup.send("✅ Server cleanup completed.")
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ The bot does not have permission to modify this server.",
                ephemeral=True,
            )
        except discord.HTTPException as e:
            await interaction.followup.send(f"❌ Discord API error: {e}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Reset failed: {e}", ephemeral=True)

    @bot.tree.command(name="status", description="Show bot status")
    async def status(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        guild = interaction.guild
        guild_id = guild.id

        embed = discord.Embed(
            title="Bot Status",
            description=f"Online in {guild.name}",
            color=discord.Color.green(),
        )
        embed.add_field(name="Guild ID", value=str(guild_id), inline=True)
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(
            name="Builder Enabled",
            value="✅ Yes" if is_builder_enabled(guild_id) else "❌ No",
            inline=True,
        )
        await interaction.response.send_message(embed=embed)