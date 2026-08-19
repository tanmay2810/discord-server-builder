from config import load_server_config
from resource_registry import add_owned_category

CONFIG = load_server_config()
CATEGORIES = CONFIG.get("categories", [])


async def create_categories(guild):
    guild_id = guild.id
    existing_categories = {category.name: category for category in guild.categories}

    for category_name in CATEGORIES:
        if category_name not in existing_categories:
            category = await guild.create_category(category_name)
            add_owned_category(guild_id, category.id)
            print(f"✅ Created category: {category_name}")
        else:
            # Ownership cannot be proven for pre-existing categories — do not register.
            print(f"⚠️ Category already exists, skipping: {category_name}")