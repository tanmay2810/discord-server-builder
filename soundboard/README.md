# Soundboard Folder

Place your sound effects and background music here to play in Discord voice channels!

## Supported Formats
- `.mp3` (recommended - widely compatible)
- `.wav` (uncompressed audio)
- `.ogg` (compressed format)

## Requirements
- **FFmpeg must be installed** on your system:
  - **Windows**: Download from https://ffmpeg.org/download.html
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`
- Python package `discord.py[voice]` is already in requirements.txt

## Folder Organization

### Example Structure
```
soundboard/
├── effects/
│   ├── notification.mp3
│   ├── alert.wav
│   ├── ding.mp3
│   └── success.wav
├── music/
│   ├── background.mp3
│   ├── chill-lounge.mp3
│   └── intro.mp3
└── games/
    ├── winning.mp3
    ├── losing.mp3
    └── level-up.wav
```

## How It Works
1. Organize sound files into category folders (effects/, music/, etc.)
2. Each folder becomes a category in the bot
3. Users use `/sounds` to see available effects
4. Users use `/play <sound_name>` to play in their voice channel
5. The sound plays to everyone in the voice channel

## Discord Commands Available
- **`/sounds`** — Lists all available soundboard effects by category
- **`/play <sound_name>`** — Play a sound effect in your voice channel
- **`/stop_audio`** — Stop current audio playback

## Example Usage
1. User is in a voice channel
2. They type `/sounds`
3. Bot shows all available effects from all category folders
4. User types `/play notification`
5. Bot plays `notification.mp3` to everyone in the channel

## Tips
- **Keep files small**: Large files take longer to play
- **Use MP3**: Most compatible format with Discord
- **Name clearly**: Use descriptive names without special characters
- **Test locally**: Make sure audio sounds good before uploading
- **Organize by category**: Makes it easier for users to find sounds

## Next Steps
1. Download or record your sound effects (MP3, WAV, or OGG)
2. Place them in organized folders (effects/, music/, etc.)
3. Ensure FFmpeg is installed on your system
4. Restart the bot
5. Use `/sounds` to see your new effects!

## Troubleshooting
- **Sounds not showing**: Restart the bot and make sure files are in correct folders
- **Play command fails**: Check you're in a voice channel when using `/play`
- **Audio quality issues**: Try MP3 format or re-encode with lower bitrate
- **FFmpeg error**: Make sure FFmpeg is installed and in your system PATH
