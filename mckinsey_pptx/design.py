"""Shared design primitives for the richer templates.

- Tones: semantic colours ("red" = problem/risk, "green" = opportunity ...).
- Rich text: `**bold**` and `{tone|coloured bold}` spans inside any string.
- Icons: a bundled Lucide icon set drawn white on a tone-coloured circle.
- Fitting: pick the largest font size whose estimated height fits a box.
- Panels: the "Key insight" side panel and the highlighted callout bar.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable, Optional

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches

from .base import add_oval, add_rect, add_textbox, set_run, write_paragraph
from .theme import Theme
from .metrics import (TONE_NAMES, fit_one_line, fit_size, plain,  # noqa: F401
                      text_height_in, text_width_pt)

ICON_DIR = Path(__file__).resolve().parent / "assets" / "icons"
ICONS = sorted(p.stem for p in ICON_DIR.glob("*.png"))



def tone_rgb(theme: Theme, tone: Optional[str]):
    pal = theme.palette
    return {
        None: pal.deep_navy, "navy": pal.deep_navy, "blue": pal.bright_blue,
        "mid_blue": pal.mid_blue, "light_blue": pal.light_blue,
        "red": pal.status_red, "green": pal.status_green,
        "amber": pal.status_amber, "gray": pal.footer_gray,
    }.get(tone, pal.deep_navy)


# ---------- rich text ----------

_SPAN = re.compile(r"(\*\*.+?\*\*|\{(?:%s)\|.+?\})" % "|".join(TONE_NAMES))


def add_rich_runs(paragraph, text, *, size, color, family, theme: Theme,
                  bold=False):
    """Append runs to `paragraph`, honouring **bold** and {tone|text} spans."""
    for part in _SPAN.split(str(text)):
        if not part:
            continue
        run_color, run_bold, s = color, bold, part
        if part.startswith("**") and part.endswith("**"):
            s, run_bold = part[2:-2], True
        elif part.startswith("{") and part.endswith("}") and "|" in part:
            tone, s = part[1:-1].split("|", 1)
            run_color, run_bold = tone_rgb(theme, tone), True
        set_run(paragraph.add_run(), s, size=size, bold=run_bold,
                color=run_color, family=family)


def write_rich_paragraph(tf, text, *, size, theme: Theme, color=None,
                         bold=False, align=PP_ALIGN.LEFT, bullet=False,
                         first=False, space_before=None, space_after=None):
    color = color or theme.palette.text_dark
    p = write_paragraph(tf, "", size=size, bold=bold, color=color,
                        family=theme.typography.family, align=align,
                        bullet=bullet, first=first, space_before=space_before,
                        space_after=space_after)
    r = p.runs[0]._r
    r.getparent().remove(r)
    add_rich_runs(p, text, size=size, color=color,
                  family=theme.typography.family, theme=theme, bold=bold)
    return p


# ---------- fitting ----------

# ---------- warnings ----------

MIN_READABLE_PT = 12


def warn_small(where: str, title: str, size: int, hint: str):
    """Tell the build log when fitting had to go below readable size."""
    if size == 0:  # layout warning, not a size
        print(f"[mckinsey_pptx] WARNING {where} \"{str(title)[:50]}\": {hint}",
              file=sys.stderr)
    elif size < MIN_READABLE_PT:
        print(f"[mckinsey_pptx] WARNING {where} \"{str(title)[:50]}\": text fitted "
              f"at {size}pt (< {MIN_READABLE_PT}pt). {hint}", file=sys.stderr)


# ---------- icons ----------

def add_icon(slide, name: Optional[str], x_in, y_in, d_in, theme: Theme,
             tone: Optional[str] = None):
    """Tone-coloured circle with a white icon (or 1-2 characters) inside."""
    add_oval(slide, x_in, y_in, d_in, d_in, fill=tone_rgb(theme, tone))
    if not name:
        return
    path = ICON_DIR / f"{name}.png"
    if path.exists():
        pad = d_in * 0.22
        slide.shapes.add_picture(str(path), Inches(x_in + pad), Inches(y_in + pad),
                                 Inches(d_in - 2 * pad), Inches(d_in - 2 * pad))
        return
    label = str(name)
    if len(label) > 2:
        print(f"[mckinsey_pptx] unknown icon {label!r}; available: "
              f"{', '.join(ICONS)}", file=sys.stderr)
        label = label[:1].upper()
    tb = add_textbox(slide, x_in, y_in, d_in, d_in, anchor=MSO_ANCHOR.MIDDLE)
    write_paragraph(tb.text_frame, label, size=max(10, int(d_in * 30)),
                    bold=True, color=theme.palette.white,
                    family=theme.typography.family, align=PP_ALIGN.CENTER,
                    first=True)


# ---------- panels ----------

def add_insight_panel(slide, theme: Theme, x, y, w, h, *, title="Key insight",
                      text: Optional[str] = None, bullets: Iterable[str] = (),
                      size: Optional[int] = None):
    """Tinted side panel: small blue title, bold insight, then bullets."""
    pal = theme.palette
    bullets = list(bullets)
    inner_w = w - 0.5
    paras = [title] + ([text] if text else []) + bullets
    # Shrink the panel to its content when the text is short (no empty box).
    need = text_height_in(paras, inner_w, 14, para_gap_pt=8, indent_in=0.3,
                          bold=True) + 0.6
    if need < h * 0.7:
        h = max(need, min(h, 1.8))
    add_rect(slide, x, y, w, h, fill=pal.soft_gray)
    inner_h = h - 0.5
    if not size:
        size = fit_size(paras, inner_w, inner_h, max_size=14, min_size=10,
                        para_gap_pt=8, indent_in=0.3)
        warn_small("insight panel", text or title, size,
                   "Keep the insight to one sentence + at most 3 short bullets.")
    tb = add_textbox(slide, x + 0.25, y + 0.25, inner_w, inner_h)
    write_paragraph(tb.text_frame, title, size=size, bold=True,
                    color=pal.mid_blue, family=theme.typography.family,
                    first=True, space_after=8)
    if text:
        write_rich_paragraph(tb.text_frame, text, size=size, theme=theme,
                             bold=True, space_after=8)
    for b in bullets:
        write_rich_paragraph(tb.text_frame, b, size=size, theme=theme,
                             bullet=True, space_before=6)


def add_callout_bar(slide, theme: Theme, x, y, w, h, text, *,
                    label: Optional[str] = "Key insight", icon="lightbulb",
                    tone="blue", size: Optional[int] = None):
    """Full-width highlighted takeaway bar with an icon on the left."""
    pal = theme.palette
    add_rect(slide, x, y, w, h, fill=pal.soft_gray)
    d = min(0.42, h - 0.16)
    add_icon(slide, icon, x + 0.18, y + (h - d) / 2, d, theme, tone)
    tx = x + 0.18 + d + 0.2
    tw = w - (tx - x) - 0.2
    full = f"{label}: {text}" if label else text
    size = size or fit_size([full], tw, h - 0.12, max_size=15, min_size=10)
    tb = add_textbox(slide, tx, y, tw, h, anchor=MSO_ANCHOR.MIDDLE)
    p = write_paragraph(tb.text_frame, "", size=size, family=theme.typography.family,
                        first=True)
    p.runs[0]._r.getparent().remove(p.runs[0]._r)
    if label:
        set_run(p.add_run(), f"{label}: ", size=size, bold=True,
                color=tone_rgb(theme, tone), family=theme.typography.family)
    add_rich_runs(p, text, size=size, color=pal.text_dark,
                  family=theme.typography.family, theme=theme)
