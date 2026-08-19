import discord

from db import append_join_log, load_invite_data, save_invite_data


async def track_invites(guild: discord.Guild):
    """Save the current invite state for a specific guild.

    This is NOT called automatically on startup. It is available for
    explicit per-guild initialization if needed.
    """
    invites = await guild.invites()
    data = {str(invite.code): invite.uses for invite in invites}
    save_invite_data(data)
    return data


async def handle_member_join(member: discord.Member):
    guild = member.guild
    invites_before = load_invite_data()
    invites_after = {str(invite.code): invite.uses for invite in await guild.invites()}

    used_invite = None
    for code, count in invites_after.items():
        before = invites_before.get(code, 0)
        if count > before:
            used_invite = code
            break

    entry = {
        "user_id": member.id,
        "user_name": str(member),
        "guild_id": guild.id,
        "guild_name": guild.name,
        "invite_code": used_invite,
    }
    append_join_log(entry)

    if used_invite:
        inviter = None
        for invite in await guild.invites():
            if str(invite.code) == used_invite:
                inviter = invite.inviter
                break
        if inviter:
            try:
                role = discord.utils.get(guild.roles, name="🌸 Member")
                if role is not None:
                    await member.add_roles(role)
            except Exception:
                pass

    save_invite_data(invites_after)