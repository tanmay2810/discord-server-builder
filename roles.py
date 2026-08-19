from config import load_server_config

CONFIG = load_server_config()

STAFF_ROLES = CONFIG.get("roles", {}).get("staff", [])
LEVEL_ROLES = CONFIG.get("roles", {}).get("levels", [])
BOT_ROLE = CONFIG.get("roles", {}).get("bot_role", "🤖 Bots")


async def create_roles(guild):
    roles_to_create = STAFF_ROLES + LEVEL_ROLES + [BOT_ROLE]

    existing_roles = [role.name for role in guild.roles]

    for role_name in reversed(roles_to_create):
        if role_name not in existing_roles:
            await guild.create_role(name=role_name)
            print(f"✅ Created role: {role_name}")
        else:
            print(f"⚠️ Role already exists: {role_name}")