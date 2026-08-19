from config import load_server_config
from resource_registry import add_owned_role

CONFIG = load_server_config()
ROLE_GROUPS = CONFIG.get("roles", {}).get("onboarding", {})

GENDER_ROLES = ROLE_GROUPS.get("gender", [])
AGE_ROLES = ROLE_GROUPS.get("age", [])
INTEREST_ROLES = ROLE_GROUPS.get("interests", [])
PLATFORM_ROLES = ROLE_GROUPS.get("platforms", [])
COLOR_ROLES = ROLE_GROUPS.get("colors", [])
NOTIFICATION_ROLES = ROLE_GROUPS.get("notifications", [])


async def create_onboarding_roles(guild):
    roles_to_create = (
        GENDER_ROLES +
        AGE_ROLES +
        INTEREST_ROLES +
        PLATFORM_ROLES +
        COLOR_ROLES +
        NOTIFICATION_ROLES
    )

    guild_id = guild.id
    existing_roles = {role.name: role for role in guild.roles}

    for role_name in roles_to_create:
        if role_name not in existing_roles:
            role = await guild.create_role(name=role_name)
            add_owned_role(guild_id, role.id)
            print(f"✅ Created role: {role_name}")
        else:
            # Ownership cannot be proven for pre-existing roles — do not register.
            print(f"⚠️ Role already exists, skipping: {role_name}")