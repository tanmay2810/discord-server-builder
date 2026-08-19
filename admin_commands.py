import discord

from config import is_builder_enabled
from admin_logger import AdminLogger
from resource_registry import (
    get_owned_role_ids,
    get_owned_channel_ids,
    get_owned_category_ids,
    clear_registry,
)

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


async def safe_server_reset(guild: discord.Guild) -> dict:
    """Delete ONLY resources recorded in the ownership registry for this guild.

    Returns a summary dict of what was deleted.
    """
    guild_id = guild.id

    # Build lookup maps of current guild resources by ID
    current_roles = {role.id: role for role in guild.roles}
    current_channels = {channel.id: channel for channel in guild.channels}
    current_categories = {category.id: category for category in guild.categories}

    # Load owned IDs from the registry
    owned_role_ids = get_owned_role_ids(guild_id)
    owned_channel_ids = get_owned_channel_ids(guild_id)
    owned_category_ids = get_owned_category_ids(guild_id)

    summary = {
        "roles_deleted": 0,
        "channels_deleted": 0,
        "categories_deleted": 0,
        "roles_skipped": 0,
        "channels_skipped": 0,
        "categories_skipped": 0,
    }

    # Delete owned categories first (channels inside them will be deleted too)
    for category_id in owned_category_ids:
        category = current_categories.get(category_id)
        if category is None:
            # Resource no longer exists in this guild — skip
            summary["categories_skipped"] += 1
            continue
        try:
            await category.delete(reason="Eldian Bot reset")
            summary["categories_deleted"] += 1
        except Exception:
            summary["categories_skipped"] += 1

    # Delete owned channels
    for channel_id in owned_channel_ids:
        channel = current_channels.get(channel_id)
        if channel is None:
            summary["channels_skipped"] += 1
            continue
        try:
            await channel.delete(reason="Eldian Bot reset")
            summary["channels_deleted"] += 1
        except Exception:
            summary["channels_skipped"] += 1

    # Delete owned roles (never @everyone — it is never in the registry)
    for role_id in owned_role_ids:
        role = current_roles.get(role_id)
        if role is None or role.is_default():
            summary["roles_skipped"] += 1
            continue
        try:
            await role.delete(reason="Eldian Bot reset")
            summary["roles_deleted"] += 1
        except Exception:
            summary["roles_skipped"] += 1

    # Clear the registry after a successful reset
    clear_registry(guild_id)

    return summary


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
        embed.add_field(name="/reset", value="Removes only Eldian-created roles and channels.", inline=False)
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

    @bot.tree.command(name="reset", description="Delete only Eldian-created roles and channels")
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
            summary = await safe_server_reset(guild)

            total_deleted = (
                summary["roles_deleted"]
                + summary["channels_deleted"]
                + summary["categories_deleted"]
            )

            if total_deleted == 0:
                await interaction.followup.send(
                    "ℹ️ No Eldian-created resources were found for this server. "
                    "Nothing was deleted.",
                    ephemeral=True,
                )
            else:
                await admin_logger.log(
                    guild,
                    "Server reset",
                    f"Deleted {summary['roles_deleted']} roles, "
                    f"{summary['channels_deleted']} channels, "
                    f"{summary['categories_deleted']} categories by {interaction.user}",
                )
                print(f"[RESET] Guild={guild.name} ID={guild_id}")
                print(f"[USER] {interaction.user} ID={interaction.user.id}")
                await interaction.followup.send(
                    f"✅ Reset complete. Deleted: "
                    f"{summary['roles_deleted']} roles, "
                    f"{summary['channels_deleted']} channels, "
                    f"{summary['categories_deleted']} categories. "
                    f"Third-party and manual resources were preserved."
                )
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