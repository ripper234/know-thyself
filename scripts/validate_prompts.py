#!/usr/bin/env python3
"""Validate content/prompts.json against design rules.

Stdlib only. Run from repo root:

    python3 scripts/validate_prompts.py           # validate only
    python3 scripts/validate_prompts.py --summary  # validate + day-by-day overview
    python3 scripts/validate_prompts.py --prompts <path>  # validate a specific file

Exits non-zero if any rule fails. Intended for CI and local use.

The --summary mode prints a one-line-per-day review aid so a human reviewer
can scan all 30 prompts (day, category, tags, anchor flag, prompt text)
without reading raw JSON.

The --prompts flag lets tests (scripts/test_validate_prompts.py) point the
validator at a mutated copy of the prompts file without touching the real one.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_PATH = REPO_ROOT / "content" / "prompts.json"

ALLOWED_TAGS = {
    "Identity",
    "Patterns",
    "Emotions",
    "Habits",
    "Values",
    "Relationships",
    "Fears",
    "Meaning",
}
ALLOWED_CATEGORIES = {"unique", "evergreen"}
ANCHOR_DAYS = {7, 14, 21, 28}
NO_FEAR_DAYS_MAX = 15  # Days 1 to 15 must not have Fear tag (trust first).
EXPECTED_DAYS = 30
EXPECTED_SEED_IDS = set(range(1, 31))


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    prompts_path = Path(args.prompts) if args.prompts else PROMPTS_PATH

    if not prompts_path.exists():
        print(f"FAIL: {prompts_path} not found", file=sys.stderr)
        return 1

    data = json.loads(prompts_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if data.get("language") != "he":
        fail(errors, f"language must be 'he', got {data.get('language')!r}")

    prompts = data.get("prompts", [])
    if not isinstance(prompts, list):
        fail(errors, "prompts must be a list")
        prompts = []

    if len(prompts) != EXPECTED_DAYS:
        fail(errors, f"expected {EXPECTED_DAYS} prompts, got {len(prompts)}")

    days_seen: list[int] = []
    seed_ids_seen: list[int] = []

    for idx, p in enumerate(prompts):
        where = f"prompts[{idx}]"

        day = p.get("day")
        if not isinstance(day, int):
            fail(errors, f"{where}.day must be int, got {day!r}")
        else:
            days_seen.append(day)

        seed_id = p.get("seed_id")
        if not isinstance(seed_id, int):
            fail(errors, f"{where}.seed_id must be int, got {seed_id!r}")
        else:
            seed_ids_seen.append(seed_id)

        cat = p.get("category")
        if cat not in ALLOWED_CATEGORIES:
            fail(errors, f"{where}.category must be one of {sorted(ALLOWED_CATEGORIES)}, got {cat!r}")

        tags = p.get("tags")
        if not isinstance(tags, list) or not (1 <= len(tags) <= 2):
            fail(errors, f"{where}.tags must be a 1-2 item list, got {tags!r}")
        else:
            for t in tags:
                if t not in ALLOWED_TAGS:
                    fail(errors, f"{where}.tags contains unknown tag {t!r}")
            if len(set(tags)) != len(tags):
                fail(errors, f"{where}.tags must be unique, got {tags!r}")

        text = p.get("text_he")
        if not isinstance(text, str) or not text.strip():
            fail(errors, f"{where}.text_he must be a non-empty string")

        # Every prompt must carry a one-line design rationale so future edits
        # have to think about placement intent, not just text.
        note = p.get("note")
        if not isinstance(note, str) or not note.strip():
            fail(errors, f"{where}.note must be a non-empty string (one-line design rationale)")

        # Day 1: no Fear/shame.
        if day == 1 and isinstance(tags, list) and "Fears" in tags:
            fail(errors, "Day 1 must not be Fear-tagged (welcome rule).")

        # Days 1 to 15 should avoid Fear-tagged prompts.
        if (
            isinstance(day, int)
            and 1 <= day <= NO_FEAR_DAYS_MAX
            and isinstance(tags, list)
            and "Fears" in tags
        ):
            fail(
                errors,
                f"Day {day} is Fear-tagged but Days 1 to {NO_FEAR_DAYS_MAX} must be Fear-free (trust first).",
            )

        # Anchor days must mark themselves.
        if isinstance(day, int) and day in ANCHOR_DAYS:
            if not p.get("anchor_day"):
                fail(errors, f"Day {day} is an anchor day and must set anchor_day=true.")
        elif p.get("anchor_day"):
            fail(errors, f"Day {day} sets anchor_day=true but is not an anchor day (7,14,21,28).")

    # Sequence coverage: days 1..30, each exactly once.
    if sorted(days_seen) != list(range(1, EXPECTED_DAYS + 1)):
        fail(
            errors,
            f"days must cover 1..{EXPECTED_DAYS} exactly once; got {sorted(days_seen)}",
        )

    # Seed-id coverage: every seed used exactly once.
    if set(seed_ids_seen) != EXPECTED_SEED_IDS:
        missing = EXPECTED_SEED_IDS - set(seed_ids_seen)
        extra = set(seed_ids_seen) - EXPECTED_SEED_IDS
        dup = [s for s in seed_ids_seen if seed_ids_seen.count(s) > 1]
        if missing:
            fail(errors, f"missing seed_ids: {sorted(missing)}")
        if extra:
            fail(errors, f"unexpected seed_ids: {sorted(extra)}")
        if dup:
            fail(errors, f"duplicate seed_ids: {sorted(set(dup))}")

    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    try:
        shown = prompts_path.relative_to(REPO_ROOT)
    except ValueError:
        shown = prompts_path
    print(f"OK: {shown} -- {len(prompts)} prompts, all rules pass.")

    if args.summary:
        print_summary(data, prompts)

    return 0


def print_summary(data: dict, prompts: list[dict]) -> None:
    """Print a day-by-day review aid.

    Format per day: ``DD  cat   anchor?  [Tag1,Tag2]   text_he``

    Ordered by day. Anchor days (7, 14, 21, 28) are marked with a star.
    """
    print()
    print(f"Day-by-day overview  (language={data.get('language')}, version={data.get('version')})")
    print("-" * 78)
    by_day = sorted(prompts, key=lambda p: p.get("day", 0))
    for p in by_day:
        day = p.get("day", "?")
        cat = p.get("category", "?")[:9]
        anchor = " *" if p.get("anchor_day") else "  "
        tags = ",".join(p.get("tags", []))
        text = p.get("text_he", "")
        print(f"  {day:>2}  {cat:<9}{anchor}  [{tags:<25}]  {text}")
    print("-" * 78)
    print("  * = anchor day (paired with weekly reflection)")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--summary",
        action="store_true",
        help="After validation, print a day-by-day overview of all prompts.",
    )
    parser.add_argument(
        "--prompts",
        default=None,
        help=(
            "Path to a prompts JSON file to validate. Defaults to "
            "content/prompts.json relative to the repo root. Used by the test "
            "suite to point at mutated copies."
        ),
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
