# know-thyself bot (solo MVP)

Telegram bot for the daily writing game. Delivers one Hebrew question per day, stores
your reply as the day's answer (presence), and sends a private AI reflection mirror on
Fridays. Questions come from a Google Sheet if configured, otherwise from
[`seed_questions.json`](seed_questions.json).

> Code here is a regenerable **cache** — the source of truth is the spec + `test-specs/`.
> See [../SPEC-DRIVEN.md](../SPEC-DRIVEN.md).

## Run locally

```bash
python -m venv .venv && .venv/Scripts/python -m pip install -r ../requirements.txt
cp ../.env.example ../.env   # fill in tokens; set DB_PATH=./know_thyself.db
python bot.py
```

## Commands
- `/start` — intro + today's question
- `/question` — today's question
- `/skip` — fallback free-write (counts as presence)
- `/stats` — current streak + total days
- any text — saved as today's answer (marks presence)

## Deploy to Railway

1. `railway login` then `railway init` (or link an existing project).
2. Add a **Volume** mounted at `/data` (persists the SQLite answers across deploys).
3. Set Variables (see [`.env.example`](../.env.example)): `TELEGRAM_BOT_TOKEN`,
   `TELEGRAM_CHAT_ID`, `ANTHROPIC_API_KEY`. Optionally the Google Sheet vars.
4. `railway up` (or connect the GitHub repo for auto-deploy).

Start command and builder are pinned in [`../railway.json`](../railway.json).
The bot uses long-polling, so no public port/domain is needed.
