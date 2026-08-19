from config import load_server_config

CONFIG = load_server_config()
CATEGORIES = CONFIG.get("categories", [])


async def create_categories(guild):
    existing_categories = [category.name for category in guild.categories]

    for category_name in CATEGORIES:
        if category_name not in existing_categories:
            await guild.create_category(category_name)
            print(f"✅ Created category: {category_name}")
        else:
            print(f"⚠️ Category already exists: {category_name}")