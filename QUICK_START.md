# Quick Start Guide: Build a Discord Server with This Bot

## Step 1: Prepare Your Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and click "Add Bot"
4. Copy the **TOKEN**
5. Enable these **Intents**:
   - ✅ Server Members Intent
   - ✅ Message Content Intent

## Step 2: Set Up Environment
1. Create a `.env` file in the project folder:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure Your Server
Edit `server_config.json` to customize:
- **Roles**: Staff roles, member levels, onboarding roles
- **Categories**: Logs, Tickets, Community, Gaming, Music, etc.
- **Channels**: Text channels, voice channels, bitrate, user limits
- **Permissions**: Who can see/write/react in each channel
- **Servers**: Which guilds have `builder_enabled = true`

### Enable the Builder for Your Server

Add your Guild ID to the `servers` section:

```json
{
  "servers": {
    "123456789012345678": {
      "builder_enabled": true
    }
  }
}
```

Replace `123456789012345678` with your actual Guild ID (right-click server → Copy Server ID).

> ⚠️ **Unknown guilds default to `builder_enabled = false`.** The bot will never modify a guild that is not explicitly configured.

## Step 4: Set Up Emojis (Optional)
1. Create `emojies/` folder in the project
2. Add `.png`, `.jpg`, or `.gif` files
3. Organize into subfolders if desired:
   ```
   emojies/
   ├── custom_emoji.png
   ├── category/
   │   └── emoji.gif
   ```
4. Use `/setup-emojis` to upload them to the current guild (they are NOT uploaded on startup)

## Step 5: Set Up Soundboard (Optional)
1. Create `soundboard/` folder with `.mp3`, `.wav`, or `.ogg` files
2. Organize by category:
   ```
   soundboard/
   ├── effects/
   │   ├── notification.mp3
   │   └── alert.wav
   ├── music/
   │   └── background.mp3
   ```
3. **Important**: Install FFmpeg on your system:
   - Windows: Download from https://ffmpeg.org
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## Step 6: Invite Bot to Your Server
1. Go to Developer Portal → OAuth2 → URL Generator
2. Select these **Scopes**: `bot`
3. Select these **Permissions**:
   - ✅ Manage Roles
   - ✅ Manage Channels
   - ✅ Manage Emojis and Stickers
   - ✅ Create Instant Invite
   - ✅ Moderate Members
   - ✅ Manage Messages
   - ✅ Embed Links
   - ✅ Attach Files
   - ✅ Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

## Step 7: Run the Bot

```bash
python main.py
```

**Starting the bot does NOT modify any server.**

Expected output:

```
============================================================
🤖 Eldian Bot Online as YourBotName
🌐 Connected to 2 servers
   • Your Server (123456789012345678)
   • Another Server (987654321098765432)
🚀 Eldian Bot is ready.
```

The bot only logs in, connects to its servers, and registers slash commands. **No roles, channels, or permissions are changed on startup.**

## Step 8: Use the Commands

### Setup Commands

All admin commands are **server-specific** — they only affect the guild where you run them.

| Command | Description | Permissions |
|---|---|---|
| `/setup` | Creates the entire server structure in the **current guild** | Administrator or Founder/Owner/Admin role + `builder_enabled` |
| `/setup-emojis` | Uploads emojis from `emojies/` to the **current guild** | Administrator or Founder/Owner/Admin role + `builder_enabled` |
| `/status` | Shows server stats (read-only) | Anyone |
| `/reset` | Deletes **only** Eldian-created resources in the **current guild** | Administrator or Founder/Owner/Admin role + `builder_enabled` |
| `/wizard` | Shows setup guide | Anyone |

> ⚠️ If `builder_enabled` is `false` for the current guild, `/setup`, `/setup-emojis`, and `/reset` are rejected with an ephemeral message and make **no changes**.

### Soundboard Commands (if soundboard/ folder exists)
- **`/sounds`** — List all available sound effects
- **`/play <sound_name>`** — Play a sound in your voice channel
- **`/stop_audio`** — Stop playback

### Member Features
- When members join:
  - 👋 Welcome embed in #welcome channel
  - 📨 DM with onboarding guide (3 steps)
  - 🎯 Automatic invite tracking (logs who invited them)
  - ⭐ Member role assigned
  - 📜 Admin action logged to #logs channel

### Reaction Roles
Members can click emoji reactions to self-assign roles (if configured in `reaction_roles.py`)

