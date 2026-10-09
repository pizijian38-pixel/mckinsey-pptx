"""Change between two states, drawn as position on one shared scale.

- slopegraph : several series, exactly two states (before / after, two years).
               Both axes share one scale and origin — the slope is the change.
- dumbbell   : categories in rows, two values per row on one horizontal scale;
               the bar between the dots is the gap.

The focal series (focus=) carries the accent and a heavier line; the rest is
neutral. Data marks are named "<kind>:<label>" so tests can measure them.
"""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from ..base import add_line, add_oval, add_textbox, write_paragraph
from ..design import (HAIRLINE_PT, check_focus, eyebrow, fmt_num, has_focus, is_focus,
                      legend_strip, mark_axis, nice_bounds, text_width_pt, tint, warn_small)
from ..labels import loc
from ..theme import Theme, DEFAULT_THEME
from .evaluation_slides import _frame


def _spread(ys, gap, lo, hi):
    """Push label centres apart to at least `gap`, inside [lo, hi], keeping order."""
    idx = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for a, b in zip(idx, idx[1:]):
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    over = max(0.0, out[idx[-1]] - hi) if idx else 0
    if over:
        for i in idx:
            out[i] -= over
        for a, b in zip(idx[::-1], idx[::-1][1:]):
            if out[a] - out[b] < gap:
                out[b] = out[a] - gap
    return [max(lo, y) for y in out]


# ---------------------------------------------------------------- slopegraph

