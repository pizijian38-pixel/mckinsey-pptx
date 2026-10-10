"""Process / metric overview slides:
 - process_flow_horizontal: 4-6 step flow with chevron-style arrows
 - funnel: top-down funnel (TAM/SAM/SOM, marketing funnel, etc.)
 - kpi_dashboard: 4-6 KPI tiles with big number + label + delta
"""
from __future__ import annotations
from typing import Sequence, Optional, Dict, Literal

from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

from ..base import (
    blank_slide, add_chrome, add_rect, add_oval, add_line, add_textbox,
    write_paragraph, add_subtitle_placeholder,
)
from ..theme import Theme, DEFAULT_THEME
from ..design import (check_focus, eyebrow, fit_one_line, fit_size, focus_tag, has_focus,
                      is_focus, text_height_in, warn_small)
from ..labels import loc
from ..design import mark_index


# ---------- Process flow (horizontal) ----------

def add_process_flow_horizontal(prs, *,
                                title="[Process flow / Insert action title]",
                                subtitle: Optional[str] = None,
                                steps: Sequence[Dict],
                                focus=None,
                                focus_label: Optional[str] = "We are here",
                                page_number=None,
                                section_marker="Section marker",
                                source="xx", footnote="1. xx",
                                theme: Theme = DEFAULT_THEME):
    """steps: [{"name": "Step 1", "description": "...", "items"?: ["...", ...]}]
    3-6 chevrons in one navy row with numbered eyebrows; under each, the
    description (bold) and optional bullets, separated by hairlines.
    focus: the step the title is about (name or index) — it stays navy with a tag
           (focus_label), the other chevrons turn light grey.
    """
    slide = blank_slide(prs)
    add_chrome(slide, title=title, theme=theme, page_number=page_number,
               section_marker=section_marker, source=source, footnote=footnote)
    pal, typo, layout = theme.palette, theme.typography, theme.layout
    left = layout.margin_left_in
    width = layout.slide_width_in - left - layout.margin_right_in
    top = 1.65
    if subtitle:
        tb = add_textbox(slide, left, 1.30, width, 0.32)
        write_paragraph(tb.text_frame, subtitle, size=typo.body_size,
                        color=pal.placeholder_gray, family=typo.family, first=True)
        top = 1.85
    names = [st.get("name", f"Step {i + 1}") for i, st in enumerate(steps)]
    check_focus("process_flow", title, focus, names)
    focused = has_focus(focus)
    n = max(len(steps), 1)
    overlap, ch = 0.22, 0.72
    cw = (width + (n - 1) * overlap) / n
    col_w = cw - overlap
    name_size = min([fit_one_line(nm, cw - 0.6, 14, 10, True) for nm in names] or [14])
    body_top = top + 0.32 + ch + 0.25
    body_bottom = layout.footer_top_in - 0.3
    descs = [st.get("description", "") for st in steps]
    dsize = min([fit_size([d] + list(st.get("items", [])), col_w - 0.3,
                          body_bottom - body_top, max_size=13, min_size=10,
                          para_gap_pt=4, indent_in=0.25)
                 for d, st in zip(descs, steps)] or [12])
    warn_small("process_flow", title, dsize, "Shorten the step descriptions.")
    col_h = max([text_height_in([d] + list(st.get("items", [])), col_w - 0.3, dsize,
                                para_gap_pt=5, indent_in=0.25)
                 for d, st in zip(descs, steps)] or [0.5]) + 0.15
    for i, st in enumerate(steps):
        x = left + i * (cw - overlap)
        f = is_focus(focus, i, names[i])
        dark = f or not focused
        fill = pal.deep_navy if dark else pal.soft_gray
        mark_index(eyebrow(slide, theme, x + (0.12 if i == 0 else 0.3), top, 1.3,
                           f"{loc(theme, 'Step')} {i + 1:02d}",
                           color=pal.bright_blue if f else pal.footer_gray, size=9))
        if f and focus_label:
            focus_tag(slide, theme, x + (0.12 if i == 0 else 0.3) + 0.95, top, focus_label)
        shp = slide.shapes.add_shape(MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON,
                                     Inches(x), Inches(top + 0.32), Inches(cw), Inches(ch))
        shp.shadow.inherit = False
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        shp.line.color.rgb = pal.white
        shp.line.width = Pt(2.5)
        try:
            shp.adjustments[0] = 0.28
        except (IndexError, KeyError):
            pass
        tb = add_textbox(slide, x + (0.15 if i == 0 else 0.34), top + 0.32, cw - 0.62, ch,
                         anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, names[i], size=name_size, bold=True,
                        color=pal.white if dark else pal.deep_navy, family=typo.family,
                        first=True)
        dx = x + (0.12 if i == 0 else 0.3)
        if i:  # divider as tall as the tallest column's text, not the whole page
            add_line(slide, x + 0.12, body_top, x + 0.12, body_top + col_h, color=pal.grid_gray,
                     width_pt=0.75)
        tb = add_textbox(slide, dx, body_top, col_w - 0.3, body_bottom - body_top)
        first = True
        if descs[i]:
            write_paragraph(tb.text_frame, descs[i], size=dsize, bold=bool(st.get("items")),
                            color=pal.deep_navy if st.get("items") else pal.text_dark,
                            family=typo.family, first=True, space_after=6)
            first = False
        for it in st.get("items", []):
            write_paragraph(tb.text_frame, it, size=dsize - 1 if dsize > 10 else dsize,
                            color=pal.text_dark, family=typo.family, bullet=True,
                            space_after=4, first=first)
            first = False
    return slide


