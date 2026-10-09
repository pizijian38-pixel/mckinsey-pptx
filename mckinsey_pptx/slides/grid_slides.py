"""Grid and set diagrams.

- heatmap : value per row x column cell, shaded on one sequential ramp (or a
            diverging one around a midpoint); the number is printed in the cell.
- radar   : 3-8 criteria x 2-5 series on one shared scale, as a native,
            editable PowerPoint radar chart.
- venn    : 2-3 overlapping sets with a label per intersection; focus = the
            "sweet spot".
Data marks are named "<kind>:<label>" so tests can measure them.
"""
from __future__ import annotations

import math
from typing import Dict, Optional, Sequence

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from ..base import add_line, add_oval, add_rect, add_textbox, write_paragraph
from ..design import (HAIRLINE_PT, check_focus, eyebrow, fit_size, fmt_num, has_focus, is_focus,
                      legend_strip, set_alpha, text_height_in, text_width_pt, tint, warn_small,
                      write_rich_paragraph)
from ..labels import loc
from ..theme import Theme, DEFAULT_THEME
from .evaluation_slides import _frame

MIN_PT = 10


def _mix(a, b, t):
    from pptx.dml.color import RGBColor
    return RGBColor(*(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))


# ---------------------------------------------------------------- heatmap

def heat_fill(theme, v, lo, hi, mid=None):
    """Fill for value v: sequential white -> navy, or diverging red <- white -> navy
    around `mid`. Returns (color, dark_text?)."""
    pal = theme.palette
    white = tint(pal.dark_navy, 0.95)
    if mid is None:
        t = 0.0 if hi == lo else (v - lo) / (hi - lo)
        return _mix(white, pal.dark_navy, 0.08 + 0.85 * t), t < 0.5
    span = max(hi - mid, mid - lo) or 1
    t = (v - mid) / span
    return (_mix(white, pal.dark_navy, 0.85 * t) if t >= 0
            else _mix(white, pal.status_red, 0.85 * -t)), abs(t) < 0.55


