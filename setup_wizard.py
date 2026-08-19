import discord


class SetupWizard:
    def __init__(self, bot):
        self.bot = bot

    async def start(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Server setup wizard started. Use the commands below to configure your server.\n"
            "- /setup\n- /status\n- /reset",
            ephemeral=True,
        )
