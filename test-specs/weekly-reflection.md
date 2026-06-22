# Test-Spec: Weekly Reflection

A private, AI-generated **mirror** of the past week's answers — delivered Friday, per the spec ("end of every week, Friday for Israel"). Saturday is the rest day.

## Constraints from the spec (non-negotiable)

- **GPT is a mirror, not an authority.** The reflection may surface continuity, recurring themes, or patterns. It must **never** evaluate, praise, judge, advise, direct, score, or rank (spec: Internal contract; GenAI Usage: "Light reflection").
- It is **private**. It is sent only to the user; nothing is shared anywhere.
- It is **distinct from the manual weekly summary** (the manual summary is human-written, never auto-generated, and is **out of MVP scope**).
- Output is in **Hebrew**.

## Criteria

### Trigger
- Fires **Friday 11:00 `Asia/Jerusalem`**, DST-aware. (Verified by the timezone behaving correctly across a DST boundary, not by wall-clock UTC.)
- **Saturday** triggers no writing task and no reflection — at most a peaceful quote (quote delivery is ⚠️ DECIDE / optional for MVP).

### Input window
- The reflection reads the present days' answers from the **past 7 days** (the 7 calendar days ending on the Friday it fires, inclusive).
- Days with no answer are simply absent from the input; the reflection does not scold or note absence as failure.

### Behavior
- If there are **zero** answers in the window, no reflection is sent (nothing to mirror), or a gentle no-pressure note is sent — ⚠️ DECIDE: silent vs. gentle note. This spec assumes **silent** (no reflection when the week is empty).
- The prompt to Claude (Opus 4.8) instructs: mirror themes/continuity only; no advice, judgment, praise, or rating; Hebrew; brief.
- The reflection text is stored (so it's reproducible/auditable) and sent to the user.

## Golden examples

These pin *behavior and shape*, not exact wording (the wording is model output).

| # | Window contents | Expected |
|---|---|---|
| W1 | Answers on Mon, Tue, Thu (3 of 7 days) | One Hebrew reflection sent Fri 11:00; mirrors themes across the 3 answers; contains **no** advice/score/praise |
| W2 | No answers in the 7-day window | No reflection sent (silent) |
| W3 | Fires on a Friday inside Israeli DST | Sends at 11:00 *local* Israel time, not 11:00 UTC |
| W4 | Answers present; reflection generated | Reflection text is persisted and retrievable, not only sent |
| W5 | It is Saturday | No question, no reflection, no writing task |

### Mirror-not-authority check (W1 detail)
The generated text must not contain directive/evaluative moves. Golden negative assertions for W1's output:
- does not tell the user what to do ("you should…", "try to…")
- does not praise or grade ("great job", "this is healthy/unhealthy")
- does not rank days or answers
- ⚠️ This is checked by a constrained assertion (e.g. an LLM-judge or keyword guardrails over the output); the *method* is an implementation detail, the *requirement* is canonical.
