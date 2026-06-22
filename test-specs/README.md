# Test-Specs

The **canonical behavioral contract** for know-thyself, written in prose. Test code is generated *from* these and frozen (see [SPEC-DRIVEN.md](../SPEC-DRIVEN.md), Rules #2–#4). Humans maintain this folder; nobody maintains the generated test code.

## Conventions

- **Golden examples are authoritative.** Where prose and a golden example disagree, the example wins and the prose must be fixed. Every behavioral area carries at least one concrete `input → expected output` pair.
- **Day boundary is `Asia/Jerusalem`.** "Today", "yesterday", and all dates mean Israel calendar days, DST-aware. A reply at 00:30 Israel time belongs to that new day.
- **Scope is the solo MVP.** Single user (Ron), Telegram, Hebrew, SQLite. Multi-user, auth, leaderboards, website, images, and the manual weekly summary are explicitly out of scope here.
- **Open product decisions** are marked `⚠️ DECIDE:` — these need a human call before the affected tests are meaningful.

## Files

- [daily-flow.md](daily-flow.md) — delivering today's question, capturing the reply, the fallback
- [presence-and-streak.md](presence-and-streak.md) — what counts as presence; streak & total-days computation
- [weekly-reflection.md](weekly-reflection.md) — Friday AI mirror, Saturday rest
- [question-store.md](question-store.md) — Google Sheet schema, how today's question is chosen
