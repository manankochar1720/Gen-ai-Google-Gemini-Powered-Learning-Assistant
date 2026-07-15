import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Server Configuration
HOST = os.getenv("API_HOST", "127.0.0.1")
PORT = int(os.getenv("API_PORT", "8000"))

# Log Storage Paths
HISTORY_FILE = "history.json"
FEEDBACK_FILE = "feedback.json"
