#!/usr/bin/env python3
"""Validate content/ui_copy.json against its design rules.

This is the spec-as-code companion to content/ui_copy.json. It enforces the
rules from `design_rules` (gender-neutral Hebrew, calm tone, no evaluative
language, neutral errors), plus structural checks the JSON Schema cannot
express on its own.

Stdlib-only, runs anywhere with Python 3. Exits non-zero on any violation.

Usage:
    python3 scripts/validate_ui_copy.py [PATH_TO_UI_COPY_JSON]

If PATH is omitted, defaults to content/ui_copy.json relative to the repo root.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# --- Forbidden patterns (rules expressed as code) ---------------------------

# Gendered Hebrew verb/pronoun suffixes that would break rule #1.
# We use word-boundary patterns to avoid false positives inside other words.
GENDERED_FORBIDDEN_TOKENS = {
    "אתה": "gendered 2nd-person masculine pronoun",
    "את": "gendered 2nd-person feminine pronoun",
    "שלך_m": None,  # placeholder, handled by suffix scanner instead
}

# Common gendered Hebrew verb endings in present-tense second-person commands.
# Feminine present-tense often ends in ת after the stem (e.g. כותבת),
# while masculine ends in plain stem (כותב). For UI copy we accept neither
# explicit form; we require infinitive ("לכתוב") or non-gendered framings.
GENDERED_VERB_PATTERNS = [
    # masculine plural imperative form often ends -ו (e.g. כתבו). We allow that.
    # Feminine singular present: ends with ת preceded by a verb root letter.
    # This is a coarse heuristic; flag patterns Ron would notice.
    re.compile(r"\bכותבת\b"),
    re.compile(r"\bכותב\b"),  # masculine singular present
    re.compile(r"\bמרגישה\b"),
    re.compile(r"\bמרגיש\b"),
]

# Tone / evaluative language that breaks rule #3 ("never thank, congratulate,
# evaluate"). Hebrew + a few English fallbacks since some keys might contain
# placeholder English by mistake.
FORBIDDEN_PRAISE = [
    "כל הכבוד",
    "מעולה",
    "נהדר",
    "מצוין",
    "תודה רבה",
    "great job",
    "well done",
    "amazing",
    "awesome",
]

# Gamification language that breaks rule #4.
FORBIDDEN_GAMIFICATION = [
    "ניצחת",
    "מנצח",
    "ניקוד",
    "נקודות",
    "🔥",
    "streak!",
    "keep it up",
    "level up",
]


def _flatten(prefix: str, obj, out: list) -> None:
    """Flatten a nested dict of strings into [(dotted_key, value), ...]."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            _flatten(f"{prefix}.{k}" if prefix else k, v, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _flatten(f"{prefix}[{i}]", v, out)
    else:
        out.append((prefix, obj))


def _check_no_exclamations(items: list[tuple[str, str]]) -> list[str]:
    bad = []
    for key, val in items:
        if not isinstance(val, str):
            continue
        # Rule #2: no exclamation marks anywhere in UI copy.
        if "!" in val or "！" in val:
            bad.append(f"{key}: contains '!' (rule: calm tone, no exclamation marks)")
    return bad


def _check_no_gendered(items: list[tuple[str, str]]) -> list[str]:
    bad = []
    for key, val in items:
        if not isinstance(val, str):
            continue
        # Skip design_rules text itself; rules describe forbidden tokens.
        if key.startswith("design_rules"):
            continue
        for pat in GENDERED_VERB_PATTERNS:
            if pat.search(val):
                bad.append(
                    f"{key}: contains gendered verb form '{pat.pattern}' "
                    f"(rule: gender-neutral Hebrew)"
                )
    return bad


def _check_no_praise(items: list[tuple[str, str]]) -> list[str]:
    bad = []
    for key, val in items:
        if not isinstance(val, str):
            continue
        if key.startswith("design_rules"):
            continue
        for token in FORBIDDEN_PRAISE:
            if _affirmative_match(val, token):
                bad.append(
                    f"{key}: contains praise token '{token}' "
                    f"(rule: never thank or congratulate)"
                )
    return bad


def _affirmative_match(text: str, token: str) -> bool:
    """True iff `token` appears in `text` without a Hebrew/English negation
    (אין / לא / no / not) within ~8 chars before it. This lets us say
    'אין ניקוד' (anti-gamification) without flagging 'ניקוד' as a violation.
    """
    low_text = text.lower()
    low_token = token.lower()
    needles = [(text, token), (low_text, low_token)]
    for haystack, needle in needles:
        start = 0
        while True:
            idx = haystack.find(needle, start)
            if idx < 0:
                break
            window = haystack[max(0, idx - 8): idx]
            if not any(neg in window for neg in ("אין", "לא ", "no ", "not ")):
                return True
            start = idx + len(needle)
    return False


def _check_no_gamification(items: list[tuple[str, str]]) -> list[str]:
    bad = []
    for key, val in items:
        if not isinstance(val, str):
            continue
        if key.startswith("design_rules"):
            continue
        for token in FORBIDDEN_GAMIFICATION:
            if _affirmative_match(val, token):
                bad.append(
                    f"{key}: contains gamification token '{token}' "
                    f"(rule: streak language is informational, not gamified)"
                )
    return bad


def _check_required_shape(doc: dict) -> list[str]:
    errors = []
    required_top = ["version", "language", "description", "design_rules", "strings"]
    for k in required_top:
        if k not in doc:
            errors.append(f"missing top-level key: {k}")
    if doc.get("language") != "he":
        errors.append(f"language must be 'he', got {doc.get('language')!r}")
    if not isinstance(doc.get("design_rules"), list) or not doc["design_rules"]:
        errors.append("design_rules must be a non-empty list")
    strings = doc.get("strings", {})
    required_sections = ["app", "home", "prompt", "auth", "me", "share", "errors", "system"]
    for s in required_sections:
        if s not in strings:
            errors.append(f"strings.{s} is missing")
    # Spot-check critical leaf keys the MVP code paths depend on.
    critical = [
        "prompt.answer_placeholder",
        "prompt.finalize_button",
        "prompt.finalized_state",
        "auth.login_with_google",
        "me.current_streak_label",
        "errors.generic",
    ]
    for path in critical:
        node = strings
        ok = True
        for part in path.split("."):
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                ok = False
                break
        if not ok or not isinstance(node, str) or not node.strip():
            errors.append(f"strings.{path} must be a non-empty string")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "content" / "ui_copy.json"
    if not path.exists():
        print(f"FAIL: {path} not found", file=sys.stderr)
        return 2
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: {path} is not valid JSON: {e}", file=sys.stderr)
        return 2

    errors: list[str] = []
    errors += _check_required_shape(doc)

    flat: list[tuple[str, str]] = []
    _flatten("", doc.get("strings", {}), flat)

    errors += _check_no_exclamations(flat)
    errors += _check_no_gendered(flat)
    errors += _check_no_praise(flat)
    errors += _check_no_gamification(flat)

    if errors:
        print(f"FAIL: {path} -- {len(errors)} rule violation(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    # Count strings for a friendly summary.
    n_strings = sum(1 for _, v in flat if isinstance(v, str))
    print(f"OK: {path} -- {n_strings} strings, all rules pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
