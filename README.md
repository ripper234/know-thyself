# know-thyself
Writing game aimed to know oneself

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
A user can start answering before signup. On save, they are prompted to log in.
A user can save annonymously which doesn't really save but rather prompts them to login.
The answer input includes a one-time placeholder text : “100% Private. Nothing is shared.” (TODO - better text that also invites, not just warns)

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
- Public exposure, when it exists, happens only through deliberate weekly synthesis.
 
Content
-------
TODO: What content would
A) be interesting specifically to me (Ron Gross).
B) would be suitable to post on facebook daily
C) Would generate some compelling posts that cause 1. FB engagement 2. Website visits

General
-------
TODO
1. Where to leverage GenAI other than (initial seeding of the curated questions + image gen per question)?
