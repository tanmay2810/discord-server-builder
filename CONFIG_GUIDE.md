# Configuration Guide

This guide explains how to customize your server using `server_config.json`.

## Quick Start
1. Copy `server_config.example.json` to `server_config.json`
2. Edit `server_config.json` with your preferred roles, channels, categories
3. Add your Guild ID to the `servers` section with `"builder_enabled": true`
4. Run `/setup` in Discord
5. Bot creates everything based on your configuration in the **current guild only**

## File Location
```
discord-server-builder/
├── server_config.json          ← Your custom config (git ignored)
├── server_config.example.json  ← Template (always safe to share)
```

> ⚠️ Never commit `server_config.json` if it has sensitive info. Use the example as template.

---

## Configuration Sections

### 1. Bot Settings

```json
{
  "bot": {
    "token_env_var": "DISCORD_TOKEN",
    "guild_name": "My Server",
    "server_description": "Auto setup bot"
  }
}
```

- `token_env_var` — Environment variable name for the bot token (don't change)
- `guild_name` — Your server display name
- `server_description` — Server description

### 2. Per-Server Configuration

The `servers` section controls which guilds are allowed to use `/setup`, `/reset`, and `/setup-emojis`.

```json
{
  "servers": {
    "123456789012345678": {
      "builder_enabled": true
    }
  }
}
```

- Replace `123456789012345678` with the actual Guild ID (right-click server → Copy Server ID).
- **Unknown guilds default to `builder_enabled = false`** — the bot will never modify them.
- `/setup` in a disabled guild returns an ephemeral rejection and makes **no changes**.

### 3. Roles

Define your server roles with emojis and hierarchy.

#### Staff Roles (Top Priority)

```json
{
  "roles": {
    "staff": [
      "👑 Founder",
      "⚜️ Owner",
      "🛡️ Admin",
      "🔨 Moderator"
    ]
  }
}
```

#### Member Levels (Progression)

```json
{
  "roles": {
    "levels": [
      "🌌 Level III",
      "🌙 Level II",
      "✨ Level I",
      "🌸 Member"
    ]
  }
}
```

- `🌌 Level III` — Highest, full permissions
- `🌙 Level II` — Mid, some restrictions
- `✨ Level I` — Low, limited permissions
- `🌸 Member` — Lowest, auto-assigned on join

#### Bot Role (For Your Bot)

```json
{
  "roles": {
    "bot_role": "🤖 Bots"
  }
}
```

#### Onboarding Roles (Self-Assign)

Members pick one from each category:

```json
{
  "roles": {
    "onboarding": {
      "gender": ["♂️ Male", "♀️ Female", "⚪ Prefer not to say"],
      "age": ["🌱 13-16", "🌿 16-18", "🌸 18-20", "🌙 21-23"],
      "interests": ["🎮 Gamer", "🌸 Anime", "🎵 Music", "🎥 Movies"],
      "platforms": ["🖥️ PC", "🎮 PlayStation", "🕹️ Xbox"],
      "colors": ["❤️ Red", "💙 Blue", "💜 Purple"],
      "notifications": ["📢 Announcements", "🎙️ VC Pings"]
    }
  }
}
```

### 4. Categories

Channel groups — appears as folders in Discord:

```json
{
  "categories": [
    "📋 logs",
    "🎫 tickets",
    "📌 information",
    "💬 community",
    "🎮 gaming",
    "🌸 anime",
    "🎵 music",
    "🎙 voice lounges"
  ]
}
```

### 5. Channels

Organized by category and type.

#### Text Channels

```json
{
  "channels": {
    "text": {
      "📋 logs": ["📜・logs"],
      "💬 community": ["💬・general-chat", "🌸・introductions"],
      "🎮 gaming": ["🎮・gaming-chat"]
    }
  }
}
```

#### Voice Channels

```json
{
  "channels": {
    "voice": {
      "🎙 voice lounges": ["☕・chill-lounge", "🔊・squad-room"],
      "🎮 gaming": ["🎮・gaming-vc"]
    }
  }
}
```

### 6. Voice Limits

Max users per voice channel (0 = unlimited):

```json
{
  "voice_limits": {
    "🔊・squad-room": 5,
    "👥・duo-room": 2,
    "👥・trio-room": 3,
    "☕・chill-lounge": 0
  }
}
```

### 7. Security Settings

```json
{
  "security": {
    "block_private_threads_for_members": true,
    "allow_external_emojis_for_members": true,
    "allow_external_stickers_for_members": true
  }
}
```

- `block_private_threads_for_members` — Prevent member-only threads
- `allow_external_emojis_for_members` — Allow external emoji use
- `allow_external_stickers_for_members` — Allow external stickers

---

## Customization Examples

### Example 1: Small Gaming Server

```json
{
  "roles": {
    "staff": ["👑 Owner", "🛡️ Admin"],
    "levels": ["⭐ Regular", "🌸 Member"],
    "onboarding": {
      "platforms": ["🖥️ PC", "🎮 Console", "📱 Mobile"],
      "interests": ["🎮 Competitive", "🎮 Casual", "🎮 Speedrun"]
    }
  },
  "categories": ["📢 announcements", "🎮 gaming", "🎙 voice"],
  "channels": {
    "text": {
      "📢 announcements": ["📢・announcements"],
      "🎮 gaming": ["🎮・lobby", "🎮・strategies"]
    },
    "voice": {
      "🎙 voice": ["🎮・ranked", "🎮・casual"]
    }
  },
  "voice_limits": {
    "🎮・ranked": 8,
    "🎮・casual": 0
  }
}
```

### Example 2: Study/Education Server

```json
{
  "roles": {
    "staff": ["👨‍🏫 Professor", "🧑‍🏫 TA", "📊 Moderator"],
    "levels": ["📚 Senior", "✏️ Junior", "📖 Freshman"]
  },
  "categories": ["📚 courses", "❓ help", "🎙 study-groups"],
  "channels": {
    "text": {
      "📚 courses": ["📖・calculus", "📖・physics", "📖・chemistry"],
      "❓ help": ["❓・ask-questions", "💡・solutions"]
    },
    "voice": {
      "🎙 study-groups": ["👥・calculus-group", "👥・physics-group"]
    }
  }
}
```

### Example 3: Community Server

```json
{
  "roles": {
    "staff": ["👑 Founder", "⚜️ Admin", "🛡️ Moderator", "💙 Helper"],
    "levels": ["⭐ VIP", "✨ Regular", "🌸 Member"],
    "onboarding": {
      "interests": ["🎮 Gaming", "🎨 Art", "🎵 Music", "📚 Books"],
      "age": ["13-18", "18-25", "25-35", "35+"]
    }
  },
  "categories": ["📌 info", "💬 social", "🎨 creative", "🎮 gaming"],
  "channels": {
    "text": {
      "💬 social": ["💬・introductions", "🖼️・memes", "📸・photos"],
      "🎨 creative": ["🎨・art-share", "✍️・writing"],
      "🎮 gaming": ["🎮・game-chat", "⚔️・esports"]
    }
  }
}
```

---

## Permission System

### Automatic Permission Rules

The bot applies these permissions automatically:

- **Staff roles**: Full access to all channels (except some member-only)
- **Member roles**: Can chat but limited in certain channels
- **#logs channel**: Staff-only (members can only read)
- **#general**: No direct links (only in #memes)
- **Level II+**: Emoji reactions, file attachments
- **Level III**: Full thread access, link sharing
- **Music channel**: Embeds and reactions only
- **Voice channels**: Level III can stream/share screen

See `permissions.py` for the complete permission rules.

### Link Permissions Note

Discord's `Embed Links` permission controls whether users see **rich link previews/embeds**. It is **NOT** a general "block URLs" permission.

- Setting `embed_links = False` prevents link previews from appearing.
- It does **NOT** prevent users from sending URLs in messages.
- If you need to block or filter URLs entirely, use Discord's **AutoMod** or an external moderation bot (Dyno, Wick, Sapphire, etc.).

---

## Common Tasks

### Add a New Role

1. Open `server_config.json`
2. Add to the appropriate section:

```json
{
  "roles": {
    "staff": ["👑 Founder", "⚜️ Owner", "🛡️ Admin", "🆕 Supporter"]
  }
}
```

3. Save and run `/setup`

### Add a New Channel

1. Open `server_config.json`
2. Find the category and add the channel:

```json
{
  "channels": {
    "text": {
      "💬 community": ["💬・general-chat", "🆕・new-channel", "🌸・introductions"]
    }
  }
}
```

3. Save and run `/setup`

### Add a New Category

1. Open `server_config.json`
2. Add to the categories array:

```json
{
  "categories": [
    "📋 logs",
    "🆕 projects",
    "💬 community"
  ]
}
```

3. Add channels for it:

```json
{
  "channels": {
    "text": {
      "🆕 projects": ["📋・project-1", "📋・project-2"]
    }
  }
}
```

### Change Role Names/Emojis

1. Edit `server_config.json`
2. Change the role name:

```json
{
  "roles": {
    "staff": ["👑 Supreme Leader", "⚜️ Executive"]
  }
}
```

3. Run `/reset` then `/setup` to rebuild with new names

### Set Voice Channel Limits

```json
{
  "voice_limits": {
    "🎮・ranked-5v5": 10,
    "🎙️・streaming": 1,
    "☕・hangout": 0
  }
}
```

(0 = unlimited)

---

## Safe Reset Ownership

`/reset` uses an **ownership registry** stored per guild at `data/registries/<guild_id>.json`.

- When `/setup` creates a new role, category, or channel, its Discord ID is recorded in the registry.
- `/reset` deletes **only** resources whose IDs are in the registry.
- **If ownership cannot be proven, the resource is NOT deleted.**

`/reset` will **never** delete:

- `@everyone`
- Third-party bot roles (Dyno, Wick, Arcane, Sapphire, TicketsBot, etc.)
- Manually created roles
- Manually created channels/categories
- Any resource not recorded in the registry

If the registry is missing, empty, or corrupted, `/reset` deletes **nothing**.

---

## Best Practices

1. **Use Emojis**: Makes channels visually organized
2. **Consistent Naming**: Use patterns like `📖・channel-name`
3. **Clear Hierarchy**: Staff > Levels > Onboarding
4. **Starter Setup**: Use `server_config.example.json` as base
5. **Test First**: Run on test server before production
6. **Backup**: Keep a copy of your config before major changes
7. **Version Control**: Use Git to track config changes

---

## Troubleshooting

**Bot didn't create channels I added**
- Verify JSON syntax is valid (no trailing commas, no comments inside JSON)
- Check channel isn't already created
- Run `/reset` then `/setup`

**/setup says "builder is not enabled"**
- Open `server_config.json`
- Add your Guild ID to the `servers` section with `"builder_enabled": true`
- Restart the bot

**Roles aren't applying correctly**
- Make sure roles are higher in the staff list for higher priority
- Check bot role is high enough to manage
- Run `/reset` then `/setup`

**Voice channels have wrong limits**
- Edit `voice_limits` with exact channel name
- Names must match exactly (emojis too)
- Run `/setup` after changes

**Permissions seem wrong**
- Some permissions are automatic (see `permissions.py`)
- Run `/reset` then `/setup` to reapply
- Check member's highest role in hierarchy

**/reset deleted nothing**
- This is expected if the registry is empty or missing
- Run `/setup` first to create and register resources
- Only Eldian-created resources are eligible for deletion

---

For more help, see:
- [QUICK_START.md](QUICK_START.md) — Getting the bot running
- [server_config.example.json](server_config.example.json) — Full template
- [permissions.py](permissions.py) — Permission rules code