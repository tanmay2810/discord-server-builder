from config import load_server_config

CONFIG = load_server_config()
TEXT_CHANNELS = CONFIG.get("channels", {}).get("text", {})
VOICE_CHANNELS = CONFIG.get("channels", {}).get("voice", {})
VOICE_LIMITS = CONFIG.get("voice_limits", {})


async def create_channels(guild):
    categories = {category.name: category for category in guild.categories}

    for category_name, channels in TEXT_CHANNELS.items():
        category = categories.get(category_name)
        if category is None:
            continue

        existing_channels = [channel.name for channel in category.channels]

        for channel_name in channels:
            if channel_name not in existing_channels:
                await guild.create_text_channel(channel_name, category=category)
                print(f"✅ Created text channel: {channel_name}")

    for category_name, channels in VOICE_CHANNELS.items():
        category = categories.get(category_name)
        if category is None:
            continue

        existing_channels = [channel.name for channel in category.channels]

        for channel_name in channels:
            if channel_name not in existing_channels:
                limit = VOICE_LIMITS.get(channel_name, 0)
                await guild.create_voice_channel(
                    channel_name,
                    category=category,
                    user_limit=limit,
                    bitrate=guild.bitrate_limit
                )
                print(f"✅ Created voice channel: {channel_name} (Max Quality)")