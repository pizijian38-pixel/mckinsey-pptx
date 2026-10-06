"""Card grids: the workhorse layout for structured content.

- card_grid: 2-8 cards (icon + header + body/bullets, or a big value),
  optional intro banner on top and key-insight bar at the bottom.
  Text size is fitted to the space, so short content gets larger type
  instead of empty cards.
- swot: a 2x2 card grid with fixed S / W / O / T colours and icons.
"""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from pptx.enum.text import MSO_ANCHOR

from ..base import add_chrome, add_rect, add_textbox, blank_slide, write_paragraph
from ..design import (warn_small, add_callout_bar, add_icon, fit_one_line, fit_size, text_height_in,
                      tone_rgb, write_rich_paragraph)
from ..theme import Theme, DEFAULT_THEME

GAP = 0.25
PAD = 0.22


def _auto_columns(n: int, has_values: bool) -> int:
    if n <= 3:
        return n
    if n == 4:
        return 4 if has_values else 2
    if n <= 6:
        return 3
    return 4


def _card_paras(card: Dict):
    paras = []
    if card.get("body"):
        paras.append(card["body"])
    paras += list(card.get("bullets", []))
    return paras


def add_card_grid(prs, *,
                  title: str = "[Card grid / Insert action title]",
                  cards: Sequence[Dict],
                  subtitle: Optional[str] = None,
                  intro: Optional[str] = None,
                  insight: Optional[str] = None,
                  insight_label: Optional[str] = "Key insight",
                  columns: Optional[int] = None,
                  page_number=None, section_marker=None,
                  source=None, footnote=None,
                  theme: Theme = DEFAULT_THEME):
    """cards: [{"title": str, "body"?: str, "bullets"?: [str], "icon"?: str,
                "tone"?: str, "value"?: str}]
    - icon: a bundled icon name (see CATALOG) or 1-2 characters ("1", "A").
    - tone: navy | blue | mid_blue | light_blue | red | green | amber | gray.
    - value: big number shown at the top of the card (KPI / target cards).
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
    if intro:
        h = 0.75
        add_rect(slide, left, top, width, h, fill=pal.deep_navy)
        size = fit_size([intro], width - 0.6, h - 0.15, max_size=16, min_size=11)
        tb = add_textbox(slide, left + 0.3, top, width - 0.6, h,
                         anchor=MSO_ANCHOR.MIDDLE)
        write_rich_paragraph(tb.text_frame, intro, size=size, theme=theme,
                             color=pal.white, first=True)
        top += h + GAP
    if insight:
        h = 0.7
        add_callout_bar(slide, theme, left, bottom - h, width, h, insight,
                        label=insight_label)
        bottom -= h + GAP

    n = max(len(cards), 1)
    has_values = any(c.get("value") for c in cards)
    cols = columns or _auto_columns(n, has_values)
    rows = -(-n // cols)
    card_w = (width - GAP * (cols - 1)) / cols
    card_h = (bottom - top - GAP * (rows - 1)) / rows

    icon_d = 0.5 if card_h >= 1.6 else 0.38
    has_icons = any(c.get("icon") for c in cards)
    header_w = card_w - 2 * PAD - ((icon_d + 0.15) if has_icons and not has_values else 0)
    value_h = min(1.3, card_h * 0.36) if has_values else 0

    # One body size for the whole grid, fitted to the tightest card.
    body_w = card_w - 2 * PAD
    sizes = []
    for c in cards:
        head_size_guess = 15
        head_h = text_height_in([c.get("title", "")], header_w, head_size_guess)
        head_h = max(head_h, icon_d if has_icons and not has_values else 0)
        avail = card_h - 2 * PAD - head_h - value_h - 0.12
        sizes.append(fit_size(_card_paras(c) or [" "], body_w, max(avail, 0.3),
                              max_size=18, min_size=10, para_gap_pt=5,
                              indent_in=0.25))
    body_size = min(sizes) if sizes else 14
    warn_small("card_grid", title, body_size,
               "Shorten the longest card's bullets, drop the subtitle or the "
               "insight bar, or split the slide.")
    head_size = min(body_size + 2, 20)

    # If the text tops out at the size cap, shrink the cards to their content
    # and centre the grid, rather than leaving the space inside each card.
    def needed(c):
        hw_ = header_w if (has_icons and not c.get("value")) else body_w
        h = 2 * PAD + text_height_in([c.get("title", "")], hw_, head_size, bold=True)
        if has_icons and not c.get("value"):
            h = max(h, 2 * PAD + icon_d)
        h += 0.12 + (value_h + 0.05 if c.get("value") else 0)
        paras = _card_paras(c)
        if paras:
            h += text_height_in(paras, body_w, body_size, para_gap_pt=5,
                                indent_in=0.25)
        return h + 0.1
    natural = max((needed(c) for c in cards), default=card_h)
    if natural < card_h * 0.85:
        grid_h = rows * card_h + GAP * (rows - 1)
        card_h = max(natural, card_h * 0.55)
        top += (grid_h - (rows * card_h + GAP * (rows - 1))) / 2

    for i, c in enumerate(cards):
        r, k = divmod(i, cols)
        x = left + k * (card_w + GAP)
        y = top + r * (card_h + GAP)
        tone = c.get("tone")
        add_rect(slide, x, y, card_w, card_h, fill=pal.soft_gray)
        cy = y + PAD

        if c.get("value"):
            # one line, never broken mid-word
            vsize = min(fit_one_line(c["value"], body_w, 54, 16, bold=True),
                        int(value_h * 72 / 1.15))
            tb = add_textbox(slide, x + PAD, cy, body_w, value_h,
                             anchor=MSO_ANCHOR.MIDDLE)
            write_rich_paragraph(tb.text_frame, c["value"], size=vsize,
                                 theme=theme, color=tone_rgb(theme, tone),
                                 bold=True, first=True)
            cy += value_h + 0.05
            hx, hw = x + PAD, body_w
        elif has_icons:
            add_icon(slide, c.get("icon"), x + PAD, cy, icon_d, theme, tone)
            hx, hw = x + PAD + icon_d + 0.15, header_w
        else:
            hx, hw = x + PAD, body_w

        head_h = text_height_in([c.get("title", "")], hw, head_size, bold=True)
        if has_icons and not c.get("value"):
            head_h = max(head_h, icon_d)
        tb = add_textbox(slide, hx, cy, hw, head_h,
                         anchor=MSO_ANCHOR.MIDDLE if has_icons and not c.get("value")
                         else MSO_ANCHOR.TOP)
        write_rich_paragraph(tb.text_frame, c.get("title", ""), size=head_size,
                             theme=theme, color=pal.text_dark, bold=True,
                             first=True)
        cy += head_h + 0.12

        paras = _card_paras(c)
        if paras:
            tb = add_textbox(slide, x + PAD, cy, body_w, y + card_h - PAD - cy)
            first = True
            if c.get("body"):
                write_rich_paragraph(tb.text_frame, c["body"], size=body_size,
                                     theme=theme, first=True, space_after=4)
                first = False
            for b in c.get("bullets", []):
                write_rich_paragraph(tb.text_frame, b, size=body_size,
                                     theme=theme, bullet=True, first=first,
                                     space_before=0 if first else 5)
                first = False
    return slide


def add_swot(prs, *,
             title: str = "[SWOT / Insert action title]",
             strengths: Sequence[str] = (),
             weaknesses: Sequence[str] = (),
             opportunities: Sequence[str] = (),
             threats: Sequence[str] = (),
             labels: Sequence[str] = ("Strengths", "Weaknesses",
                                      "Opportunities", "Threats"),
             insight: Optional[str] = None,
             subtitle: Optional[str] = None,
             page_number=None, section_marker=None,
             source=None, footnote=None,
             theme: Theme = DEFAULT_THEME):
    """Classic 2x2 SWOT. Empty quadrants are kept (shown as "—") so the frame
    stays readable; pass only what the source supports."""
    quads = [
        (labels[0], strengths, "shield", "blue"),
        (labels[1], weaknesses, "alert", "red"),
        (labels[2], opportunities, "trend_up", "green"),
        (labels[3], threats, "zap", "amber"),
    ]
    cards = [{"title": t, "bullets": list(items) or ["—"], "icon": ic, "tone": tone}
             for t, items, ic, tone in quads]
    return add_card_grid(prs, title=title, cards=cards, subtitle=subtitle,
                         insight=insight, columns=2, page_number=page_number,
                         section_marker=section_marker, source=source,
                         footnote=footnote, theme=theme)