## Safe Reset

`/reset` uses an **ownership registry** (`data/registries/<guild_id>.json`) to track which roles, channels, and categories Eldian Bot created.

- `/reset` deletes **only** resources recorded in the registry.
- It will **never** delete `@everyone`, third-party bot roles (Dyno, Wick, Arcane, Sapphire, TicketsBot, etc.), manually created roles, or manually created channels/categories.
- If the registry is missing or empty, `/reset` deletes **nothing**.

## Server Structure Created by `/setup`

### Categories (8 default)
1. **📜 Logs** — Staff-only logging channel
2. **🎫 Tickets** — Support ticket system
3. **ℹ️ Information** — Rules, guides, announcements
4. **👥 Community** — General chat, introductions, memes
5. **🎮 Gaming** — Gaming discussion
6. **📺 Anime** — Anime discussion
7. **🎵 Music** — Music sharing and chat
8. **🎙️ Voice Lounges** — Voice channel category

### Roles
- **Staff**: Owner, Admin, Moderator
- **Levels**: Member (auto), Level II, Level III (features unlock)
- **Onboarding**: Gender, Age, Interests, Platform, Color, Notifications

### Permissions
- Staff see everything, can moderate
- Members can't share links in #general (only in #memes) — this uses permissions and/or AutoMod, not just Embed Links
- Level II gets: emoji reactions, file attachments
- Level III gets: full thread access, link sharing everywhere
- Music channel: embeds and reactions only
- Voice: Level III members can stream/share screen

## Customization Tips

### Add Custom Roles
Edit `server_config.json`:

```json
{
  "roles": {
    "staff": ["👑 Founder", "⚜️ Owner", "🛡️ Admin", "🆕 Supporter"],
    "levels": ["🌌 Level III", "🌙 Level II", "✨ Level I", "🌸 Member"]
  }
}
```

### Add Custom Channels
Edit `server_config.json`:

```json
{
  "channels": {
    "text": {
      "💬 community": ["💬・general-chat", "🌸・introductions", "🆕・art-showcase"]
    },
    "voice": {
      "🎙 voice lounges": ["☕・chill-lounge", "🆕・streaming"]
    }
  }
}
```

### Adjust Voice Channel Limits
Edit `server_config.json`:

```json
{
  "voice_limits": {
    "🔊・squad-room": 5,
    "👥・duo-room": 2,
    "👥・trio-room": 3
  }
}
```

(0 = unlimited)

## Troubleshooting

**Bot doesn't respond to commands**
- Check bot has permissions in the server
- Verify DISCORD_TOKEN in .env is correct
- Restart the bot

**/setup says "builder is not enabled"**
- Open `server_config.json`
- Add your Guild ID to the `servers` section with `"builder_enabled": true`
- Restart the bot

**Emojis not uploading**
- Use `/setup-emojis` in the target guild (emojis are not uploaded on startup)
- Check file size (max 256 KB each)
- Verify format is .png, .jpg, or .gif
- Check bot has "Manage Emojis" permission

**Soundboard not working**
- Make sure FFmpeg is installed (`ffmpeg -version`)
- Verify you're in a voice channel when using `/play`
- Check soundboard/ folder exists with audio files

**Permissions not applying correctly**
- Re-run `/setup`
- Check if roles are positioned correctly (staff roles should be higher)
- Verify bot role is high enough to manage channels

**Members aren't getting welcome message or DM**
- Check #welcome channel exists (or change channel name in config)
- Verify bot has DM permissions
- Check if user has blocked DMs

## Next Steps

1. ✅ Run the bot and execute `/setup` in your enabled guild
2. ✅ Test all commands in a test server first
3. ✅ Customize roles, channels, permissions to your liking
4. ✅ Add custom emojis and soundboard effects
5. ✅ Upload to GitHub for version control
6. ✅ Deploy to your production server

---

## File Reference

Key files you might want to customize:
- `server_config.json` — Server structure, roles, and per-guild builder settings
- `config.py` — Loads configuration
- `bot.py` — Main bot logic and event handlers
- `admin_commands.py` — Command definitions
- `permissions.py` — Channel permission rules
- `emoji_manager.py` — Emoji upload logic
- `soundboard.py` — Soundboard effects
- `resource_registry.py` — Tracks Eldian-created resources for safe `/reset`

For more info, see README.md, EMOJI_SOUNDBOARD_SETUP.md, or ask the bot!