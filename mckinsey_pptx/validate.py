"""Pre-flight checks for a slide call: report everything wrong with it at once.

An agent that gets one TypeError per run needs one round trip per mistake.
`problems(name, fn, kwargs)` returns every finding for one call so the
builder can list them together:

    ("error", msg)    - the call cannot work; the builder skips it
    ("warning", msg)  - the call builds, but something will be silently lost
"""
from __future__ import annotations

import difflib
import inspect
from typing import Callable, Dict, List, Sequence, Tuple

Problem = Tuple[str, str]

# Arguments every template takes; left out of the "accepted" list to keep it short.
_COMMON = {"title", "subtitle", "page_number", "section_marker", "source", "footnote",
           "theme", "insight", "insight_label"}
# Handled by PresentationBuilder.add before the template is called.
BUILDER_ARGS = ("kicker", "group", "nav")

CARD_KEYS = {"title", "value", "icon", "tone", "body", "bullets"}
SERIES_KEYS = {"name", "values", "tone", "color"}
CHART_TYPES = ("column", "grouped_column", "stacked_column", "stacked_column_100", "bar",
               "stacked_bar", "line", "pie", "doughnut")


def near(word, options: Sequence[str]) -> str | None:
    hit = difflib.get_close_matches(str(word), [str(o) for o in options], n=1, cutoff=0.7)
    return hit[0] if hit else None


def unknown_template(name: str, available: Sequence[str]) -> str:
    s = near(name, available)
    return (f"unknown template {name!r}" + (f" — did you mean {s!r}?" if s else "")
            + " (python scripts/catalog.py lists every template)")


def signature_problems(fn: Callable, kwargs: Dict) -> List[Problem]:
    params = list(inspect.signature(fn).parameters.values())[1:]      # skip prs
    names = [p.name for p in params]
    required = [p.name for p in params if p.default is p.empty]
    out: List[Problem] = []
    for k in kwargs:
        if k not in names:
            s = near(k, names)
            out.append(("error", f"unknown argument {k!r}" + (f" — did you mean {s!r}?" if s else "")))
    for r in required:
        if r not in kwargs:
            out.append(("error", f"missing required argument {r!r}"))
    if out:
        shown = [n + ("*" if n in required else "") for n in names if n not in _COMMON]
        out.append(("error", "accepted: " + ", ".join(shown)
                    + "  (* = required; plus title, subtitle, insight, source, footnote, "
                      "kicker, group, nav)"))
    return out


def _dict_key_problems(where: str, items, allowed, what: str) -> List[Problem]:
    out: List[Problem] = []
    for i, it in enumerate(items or [], start=1):
        if not isinstance(it, dict):
            continue
        for k in it:
            if k not in allowed:
                s = near(k, allowed)
                out.append(("warning", f"{where} {what} {i}: key {k!r} is not used"
                            + (f" — did you mean {s!r}?" if s else "")
                            + f" (keys: {', '.join(sorted(allowed))})"))
    return out


def _series_problems(where: str, kw: Dict) -> List[Problem]:
    out: List[Problem] = []
    cats = kw.get("categories")
    for i, s in enumerate(kw.get("series") or [], start=1):
        if not isinstance(s, dict):
            out.append(("error", f"{where} series {i} must be a dict with name and values"))
            continue
        for need in ("name", "values"):
            if need not in s:
                out.append(("error", f"{where} series {i} has no {need!r}"))
        out += _dict_key_problems(where, [s], SERIES_KEYS, "series")
        if cats is not None and "values" in s and len(s["values"]) != len(cats):
            out.append(("error", f"{where} series {s.get('name', i)!r} has {len(s['values'])} "
                                 f"values for {len(cats)} categories"))
    return out


def item_problems(name: str, kw: Dict) -> List[Problem]:
    """Findings inside the lists a template takes (cards, rows, series ...)."""
    out: List[Problem] = []
    if name == "card_grid":
        out += _dict_key_problems(name, kw.get("cards"), CARD_KEYS, "card")
    elif name == "card_rows":
        out += _dict_key_problems(name, kw.get("rows"), CARD_KEYS, "row")
    elif name == "data_table":
        n = len(kw.get("columns") or [])
        for i, row in enumerate(kw.get("rows") or [], start=1):
            if len(row) != n:
                out.append(("warning", f"data_table row {i} has {len(row)} cells for {n} "
                                       "columns — a short row leaves blanks, a long one is cut"))
    if name in ("chart", "native_chart"):
        ct = kw.get("chart_type", "column")
        if ct not in CHART_TYPES:
            s = near(ct, CHART_TYPES)
            out.append(("error", f"chart_type {ct!r} is not a chart type"
                        + (f" — did you mean {s!r}?" if s else "")
                        + f" (one of: {', '.join(CHART_TYPES)})"))
        out += _series_problems(name, kw)
    elif name in ("line_chart", "stacked_column_chart", "grouped_column_chart"):
        out += _series_problems(name, kw)
    return out


def problems(name: str, fn: Callable, kwargs: Dict) -> List[Problem]:
    found = signature_problems(fn, kwargs)
    if any(level == "error" for level, _ in found):
        return found                       # item checks need valid arguments
    return found + item_problems(name, kwargs)
