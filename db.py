import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

INVITES_FILE = DATA_DIR / "invites.json"
JOIN_LOG_FILE = DATA_DIR / "join_log.json"


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return default


def _write_json(path: Path, data):
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_invite_data():
    return _read_json(INVITES_FILE, {})


def save_invite_data(data):
    _write_json(INVITES_FILE, data)


def load_join_log():
    return _read_json(JOIN_LOG_FILE, [])


def append_join_log(entry):
    entries = load_join_log()
    entries.append(entry)
    _write_json(JOIN_LOG_FILE, entries)
