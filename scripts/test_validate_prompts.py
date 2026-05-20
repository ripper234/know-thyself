#!/usr/bin/env python3
"""Tests for scripts/validate_prompts.py.

Stdlib only. Run from repo root:

    python3 scripts/test_validate_prompts.py

Exits non-zero if any test fails.

Each test mutates a deep copy of the real content/prompts.json into a known
invalid state, writes it to a temp file, and confirms that the validator
catches that specific violation. This locks the executable design rules
against silent regression: if anyone weakens validate_prompts.py, at least
one negative test should start failing.

Positive sanity check: the unmodified content/prompts.json must validate.

This intentionally exercises the validator through its public entry point
(``main``) with ``--prompts <path>`` so we exercise the same code path that
CI and humans use, not an internal helper API.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_PATH = REPO_ROOT / "content" / "prompts.json"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import validate_prompts  # noqa: E402


def load_canonical() -> dict[str, Any]:
    return json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))


def run_validator(data: dict[str, Any]) -> int:
    """Write data to a temp file and run the validator's main() against it.

    Returns the validator's exit code (0 = pass, non-zero = fail).
    The validator's own stdout/stderr output is suppressed; the test runner
    prints its own one-line-per-case verdict instead.
    """
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as fh:
        json.dump(data, fh, ensure_ascii=False)
        tmp_path = fh.name
    try:
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            return validate_prompts.main(["--prompts", tmp_path])
    finally:
        Path(tmp_path).unlink(missing_ok=True)


# ---------- Test cases ----------

Mutator = Callable[[dict[str, Any]], None]


def case_positive_baseline() -> tuple[Mutator, bool, str]:
    """The unmodified canonical file must pass."""

    def mutate(_d: dict[str, Any]) -> None:
        pass

    return mutate, True, "canonical content/prompts.json validates"


def case_language_not_he() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        d["language"] = "en"

    return mutate, False, "non-Hebrew language is rejected"


def case_missing_day() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        d["prompts"] = [p for p in d["prompts"] if p["day"] != 17]

    return mutate, False, "missing a day in 1..30 is rejected"


def case_duplicate_day() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        # Duplicate day 5 onto day 17 (also leaves day 17 missing).
        for p in d["prompts"]:
            if p["day"] == 17:
                p["day"] = 5
                break

    return mutate, False, "duplicate day numbers are rejected"


def case_duplicate_seed_id() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        # Take the seed_id of day 1 and stamp it onto day 30.
        first = d["prompts"][0]["seed_id"]
        for p in d["prompts"]:
            if p["day"] == 30:
                p["seed_id"] = first
                break

    return mutate, False, "duplicate seed_ids are rejected"


def case_day1_fear() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        for p in d["prompts"]:
            if p["day"] == 1:
                p["tags"] = ["Fears"]
                break

    return mutate, False, "Day 1 cannot be Fear-tagged"


def case_early_fear() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        # Day 10 is inside the trust window (1..15) and must not be Fear-tagged.
        for p in d["prompts"]:
            if p["day"] == 10:
                p["tags"] = ["Fears", "Identity"]
                break

    return mutate, False, "Fear tag inside trust window (days 1..15) is rejected"


def case_unknown_tag() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        for p in d["prompts"]:
            if p["day"] == 12:
                p["tags"] = ["Mystery"]  # not in ALLOWED_TAGS
                break

    return mutate, False, "tags outside the agreed vocabulary are rejected"


def case_unknown_category() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        for p in d["prompts"]:
            if p["day"] == 12:
                p["category"] = "exotic"  # not in ALLOWED_CATEGORIES
                break

    return mutate, False, "category outside the agreed vocabulary is rejected"


def case_too_many_tags() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        for p in d["prompts"]:
            if p["day"] == 6:
                p["tags"] = ["Identity", "Values", "Meaning"]
                break

    return mutate, False, "prompts with more than 2 tags are rejected"


def case_empty_text() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        for p in d["prompts"]:
            if p["day"] == 4:
                p["text_he"] = "   "
                break

    return mutate, False, "blank text_he is rejected"


def case_missing_note() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        for p in d["prompts"]:
            if p["day"] == 2:
                p.pop("note", None)
                break

    return mutate, False, "missing design-rationale note is rejected"


def case_anchor_day_unmarked() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        # Day 14 is an anchor day; clear the flag.
        for p in d["prompts"]:
            if p["day"] == 14:
                p["anchor_day"] = False
                break

    return mutate, False, "anchor day 14 without anchor_day=true is rejected"


def case_non_anchor_day_marked() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        # Day 13 is NOT an anchor day; mark it.
        for p in d["prompts"]:
            if p["day"] == 13:
                p["anchor_day"] = True
                break

    return mutate, False, "non-anchor day with anchor_day=true is rejected"


def case_wrong_prompt_count() -> tuple[Mutator, bool, str]:
    def mutate(d: dict[str, Any]) -> None:
        d["prompts"] = d["prompts"][:29]

    return mutate, False, "fewer than 30 prompts is rejected"


# ---------- Test runner ----------

CASES: list[Callable[[], tuple[Mutator, bool, str]]] = [
    case_positive_baseline,
    case_language_not_he,
    case_missing_day,
    case_duplicate_day,
    case_duplicate_seed_id,
    case_day1_fear,
    case_early_fear,
    case_unknown_tag,
    case_unknown_category,
    case_too_many_tags,
    case_empty_text,
    case_missing_note,
    case_anchor_day_unmarked,
    case_non_anchor_day_marked,
    case_wrong_prompt_count,
]


def main() -> int:
    canonical = load_canonical()
    passed = 0
    failed: list[str] = []

    for case in CASES:
        mutate, should_pass, label = case()
        data = copy.deepcopy(canonical)
        mutate(data)
        rc = run_validator(data)
        actually_passed = rc == 0
        if actually_passed == should_pass:
            passed += 1
            print(f"  ok    {label}")
        else:
            failed.append(label)
            verdict = "passed" if actually_passed else "failed"
            expected = "pass" if should_pass else "fail"
            print(
                f"  FAIL  {label}  (validator {verdict}, expected to {expected})",
                file=sys.stderr,
            )

    total = len(CASES)
    print(f"\n{passed}/{total} tests passed.")
    if failed:
        print("Failed tests:")
        for label in failed:
            print(f"  - {label}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
