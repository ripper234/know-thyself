# Sharing Format Spec

How a Know-Thyself question is rendered when a user shares it to Facebook,
WhatsApp, or any other social surface.

This file resolves the open README TODO:

> should the full text of the question be posted, or just a teaser - enough to make users click?

It also addresses the R4 risk flagged in `research/insights.md`
("OG image pipeline gap"): without a concrete sharing payload, the social loop
is dead on day one.

## Core Decision

**Share the full question.**
Do not use a teaser, do not truncate, do not hide the question behind a click.

## Why full text wins

1. **Practice over funnel.** The product is a daily writing game, not a content
   site. A teaser optimizes for clicks; the full question optimizes for the
   reader actually pausing for two seconds and noticing themselves.
2. **Privacy stays clean.** Sharing is always question-only (never the answer).
   If we hide the question, the only thing left to share is "I answered today",
   which drifts toward performative streak posting. The full question keeps the
   share about the prompt, not the user.
3. **One prompt per day is short by design.** Prompts target 5 to 9 words
   (see `content/hebrew-style-guide.md`). A teaser of a 7-word question is
   silly; there is nothing to tease.
4. **Click-through is not the KPI.** Presence is (see README Leaderboard).
   Optimizing share copy for clicks would distort the system toward the wrong
   metric.

## Payload (per share)

Every share renders three deterministic fields, generated from
`content/prompts.json`:

| Field | Value | Notes |
| --- | --- | --- |
| `og:title` | Full Hebrew question (`text_he`) | No prefix, no quotes, no emoji |
| `og:image` | Per-prompt generated image | One image per `seed_id`, cached |
| `og:description` | One short standing line | See "Standing line" below |

The shared URL is the canonical question permalink
(xkcd-style: `/<day>/` or `/q/<seed_id>/`). It is **not** a personalized URL
and contains no user identifier.

## Standing line (`og:description`)

A single fixed line, reused for every share:

> משחק כתיבה יומי. שאלה אחת ביום. שתי דקות.
> (English gloss: "A daily writing game. One question a day. Two minutes.")

Rationale:
- Matches the homepage promise ("A private daily writing game").
- Sets expectations honestly: not a quiz, not a coach.
- Does not promise insight, growth, or transformation.
- Same line every day, so the share never feels like marketing copy.

## OG image rules

Defined in `content/prompts.json` (one image per prompt, keyed by `seed_id`):

- Image contains the question text **rendered into the image** so previews
  that strip OG tags still show the prompt.
- No usernames. No streak counters. No "user X just answered" framing.
- Pure question + minimal visual motif.
- Aspect ratio 1.91:1 (Facebook/Twitter default) plus a 1:1 variant for
  WhatsApp and Instagram.

## What is never shared

- The user's own answer text.
- Any other user's answer text.
- Any aggregate stat that could identify a user (e.g. "Ron just hit a 30-day
  streak").
- The global "X people showed up today" counter is **allowed** on the site
  but is **not** part of the share payload. It is not a recruiting hook.

## Sharing into WhatsApp groups

WhatsApp link previews strip most OG metadata and use only image + title.
That's fine: the payload above already degrades gracefully. The user lands
on the same canonical question page.

## Out of scope for v0.1

- Localized share copy beyond Hebrew. English/other languages reuse the
  same structure, swapping the standing line and the rendered image text.
- Per-user share cards ("Ron's day 14").
- Embedded answer excerpts behind opt-in. The privacy model in
  `README.md` (private by default) holds; revisit only if a future
  weekly-summary public-share feature is built.

## Open follow-ups (track as issues, not in this spec)

- OG image generation pipeline: where it runs, how it caches, how the
  image is regenerated if a prompt's `text_he` is edited.
- Verify the 1:1 variant looks acceptable for WhatsApp status shares,
  not just chat link previews.
- Decide whether the standing line shows in Hebrew, English, or both,
  for non-Hebrew locales of the share crawler.
