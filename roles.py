from config import load_server_config
from resource_registry import add_owned_role

CONFIG = load_server_config()

STAFF_ROLES = CONFIG.get("roles", {}).get("staff", [])
LEVEL_ROLES = CONFIG.get("roles", {}).get("levels", [])
BOT_ROLE = CONFIG.get("roles", {}).get("bot_role", "🤖 Bots")


async def create_roles(guild):
    roles_to_create = STAFF_ROLES + LEVEL_ROLES + [BOT_ROLE]
    guild_id = guild.id

    existing_roles = {role.name: role for role in guild.roles}

    for role_name in reversed(roles_to_create):
        if role_name not in existing_roles:
            role = await guild.create_role(name=role_name)
            add_owned_role(guild_id, role.id)
            print(f"✅ Created role: {role_name}")
        else:
            # A role with this name already exists.
            # We do NOT register it as owned because ownership cannot be proven —
            # it may have been created manually or by a third-party bot.
            # /reset will not delete it.
            print(f"⚠️ Role already exists, skipping: {role_name}")
