# know-thyself
Writing game aimed to know oneself

Positioning
-----------
This is a **daily writing game**, not a coach.
GPT plays a minor, reflective role only. It never leads, diagnoses, or coaches.
The primary value is showing up daily and writing.

A message to the user:
"This is a solo game without points or winners. You play by showing up, writing honestly, and noticing what’s there."

It’s about developing a game from scratch that helps with self-awareness.
It’s composed of daily questions or prompts. Each prompt encourages the user to complete a short writing exercise. The exercise should be short, doable, the user should learn something about themselves.

We’ll start with a bank of 30 questions.
The game will take place in Hebrew (future instances might be in other languages).


TODO
* Project Name
* Define Purpose
  * Make something I enjoy playing in v0.1 + iterate on
  * Slowly add features to attract other users
* Should I market it first?
  * Purpose: to find early users
  * Post on Facebook
  * Prep Google Form
  * Open whatsapp/facebook group?


Spec
----

Website is modeled like xkcd. The / website is the "daily question". You can go back/forward to view past questions. URL structure models XKCD (https://xkcd.com/3197/).

Every page is sharable to Facebook/social, but sharing is limited to the QUESTION only.

Every page is a question (from a fixed pre-generated and curated list of daily questions). The user can answer.

Users can start answering before signup.
Answers are treated as a **local draft** until finalized.
To keep an answer, the user must log in.
The primary action button is **“Finalize”**. (TODO - "submit"? Something else?)
The answer input includes a one-time placeholder text inviting writing and signaling privacy (copy TBD).

Principle: A user can only answer TODAY's question, they cannot save answers to past questions.
(This is done to do a FOMO effect and have users come back every day).

TODO: What flavor would the upvote mechanism have? (plus, thumb up, a unique icon...)

A user can favorite (star) specific questions (from others & their own). They can access all questions they favorited.

Sharing never includes answer content. Shared posts include the question and the unique question graphics. We let the user add their own thoughts (or not).

TODO - should the full text of the question be posted, or just a teaser - enough to make users click?

Every question has a unique image generated that captures the essence of the question in a unique way.
Conductive to sharing it on Facebook.

Login
------
Via Facebook connect + Google
TODO - is this the right choice & order?
 
Weekly Reflection
-----------------
At the end of every week (Friday for Israel), the user is shown a private view of their answers from the past 7 days.
(The websites rests or offer a peaceful mini quote on Saturday, no writing task)

The user is invited to write a *weekly summary* that synthesizes the week.
This summary is written manually (never auto-generated from answers).

Weekly summaries are **private by default**.
The user may explicitly opt-in to make a weekly summary public. This opt-in is always on the current weekly update, never a general setting.

Weekly summaries may be shared publicly, and only after explicit opt-in.

Design principle
-----------------
- Daily answers are fully private.
- This is a daily ritual first, a social artifact second.
- GPT feedback is intentionally minimal and non-directive.
- Public exposure, when it exists, happens only through deliberate weekly synthesis, or via daily questions (not answers).
- Insight is revealed through momentum and patterns, never through judgment or scoring.

Design guardrail
----------------
- Any feature that introduces points, rankings, grading, or comparative evaluation violates the core game.
- Progress is expressed only through continuity, reflection, and pattern recognition over time.

Content
-------
TODO: What content would
A) be interesting specifically to me (Ron Gross).
B) would be suitable to post on facebook daily
C) Would generate some compelling posts that cause 1. FB engagement 2. Website visits

GenAI Usage
-----------
- Light reflection on finalized answers
- Long-term continuity & growth across a user’s journey
- Initial list of *curated* questions
- image generated for every question
- image generated in every weekly reflection

General
-------
TODO
