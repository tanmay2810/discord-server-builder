import discord

from categories import create_categories
from channels import create_channels
from onboarding_roles import create_onboarding_roles
from permissions import apply_permissions
from roles import create_roles


async def build_server(guild: discord.Guild) -> None:
    """Run the full automated server-setup flow for a guild."""
    print(f"Building server: {guild.name}")

    await create_roles(guild)
    await create_onboarding_roles(guild)
    await create_categories(guild)
    await create_channels(guild)
    await apply_permissions(guild)

    print(f"✅ Server build complete: {guild.name}")
