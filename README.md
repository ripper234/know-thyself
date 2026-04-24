# know-thyself
Writing game aimed to know oneself better with daily bite size questions, answerable in 2-3 minutes.

Positioning
-----------
This is a **daily writing game**, not a coach.
The primary value is showing up daily and writing.
GPT, when present, plays a minor reflective role only.

Directory Structure
-------------------
- README.md - main entry point
- content/guidelines.md - guidelines to generating content
- marketing/blog/ - draft blog posts
- research/ - GPT research and references

First Principles
----------------
1. Spec-driven-development. Spec is THE source of truth. Perhaps to the extreme "code is not stored in source control (other than as a cache)".
1. A. Research verdict: pure spec-generates-code is not feasible today. The spec remains the *authority* but code lives in source control normally.
1. B. Toolchain: MUST — GitHub (docs + code), static site generator or lightweight framework, auth provider. OPTIONAL — CI/CD, CDN, image generation pipeline. Detailed toolchain choices deferred to implementation phase.
2. MVP/v0.1 = something that I (Ron) enjoy playing with over time.
2. A. Once I am a consistent user, I'll naturally add features and improve.
2. B. MVP/v1.0 = something X other users try out (A) and convert to weekly users (B)
2. C. *Build in private* until the practice is embodied. No public launch until I have submitted 14 days, the flow feels boringly stable, and I have missed a day and returned.

Tooling
-------
1. Github *documentation* as source of truth
2. [tiny-pr-bot](https://github.com/ripper234/tiny-pr-bot) proposes spec improvements via automated PRs

User-facing message (unlogged homepage)
 --------------------------------------
 "A private daily writing game."
 "No points. No winners."
 "Show up. Write honestly. Notice what's there."

It's composed of daily questions or prompts. Each prompt encourages the user to complete a short writing exercise. The exercise should be short, doable, the user should learn something about themselves.

We'll start with a bank of 30 questions.
The game will take place in Hebrew (future instances might be in other languages).

Product
-------

Website
-------
Website is modeled like xkcd. The / website is the "daily question". You can go back/forward to view past questions. URL structure models XKCD (https://xkcd.com/3197/).

Every page is sharable to Facebook/social, but sharing is limited to the QUESTION only.

Every page is a question (from a fixed pre-generated and curated list of daily questions). The user can answer.

Users can start answering before signup.
Answers are treated as a **local draft** until finalized.
To keep an answer, the user must log in.
The primary action button is **"סיימתי"** ("I'm done"). This signals completion without judgment — no "submit" (too formal), no "finalize" (too corporate). The act of clicking is the practice.
The answer input includes a one-time placeholder text inviting writing and signaling privacy. Draft: *"הכתיבה פרטית. אף אחד לא רואה מה שאתה כותב כאן."* ("The writing is private. No one sees what you write here.")

Principle: A user can only answer TODAY's question, they cannot save answers to past questions.
(This encourages daily presence - the core practice.)

There is no upvote mechanism. Upvotes imply ranking and audience, which conflicts with the non-competitive core. The only interaction with a question is:
- **Star (☆)** — save a question to your personal favorites. Private, never aggregated publicly.

A user can star specific questions. They can access all questions they starred.

Sharing never includes answer content. Shared posts include the question and the unique question graphics. We let the user add their own thoughts (or not).

Shared posts show the **full question text** plus the unique question image. The question itself is the hook — hiding it behind a teaser adds clickbait energy that conflicts with the direct, honest tone. The answer is never shared.

Every question has a unique image generated that captures the essence of the question in a unique way.
Conducive to sharing it on Facebook.

Leaderboard
----------
The metric is presence.
2 private progress counters
- Total Days Submitted
- Current Streak

*Definition*
Presence = user clicks "סיימתי" on TODAY's question.
Drafting does not count. Reading does not count. Only "סיימתי" counts.

*Global Presence Indicator*
- Display: "X people showed up today."     (total number of players who submitted today)
- Optional 30-day sparkline chart of total daily submissions.
- No public ranking of answers.
- No usernames shown globally. Only each user sees their own Total Days Submitted and Current Streak.

Login
------
Via Google (primary) + Facebook connect.
Google first: broader reach, simpler flow, more trusted for privacy-sensitive products. Facebook as secondary option.

Weekly Reflection
-----------------
At the end of every week (Friday for Israel), the user is shown a private view of their answers from the past 7 days.
(The websites rests or offer a peaceful mini quote on Saturday, no writing task)

The user is invited to write a *weekly summary* that synthesizes the week.
This summary is written manually (never auto-generated from answers).

Weekly summaries are **private by default**.
The user may explicitly opt-in to make a weekly summary public. This opt-in is always on the current weekly update, never a general setting.

Weekly summaries may be shared publicly, and only after explicit opt-in.

Internal contract (design / dev)
--------------------------------
- This is a solo daily game, not coaching. Insight comes from repetition and patterns, never from judgment, scoring, or comparison.
- Privacy is the default and the rule. Daily answers are sacred; sharing happens only through deliberate synthesis or questions.
- GPT is a mirror, not an authority. It may reflect continuity or patterns, but never evaluate, praise, direct, or rank.


Content
-------
Prompt-generation rules live in [content/guidelines.md](content/guidelines.md).
Private usefulness comes first; public shareability applies to the question only, never the answer.

GenAI Usage
-----------
- Light reflection on finalized answers
- Long-term continuity & growth across a user's journey
- Initial list of *curated* questions
- image generated for every question
- image generated in every weekly reflection

Marketing
---------
[Post archive](https://docs.google.com/spreadsheets/d/1te47y6NYfcjiwMXVgDrriqWn9GKFGxyyIkgssbBqlBA/edit?gid=0#gid=0)

Posting flow:
1. Post to Facebook
2. Add link to archive
3. Post link to Whatsapp group

KPIs:
1. Setup reminder/agent to measure these!
2. Setup monthly/quarterly goals
3. Metrics:
3. A. Engagement on Facebook
3. B. Whatsapp group user count
3. C. Website metrics: daily active submitters, 7-day retention, streak distribution


TODO
- First post
  - Decide on conditions for first post
  - Discuss it in therapy (conflicting needs. "build in public" vs "don't overhype/spread yourself thin - build first")
  - Open whatsapp group
  - Write first blog post
  - Review it
  - Decide on a posting frequency (after every major work chunk/day or weekly)
  - Post it
- Getting info from users (forms/polls/when/what)


General
-------
TODO
1. Find a name & domain for the project.
2. Cleanup this readme
2. A. Move remaining TODOs to issues - partially done, continuing via tiny-pr-bot
2. B. General refactor
3. Process /research folder and extract insights/issues.
4. ~~Generate candidate first 30 questions.~~ → First Hebrew draft in PR [#37](https://github.com/ripper234/know-thyself/pull/37). Hebrew crafting process defined, resolving [#25](https://github.com/ripper234/know-thyself/issues/25).
5. Should the game pivot to or include elements of [Nomic](https://en.wikipedia.org/wiki/Nomic)? Perhaps with some AI players? It's an entirely different game. But maybe it can retain a simple core for people who just want to answer questions. Not for v0.

See also
--------
[Stoic app](https://apps.apple.com/us/app/stoic-journal-mental-health/id1312926037)


