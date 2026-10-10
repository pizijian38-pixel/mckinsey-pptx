from dataclasses import dataclass, field, replace
from typing import Optional
from pptx.util import Pt, Inches, Emu
from pptx.dml.color import RGBColor


def rgb(hex_str: str) -> RGBColor:
    h = hex_str.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


@dataclass(frozen=True)
class Palette:
    dark_navy: RGBColor = field(default_factory=lambda: rgb("0F2A4A"))
    deep_navy: RGBColor = field(default_factory=lambda: rgb("0A1F3D"))
    bright_blue: RGBColor = field(default_factory=lambda: rgb("2E9BD6"))
    mid_blue: RGBColor = field(default_factory=lambda: rgb("1F6FA8"))
    light_blue: RGBColor = field(default_factory=lambda: rgb("4FB2E5"))
    royal_blue: RGBColor = field(default_factory=lambda: rgb("2A2AE5"))
    black: RGBColor = field(default_factory=lambda: rgb("000000"))
    white: RGBColor = field(default_factory=lambda: rgb("FFFFFF"))
    text_dark: RGBColor = field(default_factory=lambda: rgb("1A1A1A"))
    rule_gray: RGBColor = field(default_factory=lambda: rgb("999999"))
    light_gray: RGBColor = field(default_factory=lambda: rgb("E8E8E8"))
    soft_gray: RGBColor = field(default_factory=lambda: rgb("F2F2F2"))
    grid_gray: RGBColor = field(default_factory=lambda: rgb("D0D0D0"))
    footer_gray: RGBColor = field(default_factory=lambda: rgb("888888"))
    placeholder_gray: RGBColor = field(default_factory=lambda: rgb("BFBFBF"))
    status_green: RGBColor = field(default_factory=lambda: rgb("4CAF50"))
    status_amber: RGBColor = field(default_factory=lambda: rgb("F4C57A"))
    status_red: RGBColor = field(default_factory=lambda: rgb("E04E5E"))


@dataclass(frozen=True)
class Typography:
    family: str = "Arial"
    # East Asian (CJK) typeface. PowerPoint renders Chinese/Japanese/Korean
    # glyphs with the run's <a:ea> font, not the Latin one, so set this for
    # CJK decks. None leaves the PowerPoint default in place.
    east_asian_family: Optional[str] = None
    title_size: int = 24
    section_title_size: int = 14
    body_size: int = 12
    small_size: int = 10
    footer_size: int = 9
    chart_label_size: int = 10
    chart_axis_size: int = 10


@dataclass(frozen=True)
class Layout:
    slide_width_in: float = 13.333
    slide_height_in: float = 7.5
    margin_left_in: float = 0.45
    margin_right_in: float = 0.45
    margin_top_in: float = 0.35
    margin_bottom_in: float = 0.3
    title_top_in: float = 0.45
    title_height_in: float = 0.7
    title_underline_top_in: float = 1.15
    body_top_in: float = 1.40
    footer_top_in: float = 7.05
    section_marker_w_in: float = 1.4
    section_marker_h_in: float = 0.3


@dataclass(frozen=True)
class Theme:
    palette: Palette = field(default_factory=Palette)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)
    # Bottom-right footer text on every content slide. Empty -> page number only.
    copyright_text: str = ""
    # Bottom-right brand mark on full-bleed slides (e.g. dark_navy_summary).
    brand_text: str = ""
    # Prefix for the `source=` line in the footer.
    source_label: str = "Source: "
    # Slide language ("en" | "zh" | "ko" | "ja"): default labels such as
    # "Key insight" are drawn in this language (see labels.py).
    lang: str = "en"


DEFAULT_THEME = Theme()


def make_zh_theme(company: Optional[str] = None, *,
                  font: str = "Microsoft YaHei",
                  latin_font: str = "Arial",
                  year: int = 2026,
                  base: Theme = DEFAULT_THEME) -> Theme:
    """Simplified-Chinese theme: Latin text in `latin_font`, Chinese glyphs in
    `font` (微软雅黑 by default; "PingFang SC" is the macOS-native choice).

    `company` fills the footer copyright ("ⓒ 2026 <company>") and the brand
    mark on full-bleed slides. Leave it None to keep both blank.
    """
    return replace(
        base,
        typography=replace(base.typography, family=latin_font,
                           east_asian_family=font),
        copyright_text=f"ⓒ {year} {company}" if company else "",
        brand_text=company or "",
        source_label="资料来源：",
        lang="zh",
    )


ZH_THEME = make_zh_theme()


def _mix(hex_a: str, hex_b: str, t: float) -> RGBColor:
    a, b = rgb(hex_a), rgb(hex_b)
    return RGBColor(*(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))


def make_brand_theme(primary: str, accent: Optional[str] = None, *,
                     base: Theme = DEFAULT_THEME) -> Theme:
    """Re-colour the deck from a brand colour (hex, e.g. "0B4DA2").

    `primary` replaces the navy family (headers, titles bands, dark slides);
    `accent` (default: a lighter tint of primary) replaces the bright blue
    used for highlights. Semantic red / green / amber stay as they are.
    Combine with make_zh_theme by passing its result as `base`.
    """
    p = primary.lstrip("#")
    acc = (accent or "").lstrip("#")
    pal = replace(
        base.palette,
        deep_navy=_mix(p, "000000", 0.15),
        dark_navy=rgb(p),
        mid_blue=_mix(p, "FFFFFF", 0.18),
        # accent must carry white text (table highlight headers, tiers)
        bright_blue=rgb(acc) if acc else _mix(p, "FFFFFF", 0.3),
        light_blue=_mix(acc or p, "FFFFFF", 0.6),
    )
    return replace(base, palette=pal)


_LANG_DEFAULTS = {
    # lang: (latin font, east-asian font, source label)
    "en": ("Arial", None, "Source: "),
    "zh": ("Arial", "Microsoft YaHei", "资料来源："),
    "ko": ("Arial", "Malgun Gothic", "출처: "),
    "ja": ("Arial", "Yu Gothic", "出典："),
}


def make_theme(company: Optional[str] = None, *, lang: str = "en",
               brand: Optional[str] = None, accent: Optional[str] = None,
               font: Optional[str] = None, year: int = 2026,
               base: Theme = DEFAULT_THEME) -> Theme:
    """One-stop theme: attribution + language + brand colours.

    lang: "en" | "zh" | "ko" | "ja" — sets the CJK font and the footer
          "Source:" label in the deck's language (use the slide language,
          not the chat language).
    company: footer "ⓒ <year> <company>" and the dark-slide brand mark.
    brand / accent: hex colours, see make_brand_theme.
    font: override the CJK font (zh: "PingFang SC", "Source Han Sans SC" ...).
    """
    latin, cjk, label = _LANG_DEFAULTS.get(lang, _LANG_DEFAULTS["en"])
    t = replace(
        base,
        typography=replace(base.typography, family=latin,
                           east_asian_family=font or cjk),
        copyright_text=f"ⓒ {year} {company}" if company else "",
        brand_text=company or "",
        source_label=label,
        lang=lang if lang in _LANG_DEFAULTS else "en",
    )
    return make_brand_theme(brand, accent, base=t) if brand else t
