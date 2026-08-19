import discord


async def send_welcome_message(member: discord.Member):
    channel = discord.utils.get(member.guild.text_channels, name="👋・welcome")
    if channel is None:
        return

    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}!",
        description=f"Hi {member.mention}, please read the rules and choose your roles.",
        color=discord.Color.blurple(),
    )
    await channel.send(embed=embed)
