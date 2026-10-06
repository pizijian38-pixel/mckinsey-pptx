"""Tier ladder: ascending tiers (price architecture, portfolio pyramid,
maturity levels) drawn as a staircase rising left to right."""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from ..base import add_chrome, add_rect, add_textbox, blank_slide, write_paragraph
from ..design import (warn_small, add_callout_bar, fit_one_line, fit_size, tone_rgb,
                      write_rich_paragraph)
from ..theme import Theme, DEFAULT_THEME

_LADDER_TONES = ("light_blue", "blue", "navy", "navy", "navy")


def add_tier_ladder(prs, *,
                    title: str = "[Tier ladder / Insert action title]",
                    tiers: Sequence[Dict],
                    subtitle: Optional[str] = None,
                    insight: Optional[str] = None,
                    insight_label: Optional[str] = "Key insight",
                    page_number=None, section_marker=None,
                    source=None, footnote=None,
                    theme: Theme = DEFAULT_THEME):
    """tiers (lowest first): [{"name": str, "value"?: str (e.g. "35-55 RMB"),
        "lines"?: [str] (e.g. products), "label"?: str (caption for `details`),
        "details"?: [str] (e.g. channels), "tone"?: str}]
    Strings accept **bold** and {tone|coloured} markup.
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
                        bold=True, color=pal.text_dark, family=typo.family,
                        first=True)
        top += 0.45
    if insight:
        h = 0.7
        add_callout_bar(slide, theme, left, bottom - h, width, h, insight,
                        label=insight_label)
        bottom -= h + 0.25

    n = max(len(tiers), 1)
    gap = 0.2
    col_w = (width - gap * (n - 1)) / n
    full_h = bottom - top
    head_h = 0.55
    pad = 0.2

    def col_h(i):
        return full_h * (0.66 + 0.34 * (i / (n - 1) if n > 1 else 1))

    # fitted body size across all tiers
    sizes = []
    for i, t in enumerate(tiers):
        paras = list(t.get("lines", [])) + ([t["label"]] if t.get("label") else []) \
            + list(t.get("details", []))
        avail = col_h(i) - head_h - 2 * pad - (0.8 if t.get("value") else 0)
        sizes.append(fit_size(paras or [" "], col_w - 2 * pad, max(avail, 0.4),
                              max_size=15, min_size=10, para_gap_pt=5))
    size = min(sizes) if sizes else 13
    warn_small("tier_ladder", title, size, "Shorten tier lines / details.")

    for i, t in enumerate(tiers):
        h = col_h(i)
        x = left + i * (col_w + gap)
        y = bottom - h
        tone = t.get("tone") or _LADDER_TONES[min(i, len(_LADDER_TONES) - 1)]
        rgb = tone_rgb(theme, tone)
        add_rect(slide, x, y, col_w, h, fill=pal.soft_gray)
        add_rect(slide, x, y, col_w, head_h, fill=rgb)
        tb = add_textbox(slide, x + pad, y, col_w - 2 * pad, head_h,
                         anchor=MSO_ANCHOR.MIDDLE)
        on_light = tone in ("light_blue", "amber")
        write_paragraph(tb.text_frame, t.get("name", ""), size=size + 3, bold=True,
                        color=pal.text_dark if on_light else pal.white, family=typo.family, align=PP_ALIGN.CENTER,
                        first=True)
        cy = y + head_h + pad
        if t.get("value"):
            tb = add_textbox(slide, x + pad, cy, col_w - 2 * pad, 0.65,
                             anchor=MSO_ANCHOR.MIDDLE)
            vsize = fit_one_line(t["value"], col_w - 2 * pad, 30, 14, bold=True)
            write_rich_paragraph(tb.text_frame, t["value"], size=vsize, theme=theme,
                                 color=pal.text_dark if tone == "light_blue" else rgb,
                                 bold=True, align=PP_ALIGN.CENTER, first=True)
            cy += 0.8
        tb = add_textbox(slide, x + pad, cy, col_w - 2 * pad, y + h - pad - cy)
        first = True
        for line in t.get("lines", []):
            write_rich_paragraph(tb.text_frame, line, size=size, theme=theme,
                                 bold=True, align=PP_ALIGN.CENTER, first=first,
                                 space_before=0 if first else 3)
            first = False
        if t.get("label"):
            write_paragraph(tb.text_frame, t["label"], size=size - 1, bold=True,
                            color=pal.mid_blue, family=typo.family,
                            align=PP_ALIGN.CENTER, first=first,
                            space_before=0 if first else 10)
            first = False
        for d in t.get("details", []):
            write_rich_paragraph(tb.text_frame, d, size=size, theme=theme,
                                 align=PP_ALIGN.CENTER, first=first,
                                 space_before=0 if first else 3)
            first = False
    return slide
