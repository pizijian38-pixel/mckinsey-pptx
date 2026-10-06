"""Planning templates: roadmap (workstreams x periods) and timeline (dated events)."""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

from ..base import add_chrome, add_line, add_oval, add_rect, add_textbox, blank_slide, write_paragraph
from ..design import (add_callout_bar, fit_one_line, fit_size, text_width_pt, tone_rgb,
                      warn_small, write_rich_paragraph)
from ..theme import Theme, DEFAULT_THEME


def _frame(prs, theme, title, subtitle, insight, insight_label, **chrome):
    slide = blank_slide(prs)
    add_chrome(slide, title=title, theme=theme, **chrome)
    pal, typo, layout = theme.palette, theme.typography, theme.layout
    left = layout.margin_left_in
    width = layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
    top = layout.body_top_in + 0.05
    bottom = layout.footer_top_in - 0.25
    if subtitle:
        tb = add_textbox(slide, left, top, width, 0.35)
        write_paragraph(tb.text_frame, subtitle, size=typo.section_title_size,
                        bold=True, color=pal.text_dark, family=typo.family, first=True)
        top += 0.45
    if insight:
        h = 0.7
        add_callout_bar(slide, theme, left, bottom - h, width, h, insight,
                        label=insight_label)
        bottom -= h + 0.25
    return slide, left, top, width, bottom


