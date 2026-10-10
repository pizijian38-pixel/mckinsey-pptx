"""AGENTS: you do not need to read this file — SKILL.md Step 3 describes the plan table; `catalog.py --plan` runs this check.

Read the slide plan (output/<slug>_plan.md) and check it.

Used by `catalog.py --plan` (before building: do the templates exist, is every
text layout justified, which catalog entries are needed) and by
`deck_check.py --plan` (after building: does the deck match the plan).

The plan is the Markdown table SKILL.md Step 3 asks for. Columns are found by
header name (`#`, `Relationship`, `Template`, `Why not text cards`), so extra or
reordered columns are fine. The Template cell reads

    chart                                one template
    growth_share · focus Batteries       text after " · " is ignored here
    composite[diagram:radar + cards + callout]
                                         a composite: its regions, in order
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?::[A-Za-z_][A-Za-z0-9_]*)?")
_EMPTY = {"", "-", "—", "–", "n/a", "none"}

Problem = Tuple[str, int, str]         # level ("error" | "warning"), plan row (1-based), message


def _registry():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from mckinsey_pptx import builder
    from mckinsey_pptx.components import COMPONENTS, DIAGRAM_MIN
    return builder, COMPONENTS, DIAGRAM_MIN


def canonical(name: str) -> str:
    """Template name with aliases collapsed ('' when the name is unknown)."""
    builder, _, _ = _registry()
    fn = builder._REGISTRY.get(name)
    return builder.template_name(fn) if fn else ""


def _cells(line: str) -> List[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip().strip("`").strip() for c in line.split("|")]


def parse_template(cell: str) -> Tuple[str, List[str]]:
    """('composite', ['diagram:radar', 'cards']) for `composite[diagram:radar + cards]`."""
    cell = cell.replace("`", "")
    cell = re.split(r"\s+[·•]\s+|\s+—\s+", cell)[0]          # " · focus X" and the like
    m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:\[(.*?)\])?", cell)
    if not m:
        return "", []
    return m.group(1), _IDENT.findall(m.group(2) or "")


def parse_plan(text: str) -> List[Dict]:
    """One dict per plan row: n, relationship, template, parts, why, raw."""
    header: Optional[List[str]] = None
    cols: Dict[str, int] = {}
    rows: List[Dict] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            if header and rows:
                break                       # the table ended
            continue
        cells = _cells(line)
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        low = [c.lower() for c in cells]
        if header is None:
            if any(c.startswith("template") for c in low):
                header = low
                for i, c in enumerate(low):
                    if c in ("#", "no", "no.", "slide"):
                        cols.setdefault("n", i)
                    elif c.startswith("relationship"):
                        cols["relationship"] = i
                    elif c.startswith("template"):
                        cols["template"] = i
                    elif c.startswith("why not"):
                        cols["why"] = i
            continue

        def cell(key):
            i = cols.get(key)
            return cells[i] if i is not None and i < len(cells) else ""
        template, parts = parse_template(cell("template"))
        n = cell("n")
        rows.append({"n": int(n) if n.isdigit() else None,
                     "relationship": cell("relationship"), "template": template,
                     "parts": parts, "why": cell("why"), "raw": cell("template")})
    return rows


def _text_layouts() -> set:
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import deck_check
    return set(deck_check._TEXT_LAYOUTS)


def check_plan(rows: List[Dict]) -> List[Problem]:
    builder, components, diagrams = _registry()
    from mckinsey_pptx import validate
    text = _text_layouts()
    out: List[Problem] = []
    if not rows:
        return [("error", 0, "no plan table found: expected a Markdown table with a "
                             "'Template' column (SKILL.md Step 3)")]
    seen = set()
    for i, r in enumerate(rows, start=1):
        n = r["n"] or i
        if n in seen:
            out.append(("warning", i, f"slide number {n} appears twice"))
        seen.add(n)
        name = r["template"]
        if not name:
            out.append(("error", i, "no template named"))
            continue
        canon = canonical(name)
        if not canon:
            out.append(("error", i, validate.unknown_template(name, list(builder._REGISTRY))))
            continue
        if not r["relationship"].strip():
            out.append(("warning", i, "Relationship is empty: name what the slide shows"))
        if canon in text and r["why"].strip().lower() in _EMPTY:
            out.append(("warning", i, f"{canon} is a text layout: say in 'Why not text cards' "
                                      "why the content is really a list, or pick a diagram"))
        if canon == "composite":
            if not r["parts"]:
                out.append(("warning", i, "composite: list its regions, e.g. "
                                          "composite[diagram:radar + cards + callout]"))
            for p in r["parts"]:
                kind, _, tpl = p.partition(":")
                if kind not in components:
                    out.append(("error", i, f"composite region {kind!r} is not a component "
                                            f"(one of: {', '.join(sorted(components))})"))
                elif kind == "diagram":
                    if not tpl:
                        out.append(("error", i, "write a diagram region as diagram:<template>"))
                    elif canonical(tpl) not in diagrams:
                        out.append(("error", i, f"diagram:{tpl} cannot be drawn in a region "
                                                f"(supported: {', '.join(sorted(diagrams))}); "
                                                "use it as a full slide"))
            if sum(p.startswith("diagram:") for p in r["parts"]) > 2:
                out.append(("warning", i, "three diagrams on one slide: split the slide"))
    return out


def entries_needed(rows: List[Dict]) -> List[str]:
    """Catalog names to print for this plan: every template, plus the diagram
    templates used inside composites."""
    names: List[str] = []
    for r in rows:
        canon = canonical(r["template"]) if r["template"] else ""
        if canon and canon not in names:
            names.append(canon)
        for p in r["parts"]:
            kind, _, tpl = p.partition(":")
            c = canonical(tpl) if kind == "diagram" and tpl else ""
            if c and c not in names:
                names.append(c)
    return names


def compare_with_deck(rows: List[Dict], built: List[Tuple[Optional[str], List[str]]]
                      ) -> List[Tuple[int, str]]:
    """Differences between the plan and the deck as (slide, message); slide 0 =
    the deck as a whole. `built`: per slide, the template name the build recorded
    and the diagram templates drawn inside it."""
    msgs: List[Tuple[int, str]] = []
    if len(rows) != len(built):
        msgs.append((0, f"the plan has {len(rows)} rows, the deck {len(built)} slides"))
    for i, r in enumerate(rows, start=1):
        n = r["n"] or i
        if n > len(built):
            msgs.append((n, f"slide {n}: planned {r['template']}, not in the deck"))
            continue
        tpl, drawn = built[n - 1]
        want = canonical(r["template"]) if r["template"] else ""
        got = canonical(tpl) if tpl else ""
        if not got:
            continue                       # slide not built through the builder
        if want and want != got:
            msgs.append((n, f"slide {n}: plan says {want}, deck has {got}"))
        elif got == "composite":
            planned = sorted(canonical(p.partition(":")[2]) for p in r["parts"]
                             if p.startswith("diagram:"))
            actual = sorted(canonical(d) for d in drawn)
            if planned != actual:
                msgs.append((n, f"slide {n}: plan has diagrams {planned or 'none'}, "
                                f"deck has {actual or 'none'}"))
    return msgs
