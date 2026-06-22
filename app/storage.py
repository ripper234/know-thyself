"""SQLite storage. The answers are sacred — they live only here, never in the Sheet.

Implements the contract in test-specs/presence-and-streak.md and question-store.md.
"""
import os
import sqlite3
from datetime import date, datetime, timedelta

from config import DB_PATH, TZ


def _connect():
    # Ensure the parent dir exists (e.g. Railway volume /data, or local cwd).
    parent = os.path.dirname(DB_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS answers (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                day          TEXT NOT NULL,          -- ISO date, Asia/Jerusalem
                question_id  INTEGER,
                text         TEXT NOT NULL,
                finalized_at TEXT NOT NULL           -- ISO datetime of first reply that day
            );
            CREATE TABLE IF NOT EXISTS daily_log (
                day          TEXT PRIMARY KEY,        -- ISO date
                question_id  INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reflections (
                week_ending  TEXT PRIMARY KEY,        -- ISO date (the Friday)
                text         TEXT NOT NULL,
                created_at   TEXT NOT NULL
            );
            """
        )


def today() -> date:
    return datetime.now(TZ).date()


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


# --- question-of-the-day mapping (question-store.md) ---

def get_served_question(day: date):
    with _connect() as conn:
        row = conn.execute(
            "SELECT question_id FROM daily_log WHERE day = ?", (day.isoformat(),)
        ).fetchone()
        return row["question_id"] if row else None


def record_served_question(day: date, question_id: int):
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO daily_log (day, question_id) VALUES (?, ?)",
            (day.isoformat(), question_id),
        )


def served_question_ids() -> set:
    with _connect() as conn:
        rows = conn.execute("SELECT question_id FROM daily_log").fetchall()
        return {r["question_id"] for r in rows}


# --- answers / presence (daily-flow.md, presence-and-streak.md) ---

def add_answer(day: date, question_id, text: str):
    """First reply of the day finalizes; later replies append (daily-flow.md D3)."""
    with _connect() as conn:
        existing = conn.execute(
            "SELECT id, text FROM answers WHERE day = ?", (day.isoformat(),)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE answers SET text = ? WHERE id = ?",
                (existing["text"] + "\n" + text, existing["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO answers (day, question_id, text, finalized_at) VALUES (?, ?, ?, ?)",
                (day.isoformat(), question_id, text, now_iso()),
            )


def present_days() -> list:
    with _connect() as conn:
        rows = conn.execute("SELECT DISTINCT day FROM answers ORDER BY day").fetchall()
        return [date.fromisoformat(r["day"]) for r in rows]


def answers_in_range(start: date, end: date) -> list:
    """Inclusive [start, end]."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT day, question_id, text FROM answers WHERE day BETWEEN ? AND ? ORDER BY day",
            (start.isoformat(), end.isoformat()),
        ).fetchall()
        return [dict(r) for r in rows]


def compute_streak_and_total(ref: date):
    """current_streak + total_days per presence-and-streak.md.

    Streak counts the maximal run of consecutive present days ending at `ref`
    if ref is present, else ending at ref-1 day (grace), else 0.
    """
    days = set(present_days())
    total = len(days)

    if ref in days:
        anchor = ref
    elif (ref - timedelta(days=1)) in days:
        anchor = ref - timedelta(days=1)
    else:
        return 0, total

    streak = 0
    cursor = anchor
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak, total


# --- reflections (weekly-reflection.md) ---

def save_reflection(week_ending: date, text: str):
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO reflections (week_ending, text, created_at) VALUES (?, ?, ?)",
            (week_ending.isoformat(), text, now_iso()),
        )
