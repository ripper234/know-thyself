# Test-Spec: Question Store

Questions live in a **Google Sheet** (issue #14) so they can be curated without touching code. The bot pulls from it; answers are **never** written back to the Sheet (answers are sacred and private — they live only in SQLite).

## Schema (one row per question)

| Column | Meaning | Required |
|---|---|---|
| `id` | Sequential integer, xkcd-style (1, 2, 3, …) | yes |
| `text_he` | Question text, Hebrew | yes |
| `tags` | 1–2 tags from the 8 in guidelines.md (Identity, Values, Emotions, Fears, Relationships, Habits, Meaning, Patterns) | yes |
| `type` | `unique` or `evergreen` | yes |
| `deep_dive_he` | Optional deep-dive extension, Hebrew | no |
| `image_url` | Optional; out of MVP scope (image generation deferred) | no |

## Criteria

### Selecting today's question
- Each present-day delivery serves exactly one question and **records the `(date → id)` mapping** in SQLite, so a day's question is stable and reproducible.
- Selection rule (MVP): serve questions in ascending `id` order — the lowest `id` not yet served. One question consumed per delivery day.
- Once a day's question is recorded, it never changes for that day, even if the Sheet is later edited or reordered.
- ⚠️ DECIDE: evergreen reuse. The spec allows evergreen questions to reappear (~30% per guidelines.md). For the solo MVP this is not needed (30 questions > 14 days); evergreen rows are served once like any other. Revisit before content runs low.

### Validation / resilience
- Rows missing a required field (`id`, `text_he`, `tags`, `type`) are skipped with a logged warning, not served.
- A `tags` value outside the 8-tag set is logged as a warning but the question is still usable (tags are invisible scaffolding, not user-facing).
- If the Sheet is unreachable at delivery time, the bot logs the error and does not deliver a malformed/empty question (fail safe, not fail loud-to-user).
- If no unserved questions remain, the bot logs this and (MVP) sends nothing new that day — ⚠️ DECIDE: behavior when the bank is exhausted.

## Golden examples

| # | Sheet state | Already served | Expected today's question |
|---|---|---|---|
| Q1 | ids 1,2,3 present | none | id 1 |
| Q2 | ids 1,2,3 present | 1 served Mon | id 2 |
| Q3 | id 2 row missing `text_he` | 1 served | id 3 (id 2 skipped + warned) |
| Q4 | ids 1,2,3; today already recorded as id 2 | n/a | id 2 (stable; re-reading the Sheet doesn't reassign) |
| Q5 | all ids served | all | nothing new delivered + logged |
| Q6 | id 1 has `deep_dive_he` set | none | id 1 delivered **with** the deep-dive marked optional |
