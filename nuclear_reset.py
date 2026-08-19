import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"☢️ Logged in as {client.user}")

    for guild in client.guilds:
        print(f"☢️ Nuclear reset on: {guild.name}")

        # Delete scheduled events
        try:
            for event in guild.scheduled_events:
                try:
                    print(f"Deleting event: {event.name}")
                    await event.delete()
                except Exception as e:
                    print(f"Failed event {event.name}: {e}")
        except:
            pass

        # Delete channels (text, voice, categories, forums, stages)
        for channel in guild.channels:
            try:
                print(f"Deleting channel: {channel.name}")
                await channel.delete()
            except Exception as e:
                print(f"Failed channel {channel.name}: {e}")

        # Delete emojis
        for emoji in guild.emojis:
            try:
                print(f"Deleting emoji: {emoji.name}")
                await emoji.delete()
            except Exception as e:
                print(f"Failed emoji {emoji.name}: {e}")

        # Delete stickers
        for sticker in guild.stickers:
            try:
                print(f"Deleting sticker: {sticker.name}")
                await sticker.delete()
            except Exception as e:
                print(f"Failed sticker {sticker.name}: {e}")

        # Delete roles except @everyone
        for role in guild.roles:
            if role.is_default():
                continue

            try:
                print(f"Deleting role: {role.name}")
                await role.delete()
            except Exception as e:
                print(f"Failed role {role.name}: {e}")

    print("☢️ Nuclear reset complete.")
    await client.close()


client.run(TOKEN)