def _diamond(slide, cx, cy, d, rgb):
    s = slide.shapes.add_shape(MSO_SHAPE.DIAMOND, Inches(cx - d / 2), Inches(cy - d / 2),
                               Inches(d), Inches(d))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def add_roadmap(prs, *,
                title: str = "[Roadmap / Insert action title]",
                periods: Sequence[str],
                lanes: Sequence[Dict],
                milestones: Sequence[Dict] = (),
                subtitle: Optional[str] = None,
                insight: Optional[str] = None,
                insight_label: Optional[str] = "Key insight",
                page_number=None, section_marker=None,
                source=None, footnote=None,
                theme: Theme = DEFAULT_THEME):
    """periods: column labels, e.g. ["Q1", "Q2", "Q3", "Q4"] or months.
    lanes: [{"name": str, "items": [{"label": str, "start": num, "end": num,
             "tone"?: str}]}] — start/end are 0-based period indices and the
             bar runs from the start of period `start` to the end of period
             `end` (start=1, end=2 -> Q2 to Q3). Add .5 to begin mid-period.
    milestones: [{"label": str, "at": num, "tone"?: str}] — `at` is a position
             on the same axis: 0 = start of the first period, 4 = end of the
             fourth (at=2 -> the boundary between period 2 and 3).
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    lane_w = 2.3
    gx, gw = left + lane_w, width - lane_w
    n_p = max(len(periods), 1)
    pw = gw / n_p
    head_h = 0.42
    ms_h = 0.85 if milestones else 0

    # sub-rows per lane so overlapping bars don't collide
    lane_rows = []
    for ln in lanes:
        rows_end = []
        placed = []
        for it in sorted(ln.get("items", []), key=lambda t: t["start"]):
            # a bar occupies [start, end + 1) in period units
            for ri, end in enumerate(rows_end):
                if it["start"] >= end:
                    rows_end[ri] = it["end"] + 1
                    placed.append((ri, it))
                    break
            else:
                rows_end.append(it["end"] + 1)
                placed.append((len(rows_end) - 1, it))
        lane_rows.append((max(len(rows_end), 1), placed))
    total_sub = sum(n for n, _ in lane_rows) or 1
    avail = bottom - top - head_h - ms_h
    sub_h = min(0.85, avail / total_sub)
    bar_h = sub_h * 0.72

    # header
    for i, p in enumerate(periods):
        x = gx + i * pw
        add_rect(slide, x + 0.02, top, pw - 0.04, head_h, fill=pal.deep_navy)
        tb = add_textbox(slide, x, top, pw, head_h, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, p, size=min(14, fit_one_line(p, pw - 0.1, 14, 9, True)),
                        bold=True, color=pal.white, family=typo.family,
                        align=PP_ALIGN.CENTER, first=True)
    y = top + head_h

    def px(at):
        return gx + (at + 0.0) * pw

    if milestones:
        line_y = y + 0.2
        add_line(slide, gx, line_y, gx + gw, line_y, color=pal.rule_gray, width_pt=0.75)
        row_right = [-1e9, -1e9]          # two label rows; drop to row 2 on collision
        for m in sorted(milestones, key=lambda m: m["at"]):
            cx = px(min(max(m["at"], 0), n_p))
            _diamond(slide, cx, line_y, 0.22, tone_rgb(theme, m.get("tone", "amber")))
            size = 11
            text_w = text_width_pt(m["label"], size, True) / 72 + 0.15
            lx = min(max(cx - text_w / 2, gx), gx + gw - text_w)
            row = 0 if lx > row_right[0] + 0.05 else 1
            row_right[row] = lx + text_w
            tb = add_textbox(slide, lx, line_y + 0.13 + row * 0.28, text_w, 0.26)
            write_paragraph(tb.text_frame, m["label"], size=size, bold=True,
                            color=pal.text_dark, family=typo.family,
                            align=PP_ALIGN.CENTER, first=True)
        y += ms_h

    grid_top = y
    grid_bottom = y + sum(n for n, _ in lane_rows) * sub_h
    for i in range(1, n_p):          # behind the bars
        add_line(slide, gx + i * pw, grid_top, gx + i * pw, grid_bottom,
                 color=pal.grid_gray, width_pt=0.5)
    sizes = []
    for (n_sub, placed), ln in zip(lane_rows, lanes):
        lane_h = n_sub * sub_h
        add_rect(slide, left, y + 0.03, lane_w - 0.1, lane_h - 0.06, fill=pal.light_gray)
        tb = add_textbox(slide, left + 0.15, y, lane_w - 0.35, lane_h, anchor=MSO_ANCHOR.MIDDLE)
        ls = fit_size([ln["name"]], lane_w - 0.35, lane_h - 0.06, max_size=14, min_size=10)
        write_rich_paragraph(tb.text_frame, ln["name"], size=ls, theme=theme,
                             bold=True, first=True)
        for ri, it in placed:
            x0 = px(max(0, it["start"])) + 0.04
            x1 = px(min(n_p, it["end"] + 1)) - 0.04
            by = y + ri * sub_h + (sub_h - bar_h) / 2
            rgb = tone_rgb(theme, it.get("tone", "blue"))
            add_rect(slide, x0, by, x1 - x0, bar_h, fill=rgb)
            s = fit_one_line(it["label"], x1 - x0 - 0.16, 14 if bar_h > 0.5 else 13, 9, bold=True)
            sizes.append(s)
            tb = add_textbox(slide, x0 + 0.08, by, x1 - x0 - 0.16, bar_h,
                             anchor=MSO_ANCHOR.MIDDLE)
            write_paragraph(tb.text_frame, it["label"], size=s, bold=True,
                            color=pal.text_dark if it.get("tone") in ("light_blue", "amber")
                            else pal.white, family=typo.family, first=True)
        y += lane_h
        add_line(slide, left, y, left + width, y, color=pal.grid_gray, width_pt=0.5)
    if sizes:
        warn_small("roadmap", title, min(sizes),
                   "Shorten bar labels or give the item a longer span.")
    return slide


def add_timeline(prs, *,
                 title: str = "[Timeline / Insert action title]",
                 events: Sequence[Dict],
                 subtitle: Optional[str] = None,
                 insight: Optional[str] = None,
                 insight_label: Optional[str] = "Key insight",
                 page_number=None, section_marker=None,
                 source=None, footnote=None,
                 theme: Theme = DEFAULT_THEME):
    """events (chronological, 3-7): [{"date": str, "title": str, "body"?: str,
    "tone"?: str}] on a horizontal line; text alternates above and below."""
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    n = max(len(events), 1)
    mid = (top + bottom) / 2
    add_line(slide, left, mid, left + width, mid, color=pal.deep_navy, width_pt=2.5)
    slot = width / n
    box_w = min(slot * 1.7, 3.6)
    box_h = (bottom - top) / 2 - 0.35
    paras_all = [[e.get("title", "")] + ([e["body"]] if e.get("body") else []) for e in events]
    size = min(fit_size(p, box_w, box_h - 0.4, max_size=18, min_size=10, para_gap_pt=4)
               for p in paras_all) if events else 13
    warn_small("timeline", title, size, "Shorten event text or use fewer events.")
    for i, e in enumerate(events):
        cx = left + slot * (i + 0.5)
        tone = e.get("tone", "blue")
        add_oval(slide, cx - 0.14, mid - 0.14, 0.28, 0.28, fill=tone_rgb(theme, tone))
        above = i % 2 == 0
        add_line(slide, cx, mid + (-0.14 if above else 0.14), cx,
                 mid + (-0.32 if above else 0.32), color=pal.rule_gray, width_pt=0.75)
        bx = min(max(cx - box_w / 2, left), left + width - box_w)
        by = mid - 0.35 - box_h if above else mid + 0.35
        tb = add_textbox(slide, bx, by, box_w, box_h,
                         anchor=MSO_ANCHOR.BOTTOM if above else MSO_ANCHOR.TOP)
        write_paragraph(tb.text_frame, e.get("date", ""), size=size, bold=True,
                        color=tone_rgb(theme, tone), family=typo.family,
                        align=PP_ALIGN.CENTER, first=True)
        write_rich_paragraph(tb.text_frame, e.get("title", ""), size=size, theme=theme,
                             bold=True, align=PP_ALIGN.CENTER, space_before=2)
        if e.get("body"):
            write_rich_paragraph(tb.text_frame, e["body"], size=size - 1, theme=theme,
                                 align=PP_ALIGN.CENTER, space_before=2)
    return slide
