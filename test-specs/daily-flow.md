# Test-Spec: Daily Flow

The core loop: each day the bot delivers one question; the user's reply is their answer and marks the day present.

## Criteria

### Delivery
- Once per day at `DAILY_DELIVERY_TIME` (`Asia/Jerusalem`), the bot sends today's question to the user.
- The message contains the question text (Hebrew) and, if the question has a deep-dive, the deep-dive clearly marked as **optional**.
- The bot delivers a given day's question **at most once**. A restart on the same day does not re-deliver.
- ⚠️ DECIDE: `DAILY_DELIVERY_TIME` (the spec is web-pull, not push; the bot needs a nudge time). Placeholder default: `08:00`.

### Capturing the answer
- A free-text reply from the user is stored as the answer for **today's** question and marks today **present** (see [presence-and-streak.md](presence-and-streak.md)). The reply *is* the spec's "Finalize."
- The answer is always attributed to **today's** question. The user can never answer a past day's question (spec: "A user can only answer TODAY's question").
- The first reply of the day sets `finalized_at`. Additional replies the same day **append** to the day's answer; `finalized_at` and presence are unchanged.
- ⚠️ DECIDE: append vs. overwrite on later same-day replies. This spec assumes **append**.

### Fallback ("nothing comes to mind")
- The user can invoke a fallback (e.g. `/skip` or a button) labeled per the guideline: *"Nothing comes to mind? Do this instead."*
- The fallback invites free reflection. Whatever the user then writes **counts fully as presence**, identical to answering the question (guidelines.md: "Free reflection counts fully as presence").
- A day with only a fallback free-write is present; total-days and streak treat it the same as a normal answer.

### Edge cases
- A reply on a day where no question was delivered (e.g. before the first-ever delivery) is still stored against that day and still counts as presence.
- Reading/receiving the question without replying does **not** count as presence (spec: "Reading does not count").

## Golden examples

| # | Input | Expected |
|---|---|---|
| D1 | Question delivered Mon 08:00; user replies "..." Mon 09:15 | Mon answer stored, `finalized_at` = Mon 09:15, Mon present |
| D2 | Mon delivered; bot process restarts Mon 14:00 | No second Mon delivery |
| D3 | Mon delivered; user replies "A" Mon 09:00, then "B" Mon 21:00 | Mon answer = "A" + "B" (appended); `finalized_at` = Mon 09:00; one present day |
| D4 | Mon delivered; user taps fallback Mon, writes "tired today, just breathing" | Mon present; answer = the free-write |
| D5 | Mon delivered; user only reads, never replies | Mon **not** present |
| D6 | User replies "..." at Tue 00:20 Israel time | Counts as **Tue**, not Mon |
