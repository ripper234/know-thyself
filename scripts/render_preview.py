#!/usr/bin/env python3
"""Render content/prompts.json as a static Hebrew RTL HTML preview.

Stdlib only. Run from repo root:

    python3 scripts/render_preview.py                       # writes ./preview.html
    python3 scripts/render_preview.py --out path/to/x.html  # custom output path
    python3 scripts/render_preview.py --prompts <path>      # render a specific file

The output is a single self-contained HTML file (no external assets) that
shows all 30 prompts the way a Hebrew reader would see them: right-to-left,
Hebrew system font, one card per day, anchor days highlighted.

This is a REVIEW AID for humans approving content/prompts.json. It is NOT
the production UI. The MVP app (see ARCHITECTURE.md, PR #39) loads
content/prompts.json directly and renders its own UI; this script just
gives a reviewer a single page to eyeball the live Hebrew text before
the JSON ships to main.

preview.html is .gitignored on purpose: it is a generated artifact, the
JSON is the source of truth.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_PATH = REPO_ROOT / "content" / "prompts.json"
DEFAULT_OUT = REPO_ROOT / "preview.html"


def load_prompts(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: {path} is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def render_card(p: dict) -> str:
    day = p["day"]
    text_he = html.escape(p["text_he"])
    text_en = html.escape(p.get("text_en", ""))
    category = html.escape(p["category"])
    tags = ", ".join(html.escape(t) for t in p.get("tags", []))
    note = html.escape(p.get("note", ""))
    anchor = p.get("anchor_day") is True
    anchor_class = " anchor" if anchor else ""
    anchor_badge = '<span class="badge anchor-badge">anchor</span>' if anchor else ""

    return f"""    <article class="card{anchor_class}">
      <header>
        <span class="day">Day {day}</span>
        <span class="badge category-{category}">{category}</span>
        {anchor_badge}
        <span class="tags">{tags}</span>
      </header>
      <p class="prompt-he" lang="he" dir="rtl">{text_he}</p>
      <p class="prompt-en" lang="en" dir="ltr">{text_en}</p>
      {f'<p class="note">{note}</p>' if note else ''}
    </article>"""


def render_html(data: dict) -> str:
    version = html.escape(data.get("version", ""))
    language = html.escape(data.get("language", ""))
    prompts = sorted(data["prompts"], key=lambda x: x["day"])
    cards = "\n".join(render_card(p) for p in prompts)
    description = html.escape(data.get("description", ""))

    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<title>know-thyself prompts preview ({version})</title>
<style>
  :root {{
    --bg: #fafaf7;
    --card: #ffffff;
    --ink: #1a1a1a;
    --muted: #666;
    --border: #e5e2d8;
    --anchor: #f6efe2;
    --anchor-border: #c9a96a;
    --evergreen: #e8f1ea;
    --unique: #eef0f5;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 24px;
    background: var(--bg);
    color: var(--ink);
    font-family: "Segoe UI", "Helvetica Neue", Arial, "Noto Sans Hebrew", sans-serif;
    line-height: 1.5;
  }}
  .meta {{
    max-width: 720px;
    margin: 0 auto 24px;
    padding: 12px 16px;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 14px;
    color: var(--muted);
  }}
  .meta strong {{ color: var(--ink); }}
  main {{
    max-width: 720px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
  }}
  .card.anchor {{
    background: var(--anchor);
    border-color: var(--anchor-border);
  }}
  header {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    margin-bottom: 10px;
    font-size: 13px;
    color: var(--muted);
  }}
  .day {{
    font-weight: 600;
    color: var(--ink);
    font-size: 14px;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .category-unique {{ background: var(--unique); color: #334; }}
  .category-evergreen {{ background: var(--evergreen); color: #2a4a35; }}
  .anchor-badge {{ background: var(--anchor-border); color: #fff; }}
  .tags {{ margin-inline-start: auto; font-size: 12px; }}
  .prompt-he {{
    font-size: 22px;
    line-height: 1.4;
    margin: 8px 0 6px;
  }}
  .prompt-en {{
    font-size: 13px;
    color: var(--muted);
    margin: 4px 0;
    font-style: italic;
  }}
  .note {{
    font-size: 12px;
    color: var(--muted);
    margin: 8px 0 0;
    padding-top: 8px;
    border-top: 1px dashed var(--border);
  }}
  footer {{
    max-width: 720px;
    margin: 24px auto 0;
    font-size: 12px;
    color: var(--muted);
    text-align: center;
  }}
</style>
</head>
<body>
  <div class="meta">
    <strong>know-thyself prompts preview</strong>
    &middot; version: {version}
    &middot; language: {language}
    &middot; {len(prompts)} prompts
    <br>
    <small>{description}</small>
  </div>
  <main>
{cards}
  </main>
  <footer>
    Generated by <code>scripts/render_preview.py</code>. Source: <code>content/prompts.json</code>. Not the production UI.
  </footer>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompts", type=Path, default=PROMPTS_PATH, help="Path to prompts.json")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output HTML path (default: ./preview.html)")
    args = parser.parse_args(argv)

    data = load_prompts(args.prompts)
    if "prompts" not in data or not isinstance(data["prompts"], list):
        print(f"ERROR: {args.prompts} has no 'prompts' array", file=sys.stderr)
        return 1

    html_text = render_html(data)
    args.out.write_text(html_text, encoding="utf-8")
    print(f"OK: wrote {args.out} ({len(data['prompts'])} prompts)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
