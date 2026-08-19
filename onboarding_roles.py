from config import load_server_config

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

    existing_roles = [role.name for role in guild.roles]

    for role_name in roles_to_create:
        if role_name not in existing_roles:
            await guild.create_role(name=role_name)
            print(f"✅ Created role: {role_name}")
        else:
            print(f"⚠️ Role already exists: {role_name}")