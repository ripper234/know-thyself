"""Question store. Pulls from a Google Sheet if configured (issue #14),
otherwise falls back to app/seed_questions.json so the bot runs out of the box.

Implements test-specs/question-store.md.
"""
import json
import logging
import os

from config import GOOGLE_SHEET_ID, GOOGLE_SERVICE_ACCOUNT_JSON
import storage

log = logging.getLogger(__name__)

REQUIRED_FIELDS = ("id", "text_he", "tags", "type")
VALID_TAGS = {
    "Identity", "Values", "Emotions", "Fears",
    "Relationships", "Habits", "Meaning", "Patterns",
}
SEED_PATH = os.path.join(os.path.dirname(__file__), "seed_questions.json")


def _normalize(raw: dict):
    """Validate one row. Returns a clean dict or None (skipped)."""
    for field in REQUIRED_FIELDS:
        if raw.get(field) in (None, "", []):
            log.warning("Skipping question, missing %s: %r", field, raw)
            return None
    try:
        qid = int(raw["id"])
    except (TypeError, ValueError):
        log.warning("Skipping question, bad id: %r", raw)
        return None

    tags = raw["tags"]
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    for t in tags:
        if t not in VALID_TAGS:
            log.warning("Question %s has unknown tag %r (kept anyway)", qid, t)

    qtype = str(raw["type"]).strip().lower()
    if qtype not in ("unique", "evergreen"):
        log.warning("Skipping question %s, bad type %r", qid, raw["type"])
        return None

    return {
        "id": qid,
        "text_he": str(raw["text_he"]).strip(),
        "tags": tags,
        "type": qtype,
        "deep_dive_he": str(raw.get("deep_dive_he", "") or "").strip(),
    }


def _load_from_sheet():
    import gspread
    from google.oauth2.service_account import Credentials

    creds_info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1
    return sheet.get_all_records()


def _load_from_seed():
    with open(SEED_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_questions() -> list:
    if GOOGLE_SHEET_ID and GOOGLE_SERVICE_ACCOUNT_JSON:
        try:
            rows = _load_from_sheet()
        except Exception as e:  # fail safe, not loud-to-user
            log.error("Sheet load failed (%s); falling back to seed", e)
            rows = _load_from_seed()
    else:
        rows = _load_from_seed()

    questions = [q for q in (_normalize(r) for r in rows) if q]
    questions.sort(key=lambda q: q["id"])
    return questions


def pick_todays_question(day):
    """Stable selection: if a question is already recorded for `day`, return it.
    Otherwise serve the lowest id not yet served and record it.
    Returns the question dict, or None if the bank is exhausted / unloadable.
    """
    questions = load_questions()
    if not questions:
        log.error("No questions available")
        return None
    by_id = {q["id"]: q for q in questions}

    recorded = storage.get_served_question(day)
    if recorded is not None:
        return by_id.get(recorded)

    served = storage.served_question_ids()
    for q in questions:  # ascending id
        if q["id"] not in served:
            storage.record_served_question(day, q["id"])
            return q

    log.warning("Question bank exhausted; nothing new to serve on %s", day)
    return None
