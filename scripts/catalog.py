"""Look up templates in the catalog without reading all 2,000+ lines.

    python scripts/catalog.py                 # one-line index of all templates
    python scripts/catalog.py sankey venn     # full sections for these templates
    python scripts/catalog.py 70 77           # same, by catalog number
    python scripts/catalog.py --guide         # "Choosing between similar templates"
    python scripts/catalog.py --options       # slide-level options + common arguments
    python scripts/catalog.py --focus         # the focus= rule and which templates take it
    python scripts/catalog.py --icons         # icon names, tones and **bold** / {red|...} markup
    python scripts/catalog.py --theme         # make_theme: language, company, brand colour
    python scripts/catalog.py --spines        # typical slide order per type of deck (no outline)
    python scripts/catalog.py --plan output/<slug>_plan.md
                                              # check the slide plan, print the entries it needs

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
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced          # "# comment" inside an example is not a heading
        if not fenced and _HEAD.match(line):
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
    """All templates in under BUDGET characters (see BUDGET below)."""
    print("Templates: number. name [aliases] — use when. "
          "Entries: python scripts/catalog.py <name> <name> ...")
    for t in templates:
        main, alias = t["names"][0], t["names"][1:]
        use = _field(t["body"], "Use when")
        a = f" [{', '.join(alias)}]" if alias else ""
        print(f"{t['num']}. {main}{a} — {_short(use, 52)}")
    print("Flags: --icons --guide --options --focus --theme --spines; "
          "--plan <plan.md> checks a plan. All 80 templates are listed above.")


def find(templates, key):
    k = key.strip().lower().strip("`")
    if k.isdigit():
        return [t for t in templates if t["num"] == int(k)]
    return [t for t in templates if k in t["names"]]


# Some agent hosts (Google Antigravity) show only the LAST ~8,100 characters of a
# command's output and drop the start. Every output stays under BUDGET, and what
# matters most (problems, what was left out and how to get it) is printed last.
BUDGET = 7000


def _markup_scope() -> str:
    sys.path.insert(0, str(CATALOG.parents[2]))
    from mckinsey_pptx.design import MARKUP_FULL, MARKUP_PARTIAL
    return ("Where `**bold**` / `{tone|text}` markup renders (anywhere else it prints "
            "literally, and the checker flags it in section [4]):\n"
            "- everywhere on the slide: " + ", ".join(f"`{n}`" for n in MARKUP_FULL) + "\n"
            "- in body text only (labels, headings, categories stay literal): "
            + ", ".join(f"`{n}`" for n in MARKUP_PARTIAL) + "\n")


def _print_markup_scope():
    print(_markup_scope())


def _entry(t) -> str:
    return "\n".join([t["head"]] + t["body"]) + "\n\n---\n"


def _compact(t) -> str:
    """The entry without its example: fields and arguments only."""
    body = []
    for line in t["body"]:
        if line.startswith("**Example"):
            break
        body.append(line)
    return "\n".join([t["head"]] + _strip(body)
                     + [f"(example: python scripts/catalog.py {t['names'][0]})"]) + "\n\n---\n"


def _pages(text: str, size: int):
    """Split one long text at line boundaries into chunks of at most `size`."""
    out, cur = [], ""
    for line in text.splitlines(keepends=True):
        if cur and len(cur) + len(line) > size:
            out.append(cur)
            cur = ""
        cur += line
    return out + ([cur] if cur else [])


def emit_entries(templates_found, tail: str = "", page: int = 1, budget: int = BUDGET) -> None:
    """Print as many full entries as fit, then compact ones, then name the rest;
    `tail` (problems, hints) is printed last so it is never the part cut off."""
    # keep room for the closing lines, which may name every template twice
    room = budget - len(tail) - 250 - 2 * sum(len(t["names"][0]) + 2 for t in templates_found)
    shown, compact, left = [], [], []
    used = 0
    if len(templates_found) == 1 and len(_entry(templates_found[0])) > room:
        t = templates_found[0]
        parts = _pages(_entry(t), room)
        page = max(1, min(page, len(parts)))
        print(parts[page - 1], end="")
        if page < len(parts):
            print(f"\n[catalog] part {page} of {len(parts)} of `{t['names'][0]}` — the rest: "
                  f"python scripts/catalog.py {t['names'][0]} --part {page + 1}")
        print(tail, end="")
        return
    # all full entries if they fit; otherwise every entry without its example
    # (arguments matter more than examples), as many as fit
    full = sum(len(_entry(t)) for t in templates_found) <= room
    for t in templates_found:
        block = _entry(t) if full else _compact(t)
        if used + len(block) <= room:
            shown.append(block)
            used += len(block)
            if not full:
                compact.append(t["names"][0])
        else:
            left.append(t["names"][0])
    print("\n".join(shown), end="")
    if compact:
        print(f"\n[catalog] shown without examples to fit the output limit: "
              f"{', '.join(compact)} (one name per call shows its example)")
    if left:
        print(f"[catalog] NOT shown (output limit): {', '.join(left)} — run: "
              f"python scripts/catalog.py {' '.join(left)}")
    print(tail, end="")


def plan_report(path, templates) -> int:
    """Check a slide plan. Entries are not reprinted: in the Crest run the agent
    had looked every template up already and --plan reprinted ~6.5 KB twice."""
    import plan_check
    try:
        rows = plan_check.parse_plan(Path(path).read_text(encoding="utf-8-sig"))
    except OSError as e:
        print(f"[catalog] cannot read the plan: {e}")
        return 1
    problems = plan_check.check_plan(rows)
    errors = [p for p in problems if p[0] == "error"]
    lines = [f"\n== plan check: {len(rows)} slides, "
             f"{len({r['template'] for r in rows})} distinct templates"]
    for level, row, msg in problems:
        lines.append(f"  {level.upper():7s} row {row}: {msg}" if row
                     else f"  {level.upper():7s} {msg}")
    if not problems:
        lines.append("  no problems — build it")
    names = [t["names"][0] for name in plan_check.entries_needed(rows)
             for t in find(templates, name)]
    if names:
        lines.append(f"Templates in this plan: {', '.join(names)}.")
        lines.append("Arguments for any you have not looked up yet: python scripts/catalog.py "
                     + " ".join(names[:6]) + (" (then the rest)" if len(names) > 6 else ""))
    print("\n".join(lines).lstrip("\n"))
    return 1 if errors else 0


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    text, templates, named = load()
    if not argv:
        print_index(templates)
        return 0
    if argv[0] == "--plan":
        if len(argv) != 2:
            print("usage: catalog.py --plan output/<slug>_plan.md")
            return 1
        return plan_report(argv[1], templates)
    page = 1
    if "--part" in argv:
        i = argv.index("--part")
        page = int(argv[i + 1]) if i + 1 < len(argv) and argv[i + 1].isdigit() else 1
        argv = argv[:i] + argv[i + 2:]
    rich = next((k for k in named if k.startswith("Rich text, tones and icons")), None)
    flags = {"--guide": ["Choosing between similar templates"],
             "--icons": [rich] if rich else [],
             "--rich": [rich] if rich else [],
             "--options": ["Slide-level options (every template)", "Common arguments"],
             "--theme": ["Theme (make_theme)"],
             "--spines": ["Deck spines"],
             "--focus": None}
    status = 0
    sections, found, notes = [], [], []
    for arg in argv:
        if arg in flags:
            if arg == "--focus":
                para = text.split("**Focus — one accent per slide.**", 1)
                sections.append("**Focus — one accent per slide.**"
                                + para[1].split("\n---", 1)[0] + "\n"
                                if len(para) == 2 else "(no focus section)\n")
            else:
                for name in flags[arg]:
                    if name in named:
                        head, body = named[name]
                        sections.append("\n".join([head] + body) + "\n")
                if arg in ("--icons", "--rich"):
                    sections.append(_markup_scope())
            continue
        hits = find(templates, arg)
        if not hits:
            every = [n for t in templates for n in t["names"]]
            near = difflib.get_close_matches(arg.lower(), every, n=5, cutoff=0.5)
            notes.append(f"[catalog] no template named '{arg}'."
                         + (f" Did you mean: {', '.join(near)}?" if near else
                            " Run with no arguments for the index."))
            status = 1
            continue
        found += [t for t in hits if t not in found]
    # flag sections first (they are short and asked for explicitly), then entries
    flag_text = "\n".join(sections)
    left_flags = []
    while len(flag_text) > BUDGET - 600 and len(sections) > 1:
        left_flags.append(sections.pop())
        flag_text = "\n".join(sections)
    print(flag_text, end="")
    tail = []
    if left_flags:
        tail.append("[catalog] some flag sections were left out (output limit): ask for "
                    "fewer flags per call.")
    tail += notes
    if found:
        tail.append("(Icon names, tones and markup: catalog.py --icons. Don't look them up "
                    "in the package source.)")
    tail_text = ("\n" + "\n".join(tail) + "\n") if tail else ""
    if found:
        emit_entries(found, tail=tail_text, page=page, budget=BUDGET - len(flag_text))
    else:
        print(tail_text, end="")
    return status


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:          # output piped into head / more
        sys.exit(0)
