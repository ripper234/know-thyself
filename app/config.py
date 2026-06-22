"""Configuration, loaded from environment. See .env.example."""
import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

# --- required for the bot to function ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")  # the solo user (Ron)

# --- AI weekly reflection ---
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")

# --- question store (optional; falls back to app/seed_questions.json) ---
GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")

# --- scheduling (Asia/Jerusalem, DST-aware) ---
TZ = ZoneInfo("Asia/Jerusalem")
DAILY_DELIVERY_TIME = os.environ.get("DAILY_DELIVERY_TIME", "08:00")  # HH:MM
WEEKLY_REFLECTION_TIME = os.environ.get("WEEKLY_REFLECTION_TIME", "11:00")  # HH:MM, fires Friday

# --- storage ---
# On Railway, mount a volume at /data and this persists. Locally it sits next to the code.
DB_PATH = os.environ.get("DB_PATH", "/data/know_thyself.db")


def parse_hhmm(value: str):
    hh, mm = value.split(":")
    return int(hh), int(mm)
