# Research insights: decisions extracted from `gpt-research-4-2-26.md`

Distillation of the deep research report into concrete, decision-grade items for
know-thyself v0.1. Every item is grouped as one of:

- **Confirms** an existing spec choice (no action; cite when defending the design)
- **Decision needed** (Ron must pick before MVP code lands)
- **Risk to mitigate** (must show up in design / copy / architecture)
- **Out of scope for v0.1** (worth knowing, but parked)

This file is a living index. When a decision is made, link the resulting issue
or PR next to the item and leave the rest as history.

## Confirms existing spec

- **"No points. No winners." holds up.** Motivation research warns that PBL
  systems and visible competition can crowd out intrinsic motivation. Keep
  scoring and leaderboards out of v0.1. _(README: "Internal contract")_
- **"Write before login, finalize requires login."** Matches B=MAP and
  Hook-style "investment before auth." This is a real activation lever, not
  cosmetic. _(README: "Users can start answering before signup.")_
- **"Share question only, never answer."** Aligns with privacy-first journaling
  norms and lets non-writers still share, removing shame pressure.
  _(README: "Sharing never includes answer content.")_
- **Weekly reflection as the depth feature, manual and private by default.**
  Stronger than AI auto-summaries for a non-coach product.
  _(PR #46 ships the week 1 to 4 prompts.)_
- **Hebrew-first, RTL as first-class.** Already the default in `prompts.json`
  and `ui_copy.json` (PRs #44, #45). Keep `dir="rtl"` at document level when the
  MVP web layer lands.

## Decisions Ron should make before MVP code

### D1. Privacy architecture: server-side encryption vs E2EE vs hybrid
- Standard server-side encryption is the cheapest path and lets GPT reflection
  run server-side without extra work.
- Zero-access E2EE is the strongest trust posture and matches Day One / Standard
  Notes positioning, but it makes GPT reflection hard (needs explicit per-entry
  opt-in to decrypt and share).
- Hybrid (E2EE by default, opt-in "AI mode" per entry) is the most
  contract-aligned option but adds real implementation cost and key-management
  complexity.
- **Trade-off Ron must own:** the choice constrains everything downstream
  (login options, AI reflection scope, marketing copy). Recommend deciding
  before any auth or persistence code lands.

### D2. Streak / FOMO visibility
- "Can only answer TODAY's question" exploits loss aversion and drives return,
  but streak culture also produces shame and dropout on misses.
- Options: (a) hide streak entirely, (b) show only private streak, (c) weekly
  streak instead of daily, (d) optional opt-in display.
- Current spec shows "Total Days Submitted" and "Current Streak" privately.
  Pick the framing for missed days now: "That question has passed; today is
  new" beats any red counter.

### D3. "Resonance" instead of "upvote"
- README has an open TODO on the upvote flavor. Research strongly recommends
  reframing as private resonance ("This question hit today") and either
  hiding aggregates or only showing thresholded, non-ranked signals.
- **Recommendation:** drop "upvote" from the vocabulary entirely; adopt
  "resonance" with private-by-default storage and a thresholded global signal
  only (e.g., "Many people starred this") if any is shown at all.

### D4. Login providers and order
- README lists Facebook + Google. For iOS, Apple historically requires
  Sign in with Apple when other third-party logins exist.
- **Recommendation:** Web MVP can ship Google first (simpler OAuth), add
  Sign in with Apple before any App Store submission, treat Facebook login as
  optional rather than primary (also reduces Meta data-sharing surface).

### D5. Local draft storage technology
- `localStorage` is fine for the tiny "one-question draft" case but is lossy
  in private browsing and on device switch.
- `IndexedDB` is the standard for resilient client-side drafts and would be
  worth it if drafts ever grow beyond one short answer.
- **Recommendation for v0.1:** `localStorage` is enough; document the limit
  in `ui_copy.json` ("Saved on this device until you finalize"). Do **not**
  market local drafts as "secure" unless WebCrypto is added.

## Risks to mitigate (must shape design)

### R1. Content safety: avoid trauma-forcing prompts
- Expressive writing about stressors has mixed evidence and can be
  contraindicated for some users (notably those low in emotional
  expressiveness).
- **Action:** `content/guidelines.md` already biases toward observation /
  values / small choices. Make this explicit as a content rule:
  > "No prompt may force trauma disclosure. Heavier territory is allowed only
  > after day 22 (intentional descent), and even then the prompt must be
  > escapable in one sentence."
- The current `prompts.json` design rule "Days 23 to 30 are the intentional
  descent" already encodes this; lift it into `guidelines.md` as a hard rule.

### R2. GPT-as-mirror, not coach (output protocol)
- "GPT is a mirror" is currently a vibe in the README. Research argues it
  must be a **constrained output protocol** to survive contact with real LLMs.
- **Required protocol when GPT reflection ships:**
  - Allowed: paraphrase, short verbatim quotes, surfacing repeated words or
    themes, optional follow-up questions.
  - Banned tokens / patterns: "you should", "try", "I recommend", diagnoses,
    comparisons to other users, evaluations ("great answer", "interesting").
  - Required hedging: "I might be wrong, but I notice..."
  - Logging: never log user text; log only metadata (prompt id, timestamp,
    success flag).
- **Action:** when GPT reflection is built, this protocol gets its own spec
  file (`content/gpt-mirror-protocol.md`) and a regression test bank.

### R3. Privacy posture mismatch
- App-store privacy disclosures are publicly compared to actual practice.
  Any gap will be noticed.
- **Action:** the privacy story in marketing/blog and in any future App Store
  listing must match the architecture chosen in D1. Do not write privacy
  marketing copy until D1 is decided.

### R4. Open Graph / sharing reliability
- "Share the question" only works if every prompt URL renders cleanly on
  Facebook/X. That requires per-prompt OG metadata, 1200x630 images, and a
  Sharing Debugger workflow.
- **Action:** the MVP architecture spec (PR #39) should be extended to
  include an OG image generation pipeline (one image per prompt) as a v0.1
  requirement, not a v0.2 polish item. Today every prompt would share as a
  generic site preview, which kills the sharing loop.

## Out of scope for v0.1 (parked, worth remembering)

- **Sign in with Apple infrastructure** — needed only when iOS distribution
  starts.
- **Hybrid E2EE + opt-in AI mode** — only relevant if D1 picks the hybrid
  route.
- **A/B testing OG description (full question vs teaser)** — useful after
  there is real share traffic to measure.
- **Duolingo-style streak wager experiments** — interesting evidence point,
  but explicitly out of the "no winners" lane until proven necessary.
- **Optional "scratch mode" for past prompts** — only worth adding if early
  cohorts show shame-driven dropout on misses.

## Suggested follow-up issues

These are the items that should become GitHub issues so the work is trackable
rather than buried in this file. Numbers will be assigned when issues are
filed; this list is the intended scope, not a guarantee they were all opened.

1. **D1 — Pick privacy architecture for v0.1.** Blocks: auth, persistence,
   any AI reflection work, all privacy marketing copy.
2. **D3 — Replace "upvote" with private "resonance" in spec.** Small README
   edit + decision recorded.
3. **R1 — Lift "no trauma-forcing prompts" into `guidelines.md` as a hard
   rule.** Single-file edit.
4. **R2 — Draft `content/gpt-mirror-protocol.md` before any GPT reflection
   code.** Spec-only, no code dependency.
5. **R4 — Add OG image generation to MVP architecture spec (extend PR #39 or
   follow-up).** Currently missing; without it the sharing loop is broken on
   day one.

## Sources

All claims above are grounded in `research/gpt-research-4-2-26.md` (the deep
research report dated 2026-04-02). Citation markers in the original
(`citeturnXsearchY`) are preserved in that file and are not duplicated here;
this document is a decision aid, not a literature review.
