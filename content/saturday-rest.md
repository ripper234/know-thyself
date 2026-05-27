# Saturday Rest Content

The README defines Saturday as a non-writing day:

> The website rests or offers a peaceful mini quote on Saturday, no writing task.

This file is the canonical spec for what Saturday actually shows, plus a small seed bank of Hebrew rest-day lines for the first weeks of use.

## Design Intent

Saturday is **not** a prompt. It is a soft pause in the rhythm of the game.

The user should arrive on Saturday and feel:
- this day is different
- nothing is expected of me here
- I can close the tab without guilt

Saturday content should **not**:
- ask a question
- imply reflection homework
- feel like a quote-of-the-day Instagram tile
- be uplifting in a forced way

Saturday content **should**:
- be one short Hebrew line
- be calm, ordinary, grounded
- read like a friend exhaling, not a coach lecturing
- be safe on a low-energy day
- never push the user toward more activity

## Format

Each Saturday line is:
- one sentence
- Hebrew, written natively (not translated)
- 5 to 12 words
- no question mark
- no second-person command ("עצור", "הרגש", "תכתוב")
- no spiritual / guru vocabulary

On Saturday the page should also:
- not show a Finalize button
- not show the writing input
- not break the user's streak (Saturday is excluded from the streak rule)
- optionally show "נחזור מחר" or equivalent next-day cue (final copy lives in `ui_copy.json`)

## Streak Interaction

Saturday is treated as a **rest day**:
- it does not count as a missed day
- it does not count as a submitted day
- the streak continues across Saturday as if the week were six days

This keeps the game honest with the "no writing task" rule and avoids
punishing users for following the spec.

## Rotation

There is no required order. The app may rotate through the lines below
weekly or randomly. The same line repeating once every few weeks is fine
because Saturday is intentionally low-information.

## Seed Lines (Hebrew)

Six lines, enough for the first ~6 weeks of use. More can be added later.

1. **שבת. בלי משימה. בלי שאלה.**

2. **היום אפשר פשוט להיות.**

3. **לפעמים השקט הוא התשובה.**

4. **אין מה לסיים היום. רק להתקיים.**

5. **השבוע היה. עכשיו לא צריך לעשות עם זה כלום.**

6. **נחזור מחר. עכשיו - מנוחה.**

## Review Checklist

Before adding a new Saturday line, ask:
1. Is it a single short Hebrew sentence?
2. Is it free of questions and commands?
3. Does it read calmly, not motivationally?
4. Would it feel okay on a hard day, not just a good one?
5. Does it avoid therapy / guru / Instagram tone?
6. Does it leave the user free to do nothing?

If any answer is no, rework the line.

## Open Items (for later, not blocking)

- Saturday image style (the rest-day image should visually differ from prompt-day images).
- Whether weekly reflection (Friday in Israel) and Saturday rest can ever appear on the same screen, or must be strictly separated.
- Localization: when the game ships in non-Hebrew languages, the rest day may shift (e.g. Sunday) and lines must be re-authored, not translated.