def add_slopegraph(prs, *,
                   title: str = "[Slopegraph / Insert action title]",
                   series: Sequence[Dict],
                   states: Sequence[str] = ("Before", "After"),
                   fmt: Optional[str] = None,
                   include_zero: bool = False,
                   focus=None,
                   subtitle: Optional[str] = None,
                   insight: Optional[str] = None,
                   insight_label: Optional[str] = "Key insight",
                   page_number=None, section_marker=None,
                   source=None, footnote=None,
                   theme: Theme = DEFAULT_THEME):
    """series: [{"name", "start", "end"}] (4-10). states: the two state captions.
    Both axes share one scale; the domain is rounded around the data (state it in
    the source line if it does not start at zero, or pass include_zero=True).
    focus: the series the title is about — accent, heavier line, bold labels.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    names = [s.get("name", "") for s in series]
    check_focus("slopegraph", title, focus, names)
    focused = has_focus(focus)
    if not 2 <= len(series) <= 10:
        warn_small("slopegraph", title, 0, f"{len(series)} series; keep to 4-10.")
    vals = [float(s["start"]) for s in series] + [float(s["end"]) for s in series]
    lo, hi, _ = nice_bounds(min(vals), max(vals), 5, include_zero)
    size = typo.chart_label_size + 1

    def lab_w(side):
        return max(text_width_pt(f"{n}  {fmt_num(s[side], fmt)}", size, True) / 72
                   for n, s in zip(names, series)) + 0.25
    gw = min(max(lab_w("start"), lab_w("end"), 1.6), 3.4)
    run = min(width - 2 * gw - 0.4, 4.6)
    xa = left + (width - run) / 2
    xb = xa + run
    ya, yb = top + 0.45, bottom - 0.15

    def y_of(v):
        return yb - (v - lo) / (hi - lo) * (yb - ya)
    for x, cap in ((xa, states[0]), (xb, states[1])):
        add_line(slide, x, ya, x, yb, color=pal.text_dark, width_pt=HAIRLINE_PT)
        eyebrow(slide, theme, x - 1.2, top, 2.4, cap, color=pal.text_dark, align=PP_ALIGN.CENTER)
    order = sorted(range(len(series)), key=lambda i: is_focus(focus, i, names[i]))
    for i in order:
        s = series[i]
        f = is_focus(focus, i, names[i])
        col = pal.bright_blue if f else (tint(pal.dark_navy, 0.55) if focused else pal.dark_navy)
        y0, y1 = y_of(float(s["start"])), y_of(float(s["end"]))
        ln = add_line(slide, xa, y0, xb, y1, color=col, width_pt=3.0 if f else 1.5)
        ln.name = f"slope:{names[i]}"
        for x, y in ((xa, y0), (xb, y1)):
            d = 0.13 if f else 0.1
            add_oval(slide, x - d / 2, y - d / 2, d, d, fill=col)
    for side, x, al in (("start", xa, PP_ALIGN.RIGHT), ("end", xb, PP_ALIGN.LEFT)):
        ys = _spread([y_of(float(s[side])) for s in series], 0.24, ya - 0.1, yb + 0.1)
        for i, (s, y) in enumerate(zip(series, ys)):
            f = is_focus(focus, i, names[i])
            strong = f or not focused
            txt = (f"{names[i]}  {fmt_num(s[side], fmt)}" if side == "start"
                   else f"{fmt_num(s[side], fmt)}  {names[i]}")
            tb = add_textbox(slide, x - gw - 0.1 if side == "start" else x + 0.12, y - 0.13,
                             gw, 0.26, anchor=MSO_ANCHOR.MIDDLE)
            write_paragraph(tb.text_frame, txt, size=size, bold=strong,
                            color=pal.deep_navy if strong else pal.footer_gray,
                            family=typo.family, align=al, first=True)
    return slide


# ---------------------------------------------------------------- dumbbell

def add_dumbbell(prs, *,
                 title: str = "[Dumbbell / Insert action title]",
                 rows: Sequence[Dict],
                 labels: Sequence[str] = ("Before", "After"),
                 fmt: Optional[str] = None,
                 sort: Optional[str] = None,
                 include_zero: bool = False,
                 focus=None,
                 subtitle: Optional[str] = None,
                 insight: Optional[str] = None,
                 insight_label: Optional[str] = "Key insight",
                 page_number=None, section_marker=None,
                 source=None, footnote=None,
                 theme: Theme = DEFAULT_THEME):
    """rows: [{"name", "a", "b"}] (3-12): two values per category on one scale —
    a = ring (labels[0]), b = dot (labels[1]); the bar between them is the gap.
    sort: None (as given) | "b" | "gap" (largest gap first).
    include_zero: start the scale at 0 — off by default: the dots encode position,
                  not length, so a tight scale is honest (state it in the source).
    focus: the row the title is about — accent, bold label.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    rows = list(rows)
    if sort == "b":
        rows.sort(key=lambda r: -float(r["b"]))
    elif sort == "gap":
        rows.sort(key=lambda r: -abs(float(r["b"]) - float(r["a"])))
    names = [r.get("name", "") for r in rows]
    check_focus("dumbbell", title, focus, names)
    focused = has_focus(focus)
    if not 2 <= len(rows) <= 12:
        warn_small("dumbbell", title, 0, f"{len(rows)} rows; keep to 3-12.")
    vals = [float(r["a"]) for r in rows] + [float(r["b"]) for r in rows]
    lo, hi, step = nice_bounds(min(vals), max(vals), 5, include_zero)
    size = typo.chart_label_size + 1
    name_w = min(max(text_width_pt(n, size, True) / 72 for n in names) + 0.3, 3.0)
    x0, x1 = left + name_w, left + width - 0.4
    y_top, y_bot = top + 0.1, bottom - 0.95
    rh = (y_bot - y_top) / max(len(rows), 1)

    def x_of(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    v = lo
    while v <= hi + 1e-9:   # faint vertical gridlines with the scale underneath
        x = x_of(v)
        add_line(slide, x, y_top, x, y_bot, color=pal.light_gray, width_pt=HAIRLINE_PT)
        tb = mark_axis(add_textbox(slide, x - 0.5, y_bot + 0.05, 1.0, 0.24))
        write_paragraph(tb.text_frame, fmt_num(v, fmt), size=typo.chart_axis_size,
                        color=pal.footer_gray, family=typo.family, align=PP_ALIGN.CENTER,
                        first=True)
        v += step
    for i, r in enumerate(rows):
        f = is_focus(focus, i, names[i])
        col = pal.bright_blue if f else (tint(pal.dark_navy, 0.55) if focused else pal.dark_navy)
        cy = y_top + (i + 0.5) * rh
        a, b = float(r["a"]), float(r["b"])
        xa_, xb_ = x_of(a), x_of(b)
        ln = add_line(slide, xa_, cy, xb_, cy, color=tint(col, 0.35), width_pt=4.0 if f else 3.0)
        ln.name = f"dumbbell:{names[i]}"
        d = 0.17 if f else 0.15
        add_oval(slide, xa_ - d / 2, cy - d / 2, d, d, fill=pal.white, line=col, line_width=1.75)
        add_oval(slide, xb_ - d / 2, cy - d / 2, d, d, fill=col)
        strong = f or not focused
        tb = add_textbox(slide, left, cy - 0.14, name_w - 0.15, 0.28, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, names[i], size=size, bold=strong,
                        color=pal.deep_navy if strong else pal.footer_gray, family=typo.family,
                        align=PP_ALIGN.RIGHT, first=True)
        (lo_x, lo_v), (hi_x, hi_v) = sorted(((xa_, a), (xb_, b)))
        for txt, x, al in ((fmt_num(lo_v, fmt), lo_x - 0.75, PP_ALIGN.RIGHT),
                           (fmt_num(hi_v, fmt), hi_x + 0.12, PP_ALIGN.LEFT)):
            tb = add_textbox(slide, x, cy - 0.12, 0.63, 0.24, anchor=MSO_ANCHOR.MIDDLE)
            write_paragraph(tb.text_frame, txt, size=typo.chart_label_size,
                            color=pal.text_dark if strong else pal.footer_gray,
                            family=typo.family, align=al, first=True)
    base = tint(pal.dark_navy, 0.55) if focused else pal.dark_navy
    legend_strip(slide, theme, [("ring", base, labels[0]), ("dot", base, labels[1])],
                 bottom - 0.42)
    return slide


# ---------------------------------------------------------------- bump

def add_bump(prs, *,
             title: str = "[Bump chart / Insert action title]",
             snapshots: Sequence[str],
             series: Sequence[Dict],
             focus=None,
             subtitle: Optional[str] = None,
             insight: Optional[str] = None,
             insight_label: Optional[str] = "Key insight",
             page_number=None, section_marker=None,
             source=None, footnote=None,
             theme: Theme = DEFAULT_THEME):
    """Rank movement across 3-6 ordered snapshots (position, not magnitude).
    snapshots: captions left to right. series: [{"name", "ranks": [1-based rank per
    snapshot, or None when absent]}] (4-10). Ranks sit on a fixed row pitch;
    straight segments, a dot at every vertex; labels at first and last appearance.
    focus: the series the title is about — accent, heavier line.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    names = [s.get("name", "") for s in series]
    check_focus("bump", title, focus, names)
    m = len(snapshots)
    if not 3 <= m <= 6:
        warn_small("bump", title, 0, f"{m} snapshots; bump needs 3-6 (2 → slopegraph).")
    for k in range(m):
        col = [s["ranks"][k] for s in series if k < len(s["ranks"]) and s["ranks"][k] is not None]
        if len(col) != len(set(col)):
            raise ValueError(f"bump \"{str(title)[:40]}\": duplicate rank in '{snapshots[k]}' ({col}).")
    focused = has_focus(focus)
    max_rank = max(r for s in series for r in s["ranks"] if r is not None)
    size = typo.chart_label_size + 1
    gw = min(max(text_width_pt(n, size, True) / 72 for n in names) + 0.75, 3.0)
    xa, xb = left + gw, left + width - gw
    ya, yb = top + 0.45, bottom - 0.2
    pitch = (yb - ya) / max(max_rank - 1, 1)
    xs = [xa + (xb - xa) * k / max(m - 1, 1) for k in range(m)]

    def y_of(r):
        return ya + (r - 1) * pitch
    for k, (x, cap) in enumerate(zip(xs, snapshots)):
        add_line(slide, x, ya - 0.1, x, yb + 0.1, color=pal.light_gray, width_pt=HAIRLINE_PT)
        eyebrow(slide, theme, x - 1.0, top, 2.0, cap, color=pal.text_dark, align=PP_ALIGN.CENTER)
    order = sorted(range(len(series)), key=lambda i: is_focus(focus, i, names[i]))
    for i in order:
        s = series[i]
        f = is_focus(focus, i, names[i])
        col = pal.bright_blue if f else (tint(pal.dark_navy, 0.6) if focused else pal.dark_navy)
        pts = [(xs[k], y_of(r)) for k, r in enumerate(s["ranks"][:m]) if r is not None]
        for (x0, y0), (x1, y1), k in zip(pts, pts[1:], range(len(pts))):
            ln = add_line(slide, x0, y0, x1, y1, color=col, width_pt=3.0 if f else 1.5)
            ln.name = f"bump:{names[i]}|{k}"
        for x, y in pts:
            d = 0.15 if f else 0.11
            add_oval(slide, x - d / 2, y - d / 2, d, d, fill=col, line=pal.white, line_width=0.75)
        ks = [k for k, r in enumerate(s["ranks"][:m]) if r is not None]
        if not ks:
            continue
        strong = f or not focused
        for k, side in ((ks[0], "left"), (ks[-1], "right")):
            r = s["ranks"][k]
            txt = f"{names[i]}  #{r}" if side == "left" else f"#{r}  {names[i]}"
            x = xs[k] - gw - 0.12 if side == "left" else xs[k] + 0.14
            tb = add_textbox(slide, x, y_of(r) - 0.13, gw, 0.26, anchor=MSO_ANCHOR.MIDDLE)
            write_paragraph(tb.text_frame, txt, size=size, bold=strong,
                            color=pal.deep_navy if strong else pal.footer_gray,
                            family=typo.family,
                            align=PP_ALIGN.RIGHT if side == "left" else PP_ALIGN.LEFT, first=True)
    return slide
