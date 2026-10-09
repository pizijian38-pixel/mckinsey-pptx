"""Look up templates in the catalog without reading all 2,000+ lines.

    python scripts/catalog.py                 # one-line index of all templates
    python scripts/catalog.py sankey venn     # full sections for these templates
    python scripts/catalog.py 70 77           # same, by catalog number
    python scripts/catalog.py --guide         # "Choosing between similar templates"
    python scripts/catalog.py --options       # slide-level options + common arguments
    python scripts/catalog.py --focus         # the focus= rule and which templates take it
    python scripts/catalog.py --icons         # icon names, tones and **bold** / {red|...} markup

Names may be template names or aliases (case-insensitive). Unknown names list the
closest matches and exit with status 1.
"""
from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "mckinsey_pptx" / "agent" / "CATALOG.md"
_HEAD = re.compile(r"^(#{1,2}) (.+)$")
_NUM = re.compile(r"^## (\d+)\. (.+)$")


def _sections(text: str):
    """[(heading, body_lines)] split at every '# ' / '## ' heading."""
    out, cur, buf = [], None, []
    for line in text.splitlines():
        if _HEAD.match(line):
            if cur is not None:
                out.append((cur, buf))
            cur, buf = line, []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out.append((cur, buf))
    return out


def _strip(body):
    while body and body[-1].strip() in ("", "---"):
        body = body[:-1]
    return body


def _field(body, label):
    """Text of a '**Label:** ...' field (continuation lines joined)."""
    for i, line in enumerate(body):
        if line.startswith(f"**{label}:**"):
            parts = [line[len(label) + 5:].strip()]
            for nxt in body[i + 1:]:
                if not nxt.strip() or nxt.startswith(("**", "-", "```")):
                    break
                parts.append(nxt.strip())
            return " ".join(p for p in parts if p)
    return ""


def load():
    text = CATALOG.read_text(encoding="utf-8")
    templates, named = [], {}
    for head, body in _sections(text):
        m = _NUM.match(head)
        if m:
            names = re.findall(r"`([a-z0-9_]+)`", m.group(2))
            templates.append({"num": int(m.group(1)), "title": m.group(2), "names": names,
                              "head": head, "body": _strip(body)})
        else:
            named[head.lstrip("# ").strip()] = (head, _strip(body))
    return text, templates, named


def _short(s, n=96):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def print_index(templates):
    print("Templates (name [aliases] — category — use when). "
          "Full entry: python scripts/catalog.py <name> ...\n")
    for t in templates:
        main, alias = t["names"][0], t["names"][1:]
        cat = _field(t["body"], "Category")
        use = _field(t["body"], "Use when")
        a = f" [{', '.join(alias)}]" if alias else ""
        print(f"{t['num']:>2}. {main}{a} — {_short(cat, 40)} — {_short(use)}")
    print("\nAlso: --icons (icon names, tones, markup)  --guide (similar templates)  "
          "--options (slide-level options)  --focus (focus= rule)")


def find(templates, key):
    k = key.strip().lower().strip("`")
    if k.isdigit():
        return [t for t in templates if t["num"] == int(k)]
    return [t for t in templates if k in t["names"]]


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    text, templates, named = load()
    if not argv:
        print_index(templates)
        return 0
    rich = next((k for k in named if k.startswith("Rich text, tones and icons")), None)
    flags = {"--guide": ["Choosing between similar templates"],
             "--icons": [rich] if rich else [],
             "--rich": [rich] if rich else [],
             "--options": ["Slide-level options (every template)", "Common arguments"],
             "--focus": None}
    status = 0
    for arg in argv:
        if arg in flags:
            if arg == "--focus":
                para = text.split("**Focus — one accent per slide.**", 1)
                print("**Focus — one accent per slide.**" + para[1].split("\n---", 1)[0]
                      if len(para) == 2 else "(no focus section)")
            else:
                for name in flags[arg]:
                    if name in named:
                        head, body = named[name]
                        print("\n".join([head] + body))
                        print()
            continue
        hits = find(templates, arg)
        if not hits:
            every = [n for t in templates for n in t["names"]]
            near = difflib.get_close_matches(arg.lower(), every, n=5, cutoff=0.5)
            print(f"[catalog] no template named '{arg}'."
                  + (f" Did you mean: {', '.join(near)}?" if near else
                     " Run with no arguments for the index."), file=sys.stderr)
            status = 1
            continue
        for t in hits:
            print("\n".join([t["head"]] + t["body"]))
            print("\n---\n")
    if any(a not in flags for a in argv):
        print("(Icon names, tones and markup: catalog.py --icons. Don't look them up in the "
              "package source.)")
    return status


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:          # output piped into head / more
        sys.exit(0)
