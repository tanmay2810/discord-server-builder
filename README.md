# Discord Server Builder

A production-ready Discord bot that automates server setup, member onboarding, invite tracking, role assignment, and admin logging.

> 📖 **First time here?** Start with [QUICK_START.md](QUICK_START.md) for a complete step-by-step guide to get the bot running.
> 
> 🎨 **Emoji & Soundboard?** Check [EMOJI_SOUNDBOARD_SETUP.md](EMOJI_SOUNDBOARD_SETUP.md) for setup instructions.

## Core Features
- **Automated Server Setup**: Creates roles, categories, channels with proper permissions when you run `/setup`
- **Member Onboarding**: Welcome embed + DM onboarding flow
- **Invite Tracking**: Records who invited whom with persistent storage
- **Reaction Roles**: Members can self-assign roles via emoji reactions
- **Admin Logging**: All actions logged to the #📜・logs channel
- **Admin Commands**: Setup, reset, status, and wizard commands
- **Config-Driven**: Customize roles, channels, and permissions via JSON
- **Safe Reset**: `/reset` only deletes resources that Eldian Bot created (tracked per guild)

## Important: Startup Behavior

```
py main.py
```

**ONLY** starts the bot. It does **NOT**:

- build any server
- reset any server
- create roles or channels
- modify permissions
- upload emojis
- initialize invite tracking
- perform any server-changing operation

The bot comes online, connects to all servers it is installed in, registers slash commands, and reports connected guild count. **No server is modified on startup.**

## Correct Workflow

```
1. Install dependencies
2. Create .env with your bot token
3. Add the target guild to server_config.json with builder_enabled: true
4. Start the bot
5. Bot comes online without changing servers
6. Run /setup inside the desired Discord server
7. /setup modifies ONLY the current guild
```

## Install

```bash
pip install -r requirements.txt
```

## Run the bot

```bash
python main.py
```

## Required environment variable
Create a local .env file with:

```
DISCORD_TOKEN=your_bot_token_here
```

## Per-Server Configuration

The `servers` section of `server_config.json` controls which guilds are allowed to use `/setup` and `/reset`:

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

## Admin Commands

All admin commands are **server-specific** — they operate only on the guild where they are used.

| Command | Description | Permissions Required |
|---|---|---|
| `/setup` | Creates the configured roles, categories, and channels in the current guild | Administrator or Founder/Owner/Admin role + `builder_enabled` |
| `/setup-emojis` | Uploads emojis from `emojies/` folder to the current guild | Administrator or Founder/Owner/Admin role + `builder_enabled` |
| `/reset` | Deletes **only** Eldian-created resources in the current guild | Administrator or Founder/Owner/Admin role + `builder_enabled` |
| `/status` | Shows server stats (read-only) | Anyone |
| `/wizard` | Shows the setup guide | Anyone |

## Safe Reset Ownership

`/reset` uses an ownership registry stored per guild at `data/registries/<guild_id>.json`.

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

## Main project files
- [main.py](main.py) — launcher for the bot
- [bot.py](bot.py) — main Discord bot class with event handlers
- [server_builder.py](server_builder.py) — full server setup flow
- [resource_registry.py](resource_registry.py) — tracks Eldian-created resources per guild for safe reset
- [admin_commands.py](admin_commands.py) — setup, reset, status, wizard commands
- [admin_logger.py](admin_logger.py) — action logging to #logs channel
- [invite_tracking.py](invite_tracking.py) — invite tracking and member join flow
- [onboarding_dm.py](onboarding_dm.py) — welcome DM flow
- [reaction_roles.py](reaction_roles.py) — emoji-to-role mapping
- [welcome_message.py](welcome_message.py) — welcome embed on join
- [db.py](db.py) — persistent data storage (JSON)
- [config.py](config.py) — configuration loader
- [roles.py](roles.py), [categories.py](categories.py), [channels.py](channels.py), [permissions.py](permissions.py), [onboarding_roles.py](onboarding_roles.py) — core server setup modules
- [server_config.json](server_config.json) — live custom server setup
- [server_config.example.json](server_config.example.json) — template structure
- [.gitignore](.gitignore) — ignores private and secret files

## Security notes
- Never commit your .env file or real tokens.
- Keep private media and profile folders out of Git.
- Use the included example config as a safe template.
- `data/registries/` contains runtime per-guild ownership data and is gitignored.

## Link Permissions Note

Discord's `Embed Links` permission controls whether users see rich link previews/embeds. It is **NOT** a general "block URLs" permission. If you need to block or filter URLs entirely, use Discord's AutoMod or an external moderation bot (Dyno, Wick, Sapphire, etc.).

## Data storage
The bot stores invite data and join logs in the `data/` directory:
- `invites.json` — current invite codes and usage count
- `join_log.json` — member join history with invite tracking
- `registries/<guild_id>.json` — per-guild ownership registry for safe `/reset`