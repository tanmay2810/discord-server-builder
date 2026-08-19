# Emojies Folder

Place your custom Discord server emojis here!

## Supported Formats
- `.png` (recommended - static images)
- `.jpg` / `.jpeg` (static images)
- `.gif` (animated emojis)

## Size Limits
- Maximum 256 KB per emoji file
- Discord emoji limit depends on your server boost level

## Organization Examples

### Flat Structure (all emojis in this folder)
```
emojies/
├── custom_emoji.png
├── animated_emoji.gif
└── reaction_emoji.jpg
```

### Organized by Category
```
emojies/
├── reactions/
│   ├── like.png
│   ├── love.png
│   └── laugh.gif
├── custom/
│   ├── logo.png
│   └── badge.png
└── animated/
    ├── loading.gif
    └── wave.gif
```

## How It Works
When you run `/setup`, the bot automatically:
1. Scans the `emojies/` folder for all image files
2. Uploads each emoji to your Discord server
3. Names them based on the filename (spaces/dashes converted to underscores)
4. Skips any that already exist

## Example Filenames
- `smile.png` → emoji name: `smile`
- `custom-badge.gif` → emoji name: `custom_badge`
- `my emoji.jpg` → emoji name: `my_emoji`

## Next Steps
1. Add your emoji files to this folder
2. Make sure they're under 256 KB each
3. Run `/setup` in Discord
4. Bot will upload them automatically!