def add_heatmap(prs, *,
                title: str = "[Heat map / Insert action title]",
                rows: Sequence[str],
                columns: Sequence[str],
                values: Sequence[Sequence[Optional[float]]],
                fmt: Optional[str] = None,
                midpoint: Optional[float] = None,
                low_label: str = "Low", high_label: str = "High",
                focus=None,
                subtitle: Optional[str] = None,
                insight: Optional[str] = None,
                insight_label: Optional[str] = "Key insight",
                page_number=None, section_marker=None,
                source=None, footnote=None,
                theme: Theme = DEFAULT_THEME):
    """rows x columns grid (3-8 x 3-8); values[r][c] a number or None (blank cell).
    Shade = value on one ramp for the whole grid (white -> navy); pass midpoint=
    for a diverging scale (below = red, above = navy). The value is printed.
    focus: a cell "Row / Column", a whole row, or a whole column — outlined in the
           accent (colour stays the data).
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    nr, nc = len(rows), len(columns)
    if not 2 <= nr <= 10 or not 2 <= nc <= 10:
        warn_small("heatmap", title, 0, f"{nr} x {nc} grid; keep to 3-8 x 3-8.")
    cells = [f"{r} / {c}" for r in rows for c in columns]
    check_focus("heatmap", title, focus, list(rows) + list(columns) + cells)
    nums = [float(v) for row in values for v in row if v is not None]
    lo, hi = (min(nums), max(nums)) if nums else (0.0, 1.0)
    size = typo.chart_label_size + 1
    lab_w = min(max(text_width_pt(r, size, True) / 72 for r in rows) + 0.3, 3.2)
    gx, gy = left + lab_w, top + 0.45
    gw, gh = width - lab_w, bottom - gy - 0.55
    cw, ch = gw / nc, gh / nr
    gap = 0.04
    for j, c in enumerate(columns):
        f = has_focus(focus) and is_focus(focus, -1, c)
        tb = add_textbox(slide, gx + j * cw, top, cw, 0.4, anchor=MSO_ANCHOR.BOTTOM)
        write_paragraph(tb.text_frame, c, size=size, bold=True,
                        color=pal.mid_blue if f else pal.text_dark, family=typo.family,
                        align=PP_ALIGN.CENTER, first=True)
    hot = []
    for i, r in enumerate(rows):
        f = has_focus(focus) and is_focus(focus, -1, r)
        tb = add_textbox(slide, left, gy + i * ch, lab_w - 0.15, ch, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, r, size=size, bold=True,
                        color=pal.mid_blue if f else pal.text_dark, family=typo.family,
                        align=PP_ALIGN.RIGHT, first=True)
        for j, c in enumerate(columns):
            v = values[i][j] if j < len(values[i]) else None
            x, y = gx + j * cw + gap / 2, gy + i * ch + gap / 2
            if v is None:
                add_rect(slide, x, y, cw - gap, ch - gap, fill=pal.white, line=pal.light_gray,
                         line_width=HAIRLINE_PT)
                continue
            fill, dark = heat_fill(theme, float(v), lo, hi, midpoint)
            box = add_rect(slide, x, y, cw - gap, ch - gap, fill=fill)
            box.name = f"heatmap:{r} / {c}"
            tb = add_textbox(slide, x, y, cw - gap, ch - gap, anchor=MSO_ANCHOR.MIDDLE)
            write_paragraph(tb.text_frame, fmt_num(v, fmt), size=size,
                            color=pal.text_dark if dark else pal.white, family=typo.family,
                            align=PP_ALIGN.CENTER, first=True)
            if has_focus(focus) and (is_focus(focus, -1, r) or is_focus(focus, -1, c)
                                     or is_focus(focus, -1, f"{r} / {c}")):
                hot.append((x, y))
    for x, y in hot:   # accent outline on top of the shading: the colour stays the data
        add_rect(slide, x, y, cw - gap, ch - gap, line=pal.bright_blue, line_width=2.5)
    if midpoint is None:
        items = [("box", heat_fill(theme, lo, lo, hi)[0], f"{loc(theme, low_label)} {fmt_num(lo, fmt)}"),
                 ("box", heat_fill(theme, hi, lo, hi)[0], f"{loc(theme, high_label)} {fmt_num(hi, fmt)}")]
    else:
        items = [("box", heat_fill(theme, lo, lo, hi, midpoint)[0], f"{fmt_num(lo, fmt)}"),
                 ("box", heat_fill(theme, midpoint, lo, hi, midpoint)[0], f"{fmt_num(midpoint, fmt)}"),
                 ("box", heat_fill(theme, hi, lo, hi, midpoint)[0], f"{fmt_num(hi, fmt)}")]
    legend_strip(slide, theme, items, bottom - 0.42,
                 note=loc(theme, "Shade = value") if midpoint is None else None)
    return slide


# ---------------------------------------------------------------- radar

def add_radar(prs, *,
              title: str = "[Radar / Insert action title]",
              criteria: Sequence[str],
              series: Sequence[Dict],
              scale_max: float = 5,
              focus=None,
              side: Optional[Dict] = None,
              subtitle: Optional[str] = None,
              insight: Optional[str] = None,
              insight_label: Optional[str] = "Key insight",
              page_number=None, section_marker=None,
              source=None, footnote=None,
              theme: Theme = DEFAULT_THEME):
    """criteria: the axes (3-8). series: [{"name", "values": [one per criterion]}] (2-5),
    all on one scale 0..scale_max (normalise first — the shape is the message).
    Native PowerPoint radar chart (Edit Data works).
    focus: the series the title is about — accent, heavier line; others grey.
    side: {"title", "bullets"} — the reading of the chart, in a panel on the right.
    """
    from .framework_slides import _items, _write_items
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    names = [s.get("name", "") for s in series]
    check_focus("radar", title, focus, names)
    if not 3 <= len(criteria) <= 8 or not 1 <= len(series) <= 5:
        warn_small("radar", title, 0, f"{len(criteria)} axes x {len(series)} series; keep to "
                   "3-8 x 2-5 (else a table).")
    bad = [v for s in series for v in s.get("values", []) if v is None or not 0 <= float(v) <= scale_max]
    if bad:
        raise ValueError(f"radar \"{str(title)[:40]}\": values must lie in 0..{scale_max} on one "
                         f"scale (got {bad[:3]}); normalise them first.")
    focused = has_focus(focus)
    cw = width * 0.62 if side else width
    cd = CategoryChartData()
    cd.categories = list(criteria)
    for s in series:
        cd.add_series(s["name"], [float(v) for v in s["values"]])
    gf = slide.shapes.add_chart(XL_CHART_TYPE.RADAR_MARKERS, Inches(left), Inches(top),
                                Inches(cw), Inches(bottom - top), cd)
    gf.name = "radar:chart"
    chart = gf.chart
    chart.font.size = Pt(12)
    chart.font.name = typo.family
    chart.font.color.rgb = pal.text_dark
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(12)
    va = chart.value_axis
    va.minimum_scale, va.maximum_scale = 0, scale_max
    va.major_gridlines.format.line.color.rgb = pal.grid_gray
    va.tick_labels.font.size = Pt(10)
    va.tick_labels.font.color.rgb = pal.footer_gray
    greys = [tint(pal.dark_navy, t) for t in (0.45, 0.6, 0.72, 0.8)]
    for i, (s, ps) in enumerate(zip(series, chart.plots[0].series)):
        f = is_focus(focus, i, s["name"])
        col = (pal.bright_blue if f else greys[min(i, 3)]) if focused else \
            [pal.dark_navy, pal.bright_blue, pal.mid_blue, pal.footer_gray, pal.light_blue][i % 5]
        ps.format.line.color.rgb = col
        ps.format.line.width = Pt(3.0 if f else 1.75)
        ps.smooth = False
        mk = ps.marker
        mk.size = 7 if f or not focused else 5
        mk.format.fill.solid()
        mk.format.fill.fore_color.rgb = col
        mk.format.line.color.rgb = col
    if side:
        sx = left + cw + 0.3
        sw = width - cw - 0.3
        add_rect(slide, sx, top, sw, bottom - top, fill=pal.soft_gray)
        tb = add_textbox(slide, sx + 0.25, top + 0.2, sw - 0.5, 0.8)
        write_rich_paragraph(tb.text_frame, side.get("title", ""), size=15, theme=theme, bold=True,
                             first=True)
        th = text_height_in([side.get("title", "")], sw - 0.5, 15, bold=True) + 0.35
        its = _items(side)
        ss = fit_size(its or [" "], sw - 0.5, bottom - top - th - 0.4, max_size=15,
                      min_size=MIN_PT, para_gap_pt=8, indent_in=0.22)
        _write_items(slide, theme, sx + 0.25, top + th + 0.2, sw - 0.5, bottom - top - th - 0.3,
                     its, ss)
    return slide


# ---------------------------------------------------------------- venn

def add_venn(prs, *,
             title: str = "[Venn / Insert action title]",
             sets: Sequence[Dict],
             overlaps: Optional[Dict[str, str]] = None,
             focus=None,
             side: Optional[Dict] = None,
             subtitle: Optional[str] = None,
             insight: Optional[str] = None,
             insight_label: Optional[str] = "Key insight",
             page_number=None, section_marker=None,
             source=None, footnote=None,
             theme: Theme = DEFAULT_THEME):
    """sets: [{"name", "note"?}] (2-3) — what each circle stands for.
    overlaps: {"A & B": label, ..., "A & B & C": label} keyed by set names joined
              with " & " (any order) — what sits in each intersection.
    focus: one intersection key (the sweet spot) or a set name.
    side: {"title", "bullets"} — implication panel on the right.
    """
    from .framework_slides import _items, _write_items
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    n = len(sets)
    if n not in (2, 3):
        raise ValueError(f"venn \"{str(title)[:40]}\": 2 or 3 sets (got {n}); use a matrix for more.")
    names = [s.get("name", "") for s in sets]

    def key(k):
        return frozenset(p.strip().lower() for p in k.split("&"))
    ov = {key(k): (k, v) for k, v in (overlaps or {}).items()}
    lower = {nm.lower() for nm in names}
    for k in ov:
        if not k <= lower or len(k) < 2:
            warn_small("venn", title, 0, f"overlap '{ov[k][0]}' does not name 2+ of the sets {names}.")
    check_focus("venn", title, focus, names + [v[0] for v in ov.values()])
    focused = has_focus(focus)
    cw = width * 0.64 if side else width
    H = bottom - top
    cx, cy = left + cw / 2, top + H / 2
    if n == 2:
        R = min(H * 0.44, cw * 0.27)
        centres = [(cx - R * 0.6, cy), (cx + R * 0.6, cy)]
    else:   # centres on an equilateral triangle, side = R: every pair overlaps
        R = min(H / 2.95, cw / 3.2)
        h = R * math.sqrt(3) / 2
        centres = [(cx - R / 2, cy - h / 3), (cx + R / 2, cy - h / 3), (cx, cy + 2 * h / 3)]
    gx_, gy_ = sum(c[0] for c in centres) / n, sum(c[1] for c in centres) / n
    fills = [pal.dark_navy, pal.mid_blue, pal.bright_blue]
    for i, ((x, y), s) in enumerate(zip(centres, sets)):
        f = focused and is_focus(focus, i, names[i])
        o = add_oval(slide, x - R, y - R, 2 * R, 2 * R, fill=fills[i], line=fills[i],
                     line_width=2.5 if f else 1.0)
        set_alpha(o, 0.28 if f else 0.16)
        o.name = f"venn:{names[i]}"
    # set labels outside the circles, away from the centre
    for i, ((x, y), s) in enumerate(zip(centres, sets)):
        ux, uy = x - gx_, y - gy_
        L = math.hypot(ux, uy) or 1
        ux, uy = ux / L, uy / L
        lx, ly = x + ux * (R * 0.5), y + uy * (R * 0.5)
        lw = R * 0.9
        tb = add_textbox(slide, lx - lw / 2, ly - 0.35, lw, 0.7, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, names[i], size=15, bold=True, color=pal.deep_navy,
                        family=typo.family, align=PP_ALIGN.CENTER, first=True)
        if s.get("note"):
            write_rich_paragraph(tb.text_frame, s["note"], size=11, theme=theme,
                                 color=pal.footer_gray, align=PP_ALIGN.CENTER)
    # intersection labels at the centroid of the circles involved
    for k, (raw, lab) in ov.items():
        idx = [i for i, nm in enumerate(names) if nm.lower() in k]
        if len(idx) < 2:
            continue
        px = sum(centres[i][0] for i in idx) / len(idx)
        py = sum(centres[i][1] for i in idx) / len(idx)
        if n == 3 and len(idx) == 2:   # pair region: away from the third circle
            ox, oy = px - gx_, py - gy_
            L = math.hypot(ox, oy) or 1
            px, py = px + ox / L * R * 0.32, py + oy / L * R * 0.32
        f = focused and is_focus(focus, -1, raw)
        w = R * (0.62 if n == 2 else (0.5 if len(idx) == 3 else 0.55))
        h = 0.62 if n == 2 or len(idx) == 3 else 0.5
        if f:
            box = add_rect(slide, px - w / 2, py - h / 2, w, h, fill=pal.deep_navy)
            box.name = f"venn-sweet:{raw}"
        tb = add_textbox(slide, px - w / 2 + 0.05, py - h / 2, w - 0.1, h, anchor=MSO_ANCHOR.MIDDLE)
        sz = fit_size([lab], w - 0.1, h, max_size=13, min_size=MIN_PT, bold=True)
        write_rich_paragraph(tb.text_frame, lab, size=sz, theme=theme,
                             color=pal.white if f else pal.deep_navy, bold=True,
                             align=PP_ALIGN.CENTER, first=True)
    if side:
        sx = left + cw + 0.3
        sw = width - cw - 0.3
        add_rect(slide, sx, top, sw, bottom - top, fill=pal.soft_gray)
        tb = add_textbox(slide, sx + 0.25, top + 0.2, sw - 0.5, 0.8)
        write_rich_paragraph(tb.text_frame, side.get("title", ""), size=15, theme=theme, bold=True,
                             first=True)
        th = text_height_in([side.get("title", "")], sw - 0.5, 15, bold=True) + 0.35
        its = _items(side)
        ss = fit_size(its or [" "], sw - 0.5, bottom - top - th - 0.4, max_size=15,
                      min_size=MIN_PT, para_gap_pt=8, indent_in=0.22)
        _write_items(slide, theme, sx + 0.25, top + th + 0.2, sw - 0.5, bottom - top - th - 0.3,
                     its, ss)
    return slide
