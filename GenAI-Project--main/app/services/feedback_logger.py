import json
import os
from app.config import FEEDBACK_FILE

def save_feedback(data: dict):
    """
    Saves student feedback ratings and suggestions to feedback.json.
    """
    feedback_list = []

    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                feedback_list = json.load(f)
        except Exception:
            feedback_list = []

    feedback_list.append(data)

    try:
        with open(FEEDBACK_FILE, "w") as f:
            json.dump(feedback_list, f, indent=4)
    except Exception as e:
        print(f"Error saving feedback: {e}")

def get_feedback() -> list:
    """
    Retrieves all feedback logs.
    """
    if not os.path.exists(FEEDBACK_FILE):
        return []

    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []
