"""Qualitative diagrams.

- fishbone : one observed effect, causes grouped into 3-6 categories (bones),
             2-3 sub-causes per bone. focus = the confirmed root cause.
- journey  : what one customer does across 3-6 stages and how it feels; the
             sentiment line is the point of the slide. focus = the stage the
             title is about (usually the trough).
"""
from __future__ import annotations

import math
from typing import Dict, Optional, Sequence, Union

from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

from ..base import add_line, add_oval, add_rect, add_textbox, write_paragraph
from ..design import (HAIRLINE_PT, add_arrow, check_focus, eyebrow, fit_size, focus_tag,
                      has_focus, is_focus, set_dashed, text_height_in, text_width_pt, tint, warn_small,
                      write_rich_paragraph)
from ..labels import loc
from ..theme import Theme, DEFAULT_THEME
from .evaluation_slides import _frame

MIN_PT = 10


# ---------------------------------------------------------------- fishbone

def add_fishbone(prs, *,
                 title: str = "[Fishbone / Insert action title]",
                 effect: str,
                 causes: Sequence[Dict],
                 focus=None,
                 subtitle: Optional[str] = None,
                 insight: Optional[str] = None,
                 insight_label: Optional[str] = "Key insight",
                 page_number=None, section_marker=None,
                 source=None, footnote=None,
                 theme: Theme = DEFAULT_THEME):
    """effect: the observed problem (a symptom, not a fix).
    causes: [{"category", "items": [str, ...]}] (3-6 bones, 1-3 items each),
            named from the analysis — not an empty 6M checklist.
    focus: the confirmed root cause — a category (whole bone) or one item.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    causes = list(causes)
    labels = [c.get("category", "") for c in causes] + [i for c in causes
                                                        for i in c.get("items", [])]
    check_focus("fishbone", title, focus, labels)
    if not 2 <= len(causes) <= 6 or any(len(c.get("items", [])) > 3 for c in causes):
        warn_small("fishbone", title, 0, "keep to 3-6 categories with 1-3 causes each.")
    empty = [c.get("category", "") for c in causes if not c.get("items")]
    if empty:
        warn_small("fishbone", title, 0, f"categories without causes: {empty} — drop them.")

    cy = (top + bottom) / 2
    head_w = min(2.4, width * 0.2)
    head_x = left + width - head_w
    n_up = math.ceil(len(causes) / 2)
    slot = (head_x - 0.3 - left - 0.1) / max(n_up, 1)
    tag_h = 0.36
    bh = (bottom - top) / 2 - tag_h - 0.05
    dx = bh * math.tan(math.radians(30))
    tag_w = min(slot - 0.25, 2.2)
    lab_w = slot - dx * 0.15 - 0.4
    # Cause labels are sentences, so they get body size (12-13pt): the largest
    # size at which every label fits between its neighbours on the bone.
    def fits(sz):
        for c in causes:
            items = list(c.get("items", []))
            gap = bh / (len(items) + 1)
            if any(text_height_in([it], lab_w, sz) > gap * 0.95 for it in items):
                return False
            if text_width_pt(c.get("category", ""), sz, True) / 72 > tag_w - 0.15:
                return False
        return True
    size = next((sz for sz in (13, 12, 11, 10) if fits(sz)), 10)
    warn_small("fishbone", title, size, "Shorten the cause labels or use fewer causes per bone.")

    add_line(slide, left, cy, head_x - 0.04, cy, color=pal.text_dark, width_pt=1.5)
    add_arrow(slide, head_x - 0.3, cy, head_x - 0.02, cy, color=pal.text_dark, width_pt=1.5)
    for k, c in enumerate(causes):
        j, up = k // 2, k % 2 == 0
        sgn = -1 if up else 1
        ax = head_x - 0.3 - j * slot
        fx, fy = ax - dx, cy + sgn * bh
        hot = is_focus(focus, -1, c.get("category", ""))
        ln = add_line(slide, ax, cy, fx, fy, color=pal.bright_blue if hot else pal.text_dark,
                      width_pt=2.25 if hot else 1.0)
        ln.name = f"fishbone:{c.get('category', '')}"
        tx, ty = fx - tag_w / 2, (fy - tag_h) if up else fy
        add_rect(slide, tx, ty, tag_w, tag_h, fill=pal.bright_blue if hot else pal.white,
                 line=None if hot else pal.deep_navy, line_width=None if hot else 1.0)
        tb = add_textbox(slide, tx, ty, tag_w, tag_h, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, c.get("category", ""), size=size, bold=True,
                        color=pal.white if hot else pal.deep_navy, family=typo.family,
                        align=PP_ALIGN.CENTER, first=True)
        items = list(c.get("items", []))
        m = len(items)
        for i, it in enumerate(items):
            t = (i + 1) / (m + 1)              # fraction from the far end toward the spine
            px, py = fx + (ax - fx) * t, fy + (cy - fy) * t
            f = hot or is_focus(focus, -1, it)
            add_line(slide, px - 0.22, py, px, py,
                     color=pal.bright_blue if f else pal.rule_gray, width_pt=HAIRLINE_PT)
            h = text_height_in([it], lab_w, size) + 0.04
            tb = add_textbox(slide, px - 0.27 - lab_w, py - h / 2, lab_w, h,
                             anchor=MSO_ANCHOR.MIDDLE)
            write_rich_paragraph(tb.text_frame, it, size=size, theme=theme, bold=f,
                                 color=pal.deep_navy if f else pal.text_dark,
                                 align=PP_ALIGN.RIGHT, first=True)
    eh = min(1.6, bottom - top - 0.4)
    add_rect(slide, head_x, cy - eh / 2, head_w, eh, fill=pal.deep_navy)
    eyebrow(slide, theme, head_x + 0.15, cy - eh / 2 + 0.08, head_w - 0.3, "Effect",
            color=pal.light_blue, size=9)
    es = fit_size([effect], head_w - 0.3, eh - 0.5, max_size=16, min_size=MIN_PT, bold=True)
    tb = add_textbox(slide, head_x + 0.15, cy - eh / 2 + 0.34, head_w - 0.3, eh - 0.44,
                     anchor=MSO_ANCHOR.MIDDLE)
    write_rich_paragraph(tb.text_frame, effect, size=es, theme=theme, color=pal.white, bold=True,
                         first=True)
    return slide


# ---------------------------------------------------------------- journey

_SENT = {"very positive": 2, "positive": 1, "neutral": 0, "negative": -1, "very negative": -2}


def _sent(v) -> float:
    if isinstance(v, str):
        return float(_SENT.get(v.strip().lower(), 0))
    return max(-2.0, min(2.0, float(v)))


def add_journey(prs, *,
                title: str = "[Customer journey / Insert action title]",
                stages: Sequence[Dict],
                persona: Optional[str] = None,
                row_labels: Sequence[str] = ("Actions", "Touchpoints", "Pain points"),
                focus=None,
                focus_label: Optional[str] = None,
                subtitle: Optional[str] = None,
                insight: Optional[str] = None,
                insight_label: Optional[str] = "Key insight",
                page_number=None, section_marker=None,
                source=None, footnote=None,
                theme: Theme = DEFAULT_THEME):
    """stages: [{"name", "sentiment", "action"?, "touchpoint"?, "pain"?}] (3-6), one persona.
    sentiment: -2..2 or "very negative" | "negative" | "neutral" | "positive" |
               "very positive" — named levels, not a score.
    pain: a short pain point, drawn as a dashed red tag (at most 2 per journey).
    focus: the stage the title is about (usually the trough) — accent dot and
           the segment into it.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle or persona, insight, insight_label,
        page_number=page_number, section_marker=section_marker, source=source,
        footnote=footnote)
    pal, typo = theme.palette, theme.typography
    stages = list(stages)
    n = len(stages)
    names = [s.get("name", "") for s in stages]
    check_focus("journey", title, focus, names)
    if not 3 <= n <= 6:
        warn_small("journey", title, 0, f"{n} stages; keep to 3-6 (split acquisition / retention).")
    pains = [s for s in stages if s.get("pain")]
    if len(pains) > 2:
        warn_small("journey", title, 0, f"{len(pains)} pain points; mark at most 2 or none is focal.")

    lab_w = 1.35
    cw = (width - lab_w) / max(n, 1)
    xs = [left + lab_w + i * cw for i in range(n)]
    size = typo.body_size
    # header
    for i, s in enumerate(stages):
        f = is_focus(focus, i, names[i])
        eyebrow(slide, theme, xs[i] + 0.1, top, cw - 0.2, f"{loc(theme, 'Stage')} {i + 1}",
                color=pal.bright_blue if f else pal.footer_gray, size=9, align=PP_ALIGN.CENTER)
        tb = add_textbox(slide, xs[i] + 0.05, top + 0.24, cw - 0.1, 0.34, anchor=MSO_ANCHOR.TOP)
        write_paragraph(tb.text_frame, names[i], size=size + 1, bold=True, color=pal.deep_navy,
                        family=typo.family, align=PP_ALIGN.CENTER, first=True)
    # rows below the sentiment band, sized to their text
    rows = []
    for key, lab in zip(("action", "touchpoint", "pain"), row_labels):
        if any(s.get(key) for s in stages):
            rh = max(text_height_in([s.get(key) or " "], cw - 0.3, size - (1 if key != "action"
                                                                          else 0))
                     for s in stages) + (0.3 if key == "pain" else 0.2)
            rows.append((key, lab, rh))
    band_top = top + 0.75
    band_h = max(1.3, bottom - band_top - sum(r[2] for r in rows) - 0.25)
    levels = [(1, "Positive"), (0, "Neutral"), (-1, "Negative")]

    def y_of(v):
        return band_top + 0.15 + (2 - v) / 4 * (band_h - 0.3)
    for v, lab in levels:
        y = y_of(v * 2)
        add_line(slide, xs[0], y, left + width, y, color=pal.light_gray, width_pt=HAIRLINE_PT)
        eyebrow(slide, theme, left, y - 0.12, lab_w - 0.1, lab, size=9)
    pts = [(xs[i] + cw / 2, y_of(_sent(s.get("sentiment", 0)))) for i, s in enumerate(stages)]
    focal = [i for i in range(n) if is_focus(focus, i, names[i])]
    for i in range(1, n):
        hot = i in focal
        ln = add_line(slide, *pts[i - 1], *pts[i], color=pal.bright_blue if hot else pal.dark_navy,
                      width_pt=2.5 if hot else 1.75)
        ln.name = f"journey:{names[i - 1]}→{names[i]}"
    for i, (x, y) in enumerate(pts):
        hot = i in focal
        d = 0.2 if hot else 0.15
        add_oval(slide, x - d / 2, y - d / 2, d, d, fill=pal.bright_blue if hot else pal.dark_navy,
                 line=pal.white, line_width=1.0)
        if hot and focus_label:
            focus_tag(slide, theme, x + 0.15, y - 0.36, focus_label)
    # content rows
    y = band_top + band_h + 0.1
    for key, lab, rh in rows:
        add_line(slide, left, y, left + width, y, color=pal.grid_gray, width_pt=HAIRLINE_PT)
        eyebrow(slide, theme, left, y + 0.08, lab_w - 0.1, lab, color=pal.text_dark, size=9,
                anchor=MSO_ANCHOR.TOP)
        for i, s in enumerate(stages):
            txt = s.get(key)
            if not txt:
                continue
            if key == "pain":
                bx, by, bw, bh_ = xs[i] + 0.12, y + 0.1, cw - 0.24, rh - 0.18
                box = add_rect(slide, bx, by, bw, bh_, fill=tint(pal.status_red, 0.92))
                set_dashed(box, pal.status_red, 1.0)
                tb = add_textbox(slide, bx + 0.08, by, bw - 0.16, bh_, anchor=MSO_ANCHOR.MIDDLE)
                write_rich_paragraph(tb.text_frame, txt, size=size - 1, theme=theme,
                                     color=pal.text_dark, align=PP_ALIGN.CENTER, first=True)
            else:
                tb = add_textbox(slide, xs[i] + 0.15, y + 0.1, cw - 0.3, rh - 0.1)
                write_rich_paragraph(tb.text_frame, txt, size=size - (0 if key == "action" else 1),
                                     theme=theme,
                                     color=pal.text_dark if key == "action" else pal.footer_gray,
                                     align=PP_ALIGN.CENTER, first=True)
        y += rh
    return slide
