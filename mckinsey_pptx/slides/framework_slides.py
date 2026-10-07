"""Framework templates used in strategy cases.

- business_model_canvas : the nine-block canvas (partners, activities,
                          resources, value proposition, relationships,
                          channels, segments, cost structure, revenue).
- strategic_triangle    : goals in the centre; resources & capabilities,
                          business & value proposition, and structure /
                          systems / people around it.
- hub_spoke             : one concept and the 3-6 elements that make it up
                          (with a note each), and what that implies.
"""
from __future__ import annotations

import math
from typing import Dict, Optional, Sequence, Union

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

from ..base import add_line, add_oval, add_rect, add_textbox, write_paragraph
from ..components import letter_space
from ..design import (add_arrow, add_icon, add_stage_banners, fit_one_line, fit_size, plain,
                      set_dashed, text_height_in, tint, warn_small, write_rich_paragraph)
from ..labels import loc
from ..theme import Theme, DEFAULT_THEME
from .evaluation_slides import _frame

MIN_PT = 10
Block = Union[str, Sequence[str], Dict, None]


def _items(b: Block):
    if b is None:
        return []
    if isinstance(b, str):
        return [b]
    if isinstance(b, dict):
        return ([b["body"]] if b.get("body") else []) + list(b.get("bullets", []))
    return [str(x) for x in b]


def _write_items(slide, theme, x, y, w, h, items, size, *, bullets=True, color=None,
                 anchor=MSO_ANCHOR.TOP):
    tb = add_textbox(slide, x, y, w, h, anchor=anchor)
    for i, t in enumerate(items or ["—"]):
        write_rich_paragraph(tb.text_frame, t, size=size, theme=theme, color=color,
                             bullet=bullets and len(items) > 0, first=i == 0,
                             space_before=None if i == 0 else 4)


# ---------- business model canvas ----------

_BMC = [  # key, default label, icon
    ("partners", "Key partners", "handshake"),
    ("activities", "Key activities", "settings"),
    ("resources", "Key resources", "database"),
    ("value_proposition", "Value proposition", "gem"),
    ("relationships", "Customer relationships", "heart"),
    ("channels", "Channels", "truck"),
    ("segments", "Customer segments", "users"),
    ("costs", "Cost structure", "money"),
    ("revenue", "Revenue streams", "coins"),
]


