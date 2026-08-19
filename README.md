# Discord Server Builder

A production-ready Discord bot that automates server setup, member onboarding, invite tracking, role assignment, and admin logging.

> 📖 **First time here?** Start with [QUICK_START.md](QUICK_START.md) for a complete step-by-step guide to get the bot running.
> 
> 🎨 **Emoji & Soundboard?** Check [EMOJI_SOUNDBOARD_SETUP.md](EMOJI_SOUNDBOARD_SETUP.md) for setup instructions.

## Core Features
- **Automated Server Setup**: Creates roles, categories, channels with proper permissions
- **Member Onboarding**: Welcome embed + DM onboarding flow
- **Invite Tracking**: Records who invited whom with persistent storage
- **Reaction Roles**: Members can self-assign roles via emoji reactions
- **Admin Logging**: All actions logged to the #📜・logs channel
- **Admin Commands**: Setup, reset, status, and wizard commands
- **Config-Driven**: Customize roles, channels, and permissions via JSON

## Production-ready setup
1. Copy the example environment file and add your bot token.
2. Update your server configuration in [server_config.json](server_config.json).
3. Install dependencies.
4. Run the bot.

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

## Main project files
- [main.py](main.py) — launcher for the bot
- [bot.py](bot.py) — main Discord bot class with event handlers
- [server_builder.py](server_builder.py) — full server setup flow
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
- The `data/` directory contains persistent storage and should not be committed in multi-bot setups.

## Admin commands available
- **/wizard** — shows the setup wizard guide
- **/setup** — creates the configured server structure
- **/reset** — removes generated roles and channels
- **/status** — checks the bot status and server stats

## Data storage
The bot stores invite data and join logs in the `data/` directory:
- `invites.json` — current invite codes and usage count
- `join_log.json` — member join history with invite tracking
