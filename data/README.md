# Data Folder

This folder stores persistent bot data (JSON files). It's created automatically when the bot runs.

## Files Stored Here

### `invites.json`
Stores all Discord server invites and their current usage counts.
- Auto-created on first bot run
- Updated when new invites are created
- Used to track which invite was used by joining members

Example:
```json
{
  "invite_code_1": 5,
  "invite_code_2": 12,
  "invite_code_3": 0
}
```

### `join_log.json`
Logs when members join and which invite they used.
- Records: timestamp, member ID, member name, invite used
- Useful for tracking community growth
- Auto-created on first member join

Example:
```json
[
  {
    "timestamp": "2025-01-15 14:30:45 UTC",
    "member_id": 123456789,
    "member": "Username#1234",
    "invite": "ABC123"
  }
]
```

## Git Configuration
- ⚠️ The `data/` folder is NOT automatically ignored
- If running multiple bot instances, consider adding to `.gitignore`
- For single bot: safe to commit
- For multiple bots: add to `.gitignore` to avoid merge conflicts

To ignore in git:
```bash
echo "data/" >> .gitignore
```

## Manual Management
- **Backup**: Copy the `data/` folder before major updates
- **Reset invites**: Delete `invites.json` to re-scan all server invites
- **Clear logs**: Delete `join_log.json` to start fresh join tracking
- **Restore**: Copy backed up `data/` folder to restore previous state

## Notes
- Files are created automatically - don't manually create them
- JSON format makes them human-readable and easy to analyze
- No database needed - flat files work great for small to medium servers
- Always backup before deleting or modifying these files