# ---------- Funnel ----------

def add_funnel(prs, *,
               title="[Funnel / Insert action title]",
               subtitle: Optional[str] = None,
               stages: Sequence[Dict],
               focus=None,
               page_number=None,
               section_marker="Section marker",
               source="xx", footnote="1. xx",
               theme: Theme = DEFAULT_THEME):
    """stages: [{"name": "Awareness", "value": "1.2M", "description": "..."}]
    Top-down funnel of trapezoid bands; each band's description sits on the right,
    joined to it by a hairline leader.
    focus: the stage the title is about (name or index) — stays navy, the other
           bands turn light grey.
    """
    from ..components import _polygon
    slide = blank_slide(prs)
    add_chrome(slide, title=title, theme=theme, page_number=page_number,
               section_marker=section_marker, source=source, footnote=footnote)
    pal, typo, layout = theme.palette, theme.typography, theme.layout

    if subtitle:
        tb = add_textbox(slide, layout.margin_left_in, 1.30,
                         layout.slide_width_in - layout.margin_left_in
                         - layout.margin_right_in, 0.32)
        write_paragraph(tb.text_frame, subtitle, size=typo.body_size,
                        color=pal.placeholder_gray, family=typo.family,
                        first=True)

    names = [st.get("name", f"Stage {i + 1}") for i, st in enumerate(stages)]
    check_focus("funnel", title, focus, names)
    focused = has_focus(focus)
    width = layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
    body_top = 1.95
    body_bottom = layout.footer_top_in - 0.25
    n = max(len(stages), 1)
    gap = 0.08
    band_h = min(1.2, (body_bottom - body_top - gap * (n - 1)) / n)
    total_h = n * band_h + gap * (n - 1)
    body_top += (body_bottom - body_top - total_h) / 2

    f_left = layout.margin_left_in + 0.2
    f_right = layout.margin_left_in + width * 0.5
    w_top, w_bot = f_right - f_left, (f_right - f_left) * 0.3
    cx = (f_left + f_right) / 2
    right_left = f_right + 0.8
    right_w = layout.slide_width_in - layout.margin_right_in - right_left

    def half(t):  # half-width at fraction t of the funnel height
        return (w_top * (1 - t) + w_bot * t) / 2

    for i, st in enumerate(stages):
        y0 = body_top + i * (band_h + gap)
        y1 = y0 + band_h
        t0, t1 = (y0 - body_top) / total_h, (y1 - body_top) / total_h
        f = is_focus(focus, i, names[i])
        dark = f or not focused
        _polygon(slide, [(cx - half(t0), y0), (cx + half(t0), y0),
                         (cx + half(t1), y1), (cx - half(t1), y1)],
                 pal.deep_navy if dark else pal.soft_gray)
        tw = 2 * half(t1) - 0.2
        tb = add_textbox(slide, cx - tw / 2, y0, tw, band_h, anchor=MSO_ANCHOR.MIDDLE)
        tf = tb.text_frame
        write_paragraph(tf, names[i], size=typo.body_size, bold=True,
                        color=pal.white if dark else pal.deep_navy, family=typo.family,
                        align=PP_ALIGN.CENTER, first=True)
        if st.get("value"):
            write_paragraph(tf, str(st["value"]), size=typo.body_size + 4, bold=True,
                            color=pal.white if dark else pal.deep_navy, family=typo.family,
                            align=PP_ALIGN.CENTER)
        ym = (y0 + y1) / 2
        add_line(slide, cx + half((ym - body_top) / total_h) + 0.08, ym, right_left - 0.12, ym,
                 color=pal.bright_blue if f else pal.grid_gray, width_pt=0.75)
        if st.get("description"):
            tb = add_textbox(slide, right_left, y0, right_w, band_h, anchor=MSO_ANCHOR.MIDDLE)
            write_paragraph(tb.text_frame, st["description"], size=typo.body_size,
                            bold=f, color=pal.deep_navy if f else pal.text_dark,
                            family=typo.family, first=True)
    return slide


