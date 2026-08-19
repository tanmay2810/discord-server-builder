import discord


async def send_onboarding_dm(member: discord.Member):
    embed = discord.Embed(
        title="Welcome to the server!",
        description="Please pick your interests by reacting to the role message in the server.",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Step 1", value="Read the rules.", inline=False)
    embed.add_field(name="Step 2", value="Pick your roles in #💬・general-chat.", inline=False)
    embed.add_field(name="Step 3", value="Introduce yourself in the introductions channel.", inline=False)

    try:
        await member.send(embed=embed)
    except Exception:
        pass
