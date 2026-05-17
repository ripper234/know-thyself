#!/usr/bin/env python3
"""Validate content/weekly-reflection.json against design rules.

Stdlib only. Run from repo root:

    python3 scripts/validate_weekly_reflection.py

Exits non-zero if any rule fails. Intended for CI and local use.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WEEKLY_PATH = REPO_ROOT / "content" / "weekly-reflection.json"
PROMPTS_PATH = REPO_ROOT / "content" / "prompts.json"

EXPECTED_WEEKS = 4
EXPECTED_ANCHORS = [7, 14, 21, 28]
# Punctuation rule: no exclamation marks. Match the tone of the daily prompts.
DISALLOWED_CHARS = ["!"]


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def main() -> int:
    if not WEEKLY_PATH.exists():
        print(f"FAIL: {WEEKLY_PATH} not found", file=sys.stderr)
        return 1

    data = json.loads(WEEKLY_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    if data.get("language") != "he":
        fail(errors, f"language must be 'he', got {data.get('language')!r}")

    weeks = data.get("weeks", [])
    if not isinstance(weeks, list):
        fail(errors, "weeks must be a list")
        weeks = []

    if len(weeks) != EXPECTED_WEEKS:
        fail(errors, f"expected exactly {EXPECTED_WEEKS} weeks, got {len(weeks)}")

    seen_weeks: set[int] = set()
    seen_anchors: set[int] = set()
    for entry in weeks:
        w = entry.get("week")
        a = entry.get("anchor_day")
        t = entry.get("text_he", "")
        n = entry.get("note", "")

        if w in seen_weeks:
            fail(errors, f"duplicate week number: {w}")
        seen_weeks.add(w)

        if a in seen_anchors:
            fail(errors, f"duplicate anchor_day: {a}")
        seen_anchors.add(a)

        if a not in EXPECTED_ANCHORS:
            fail(errors, f"week {w}: anchor_day {a} not in {EXPECTED_ANCHORS}")

        if not isinstance(t, str) or not t.strip():
            fail(errors, f"week {w}: text_he must be a non-empty string")
        else:
            for bad in DISALLOWED_CHARS:
                if bad in t:
                    fail(errors, f"week {w}: text_he contains disallowed char {bad!r}")
            if len(t) > 120:
                fail(errors, f"week {w}: text_he too long ({len(t)} chars); weekly prompts are single lines")

        if not isinstance(n, str) or not n.strip():
            fail(errors, f"week {w}: note must be a non-empty string")

    missing_anchors = set(EXPECTED_ANCHORS) - seen_anchors
    if missing_anchors:
        fail(errors, f"missing weekly entries for anchor days: {sorted(missing_anchors)}")

    # Cross-check against prompts.json if it exists: every anchor_day here must
    # be an anchor_day=true entry there. We do not fail if prompts.json is
    # absent (the two files are merged on separate PR tracks).
    if PROMPTS_PATH.exists():
        try:
            prompts_data = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
            anchor_days_in_prompts = {
                p["day"] for p in prompts_data.get("prompts", [])
                if p.get("anchor_day") is True
            }
            for a in seen_anchors:
                if a not in anchor_days_in_prompts:
                    fail(
                        errors,
                        f"anchor_day {a} not marked anchor_day=true in content/prompts.json",
                    )
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"could not cross-check content/prompts.json: {exc}")

    if errors:
        print("FAIL: weekly-reflection.json validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK: content/weekly-reflection.json valid ({len(weeks)} weeks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