def add_business_model_canvas(prs, *,
                              title: str = "[Business model canvas / Insert action title]",
                              partners: Block = None, activities: Block = None,
                              resources: Block = None, value_proposition: Block = None,
                              relationships: Block = None, channels: Block = None,
                              segments: Block = None, costs: Block = None, revenue: Block = None,
                              labels: Optional[Dict[str, str]] = None,
                              highlight: Sequence[str] = ("value_proposition",),
                              subtitle: Optional[str] = None,
                              insight: Optional[str] = None,
                              insight_label: Optional[str] = "Key insight",
                              page_number=None, section_marker=None,
                              source=None, footnote=None,
                              theme: Theme = DEFAULT_THEME):
    """Each block: str | [bullets] | {body?, bullets?}. Empty blocks show "—".
    labels: override block names, e.g. {"segments": "Target customers"}.
    highlight: blocks drawn with a dark header (default: the value proposition).
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    vals = dict(partners=partners, activities=activities, resources=resources,
                value_proposition=value_proposition, relationships=relationships,
                channels=channels, segments=segments, costs=costs, revenue=revenue)
    labels = labels or {}
    g = 0.08
    H = bottom - top
    top_h = H * 0.68
    bot_h = H - top_h - g
    cw = (width - 4 * g) / 5
    xs = [left + i * (cw + g) for i in range(5)]
    half = (top_h - g) / 2
    boxes = {  # key -> (x, y, w, h)
        "partners": (xs[0], top, cw, top_h),
        "activities": (xs[1], top, cw, half),
        "resources": (xs[1], top + half + g, cw, half),
        "value_proposition": (xs[2], top, cw, top_h),
        "relationships": (xs[3], top, cw, half),
        "channels": (xs[3], top + half + g, cw, half),
        "segments": (xs[4], top, cw, top_h),
        "costs": (left, top + top_h + g, (width - g) / 2, bot_h),
        "revenue": (left + (width + g) / 2, top + top_h + g, (width - g) / 2, bot_h),
    }
    head_h = 0.36
    pad = 0.12
    size = 15
    for key, _l, _i in _BMC:
        x, y, w, h = boxes[key]
        its = _items(vals[key]) or ["—"]
        size = min(size, fit_size(its, w - 2 * pad, h - head_h - 2 * pad, max_size=15,
                                  min_size=MIN_PT, para_gap_pt=4, indent_in=0.22))
    warn_small("business_model_canvas", title, size, "Keep 2-4 short bullets per block.")
    names = {k: loc(theme, labels.get(k, lab)) for k, lab, _ in _BMC}
    hsize = min(12, min(fit_one_line(names[k], boxes[k][2] - 0.55, 12, 9, True)
                        for k in names))
    for key, _lab, icon in _BMC:
        x, y, w, h = boxes[key]
        dark = key in highlight
        add_rect(slide, x, y, w, h, fill=pal.soft_gray)
        add_rect(slide, x, y, w, head_h, fill=pal.deep_navy if dark else tint(pal.mid_blue, 0.82))
        add_icon(slide, icon, x + 0.06, y + 0.04, head_h - 0.08, theme,
                 "blue" if dark else "navy")
        tb = add_textbox(slide, x + head_h + 0.04, y, w - head_h - 0.1, head_h,
                         anchor=MSO_ANCHOR.MIDDLE)
        write_paragraph(tb.text_frame, names[key], size=hsize, bold=True,
                        color=pal.white if dark else pal.deep_navy, family=typo.family,
                        first=True)
        its = _items(vals[key])
        _write_items(slide, theme, x + pad, y + head_h + pad, w - 2 * pad,
                     h - head_h - 2 * pad, its, size, bullets=bool(its))
    return slide


# ---------- strategic triangle ----------

def _blocks(b):
    if b is None:
        return []
    if isinstance(b, dict):
        return [b]
    if isinstance(b, str):
        return [{"bullets": [b]}]
    out = []
    for x in b:
        out.append(x if isinstance(x, dict) else {"bullets": [str(x)]})
    return out


def _block_paras(bl):
    out = []
    for b in bl:
        if b.get("title"):
            out.append("**" + b["title"] + "**")
        out += _items(b)
    return out


def _write_blocks(slide, theme, x, y, w, h, bl, size, anchor=MSO_ANCHOR.TOP):
    pal = theme.palette
    tb = add_textbox(slide, x, y, w, h, anchor=anchor)
    first = True
    for b in bl:
        if b.get("title"):
            write_rich_paragraph(tb.text_frame, b["title"], size=size, theme=theme,
                                 color=pal.mid_blue, bold=True, first=first,
                                 space_before=None if first else 6)
            first = False
        for t in _items(b):
            write_rich_paragraph(tb.text_frame, t, size=size, theme=theme, bullet=True,
                                 first=first, space_before=None if first else 3)
            first = False


def add_strategic_triangle(prs, *,
                           title: str = "[Strategic triangle / Insert action title]",
                           goal: str,
                           resources: Block = None,
                           business: Block = None,
                           structure: Sequence = (),
                           labels: Sequence[str] = ("Resources & capabilities",
                                                    "Business & value proposition",
                                                    "Structure, systems & people"),
                           goal_label: str = "Goals",
                           subtitle: Optional[str] = None,
                           insight: Optional[str] = None,
                           insight_label: Optional[str] = "Key insight",
                           page_number=None, section_marker=None,
                           source=None, footnote=None,
                           theme: Theme = DEFAULT_THEME):
    """goal: the goal / mission in the centre of the triangle.
    resources, business: blocks for the left and right corners —
        str | [str] | {title?, bullets} | [{title, bullets}, ...].
    structure: 1-3 blocks along the bottom (e.g. Structure & systems, People).
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    labels = [loc(theme, t) for t in labels]
    rb, bb, sb = _blocks(resources), _blocks(business), _blocks(structure)
    H = bottom - top
    top_h = H * (0.62 if sb else 1.0)
    side_w = width * 0.31
    tri_w = width - 2 * side_w - 0.4
    tri_x = left + side_w + 0.2
    # triangle
    th = min(top_h - 0.55, tri_w * 0.88)
    ty = top + 0.1
    tx = tri_x + (tri_w - th / 0.88) / 2
    tw = th / 0.88
    tri = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(tx), Inches(ty),
                                 Inches(tw), Inches(th))
    tri.fill.solid()
    tri.fill.fore_color.rgb = tint(pal.light_blue, 0.82)
    tri.line.color.rgb = pal.mid_blue
    tri.shadow.inherit = False
    gl = loc(theme, goal_label)
    inner_w = tw * 0.62
    gsize = fit_size([goal], inner_w, th * 0.4, max_size=15, min_size=MIN_PT)
    warn_small("strategic_triangle", title, gsize, "Shorten the goal to one short sentence.")
    tb = add_textbox(slide, tx + (tw - inner_w) / 2, ty + th * 0.4, inner_w, th * 0.56,
                     anchor=MSO_ANCHOR.MIDDLE)
    write_paragraph(tb.text_frame, gl, size=gsize + 3, bold=True, color=pal.deep_navy,
                    family=typo.family, align=PP_ALIGN.CENTER, first=True, space_after=4)
    write_rich_paragraph(tb.text_frame, goal, size=gsize, theme=theme, color=pal.text_dark,
                         align=PP_ALIGN.CENTER)
    # corner labels
    lab_size = min(15, min(fit_one_line(max(plain(t).split() or [""], key=len), side_w * 0.6,
                                        15, 10, True) for t in labels))
    tb = add_textbox(slide, tx - 1.2, ty + th * 0.35, 1.6, 0.8, anchor=MSO_ANCHOR.MIDDLE)
    write_paragraph(tb.text_frame, labels[0], size=lab_size, bold=True, color=pal.deep_navy,
                    family=typo.family, align=PP_ALIGN.RIGHT, first=True)
    tb = add_textbox(slide, tx + tw - 0.4, ty + th * 0.35, 1.6, 0.8, anchor=MSO_ANCHOR.MIDDLE)
    write_paragraph(tb.text_frame, labels[1], size=lab_size, bold=True, color=pal.deep_navy,
                    family=typo.family, align=PP_ALIGN.LEFT, first=True)
    tb = add_textbox(slide, tx - 0.5, ty + th + 0.05, tw + 1.0, 0.4, anchor=MSO_ANCHOR.MIDDLE)
    write_paragraph(tb.text_frame, labels[2], size=lab_size, bold=True, color=pal.deep_navy,
                    family=typo.family, align=PP_ALIGN.CENTER, first=True)
    # side texts (keep clear of the corner labels)
    side_text_w = side_w - 0.6
    paras_l, paras_r = _block_paras(rb), _block_paras(bb)
    size = min(fit_size(paras_l or [" "], side_text_w, top_h - 0.1, max_size=15, min_size=MIN_PT,
                        para_gap_pt=4, indent_in=0.22),
               fit_size(paras_r or [" "], side_text_w, top_h - 0.1, max_size=15, min_size=MIN_PT,
                        para_gap_pt=4, indent_in=0.22))
    sb_w = (width - 0.3 * (len(sb) - 1)) / max(len(sb), 1)
    bot_top = top + top_h + 0.25
    if sb:
        size = min([size] + [fit_size(_block_paras([b]) or [" "], sb_w - 0.2, bottom - bot_top - 0.1,
                                      max_size=15, min_size=MIN_PT, para_gap_pt=4,
                                      indent_in=0.22) for b in sb])
    warn_small("strategic_triangle", title, size, "Shorten the corner texts.")
    _write_blocks(slide, theme, left, top, side_text_w, top_h, rb, size, MSO_ANCHOR.MIDDLE)
    _write_blocks(slide, theme, left + width - side_text_w, top, side_text_w, top_h, bb, size,
                  MSO_ANCHOR.MIDDLE)
    if sb:
        add_line(slide, left, bot_top - 0.1, left + width, bot_top - 0.1, color=pal.rule_gray,
                 width_pt=1.0)
        for i, b in enumerate(sb):
            x = left + i * (sb_w + 0.3)
            if i:
                ln = add_line(slide, x - 0.15, bot_top, x - 0.15, bottom, color=pal.rule_gray,
                              width_pt=1.0)
                from pptx.enum.dml import MSO_LINE_DASH_STYLE
                ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            _write_blocks(slide, theme, x + 0.05, bot_top, sb_w - 0.15, bottom - bot_top, [b], size)
    return slide


