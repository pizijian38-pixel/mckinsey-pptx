"""2x2 matrix: four labelled quadrants with items, or plotted points."""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from ..base import add_chrome, add_line, add_oval, add_rect, add_textbox, blank_slide, write_paragraph
from ..design import add_callout_bar, fit_size, tone_rgb, warn_small, write_rich_paragraph
from ..theme import Theme, DEFAULT_THEME


def add_matrix_2x2(prs, *,
                   title: str = "[2x2 matrix / Insert action title]",
                   x_label: str,
                   y_label: str,
                   quadrants: Sequence[Dict] = (),
                   points: Sequence[Dict] = (),
                   x_ends: Sequence[str] = ("Low", "High"),
                   y_ends: Sequence[str] = ("Low", "High"),
                   highlight: Optional[int] = None,
                   subtitle: Optional[str] = None,
                   insight: Optional[str] = None,
                   insight_label: Optional[str] = "Key insight",
                   page_number=None, section_marker=None,
                   source=None, footnote=None,
                   theme: Theme = DEFAULT_THEME):
    """quadrants (order: top-left, top-right, bottom-left, bottom-right):
         [{"title": str, "items"?: [str], "tone"?: str}]
    points: [{"label": str, "x": 0-1, "y": 0-1, "tone"?: str}] plotted on the grid
    highlight: quadrant index (0-3) to tint as the target / priority quadrant.
    Axes: x_label left→right (x_ends), y_label bottom→top (y_ends).
    """
    slide = blank_slide(prs)
    add_chrome(slide, title=title, theme=theme, page_number=page_number,
               section_marker=section_marker, source=source, footnote=footnote)
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

    axis_w, axis_h = 0.55, 0.45
    gx, gy = left + axis_w, top
    gw, gh = width - axis_w, bottom - top - axis_h
    qw, qh = (gw - 0.12) / 2, (gh - 0.12) / 2
    origins = [(gx, gy), (gx + qw + 0.12, gy), (gx, gy + qh + 0.12),
               (gx + qw + 0.12, gy + qh + 0.12)]

    q_paras = [[q.get("title", "")] + list(q.get("items", [])) for q in quadrants]
    size = min((fit_size(p, qw - 0.5, qh - 0.4, max_size=16, min_size=10, para_gap_pt=4,
                         indent_in=0.25) for p in q_paras), default=14)
    warn_small("matrix_2x2", title, size, "Shorten quadrant items.")
    for i, (x, y) in enumerate(origins):
        fill = pal.light_gray if highlight == i else pal.soft_gray
        add_rect(slide, x, y, qw, qh, fill=fill)
        if i < len(quadrants):
            q = quadrants[i]
            tone = q.get("tone")
            tb = add_textbox(slide, x + 0.25, y + 0.2, qw - 0.5, qh - 0.4)
            write_rich_paragraph(tb.text_frame, q.get("title", ""), size=size + 2,
                                 theme=theme, bold=True,
                                 color=tone_rgb(theme, tone) if tone else pal.text_dark,
                                 first=True, space_after=4)
            for it in q.get("items", []):
                write_rich_paragraph(tb.text_frame, it, size=size, theme=theme,
                                     bullet=True, space_before=3)
    # points
    for p in points:
        cx = gx + p["x"] * gw
        cy = gy + (1 - p["y"]) * gh
        d = 0.26
        add_oval(slide, cx - d / 2, cy - d / 2, d, d, fill=tone_rgb(theme, p.get("tone", "blue")))
        tb = add_textbox(slide, cx + d / 2 + 0.05, cy - 0.15, 2.2, 0.3, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, p["label"], size=12, bold=True, color=pal.text_dark,
                        family=typo.family, first=True)
    # axes
    add_line(slide, gx, gy + gh + 0.08, gx + gw, gy + gh + 0.08, color=pal.rule_gray, width_pt=1)
    add_line(slide, gx - 0.08, gy, gx - 0.08, gy + gh, color=pal.rule_gray, width_pt=1)
    from ..labels import loc
    x_ends = [loc(theme, t) for t in x_ends]
    y_ends = [loc(theme, t) for t in y_ends]
    for txt, x, al in ((x_ends[0], gx, PP_ALIGN.LEFT), (x_ends[1], gx + gw - 2, PP_ALIGN.RIGHT)):
        tb = add_textbox(slide, x, gy + gh + 0.12, 2, 0.3)
        write_paragraph(tb.text_frame, txt, size=11, color=pal.footer_gray,
                        family=typo.family, align=al, first=True)
    tb = add_textbox(slide, gx + gw / 2 - 2.5, gy + gh + 0.12, 5, 0.3)
    write_paragraph(tb.text_frame, x_label + "  →", size=12, bold=True, color=pal.text_dark,
                    family=typo.family, align=PP_ALIGN.CENTER, first=True)
    # vertical y-axis label: a wide box rotated 270° around its centre
    cx, cy = left + (axis_w - 0.1) / 2, gy + gh / 2
    bw, bh = min(5.0, gh), 0.35
    tb = add_textbox(slide, cx - bw / 2, cy - bh / 2, bw, bh, anchor=MSO_ANCHOR.MIDDLE)
    tb.rotation = 270
    write_paragraph(tb.text_frame, y_label + "  →", size=12, bold=True,
                    color=pal.text_dark, family=typo.family, align=PP_ALIGN.CENTER,
                    first=True)
    for txt, y in ((y_ends[1], gy), (y_ends[0], gy + gh - 0.3)):
        tb = add_textbox(slide, left - 0.05, y, axis_w - 0.1, 0.3)
        write_paragraph(tb.text_frame, txt, size=10, color=pal.footer_gray,
                        family=typo.family, align=PP_ALIGN.CENTER, first=True)
    return slide
