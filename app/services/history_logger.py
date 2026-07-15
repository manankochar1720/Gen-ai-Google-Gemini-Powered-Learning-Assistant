import json
import os
from app.config import HISTORY_FILE

def save_history(data: dict):
    """
    Saves a learning session details to history.json.
    """
    history = []

    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except Exception:
            history = []

    history.append(data)

    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"Error saving history: {e}")

def get_history() -> list:
    """
    Retrieves the list of logged learning sessions.
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def get_session_by_timestamp(timestamp: str) -> dict:
    """
    Retrieves a logged learning session by its timestamp.
    """
    history = get_history()
    for item in history:
        if item.get("timestamp") == timestamp:
            return item
    return None
