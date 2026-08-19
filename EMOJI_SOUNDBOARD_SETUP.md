# Emoji & Soundboard Setup Guide

## Emoji Manager 🎨

### Folder Structure
Place custom emojis in the `emojies/` folder:

```
emojies/
├── custom_emoji1.png
├── custom_emoji2.gif
├── category1/
│   ├── emoji_a.png
│   ├── emoji_b.png
└── category2/
    ├── emoji_c.gif
    └── emoji_d.jpg
```

### Supported Formats
- `.png` - Static images (recommended)
- `.jpg` / `.jpeg` - Static images
- `.gif` - Animated emojis

### Size Limits
- Maximum 256 KB per emoji
- Discord emoji limit depends on server boosting level

### How It Works
- When `/setup` runs, the bot automatically uploads all emojis from the `emojies/` folder
- Emoji names are derived from filenames (spaces and dashes converted to underscores)
- If an emoji already exists, it skips it automatically

### Commands
- **`/wizard`** — Shows emoji upload stats along with other server info
- **`/status`** — Displays total emojis uploaded

---

## Soundboard 🔊

### Folder Structure
Create a `soundboard/` folder with sound effects organized by category:

```
soundboard/
├── effects/
│   ├── notification.mp3
│   ├── alert.wav
│   └── ding.ogg
├── music/
│   ├── background.mp3
│   └── intro.mp3
└── games/
    ├── winning.mp3
    └── losing.mp3
```

### Supported Formats
- `.mp3` - Recommended (wide compatibility)
- `.wav` - Uncompressed audio
- `.ogg` - Compressed format

### Requirements
- FFmpeg must be installed on your system:
  - **Windows**: Download from https://ffmpeg.org/download.html
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg` (or equivalent)

### Commands
- **`/sounds`** — Lists all available sound effects by category
- **`/play <sound>`** — Play a sound effect in your voice channel
- **`/stop_audio`** — Stop current playback

### Usage
1. Create `soundboard/` folder with sound files
2. Join a Discord voice channel
3. Run `/sounds` to see available effects
4. Run `/play <effect_name>` to play it
5. Sound plays to everyone in your voice channel

---

## Installation

After setting up emoji and soundboard folders, reinstall dependencies:

```bash
pip install -r requirements.txt
```

This installs discord.py[voice] which includes FFmpeg support.

---

## Example Directory Tree

```
Discord Server Builder/
├── emojies/
│   ├── custom_emoji.png
│   ├── animated.gif
│   └── emotes/
│       ├── happy.png
│       ├── sad.png
│       └── cool.png
├── soundboard/
│   ├── effects/
│   │   ├── notification.mp3
│   │   └── alert.wav
│   └── music/
│       └── background.mp3
├── bot.py
├── emoji_manager.py
├── soundboard.py
├── main.py
└── ... (other files)
```

---

## Troubleshooting

**Emoji upload fails**: Check file size (max 256 KB) and format (PNG, JPG, GIF only)

**Soundboard not working**: Ensure FFmpeg is installed and in PATH

**Sounds not playing**: Make sure you're in a voice channel when using `/play`

**Permission denied**: Bot needs `Manage Emojis` and `Connect` voice permissions
