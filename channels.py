from config import load_server_config
from resource_registry import add_owned_channel

CONFIG = load_server_config()
TEXT_CHANNELS = CONFIG.get("channels", {}).get("text", {})
VOICE_CHANNELS = CONFIG.get("channels", {}).get("voice", {})
VOICE_LIMITS = CONFIG.get("voice_limits", {})


async def create_channels(guild):
    guild_id = guild.id
    categories = {category.name: category for category in guild.categories}

    for category_name, channels in TEXT_CHANNELS.items():
        category = categories.get(category_name)
        if category is None:
            continue

        existing_channels = {channel.name: channel for channel in category.channels}

        for channel_name in channels:
            if channel_name not in existing_channels:
                channel = await guild.create_text_channel(channel_name, category=category)
                add_owned_channel(guild_id, channel.id)
                print(f"✅ Created text channel: {channel_name}")
            else:
                # Ownership cannot be proven for pre-existing channels — do not register.
                print(f"⚠️ Text channel already exists, skipping: {channel_name}")

    for category_name, channels in VOICE_CHANNELS.items():
        category = categories.get(category_name)
        if category is None:
            continue

        existing_channels = {channel.name: channel for channel in category.channels}

        for channel_name in channels:
            if channel_name not in existing_channels:
                limit = VOICE_LIMITS.get(channel_name, 0)
                channel = await guild.create_voice_channel(
                    channel_name,
                    category=category,
                    user_limit=limit,
                    bitrate=guild.bitrate_limit
                )
                add_owned_channel(guild_id, channel.id)
                print(f"✅ Created voice channel: {channel_name} (Max Quality)")
            else:
                # Ownership cannot be proven for pre-existing channels — do not register.
                print(f"⚠️ Voice channel already exists, skipping: {channel_name}")