# Test-Spec: Presence, Streak & Total Days

Presence is the only metric (spec: "The metric is presence"). Everything here is computed from the set of **present days**.

## Definitions

- A day is **present** if the user finalized on that day — i.e. produced at least one reply or fallback free-write (see [daily-flow.md](daily-flow.md)). Drafting/reading do not count.
- **`total_days`** = count of distinct present days.
- **`current_streak`** = length of the maximal run of consecutive present days, evaluated relative to *today*:
  - if **today** is present → run length ending today;
  - else if **yesterday** is present → run length ending yesterday (the streak is still alive; today isn't over);
  - else → `0`.

Consecutive means no gap of a full calendar day (`Asia/Jerusalem`) between present days.

## Criteria

- A second reply on an already-present day does not increase `total_days` or `current_streak`.
- A single missed day breaks the streak; returning starts a new run (this is the MVP's "missed a day and returned" case — it must compute correctly, not error).
- `total_days` never decreases.

## Golden examples

Let present-day sets be listed by weekday within one week. "today" is given per row.

| # | Present days | today | `current_streak` | `total_days` |
|---|---|---|---|---|
| S1 | Mon, Tue, Thu | Thu | 1 | 3 |
| S2 | Mon, Tue, Wed | Wed | 3 | 3 |
| S3 | Mon, Tue, Wed | Thu (not yet present) | 3 | 3 |
| S4 | Mon, Tue, Wed | Fri (Thu & Fri missed) | 0 | 3 |
| S5 | Mon, Tue, Thu, Fri | Fri | 2 | 4 |
| S6 | (none) | Mon | 0 | 0 |
| S7 | Mon (replied twice Mon) | Mon | 1 | 1 |

- **S1** = the canonical golden example from SPEC-DRIVEN.md: Wed gap → streak resets to just Thu.
- **S5** = "missed Wed, returned Thu": the live run is Thu→Fri = 2; total still counts all four.
- **S3** vs **S4** = the grace rule: streak stays alive the day after a present day, dies once a full day is missed.