# ---------- hub and spoke ----------

def add_hub_spoke(prs, *,
                  title: str = "[Hub and spoke / Insert action title]",
                  center: str,
                  spokes: Sequence[Dict],
                  direction: str = "in",
                  heading: Optional[str] = None,
                  side: Optional[Dict] = None,
                  subtitle: Optional[str] = None,
                  insight: Optional[str] = None,
                  insight_label: Optional[str] = "Key insight",
                  page_number=None, section_marker=None,
                  source=None, footnote=None,
                  theme: Theme = DEFAULT_THEME):
    """center: the concept in the middle.
    spokes: [{"title", "note"?, "icon"?}] (3-6) around it, each with a short note.
    direction: "in" (elements feed the centre) | "out" (centre drives them).
    heading: a caption above the diagram (the claim the diagram makes).
    side: {"title", "bullets"? | "body"?} — the implication, in a panel on the right.
    """
    slide, left, top, width, bottom = _frame(
        prs, theme, title, subtitle, insight, insight_label, page_number=page_number,
        section_marker=section_marker, source=source, footnote=footnote)
    pal, typo = theme.palette, theme.typography
    lw = width * 0.65 if side else width
    if side:
        # left region outline pointing at the panel
        sx = left + lw + 0.35
        sw = width - lw - 0.35
        add_rect(slide, sx, top, sw, bottom - top, fill=pal.white, line=pal.grid_gray,
                 line_width=1.0)
        stt = side.get("title", "")
        ts = fit_size([stt], sw - 0.4, 0.7, max_size=15, min_size=11, bold=True)
        th_ = text_height_in([stt], sw - 0.4, ts, bold=True) + 0.2
        tb = add_textbox(slide, sx + 0.2, top + 0.12, sw - 0.4, th_)
        write_rich_paragraph(tb.text_frame, stt, size=ts, theme=theme, bold=True, first=True)
        add_line(slide, sx + 0.2, top + 0.12 + th_, sx + sw - 0.2, top + 0.12 + th_,
                 color=pal.rule_gray, width_pt=0.75)
        its = _items(side)
        ss = fit_size(its or [" "], sw - 0.4, bottom - top - th_ - 0.5, max_size=15,
                      min_size=MIN_PT, para_gap_pt=8, indent_in=0.22)
        warn_small("hub_spoke", title, ss, "Shorten the side panel.")
        _write_items(slide, theme, sx + 0.2, top + th_ + 0.3, sw - 0.4,
                     bottom - top - th_ - 0.4, its, ss)
    y0 = top
    if heading:
        hs = fit_size([heading], lw - 0.2, 0.6, max_size=14, min_size=11, bold=True)
        hh = text_height_in([heading], lw - 0.2, hs, bold=True) + 0.15
        tb = add_textbox(slide, left, top, lw, hh)
        write_rich_paragraph(tb.text_frame, heading, size=hs, theme=theme, bold=True, first=True)
        add_line(slide, left, top + hh, left + lw, top + hh, color=pal.rule_gray, width_pt=0.75)
        y0 = top + hh + 0.1
    H = bottom - y0
    cx, cy = left + lw / 2, y0 + H / 2
    n = max(len(spokes), 1)
    note_w = min(1.75, lw * 0.21)
    d = min(1.2, H * 0.27)
    D = min(1.35, H * 0.3)
    rx = min(lw / 2 - note_w - d / 2 - 0.12, H * 0.75)
    rx = max(rx, D / 2 + d / 2 + 0.3)
    ry = H / 2 - d / 2 - 0.05
    pos = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + rx * math.cos(a), cy + ry * math.sin(a), a))
    # arrows first
    for px, py, a in pos:
        ux, uy = math.cos(a), math.sin(a)
        dist = math.hypot(px - cx, py - cy)
        ux, uy = (px - cx) / dist, (py - cy) / dist
        p_out = (px - ux * (d / 2 + 0.06), py - uy * (d / 2 + 0.06))
        p_in = (cx + ux * (D / 2 + 0.06), cy + uy * (D / 2 + 0.06))
        a0, a1 = (p_out, p_in) if direction == "in" else (p_in, p_out)
        add_arrow(slide, a0[0], a0[1], a1[0], a1[1], color=pal.mid_blue, width_pt=2.0)
    add_oval(slide, cx - D / 2, cy - D / 2, D, D, fill=pal.bright_blue)
    csz = fit_size([center], D * 0.74, D * 0.6, max_size=17, min_size=MIN_PT, bold=True)
    tb = add_textbox(slide, cx - D * 0.37, cy - D * 0.3, D * 0.74, D * 0.6,
                     anchor=MSO_ANCHOR.MIDDLE)
    write_rich_paragraph(tb.text_frame, center, size=csz, theme=theme, color=pal.white,
                         bold=True, align=PP_ALIGN.CENTER, first=True)
    titles = [s.get("title", "") for s in spokes]

    def title_size(with_icon):
        sz = min(fit_size([t], d * 0.84, d * (0.46 if with_icon else 0.72), max_size=15,
                          min_size=8, bold=True) for t in titles)
        return min([sz] + [fit_one_line(max(plain(t).split() or [""], key=len), d * 0.88, 15,
                                        8, True) for t in titles])
    has_icon = any(s.get("icon") for s in spokes)
    tsz = title_size(has_icon)
    if has_icon and tsz < 11:  # icons would squeeze the titles: drop them
        has_icon, tsz = False, title_size(False)
    notes = [s.get("note", "") for s in spokes]
    nsz = min([fit_size([t], note_w - 0.16, H / max(n, 3) * 0.9, max_size=13, min_size=MIN_PT)
               for t in notes if t] or [12])
    warn_small("hub_spoke", title, min(nsz, tsz + 2),
               "Shorten the spoke titles (1-2 words) and notes (one short line).")
    for (px, py, a), s in zip(pos, spokes):
        add_oval(slide, px - d / 2, py - d / 2, d, d, fill=pal.deep_navy)
        if s.get("icon") and has_icon:
            idd = d * 0.3
            add_icon(slide, s["icon"], px - idd / 2, py + d * 0.1, idd, theme, "navy")
            tb = add_textbox(slide, px - d * 0.44, py - d * 0.4, d * 0.88, d * 0.48,
                             anchor=MSO_ANCHOR.BOTTOM)
        else:
            tb = add_textbox(slide, px - d * 0.44, py - d * 0.38, d * 0.88, d * 0.76,
                             anchor=MSO_ANCHOR.MIDDLE)
        write_rich_paragraph(tb.text_frame, s.get("title", ""), size=tsz, theme=theme,
                             color=pal.white, bold=True, align=PP_ALIGN.CENTER, first=True)
        if s.get("note"):
            nh = text_height_in([s["note"]], note_w - 0.16, nsz) + 0.16
            right = math.cos(a) >= -1e-6
            nx = px + d / 2 + 0.08 if right else px - d / 2 - 0.08 - note_w
            ny = min(max(py - nh / 2, y0), bottom - nh)
            box = add_rect(slide, nx, ny, note_w, nh, fill=pal.soft_gray)
            set_dashed(box, pal.grid_gray, 0.75)
            tb = add_textbox(slide, nx + 0.08, ny, note_w - 0.16, nh, anchor=MSO_ANCHOR.MIDDLE)
            write_rich_paragraph(tb.text_frame, s["note"], size=nsz, theme=theme, first=True)
    return slide
