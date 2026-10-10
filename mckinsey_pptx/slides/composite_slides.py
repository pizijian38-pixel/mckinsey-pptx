"""Composite slide: a grid of regions, each holding one component.

    b.add("composite", title=...,
          columns=[[{"type": "flow", "heading": "Business model", ...},
                    {"type": "kv_table", "heading": "Unit economics", ...}],
                   [{"type": "cards", "cards": [...], "columns": 2}]],
          widths=[1.2, 1], insight="...", insight_label="Verdict")

`columns` is a list of columns; each column is one region (dict) or a list
of regions stacked top to bottom (`weight` sets their height share).

Logic options (for pages that read left to right as one argument —
"current situation -> strategy -> advantages -> disadvantages"):
- headers=[...]          one header per column (str or {"text", "dark": bool})
- header_style=          "chevron" | "rule" | "bar"
- connectors=True        arrow between consecutive columns
- region "arrow": True   down arrow from the region above (same column)
- region "panel":        True (gray) | "outline" | "tint"
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Union

from ..base import add_chrome, add_textbox, blank_slide, write_paragraph
from ..components import draw_region
from ..design import add_callout_bar, add_icon, add_stage_banners, add_wedge, tint
from ..theme import Theme, DEFAULT_THEME

COL_GAP = 0.35
CONNECTOR_GAP = 0.55
ROW_GAP = 0.25
ARROW_GAP = 0.42

Region = Dict
Column = Union[Region, List[Region]]


def add_composite(prs, *,
                  title: str = "[Composite / Insert action title]",
                  columns: Sequence[Column],
                  widths: Optional[Sequence[float]] = None,
                  headers: Optional[Sequence[Union[str, Dict]]] = None,
                  header_style: Optional[str] = None,
                  connectors: bool = False,
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
    gap = CONNECTOR_GAP if connectors else COL_GAP
    avail_w = width - gap * (len(cols) - 1)
    col_ws = [avail_w * wt / tot for wt in weights]
    col_xs = []
    x = left
    for cw in col_ws:
        col_xs.append(x)
        x += cw + gap

    if headers:
        style = header_style or ("chevron" if connectors else "rule")
        spans = []
        for cx, cw, hd in zip(col_xs, col_ws, headers):
            if hd is None:
                continue
            text = hd.get("text", "") if isinstance(hd, dict) else str(hd)
            dark = bool(hd.get("dark")) if isinstance(hd, dict) else False
            spans.append((cx, cw, text, "result" if dark else "stage"))
        hh = 0.42
        add_stage_banners(slide, theme, spans, top, hh, style=style, where=title)
        top += hh + 0.15

    for cx, cw, col in zip(col_xs, col_ws, cols):
        gaps = [0.0] + [ARROW_GAP if r.get("arrow") else ROW_GAP for r in col[1:]]
        hs = [float(r.get("weight", 1.0)) for r in col]
        avail_h = bottom - top - sum(gaps)
        y = top
        for k, (region, hw) in enumerate(zip(col, hs)):
            if k and region.get("arrow"):
                g = gaps[k]
                add_wedge(slide, cx + cw / 2 - 0.22, y - g + (g - 0.2) / 2, 0.44, 0.2,
                          tint(pal.mid_blue, 0.3), direction="down")
            rh = avail_h * hw / sum(hs)
            draw_region(slide, theme, cx, y, cw, rh, region, where=title)
            y += rh + (gaps[k + 1] if k + 1 < len(gaps) else 0)
    if connectors:
        d = 0.34
        cy = top + (bottom - top) / 2 - d / 2
        for i in range(len(cols) - 1):
            ax = col_xs[i] + col_ws[i] + (gap - d) / 2
            add_icon(slide, "arrow_right", ax, cy, d, theme, "light_blue")
    return slide
