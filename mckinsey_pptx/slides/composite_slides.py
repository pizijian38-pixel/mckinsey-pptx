"""Composite slide: a grid of regions, each holding one component.

    b.add("composite", title=...,
          columns=[[{"type": "flow", "heading": "Business model", ...},
                    {"type": "kv_table", "heading": "Unit economics", ...}],
                   [{"type": "cards", "cards": [...], "columns": 2}]],
          widths=[1.2, 1], insight="...", insight_label="Verdict")

`columns` is a list of columns; each column is one region (dict) or a list
of regions stacked top to bottom (`weight` sets their height share).
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Union

from ..base import add_chrome, add_textbox, blank_slide, write_paragraph
from ..components import draw_region
from ..design import add_callout_bar
from ..theme import Theme, DEFAULT_THEME

COL_GAP = 0.35
ROW_GAP = 0.25

Region = Dict
Column = Union[Region, List[Region]]


def add_composite(prs, *,
                  title: str = "[Composite / Insert action title]",
                  columns: Sequence[Column],
                  widths: Optional[Sequence[float]] = None,
                  subtitle: Optional[str] = None,
                  insight: Optional[str] = None,
                  insight_label: Optional[str] = "Key insight",
                  page_number=None, section_marker=None,
                  source=None, footnote=None,
                  theme: Theme = DEFAULT_THEME):
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
        bottom -= h + ROW_GAP

    cols = [c if isinstance(c, list) else [c] for c in columns]
    weights = list(widths) if widths else [1.0] * len(cols)
    tot = sum(weights)
    avail_w = width - COL_GAP * (len(cols) - 1)
    x = left
    for col, wt in zip(cols, weights):
        cw = avail_w * wt / tot
        hs = [float(r.get("weight", 1.0)) for r in col]
        avail_h = bottom - top - ROW_GAP * (len(col) - 1)
        y = top
        for region, hw in zip(col, hs):
            rh = avail_h * hw / sum(hs)
            draw_region(slide, theme, x, y, cw, rh, region, where=title)
            y += rh + ROW_GAP
        x += cw + COL_GAP
    return slide
