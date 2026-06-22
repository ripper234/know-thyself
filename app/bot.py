"""know-thyself Telegram bot (solo MVP).

Two scheduled flows + interaction:
  - daily:  deliver today's question at DAILY_DELIVERY_TIME
  - weekly: Friday at WEEKLY_REFLECTION_TIME, send a private AI mirror of the week
  - replies are stored as the day's answer and mark presence ("Finalize")

See test-specs/ for the behavioral contract.
"""
import logging
from datetime import time

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import questions
import reflection
import storage
from config import (
    DAILY_DELIVERY_TIME,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TZ,
    WEEKLY_REFLECTION_TIME,
    parse_hhmm,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s"
)
log = logging.getLogger("know-thyself")

FALLBACK_HINT = "אין לך מה לכתוב היום? הקלד /skip ופשוט כתוב מה שנוכח כרגע."


def _is_owner(update: Update) -> bool:
    """Solo MVP: only the configured user is served."""
    if not TELEGRAM_CHAT_ID:
        return True  # unset => accept (local testing)
    return str(update.effective_chat.id) == str(TELEGRAM_CHAT_ID)


def _format_question(q: dict) -> str:
    text = q["text_he"]
    if q.get("deep_dive_he"):
        text += f"\n\n<i>צלילה עמוקה (לא חובה):</i> {q['deep_dive_he']}"
    return text


async def deliver_question(chat_id, context: ContextTypes.DEFAULT_TYPE):
    day = storage.today()
    if storage.get_served_question(day) is not None:
        return  # already delivered today (daily-flow.md D2)
    q = questions.pick_todays_question(day)
    if q is None:
        log.warning("No question to deliver on %s", day)
        return
    await context.bot.send_message(
        chat_id=chat_id, text=_format_question(q), parse_mode=ParseMode.HTML
    )
    await context.bot.send_message(chat_id=chat_id, text=FALLBACK_HINT)


# --- scheduled jobs ---

async def daily_job(context: ContextTypes.DEFAULT_TYPE):
    await deliver_question(TELEGRAM_CHAT_ID, context)


async def weekly_job(context: ContextTypes.DEFAULT_TYPE):
    # Gate on weekday here (robust against run_daily day-index ambiguity).
    from datetime import datetime

    now = datetime.now(TZ)
    if now.weekday() != 4:  # Monday=0 ... Friday=4
        return
    end = storage.today()
    start = end.fromordinal(end.toordinal() - 6)  # 7-day inclusive window
    answers = storage.answers_in_range(start, end)
    text = reflection.generate_weekly_reflection(answers)
    if not text:
        log.info("Empty week or no reflection; staying silent")
        return
    storage.save_reflection(end, text)
    header = "🪞 השתקפות שבועית (פרטית):\n\n"
    await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=header + text)


# --- handlers ---

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    await update.message.reply_text(
        "ברוך הבא למשחק הכתיבה היומי. כל יום תקבל שאלה אחת. "
        "ענה עליה כדי לסמן נוכחות. אין נקודות, אין מנצחים. /question לשאלה של היום, "
        "/stats לרצף שלך."
    )
    await deliver_question(update.effective_chat.id, context)


async def cmd_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    day = storage.today()
    qid = storage.get_served_question(day)
    if qid is None:
        await deliver_question(update.effective_chat.id, context)
        return
    q = questions.pick_todays_question(day)
    await update.message.reply_text(_format_question(q), parse_mode=ParseMode.HTML)


async def cmd_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    await update.message.reply_text(
        "אם השאלה של היום לא מציתה כלום — עצור וכתוב מה שנוכח כרגע. "
        "בלי מבנה, בלי הופעה. רק הרגע. (זה נחשב נוכחות מלאה.)"
    )


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    streak, total = storage.compute_streak_and_total(storage.today())
    await update.message.reply_text(
        f"רצף נוכחי: {streak} ימים\nסך הכל ימים: {total}"
    )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    day = storage.today()
    qid = storage.get_served_question(day)
    if qid is None:
        # No question recorded yet today; record one so the answer attaches to it.
        q = questions.pick_todays_question(day)
        qid = q["id"] if q else None
    storage.add_answer(day, qid, update.message.text)
    streak, total = storage.compute_streak_and_total(day)
    await update.message.reply_text(
        f"נשמר. נוכחות נרשמה. 🌱  רצף: {streak} | סך הכל: {total}"
    )


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")
    storage.init_db()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("question", cmd_question))
    app.add_handler(CommandHandler("skip", cmd_skip))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    dh, dm = parse_hhmm(DAILY_DELIVERY_TIME)
    wh, wm = parse_hhmm(WEEKLY_REFLECTION_TIME)
    jq = app.job_queue
    jq.run_daily(daily_job, time=time(hour=dh, minute=dm, tzinfo=TZ))
    # Runs every day at the weekly time; weekly_job no-ops unless it's Friday.
    jq.run_daily(weekly_job, time=time(hour=wh, minute=wm, tzinfo=TZ))

    log.info("know-thyself bot starting (polling)")
    app.run_polling()


if __name__ == "__main__":
    main()
