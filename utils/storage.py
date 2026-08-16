import json
import os

SETTINGS_FILE = "user_settings.json"

DEFAULT_SETTINGS = {
    "current_language": "en",
    "user_mode": "grid",
    "stars": 0
}

def load_settings():
    """Loads user preferences and star count from JSON storage."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return {**DEFAULT_SETTINGS, **json.load(f)}
        except Exception:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(data):
    """Saves user preferences and star count to JSON storage."""
    try:
        current = load_settings()
        current.update(data)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(current, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")