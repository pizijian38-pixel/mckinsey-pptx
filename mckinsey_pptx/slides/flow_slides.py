"""Who-does-what and stacked-structure diagrams.

- swimlane    : a process across 2-5 actors (lanes); steps in order, hand-offs
                between lanes drawn as right-angle connectors. focus = the
                step the title is about (bottleneck, new step, owner change).
- layer_stack : 3-6 stacked layers (capability stack, tech stack, operating
                model levels), each with a note on the right. focus = the layer
                where the work or the gap is.
"""
from __future__ import annotations

from typing import Dict, Optional, Sequence

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from ..base import add_line, add_rect, add_textbox, write_paragraph
from ..design import (HAIRLINE_PT, add_arrow, check_focus, eyebrow, fit_size, focus_tag,
                      has_focus, is_focus, text_height_in, text_width_pt, tint, warn_small,
                      write_rich_paragraph)
from ..labels import loc
from ..theme import Theme, DEFAULT_THEME
from .evaluation_slides import _frame

MIN_PT = 10


# ---------------------------------------------------------------- swimlane

def add_swimlane(prs, *,
                 title: str = "[Swimlane / Insert action title]",
                 lanes: Sequence[str],
                 steps: Sequence[Dict],
                 focus=None,
                 focus_label: Optional[str] = None,
                 subtitle: Optional[str] = None,
                 insight: Optional[str] = None,
                 insight_label: Optional[str] = "Key insight",
                 page_number=None, section_marker=None,
                 source=None, footnote=None,
                 theme: Theme = DEFAULT_THEME):
    """lanes: the actors, top to bottom (2-5).
    steps: [{"lane", "title", "body"?, "col"?}] in process order (<= 12). Each
           step sits in its lane, one column right of the previous step unless
           "col" (0-based) puts two steps in the same column (parallel work).
    Consecutive steps are joined; a lane change is a hand-off (elbow connector).
    focus: the step the title is about (title or index); focus_label tags it.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    nl = len(lanes)
    titles = [s.get("title", "") for s in steps]
    check_focus("swimlane", title, focus, titles)
    bad = [s.get("lane") for s in steps if s.get("lane") not in lanes]
    if bad:
        raise ValueError(f"swimlane \"{str(title)[:40]}\": steps name unknown lanes {bad}; "
                         f"lanes are {list(lanes)}.")
    if not 2 <= nl <= 5 or len(steps) > 12:
        warn_small("swimlane", title, 0, f"{nl} lanes, {len(steps)} steps; keep to 2-5 / 12.")
    cols, c = [], -1
    for s in steps:
        c = s["col"] if "col" in s else c + 1
        cols.append(c)
    ncol = max(cols) + 1 if cols else 1
    lab_w = min(max(text_width_pt(l, 12, True) / 72 for l in lanes) + 0.35, 2.0)
    lh = (bottom - top) / max(nl, 1)
    gx = left + lab_w
    pitch = (width - lab_w) / ncol
    bw = min(pitch - 0.35, 2.4)
    bh = min(lh - 0.3, 1.0)
    size = min([fit_size([t] + ([s["body"]] if s.get("body") else []), bw - 0.2, bh - 0.12,
                         max_size=13, min_size=MIN_PT, bold=True, para_gap_pt=1)
                for t, s in zip(titles, steps)] or [12])
    warn_small("swimlane", title, size, "Shorten the step titles or use fewer columns.")
    for i, l in enumerate(lanes):
        y = top + i * lh
        add_rect(slide, left, y + 0.03, lab_w - 0.1, lh - 0.06, fill=pal.soft_gray)
        tb = add_textbox(slide, left + 0.1, y, lab_w - 0.3, lh, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, l, size=12, bold=True, color=pal.deep_navy,
                        family=typo.family, first=True)
        if i:
            add_line(slide, left, y, left + width, y, color=pal.grid_gray, width_pt=HAIRLINE_PT)

    def box(k):
        li = list(lanes).index(steps[k]["lane"])
        x = gx + cols[k] * pitch + (pitch - bw) / 2
        y = top + li * lh + (lh - bh) / 2
        return x, y
    # connectors first (under the boxes)
    for k in range(1, len(steps)):
        (x0, y0), (x1, y1) = box(k - 1), box(k)
        a = (x0 + bw, y0 + bh / 2)
        b = (x1, y1 + bh / 2)
        handoff = steps[k]["lane"] != steps[k - 1]["lane"]
        col = pal.mid_blue
        if cols[k] == cols[k - 1]:      # parallel step below / above: drop straight down
            a = (x0 + bw / 2, y0 + (bh if y1 > y0 else 0))
            b = (x1 + bw / 2, y1 + (0 if y1 > y0 else bh))
            add_arrow(slide, *a, *b, color=col, width_pt=1.25)
        elif not handoff:
            add_arrow(slide, *a, *b, color=col, width_pt=1.25)
        else:                           # hand-off: right, then down/up, then right
            mx = (a[0] + b[0]) / 2
            add_line(slide, a[0], a[1], mx, a[1], color=col, width_pt=1.25)
            add_line(slide, mx, a[1], mx, b[1], color=col, width_pt=1.25)
            add_arrow(slide, mx, b[1], b[0], b[1], color=col, width_pt=1.25)
    for k, s in enumerate(steps):
        x, y = box(k)
        f = is_focus(focus, k, titles[k])
        r = add_rect(slide, x, y, bw, bh, fill=pal.deep_navy if f else pal.white,
                     line=pal.deep_navy if f else pal.rule_gray, line_width=1.0 if f else HAIRLINE_PT)
        r.name = f"swimlane:{titles[k]}"
        tb = add_textbox(slide, x + 0.1, y, bw - 0.2, bh, anchor=MSO_ANCHOR.MIDDLE)
        write_rich_paragraph(tb.text_frame, titles[k], size=size, theme=theme, bold=True,
                             color=pal.white if f else pal.text_dark, align=PP_ALIGN.CENTER,
                             first=True)
        if s.get("body"):
            write_rich_paragraph(tb.text_frame, s["body"], size=max(size - 2, MIN_PT), theme=theme,
                                 color=tint(pal.white, 0) if f else pal.footer_gray,
                                 align=PP_ALIGN.CENTER)
        if f and focus_label:
            focus_tag(slide, theme, x + bw, y - 0.13, focus_label, h=0.26, anchor="right")
    return slide


# ---------------------------------------------------------------- layer stack

def add_layer_stack(prs, *,
                    title: str = "[Layer stack / Insert action title]",
                    layers: Sequence[Dict],
                    axis: Optional[Sequence[str]] = None,
                    focus=None,
                    focus_label: Optional[str] = None,
                    subtitle: Optional[str] = None,
                    insight: Optional[str] = None,
                    insight_label: Optional[str] = "Key insight",
                    page_number=None, section_marker=None,
                    source=None, footnote=None,
                    theme: Theme = DEFAULT_THEME):
    """layers: [{"name", "note"?, "items"?: [str]}] top to bottom (3-6) — each
    layer builds on the one below (customer-facing on top, foundations at the bottom).
    axis: (top caption, bottom caption) for the vertical arrow on the left,
          e.g. ("Closer to the customer", "Foundations").
    focus: the layer the title is about — tinted and outlined; focus_label tags it.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    names = [l.get("name", "") for l in layers]
    check_focus("layer_stack", title, focus, names)
    n = len(layers)
    if not 2 <= n <= 6:
        warn_small("layer_stack", title, 0, f"{n} layers; keep to 3-6.")
    focused = has_focus(focus)
    ax_w = 0.9 if axis else 0.0
    x0 = left + ax_w
    w = width - ax_w
    gap = 0.1
    lh = (bottom - top - gap * (n - 1)) / max(n, 1)
    name_w = min(max(text_width_pt(nm, 15, True) / 72 for nm in names) + 0.6, w * 0.38)
    notes = [" · ".join(l.get("items", [])) if l.get("items") else l.get("note", "") for l in layers]
    nsize = min([fit_size([t], w - name_w - 0.5, lh - 0.15, max_size=14, min_size=MIN_PT)
                 for t in notes if t] or [13])
    warn_small("layer_stack", title, nsize, "Shorten the layer notes.")
    if axis:
        ax = left + ax_w / 2 - 0.05
        add_arrow(slide, ax, bottom - 0.6, ax, top + 0.6, color=pal.text_dark,
                  width_pt=HAIRLINE_PT)
        for txt, y, anc in ((axis[0], top, MSO_ANCHOR.TOP), (axis[1], bottom - 0.52,
                                                            MSO_ANCHOR.BOTTOM)):
            tb = add_textbox(slide, left, y, ax_w - 0.1, 0.52, anchor=anc)
            write_paragraph(tb.text_frame, loc(theme, txt), size=MIN_PT, color=pal.footer_gray,
                            family=typo.family, align=PP_ALIGN.CENTER, first=True)
    for i, l in enumerate(layers):
        y = top + i * (lh + gap)
        f = is_focus(focus, i, names[i])
        fill = tint(pal.bright_blue, 0.86) if f else (pal.soft_gray if focused or i % 2 else
                                                      tint(pal.dark_navy, 0.9))
        r = add_rect(slide, x0, y, w, lh, fill=fill, line=pal.bright_blue if f else None,
                     line_width=2.0 if f else None)
        r.name = f"layer:{names[i]}"
        eyebrow(slide, theme, x0 + 0.2, y + 0.06, 0.6, f"L{n - i}",
                color=pal.mid_blue if f else pal.footer_gray, size=9, h=0.2)
        tb = add_textbox(slide, x0 + 0.2, y, name_w - 0.3, lh, anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, names[i], size=15, bold=True, color=pal.deep_navy,
                        family=typo.family, first=True)
        if notes[i]:
            tb = add_textbox(slide, x0 + name_w, y, w - name_w - 0.3, lh, anchor=MSO_ANCHOR.MIDDLE)
            write_rich_paragraph(tb.text_frame, notes[i], size=nsize, theme=theme,
                                 color=pal.text_dark, first=True)
        if f and focus_label:
            focus_tag(slide, theme, x0 + w - 0.1, y + 0.08, focus_label, anchor="right")
    return slide
