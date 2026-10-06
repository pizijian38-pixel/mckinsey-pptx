"""Text measurement (Arial metrics via Pillow when available)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

TONE_NAMES = ("navy", "blue", "mid_blue", "light_blue", "red", "green",
              "amber", "gray", "gold")


def plain(text) -> str:
    """Text with markup removed (for measuring)."""
    return re.sub(r"\{(?:%s)\|(.+?)\}" % "|".join(TONE_NAMES), r"\1",
                  str(text)).replace("**", "")


_CJK = re.compile(r"[\u2e80-\u9fff\uac00-\ud7af\uff00-\uffef]")
_FONT_CANDIDATES = (  # (regular, bold)
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf",
     "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
     "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ("/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf",
     "/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf"),
)
_REF = 100
_fonts = None


def _measure_font(bold=False):
    """Arial-metric fonts for measuring Latin text (None -> heuristic)."""
    global _fonts
    if _fonts is None:
        _fonts = (None, None)
        try:
            from PIL import ImageFont
            for reg, bld in _FONT_CANDIDATES:
                if Path(reg).exists():
                    _fonts = (ImageFont.truetype(reg, _REF),
                              ImageFont.truetype(bld, _REF) if Path(bld).exists()
                              else None)
                    break
        except Exception:
            pass
    return _fonts[1] if bold and _fonts[1] is not None else _fonts[0]


def _latin_width(text: str, size: float, bold=False) -> float:
    f = _measure_font(bold)
    if f is not None:
        w = f.getlength(text) * size / _REF
        # regular font standing in for bold
        return w * 1.08 if bold and _fonts[1] is None else w
    w = 0.0
    for c in text:
        w += 0.66 if (c.isupper() or c in "MW%@") else 0.28 if c in " ilj.,;:'|!" else 0.5
    return w * size * (1.1 if bold else 1.0)


def text_width_pt(text: str, size: float, bold=False) -> float:
    t = plain(text)
    cjk = len(_CJK.findall(t))
    latin = _CJK.sub("", t)
    return _latin_width(latin, size, bold) + cjk * size


def _wrap_lines(text: str, width_pt: float, size: float, bold=False) -> int:
    """Greedy word wrap (CJK breaks anywhere) -> number of lines."""
    t = plain(text)
    tokens = re.findall(r"[\u2e80-\u9fff\uac00-\ud7af\uff00-\uffef]|\S+\s*", t)
    lines, cur = 1, 0.0
    for tok in tokens:
        w = text_width_pt(tok, size, bold)
        if cur + w > width_pt and cur > 0:
            lines += 1
            cur = text_width_pt(tok.rstrip(), size, bold)
        else:
            cur += w
    return lines


def text_height_in(paragraphs: Sequence[str], width_in: float, size: float,
                   line_spacing=1.2, para_gap_pt=4.0, indent_in=0.0,
                   bold=False) -> float:
    width_pt = max((width_in - indent_in) * 72, 1)
    lines = sum(_wrap_lines(p, width_pt, size, bold) for p in paragraphs)
    gaps = max(len(paragraphs) - 1, 0) * para_gap_pt
    return (lines * size * line_spacing + gaps) / 72


def fit_size(paragraphs: Sequence[str], width_in: float, height_in: float,
             max_size=16, min_size=10, **kw) -> int:
    for s in range(max_size, min_size - 1, -1):
        if text_height_in(paragraphs, width_in, s, **kw) <= height_in:
            return s
    return min_size


def fit_one_line(text: str, width_in: float, max_size: int, min_size: int,
                 bold=False) -> int:
    """Largest size at which `text` fits on a single line."""
    for s in range(max_size, min_size - 1, -1):
        if text_width_pt(text, s, bold) <= width_in * 72 * 0.95:
            return s
    return min_size
