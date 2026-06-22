"""Weekly AI reflection — a mirror, never an authority.

Implements test-specs/weekly-reflection.md. Output is Hebrew, brief, and must
not advise, judge, praise, score, or rank.
"""
import logging

from anthropic import Anthropic

from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL

log = logging.getLogger(__name__)

SYSTEM = (
    "אתה מראָה, לא סמכות. תפקידך לשקף בעדינות נושאים, רציפות ודפוסים שחוזרים "
    "על פני התשובות של השבוע. בעברית, קצר (3-5 משפטים). "
    "אסור לך לייעץ, לשפוט, לשבח, לדרג, להעריך, או להגיד למשתמש מה לעשות. "
    "אל תשתמש בשפת 'כדאי לך' או 'נסה'. רק שיקוף נוכח ורגוע של מה שכבר נכתב."
)


def generate_weekly_reflection(answers: list) -> str | None:
    """answers: list of {day, question_id, text}. Returns Hebrew text, or None
    if there is nothing to mirror (empty week -> silent, per W2)."""
    if not answers:
        return None
    if not ANTHROPIC_API_KEY:
        log.error("ANTHROPIC_API_KEY missing; cannot generate reflection")
        return None

    joined = "\n\n".join(f"[{a['day']}]\n{a['text']}" for a in answers)
    user = (
        "אלה התשובות שלי מהשבוע האחרון. שקף לי בעדינות נושאים ודפוסים שאתה רואה, "
        "בלי עצות ובלי שיפוט:\n\n" + joined
    )

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=600,
        system=SYSTEM,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in msg.content if block.type == "text").strip()
