# Configuration Guide

This guide explains how to customize your server using `server_config.json`.

## Quick Start
1. Copy `server_config.example.json` to `server_config.json`
2. Edit `server_config.json` with your preferred roles, channels, categories
3. Run `/setup` in Discord
4. Bot creates everything based on your configuration

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
    "token_env_var": "DISCORD_TOKEN",      // Env variable name (don't change)
    "guild_name": "My Server",             // Your server display name
    "server_description": "Auto setup bot" // Server description
  }
}
```

### 2. Roles
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
    "levels": [
      "🌌 Level III",  // Highest - full permissions
      "🌙 Level II",   // Mid - some restrictions
      "✨ Level I",    // Low - limited permissions
      "🌸 Member"      // Lowest - auto-assigned on join
    ]
  }
}
```

#### Bot Role (For Your Bot)
```json
{
  "bot_role": "🤖 Bots"  // Role for all bots
}
```

#### Onboarding Roles (Self-Assign)
Members pick one from each category:
```json
{
  "onboarding": {
    "gender": ["♂️ Male", "♀️ Female", "⚪ Prefer not to say"],
    "age": ["🌱 13-16", "🌿 16-18", "🌸 18-20", "🌙 21-23"],
    "interests": ["🎮 Gamer", "🌸 Anime", "🎵 Music", "🎥 Movies"],
    "platforms": ["🖥️ PC", "🎮 PlayStation", "🕹️ Xbox"],
    "colors": ["❤️ Red", "💙 Blue", "💜 Purple"],
    "notifications": ["📢 Announcements", "🎙️ VC Pings"]
  }
}
```

### 3. Categories
Channel groups - appears as folders in Discord:
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

### 4. Channels
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

### 5. Voice Limits
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

### 6. Security Settings
```json
{
  "security": {
    "block_private_threads_for_members": true,    // Prevent member-only threads
    "allow_external_emojis_for_members": true,   // Allow external emoji use
    "allow_external_stickers_for_members": true  // Allow external stickers
  }
}
```

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

---

## Common Tasks

### Add a New Role
1. Open `server_config.json`
2. Add to appropriate section:
   ```json
   "staff": ["👑 Founder", "⚜️ Owner", "🛡️ Admin", "🆕 Supporter"]
   ```
3. Save and run `/setup`

### Add a New Channel
1. Open `server_config.json`
2. Find the category and add the channel:
   ```json
   "💬 community": ["💬・general", "🆕 new-channel", "🌸・introductions"]
   ```
3. Save and run `/setup`

### Add a New Category
1. Open `server_config.json`
2. Add to categories array:
   ```json
   "categories": [
     "📋 logs",
     "🆕 projects",  // NEW
     "💬 community"
   ]
   ```
3. Add channels for it:
   ```json
   "channels": {
     "text": {
       "🆕 projects": ["📋・project-1", "📋・project-2"]
     }
   }
   ```

### Change Role Names/Emojis
1. Edit `server_config.json`
2. Change the role name:
   ```json
   "staff": ["👑 Supreme Leader", "⚜️ Executive"]  // Changed from Owner
   ```
3. Run `/reset` then `/setup` to rebuild with new names

### Set Voice Channel Limits
```json
{
  "voice_limits": {
    "🎮・ranked-5v5": 10,
    "🎙️・streaming": 1,
    "☕・hangout": 0  // unlimited
  }
}
```

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
- Verify JSON syntax is valid (no trailing commas)
- Check channel isn't already created
- Run `/reset` then `/setup`

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

---

For more help, see:
- [QUICK_START.md](QUICK_START.md) — Getting the bot running
- [server_config.example.json](server_config.example.json) — Full template
- [permissions.py](permissions.py) — Permission rules code
