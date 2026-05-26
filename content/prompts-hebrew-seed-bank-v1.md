# Hebrew Seed Bank v1

First curated bank of 30 Hebrew prompts for Know-Thyself.

Design intent:
- 21 **unique** prompts
- 9 **evergreen** prompts
- each prompt has 1 to 2 tags
- all prompts should be answerable in 2 to 3 minutes
- prompts are written in **active form**, addressing the reader directly
- gender-marked verbs use the **את.ה / verb.ת dotted form** as the stored canonical, resolved to proper gender at runtime when known (see [hebrew-style-guide.md](hebrew-style-guide.md))

## Unique Prompts

1. **מה כבר ברור לך, אבל עוד לא אמרת בקול?**  
   Tags: Identity, Patterns

2. **איזה רגע קטן מהשבוע לא יוצא לך מהראש?**  
   Tags: Emotions, Patterns

3. **מה נהיה קל יותר בשבילך לאחרונה?**  
   Tags: Identity, Habits

4. **לאן הולכת לך אנרגיה על דברים פחות חשובים?**  
   Tags: Values, Patterns

5. **מה את.ה ממשיך.ה לדחות מסיבה שכבר לא רלוונטית?**  
   Tags: Fears, Habits

6. **מה חשוב לך לשמור בשליטה עכשיו?**  
   Tags: Fears, Patterns

7. **על מה את.ה אומר.ת "אין לי זמן" כשבעצם אין רצון?**  
   Tags: Values, Habits

8. **איזה חלק ביום שלך מרגיש הכי אמיתי?**  
   Tags: Identity, Meaning

9. **איזו אמת את.ה אומר.ת לאחרים, וקשה לך לחיות אותה?**  
   Tags: Identity, Relationships

10. **איזה צורך שלך קיבל הכי מעט מקום השבוע?**  
    Tags: Emotions, Values

11. **מה את.ה עושה לאחרונה על אוטומט?**  
    Tags: Habits, Patterns

12. **איפה את.ה נוטה להתקטן כדי שיהיה פשוט יותר?**  
    Tags: Identity, Relationships

13. **מה ביקשת מעצמך השבוע שהיה לא הוגן?**  
    Tags: Emotions, Patterns

14. **מתי הרגשת קנאה, ועל מה היא הצביעה?**  
    Tags: Emotions, Values

15. **איזה מחיר שקט את.ה משלם.ת על משהו שנראה "בסדר"?**  
    Tags: Patterns, Meaning

16. **מה את.ה ממשיך.ה לסחוב רק מתוך הרגל?**  
    Tags: Habits, Patterns

17. **מה הפתיע אותך בעצמך החודש?**  
    Tags: Identity, Emotions

18. **מה נשאר אצלך בפנים, אבל לא יוצא החוצה?**  
    Tags: Relationships, Fears

19. **איזה אישור את.ה עדיין מבקש.ת, גם כשהוא לא נחוץ?**  
    Tags: Identity, Relationships

20. **מה כבר לא מתאים לך עכשיו?**  
    Tags: Identity, Meaning

21. **איזה רגע היום ביקש ממך לעצור, ולא עצרת?**  
    Tags: Habits, Patterns

## Evergreen Prompts

22. **מה באמת חשוב לך יותר ממה שנראה כלפי חוץ?**  
    Tags: Values, Identity

23. **איזה דפוס חוזר אצלך?**  
    Tags: Patterns

24. **מתי הכי נוח לך בתוך עצמך?**  
    Tags: Identity, Meaning

25. **מה קשה לך לתת לעצמך, אבל קל לבקש מאחרים?**  
    Tags: Relationships, Emotions

26. **מה מפחיד אותך לאבד, ומה זה אומר עליך?**  
    Tags: Fears, Identity

27. **איזה הרגל עוזר לך, ואיזה רק מרגיע אותך?**  
    Tags: Habits, Patterns

28. **מה נותן לך תחושת משמעות גם בלי הכרה?**  
    Tags: Meaning, Values

29. **מה את.ה יודע.ת על עצמך היום שלא ידעת לפני שנה?**  
    Tags: Identity, Patterns

30. **מה את.ה מסתיר.ה גם מעצמך?**  
    Tags: Fears, Identity

## Notes

- Canonical stored form uses **active voice with dotted gender markers** (`את.ה`, `מבקש.ת`, `ממשיך.ה`, etc.) where a verb form differs by gender.
- At runtime, when the user's gender is known, the dotted form is resolved to a clean gendered form (`אתה מבקש` / `את מבקשת`).
- Past-tense second-person forms in unvocalized Hebrew (`אמרת`, `ביקשת`, `הרגשת`, `עצרת`, `ידעת`) are spelled identically for masc/fem, so they need no dots.
- Where the subject is not the reader (e.g. "איזה חלק...", "איזה צורך...", "מה הפתיע אותך..."), no dotted form is needed.
- Passive constructions were intentionally removed: active phrasing preserves agency and reads stronger.
- These prompts should still be reviewed aloud in Hebrew before publishing.
- A later pass can add optional deep dives for the strongest 3 to 5 prompts, but the short core prompt should remain primary.
