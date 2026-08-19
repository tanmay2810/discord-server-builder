"""
Emoji Manager — Upload custom emojis from the emojies/ folder to Discord
Automatically categorizes emojis and uploads them to the server on setup
"""

import discord
from pathlib import Path


async def upload_server_emojis(guild: discord.Guild) -> dict:
    """
    Upload all emojis from the emojies/ folder to the Discord server.
    Returns a dict with success/failure counts.
    
    Supported formats: .png, .jpg, .jpeg, .gif (animated)
    Max size: 256 KB per emoji
    """
    emojies_path = Path("emojies")
    
    if not emojies_path.exists():
        print(f"❌ emojies/ folder not found")
        return {"uploaded": 0, "failed": 0, "errors": []}
    
    results = {"uploaded": 0, "failed": 0, "errors": []}
    
    # Get all emoji files (recursively, without duplicates)
    emoji_files = [f for f in emojies_path.rglob("*") if f.is_file() and f.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]]
    
    print(f"📁 Found {len(emoji_files)} emoji files")
    
    for emoji_file in emoji_files:
        try:
            # Read emoji file
            with open(emoji_file, "rb") as f:
                emoji_data = f.read()
            
            # Check file size (Discord limit: 256 KB)
            if len(emoji_data) > 256 * 1024:
                results["failed"] += 1
                results["errors"].append(f"{emoji_file.name}: File too large (>256KB)")
                print(f"⚠️  Skipped {emoji_file.name}: File too large")
                continue
            
            # Create emoji name from filename
            emoji_name = emoji_file.stem.replace("-", "_").replace(" ", "_")[:32]
            
            # Upload emoji
            emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_data)
            results["uploaded"] += 1
            print(f"✅ Uploaded: {emoji_name}")
            
        except discord.errors.HTTPException as e:
            if "already exists" in str(e):
                results["failed"] += 1
                print(f"⚠️  Skipped {emoji_file.name}: Already exists")
            else:
                results["failed"] += 1
                results["errors"].append(f"{emoji_file.name}: {str(e)}")
                print(f"❌ Failed {emoji_file.name}: {str(e)}")
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"{emoji_file.name}: {str(e)}")
            print(f"❌ Error uploading {emoji_file.name}: {str(e)}")
    
    return results


async def get_emoji_list(guild: discord.Guild) -> list:
    """Get all custom emojis in the server"""
    return guild.emojis


async def emoji_stats(guild: discord.Guild) -> dict:
    """Get emoji usage statistics"""
    emojis = await get_emoji_list(guild)
    return {
        "total": len(emojis),
        "animated": sum(1 for e in emojis if e.animated),
        "static": sum(1 for e in emojis if not e.animated),
        "limit": guild.emoji_limit
    }


async def list_emojis(guild: discord.Guild) -> str:
    """Generate a formatted list of all server emojis"""
    emojis = await get_emoji_list(guild)
    
    if not emojis:
        return "No custom emojis in this server."
    
    emoji_list = []
    for emoji in emojis:
        emoji_type = "🎬 Animated" if emoji.animated else "📸 Static"
        emoji_list.append(f"{emoji} — `{emoji.name}` ({emoji_type})")
    
    return "\n".join(emoji_list)