# ---------- KPI dashboard ----------

def add_kpi_dashboard(prs, *,
                      title="[KPI dashboard / Insert action title]",
                      subtitle: Optional[str] = None,
                      kpis: Sequence[Dict],
                      columns: int = 4,
                      page_number=None,
                      section_marker="Section marker",
                      source="xx", footnote="1. xx",
                      theme: Theme = DEFAULT_THEME):
    """kpis: [{"label": "ARR", "value": "$1.2B", "delta": "+12% YoY",
                "delta_dir": "up"|"down"|"flat", "context": "..."}]
    Renders 4-8 tiles arranged in `columns` x ceil(n/columns) grid.
    """
    slide = blank_slide(prs)
    add_chrome(slide, title=title, theme=theme, page_number=page_number,
               section_marker=section_marker, source=source, footnote=footnote)
    pal, typo, layout = theme.palette, theme.typography, theme.layout

    if subtitle:
        tb = add_textbox(slide, layout.margin_left_in, 1.30,
                         layout.slide_width_in - layout.margin_left_in
                         - layout.margin_right_in, 0.32)
        write_paragraph(tb.text_frame, subtitle, size=typo.body_size,
                        color=pal.placeholder_gray, family=typo.family,
                        first=True)

    width = layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
    body_top = 1.95
    body_bottom = layout.footer_top_in - 0.20
    body_h = body_bottom - body_top

    n = max(len(kpis), 1)
    cols = max(1, min(columns, n))
    rows = (n + cols - 1) // cols
    gap = 0.20
    tile_w = (width - (cols - 1) * gap) / cols
    tile_h = (body_h - (rows - 1) * gap) / rows

    delta_color_map = {
        "up": pal.status_green,
        "down": pal.status_red,
        "flat": pal.footer_gray,
    }
    delta_glyph_map = {
        "up": "▲",
        "down": "▼",
        "flat": "▬",
    }

    for i, k in enumerate(kpis):
        ci = i % cols
        ri = i // cols
        x = layout.margin_left_in + ci * (tile_w + gap)
        y = body_top + ri * (tile_h + gap)
        # Tile background
        add_rect(slide, x, y, tile_w, tile_h, fill=pal.soft_gray)
        # Top accent bar
        add_rect(slide, x, y, tile_w, 0.10, fill=pal.bright_blue)

        # Label (top)
        tb = add_textbox(slide, x + 0.20, y + 0.20, tile_w - 0.40, 0.32)
        write_paragraph(tb.text_frame, k.get("label", "[KPI]"),
                        size=typo.body_size, bold=True,
                        color=pal.text_dark, family=typo.family, first=True)

        # Big value (centered)
        val_top = y + 0.55
        val_h = tile_h - 1.20
        tb = add_textbox(slide, x + 0.20, val_top, tile_w - 0.40, val_h,
                         anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, str(k.get("value", "—")),
                        size=typo.title_size + 12, bold=True,
                        color=pal.deep_navy, family=typo.family,
                        align=PP_ALIGN.CENTER, first=True)

        # Delta + glyph
        delta_dir = k.get("delta_dir", "flat")
        delta_text = k.get("delta")
        if delta_text:
            tb = add_textbox(slide, x + 0.20, y + tile_h - 0.55,
                             tile_w - 0.40, 0.30, anchor=MSO_ANCHOR.MIDDLE)
            tf = tb.text_frame
            p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            r1 = p.add_run()
            r1.text = delta_glyph_map.get(delta_dir, "") + " "
            r1.font.size = Pt(typo.body_size); r1.font.bold = True
            r1.font.color.rgb = delta_color_map.get(delta_dir, pal.footer_gray)
            r1.font.name = typo.family
            r2 = p.add_run()
            r2.text = str(delta_text)
            r2.font.size = Pt(typo.body_size); r2.font.bold = True
            r2.font.color.rgb = delta_color_map.get(delta_dir, pal.footer_gray)
            r2.font.name = typo.family

        # Context line (very bottom, small)
        if k.get("context"):
            tb = add_textbox(slide, x + 0.20, y + tile_h - 0.27,
                             tile_w - 0.40, 0.22)
            write_paragraph(tb.text_frame, k["context"],
                            size=typo.chart_label_size, color=pal.footer_gray,
                            family=typo.family, align=PP_ALIGN.CENTER,
                            first=True)
    return slide
