# Hebrew Prompt Crafting Guide

This guide defines how Know-Thyself prompts should be written in Hebrew.

Goal: make prompt writing repeatable, calm, and consistent with the product's core tone.

## Core Decision

Prompts are written **originally in Hebrew**.

We may brainstorm in English, but the publishable prompt must be rewritten from scratch in Hebrew.
Literal translation is not good enough. Hebrew rhythm, softness, and directness behave differently.

## Target Voice

Default register:
- modern written-spoken Hebrew
- direct, but not blunt
- intimate, but not therapeutic
- clear, but not academic
- calm, not dramatic

The question should feel like:
- a clean invitation
- something a thoughtful friend might ask
- easy to enter on a busy day

It should **not** feel like:
- a diagnosis
- a slogan
- a riddle
- a Facebook-bait line

## Length Rules

Default target:
- **5 to 9 words**
- one question only
- one idea only

Soft limits:
- up to 12 words if clarity improves
- avoid subclauses unless essential
- avoid explanatory setup inside the prompt

If a prompt needs too much framing, it is probably two prompts.

## Active Voice + Dotted Gender (canonical rule)

This is the load-bearing rule for Hebrew prompts.

**Rule**: prefer the **active second-person form** addressed to the reader. When the verb form differs by gender, write it once in the **dotted canonical form** (`את.ה`, verb.ת / verb.ה).

Why this matters:
- Active form preserves agency. The reader is the doer, not the recipient.
- Passive Hebrew ("מה נדחה?", "מה נאמר?", "מה משולם?") sounds therapeutic, observational, or evasive. It pulls the reader away from themselves.
- The dotted form keeps the canonical text editable as one string, while letting the app render a clean gendered form at runtime when the user's gender is known.

Examples:

Prefer (active + dotted):
- ✅ `מה את.ה דוחה?`
- ✅ `על מה את.ה אומר.ת "אין לי זמן"?`
- ✅ `איזה אישור את.ה עדיין מבקש.ת?`
- ✅ `איפה את.ה מרגיש.ה הכי חי.ה?`

Avoid (passive / impersonal hedge):
- ❌ `מה נדחה אצלך?`
- ❌ `על מה נאמר "אין לי זמן"?`
- ❌ `איזה אישור עדיין מבוקש?`
- ❌ `איפה יש נטייה להיסגר?`

When the subject of the question is **not** the reader, no dotted form is needed:
- `איזה חלק ביום שלך מרגיש הכי אמיתי?` (subject = החלק)
- `איזה צורך שלך קיבל הכי מעט מקום השבוע?` (subject = הצורך)
- `מה הפתיע אותך בעצמך החודש?` (subject = מה)

When the verb form is **identical for masc and fem in unvocalized Hebrew** (most past-tense second-person singular forms: `אמרת`, `ביקשת`, `הרגשת`, `עצרת`, `ידעת`), no dots are needed.

When `לך` dative phrasing reads naturally and is not a passive hedge, it is fine:
- `מה קשה לך לבקש?`
- `לאן הולכת לך אנרגיה על דברים פחות חשובים?`

## Runtime Resolution

The dotted canonical form is the **stored** prompt. The app resolves it before rendering:

- If gender known and masc: drop `.ה` / `.ת` segments → `אתה מבקש`
- If gender known and fem: replace dotted segment with fem suffix → `את מבקשת`
- If gender unknown or non-binary: render the dotted form as-is (`את.ה מבקש.ת`)

Onboarding asks: זכר / נקבה / אחר.

## Vocabulary Boundaries

Prefer words from ordinary life:
- יום
- רגע
- הרגל
- פחד
- צורך
- בחירה
- קשר
- משמעות
- דפוס

Prefer concrete language over abstraction.

Prefer:
- "מה את.ה דוחה?"
- "איפה את.ה נוטה להיסגר?"
- "מה נהיה קל יותר?"

Avoid:
- therapy jargon
- academic abstraction
- self-help clichés
- inflated spiritual language
- HR / LinkedIn / startup speak

## Avoidance List

Do not use:
- "לרפא"
- "לשחרר טראומה"
- "להיות בגרסה הגבוהה שלך"
- "לממש את הפוטנציאל שלך"
- "מה היקום מנסה להגיד לך"
- "כיצד אתה מתבונן בתהליך הרגשי שלך"

Avoid question forms that sound like school, therapy, or a workshop handout:
- "כיצד..."
- "באילו אופנים..."
- "מהו..."

Prefer:
- "מה..."
- "איפה..."
- "מתי..."
- "איזה..."
- "על מה..."

## Prompt Patterns That Usually Work

Useful shapes (all active, second-person):
- What are you avoiding / allowing / noticing?
- Where do you feel friction / ease / truth / performance?
- Which pattern / tradeoff / need is active right now?
- What became easier / harder / clearer lately?
- What are you asking of others that you struggle to give yourself?

## Quality Bar

A good prompt should:
- open quickly
- invite honesty without pressure
- lead to 2 to 6 sentences naturally
- reveal something usable about the self
- still feel okay on a low-energy day

## Fast Review Checklist

Before adding a prompt to the bank, ask:
1. Is it understandable on first read?
2. Does it sound like Hebrew, not translated English?
3. Is it short enough?
4. Is it concrete enough?
5. Does it avoid therapy / guru / cliché energy?
6. **Is it active? If the reader is the doer, is the verb in active second-person (with `את.ה verb.ת/ה` form where needed)?**
7. Could Ron answer it in under 3 minutes?
8. Does it create self-clarity rather than pressure?

If two people can read it aloud and it still sounds natural, it is probably in-bounds.
