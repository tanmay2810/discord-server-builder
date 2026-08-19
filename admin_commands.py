import discord

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
    @bot.tree.command(name="wizard", description="Start the setup wizard for this server")
    async def wizard(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Server Setup Wizard",
            description="Use the commands below to configure and manage your server.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="/setup", value="Creates the main server structure.", inline=False)
        embed.add_field(name="/status", value="Shows server and bot status.", inline=False)
        embed.add_field(name="/reset", value="Removes generated roles and channels.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="setup", description="Build the Discord server structure")
    async def setup(interaction: discord.Interaction):
        from server_builder import build_server

        if interaction.guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        await build_server(interaction.guild)
        await interaction.followup.send("Server setup completed.")

    @bot.tree.command(name="reset", description="Delete generated roles and channels")
    async def reset(interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)
        await safe_server_reset(guild)
        await interaction.followup.send("Server cleanup completed.")

    @bot.tree.command(name="status", description="Show bot status")
    async def status(interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command must be used inside a server.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Bot Status",
            description=f"Online in {guild.name}",
            color=discord.Color.green(),
        )
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        await interaction.response.send_message(embed=embed)
