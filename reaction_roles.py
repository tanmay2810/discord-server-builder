import discord

REACTION_ROLE_MAP = {
    "🎮": "🎮 Gamer",
    "🌸": "🌸 Anime Lover",
    "🎵": "🎵 Music Lover",
    "🎥": "🎥 Movie Buff",
}


async def setup_reaction_roles(
    guild: discord.Guild,
    channel_name: str,
    role_map: dict[str, str] | None = None,
    message_text: str = "Choose your roles!"
):
    channel = discord.utils.get(guild.text_channels, name=channel_name)
    if channel is None:
        return None

    message = await channel.send(message_text)
    role_map = role_map or REACTION_ROLE_MAP
    for emoji, role_name in role_map.items():
        role = discord.utils.get(guild.roles, name=role_name)
        if role is not None:
            await message.add_reaction(emoji)

    return message


async def handle_reaction_add(bot, payload: discord.RawReactionActionEvent):
    if payload.member is None or payload.member.bot:
        return

    role_name = REACTION_ROLE_MAP.get(str(payload.emoji))
    if role_name is None:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        return

    member = guild.get_member(payload.user_id)
    if member is not None:
        await member.add_roles(role)


async def handle_reaction_remove(bot, payload: discord.RawReactionActionEvent):
    if payload.member is not None and payload.member.bot:
        return

    role_name = REACTION_ROLE_MAP.get(str(payload.emoji))
    if role_name is None:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        return

    member = guild.get_member(payload.user_id)
    if member is not None:
        await member.remove_roles(role)
