# MVP Architecture (v0.1)

Technical decisions for the first build: a private daily writing game Ron can use himself.

---

## Scope: what v0.1 includes

- Single daily Hebrew prompt (XKCD-style `/1`, `/2`, … URLs)
- `/` always redirects to today's prompt number
- Answer text area with local-draft autosave
- "סיימתי" (Finalize) button; saves answer server-side
- Login via Google (one provider is enough for v0.1)
- Private progress counters: Total Days Submitted, Current Streak
- Static prompt list loaded from a JSON/Markdown source file
- Mobile-friendly, RTL, minimal UI

## Scope: explicitly NOT in v0.1

- Weekly reflection view
- Social sharing / OG images
- Facebook login
- Public presence indicator ("X people showed up today")
- Favorites / stars
- GPT reflection on answers
- Deep-dive extensions (content exists, UI deferred)
- Image generation per prompt

---

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | **Next.js (App Router)** | SSR for share previews later, file-based routing maps cleanly to `/[id]`, React ecosystem, Vercel-native |
| Language | **TypeScript** | Type safety for data model, standard for Next.js |
| Styling | **Tailwind CSS** | Fast prototyping, RTL support via `dir="rtl"`, no theme ceremony |
| Auth | **NextAuth.js** with Google provider | One dependency, session handling built in, add Facebook later with a config line |
| Database | **Supabase (Postgres)** | Free tier covers solo use, row-level security for answer privacy, hosted so no infra to manage |
| Hosting | **Vercel** | Zero-config Next.js deploys, generous free tier, preview deploys for PRs |

### Alternatives considered

- **Firebase**: heavier SDK, Firestore query model less natural for relational data (user-answer-prompt joins)
- **Railway**: good for backend services, but Vercel is simpler for a Next.js frontend with no custom backend
- **SQLite / Turso**: viable for solo use, but Supabase gives a dashboard and auth helpers for free
- **Plain static site + localStorage only**: tempting for v0.1, but makes the "login to keep answers" requirement awkward and delays real auth integration

---

## Data Model

Three tables. That's it.

```
users
  id          uuid  PK (from auth provider)
  email       text
  name        text
  created_at  timestamp

answers
  id          uuid  PK
  user_id     uuid  FK → users
  prompt_id   int   (1-based, matches URL)
  body        text
  finalized   boolean  default false
  created_at  timestamp
  updated_at  timestamp
  UNIQUE(user_id, prompt_id)

streaks (materialized or computed)
  user_id           uuid
  total_finalized   int
  current_streak    int
  last_finalized_at date
```

Prompt content lives in a static file (`content/prompts.json`) deployed with the app. No prompts table needed until we want runtime editing.

---

## URL Routing

| Path | Behavior |
|------|----------|
| `/` | Redirect to `/N` where N = today's prompt number |
| `/[id]` | Show prompt #id. If id > today's number, 404. If id < today's, show prompt read-only (no answer input). |
| `/login` | Google OAuth flow |
| `/me` | Private dashboard: streak, total days, list of finalized prompts |

"Today's prompt number" = days since launch date, 1-indexed. Hardcoded launch date in config.

---

## Answer Flow

1. User lands on today's prompt
2. Text area appears with placeholder: *"זה רק בינך לבין עצמך. כתוב בכנות."*
3. Text saves to `localStorage` on every keystroke (draft)
4. User clicks **"סיימתי"**
5. If not logged in → prompt login, then finalize
6. If logged in → `POST /api/answers` with `{ prompt_id, body, finalized: true }`
7. Streak counters update
8. Button changes to a checkmark; answer becomes read-only for today

Draft-to-finalize is a one-way door per prompt. No editing after finalize. (This matches the "presence = deliberate act" philosophy.)

---

## RTL and Hebrew

- `<html lang="he" dir="rtl">` on all pages
- Tailwind RTL plugin or manual `rtl:` variants where needed
- Font: system Hebrew stack (`"Segoe UI", "Arial", sans-serif`) for v0.1; revisit with a custom font later
- All UI labels in Hebrew; keep code/comments in English

---

## Deployment

1. GitHub repo (this one) holds spec + content
2. Separate repo for code (or a `/app` directory here, Ron's call)
3. Vercel project connected to code repo
4. Supabase project created manually, connection string in Vercel env vars
5. Domain: TBD (pending name decision, General TODO #1)

---

## What's Needed to Start Building

1. **Merge PR #37** (seed bank) so prompt content is on main
2. **Merge PR #38** (product decisions) so the spec is unambiguous
3. **Create Supabase project** (5 min, free tier)
4. **Create Vercel project** linked to a code repo
5. **Scaffold Next.js app** with the stack above
6. Ron decides: code in this repo (`/app`) or separate repo?

After those 6 steps, the first working page with a prompt and text area is maybe 2-3 hours of coding.

---

## Open Questions (for Ron)

1. **Code location**: `/app` directory in this repo, or separate repo?
2. **Domain**: any name candidates yet? (Blocks nothing for v0.1, `*.vercel.app` works meanwhile)
3. **Launch date**: when does day 1 start? This determines prompt-to-date mapping.
