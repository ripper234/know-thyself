# 30-Day Prompt Sequence (v1)

Defines the order in which the 30 Hebrew seed prompts from
[prompts-hebrew-seed-bank-v1.md](prompts-hebrew-seed-bank-v1.md) are served
across a user's first 30 days.

Until now, the seed bank file numbered prompts 1 to 30 by category
(unique first, evergreen last). That ordering is a **catalog**, not a
**sequence**. This document defines the **daily sequence**: which prompt is
Day 1, Day 2, ... Day 30.

## Why sequencing matters

The seed bank is the user's first month with the game. The order shapes the
experience:

- **Day 1** is the user's first contact. It should be inviting, not heavy.
- **Days 2 to 6** establish the rhythm. Variety of tone and tag.
- **Day 7** lands on the first weekly reflection. Pair it with a prompt
  that pairs well with a weekly look back.
- **Day 30** closes the first cycle. Use a "what changed?" prompt that
  rewards continuity.
- Heavier prompts (fears, jealousy, control) are spaced apart so no two
  hard days fall back to back.

## Design rules

1. **Day 1 is light and welcoming.** No fear or shame on the first day.
2. **Adjacent days vary by primary tag** when possible (Identity, Patterns,
   Habits, Values, etc.) so the texture does not flatten.
3. **The first half of the month (Days 1 to 15) avoids Fear-tagged
   prompts.** The user is still building the habit and trust in the game.
4. **The last week (Days 23 to 30) is the intentional descent.** Fear and
   identity-edge prompts cluster here, on purpose. By Day 23 the user has
   shown up enough times to handle harder questions.
5. **Evergreen prompts are interleaved**, not bunched at the end. They
   re-anchor the user on core questions across the month.
6. **Day 7, 14, 21, 28** are designated *anchor days* that pair naturally
   with a weekly reflection (these are reflective / patterns / values
   prompts, not narrow situational ones).
7. **Day 30 is a forward-facing prompt** ("what is already clear but
   unsaid?"), pointing into month 2 rather than just looking back.

## The Sequence

Format: `Day N -> Seed Bank Prompt #X (short tag)`

| Day | Seed # | Primary Tag | Why this slot |
|----:|-------:|-------------|---------------|
|   1 |     24 | Identity | "מתי הכי נוח לך בתוך עצמך?" — soft, inviting, no shame |
|   2 |      3 | Identity | "מה נהיה קל יותר בשבילך לאחרונה?" — positive momentum |
|   3 |     11 | Habits | Auto-pilot noticing, low stakes |
|   4 |      8 | Identity | What feels real today — grounding |
|   5 |     10 | Emotions | Underserved needs — opens emotion register gently |
|   6 |     22 | Values | First values prompt — anchor before weekly |
|   7 |     23 | Patterns | **Anchor day:** "איזה דפוס חוזר אצלך?" — perfect for weekly view |
|   8 |     17 | Identity | Surprise about self — re-energizes after week 1 |
|   9 |     16 | Habits | What is being carried by habit alone |
|  10 |     14 | Emotions | Jealousy as signal (first "heavier" prompt) |
|  11 |      4 | Values | Energy leaks — practical, low charge |
|  12 |     27 | Habits | Help vs comfort — useful distinction |
|  13 |     21 | Habits | "Asked to stop and didn't" — observational |
|  14 |     28 | Meaning | **Anchor day:** meaning without recognition |
|  15 |      2 | Emotions | Sticky moment of the week |
|  16 |      7 | Values | "Time vs will" — values question with bite |
|  17 |     12 | Identity | Where I shrink to keep things simple |
|  18 |     25 | Relationships | What's hard to give yourself |
|  19 |     13 | Emotions | Unfair asks of self |
|  20 |     20 | Identity | "What no longer fits?" — preps for end of month |
|  21 |     29 | Identity | **Anchor day:** "what do I know now I didn't a year ago?" |
|  22 |      9 | Relationships | Truth told to others but hard to live |
|  23 |      5 | Fears | Stuck on an outdated reason (heavier — spaced) |
|  24 |     19 | Identity | Approval still being sought |
|  25 |     15 | Patterns | "Quiet price" — deeper noticing |
|  26 |     26 | Fears | Fear of loss (heaviest evergreen, well-spaced) |
|  27 |     18 | Relationships | What stays inside |
|  28 |      6 | Fears | **Anchor day:** what I need to keep in control |
|  29 |     30 | Fears | "What stays hidden even from yourself?" — closing depth |
|  30 |      1 | Identity | "What is already clear but unsaid?" — voice forward into month 2 |

Note: prompts not used above in the daily sequence are **all 30 prompts** —
the sequence above uses every prompt exactly once.

## Verification (counts)

- 30 days, 30 prompts, each prompt used once (verified mechanically).
- Fear-tagged seed prompts (#5, #6, #18, #26, #30) fall on days
  23, 28, 27, 26, 29 respectively. All are within the intentional
  Days 23 to 30 descent window. None appear before Day 23.
- Anchor days: Day 7 -> #23 (patterns), Day 14 -> #28 (meaning),
  Day 21 -> #29 (year-over-year identity), Day 28 -> #6 (fear / control).
  Day 28 is the only anchor day with a heavier prompt, intentional as the
  user enters the closing week.
- Evergreen prompts (#22-30 in the seed bank) are spread across Days 6,
  7, 12, 14, 18, 20, 21, 26, 29, 30. Not bunched at the end.

## Open questions (for Ron's review)

1. **Day 1 choice.** Currently prompt #24
   ("מתי הכי נוח לך בתוך עצמך?"). Alternatives: prompt #3
   ("what got easier lately?") or a brand-new onboarding-only prompt that
   does not exist in the seed bank. Worth deciding before launch.
2. **Day 30 -> Day 31.** What happens after day 30? Loop? Curate v2?
   Currently out of scope for v0.1.
3. **Sequencing changes after Ron does the 14-day pilot.** The build-in-
   private rule (README) says Ron must use this himself before public
   launch. The sequence is expected to change based on lived experience.
4. **Saturday handling.** README says the site rests on Saturday. The
   sequence here is 30 writing days, not 30 calendar days. Need a
   sequence-vs-calendar mapping rule.

## Storage / implementation note

For v0.1 (per [ARCHITECTURE.md, PR #39](https://github.com/ripper234/know-thyself/pull/39)),
this sequence becomes a static JSON file mapping `prompt_number -> seed_bank_id`.
Example shape:

```json
[
  {"day": 1, "prompt_id": 24},
  {"day": 2, "prompt_id": 3},
  ...
]
```

The "today's prompt number" calculation in ARCHITECTURE.md (days since
launch, 1-indexed) then becomes "the prompt_id at that day's index".
