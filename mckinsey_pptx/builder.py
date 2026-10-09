"""High-level builder + adaptive slide selector.

The user supplies a list of slide-spec dicts. Each spec has a `type`
(or none — in which case we auto-pick) plus payload. The builder
applies the matching template while keeping the McKinsey design intact.

Spec example:
    {"type": "executive_summary", "paragraphs": [...] }
    {"type": "column_chart", "categories": [...], "values": [...]}

If `type` is missing, `infer_slide_type` chooses based on the payload shape.
"""
from __future__ import annotations
from typing import Sequence, Optional, Dict, Any, Iterable, List

from .base import init_presentation, apply_east_asian_font
from .theme import Theme, DEFAULT_THEME
from .slides import (
    executive_summary, assessment_table, bubble_chart, column_chart,
    trends_slides, org_charts, timeline_slides, summary_slide,
    structure_slides, comparison_slides, extra_charts, process_extras,
    table_slides, card_slides, native_chart, ladder_slides,
    finance_slides, plan_slides, matrix_slides, composite_slides,
    evaluation_slides, logic_slides, analysis_slides, framework_slides,
)


# Routing table: type -> (callable, default kwargs override)
_REGISTRY = {
    # Executive summary
    "executive_summary": executive_summary.add_paragraph_summary,
    "executive_summary_paragraph": executive_summary.add_paragraph_summary,
    "executive_summary_takeaways": executive_summary.add_keytakeaway_summary,

    # Assessment
    "assessment_table": assessment_table.add_assessment_table,
    "status_overview": assessment_table.add_assessment_table,

    # Bubble / scatter
    "bubble_chart": bubble_chart.add_bubble_chart,
    "bubble_chart_takeaways": bubble_chart.add_bubble_chart_with_takeaways,
    "growth_share": bubble_chart.add_growth_share_matrix,
    "bcg_matrix": bubble_chart.add_growth_share_matrix,
    "prioritization_matrix": bubble_chart.add_prioritization_matrix,
    "assessment_matrix": bubble_chart.add_prioritization_matrix,

    # Column charts
    "column_comparison": column_chart.add_column_comparison,
    "column_simple_growth": column_chart.add_column_simple_growth,
    "column_split_growth": column_chart.add_column_split_growth,
    "column_historic_forecast": column_chart.add_column_historic_forecast,

    # Trends / areas
    "three_trends_icons": trends_slides.add_three_trends_icons,
    "three_trends_table": trends_slides.add_three_trends_table,
    "three_trends_numbered": trends_slides.add_three_trends_numbered,
    "five_key_areas": trends_slides.add_five_key_areas,

    # Org / team / hierarchy
    "issue_tree": org_charts.add_issue_tree,
    "org_chart": org_charts.add_org_chart,
    "project_team_circles": org_charts.add_project_team_circles,
    "team_chart": org_charts.add_team_chart,

    # Timeline / roadmap / process
    "phases_chevron_3": timeline_slides.add_phases_chevron_3,
    "phases_table_4": timeline_slides.add_phases_table_4,
    "waves_timeline_4": timeline_slides.add_waves_timeline_4,
    "gantt_timeline": timeline_slides.add_gantt_timeline,
    "overview_areas": timeline_slides.add_overview_areas,
    "process_activities": timeline_slides.add_process_activities,

    # Generic table
    "data_table": table_slides.add_data_table,
    "table": table_slides.add_data_table,

    # Rich layouts
    "card_grid": card_slides.add_card_grid,
    "cards": card_slides.add_card_grid,
    "swot": card_slides.add_swot,
    "card_rows": card_slides.add_card_rows,
    "chart": native_chart.add_native_chart,
    "native_chart": native_chart.add_native_chart,
    "tier_ladder": ladder_slides.add_tier_ladder,
    "waterfall": finance_slides.add_waterfall,
    "bridge": finance_slides.add_waterfall,
    "scorecard": finance_slides.add_scorecard,
    "roadmap": plan_slides.add_roadmap,
    "timeline": plan_slides.add_timeline,
    "matrix_2x2": matrix_slides.add_matrix_2x2,
    "matrix": matrix_slides.add_matrix_2x2,
    "composite": composite_slides.add_composite,
    "option_profiles": evaluation_slides.add_option_profiles,
    "decision_matrix": evaluation_slides.add_decision_matrix,
    "scoring_matrix": evaluation_slides.add_decision_matrix,
    "risk_register": evaluation_slides.add_risk_register,
    "price_ladder": ladder_slides.add_tier_ladder,

    # Logic (one page that carries an argument)
    "logic_grid": logic_slides.add_logic_grid,
    "logic_chain": logic_slides.add_logic_grid,
    "strategic_challenge": logic_slides.add_strategic_challenge,
    "key_question": logic_slides.add_strategic_challenge,
    "storyline_summary": logic_slides.add_storyline_summary,
    "cycle": analysis_slides.add_cycle,
    "flywheel": analysis_slides.add_cycle,
    "risk_heatmap": analysis_slides.add_risk_heatmap,
    "risk_matrix": analysis_slides.add_risk_heatmap,
    "positioning_scale": analysis_slides.add_positioning_scale,
    "value_chain": analysis_slides.add_value_chain,
    "phase_grid": plan_slides.add_phase_grid,
    "implementation_grid": plan_slides.add_phase_grid,
    "evaluation_matrix": evaluation_slides.add_evaluation_matrix,
    "business_model_canvas": framework_slides.add_business_model_canvas,
    "bmc": framework_slides.add_business_model_canvas,
    "strategic_triangle": framework_slides.add_strategic_triangle,
    "hub_spoke": framework_slides.add_hub_spoke,

    # Summary
    "dark_navy_summary": summary_slide.add_dark_navy_summary,

    # Structural slides
    "cover_slide": structure_slides.add_cover_slide,
    "cover": structure_slides.add_cover_slide,
    "section_divider": structure_slides.add_section_divider,
    "agenda": structure_slides.add_agenda,
    "stat_hero": structure_slides.add_stat_hero,
    "big_number": structure_slides.add_stat_hero,
    "quote_slide": structure_slides.add_quote_slide,
    "quote": structure_slides.add_quote_slide,

    # Comparison
    "comparison_table": comparison_slides.add_comparison_table,
    "option_compare": comparison_slides.add_comparison_table,
    "pros_cons": comparison_slides.add_pros_cons,
    "two_column_compare": comparison_slides.add_two_column_compare,
    "before_after": comparison_slides.add_two_column_compare,

    # Extra charts
    "stacked_column_chart": extra_charts.add_stacked_column_chart,
    "stacked_column": extra_charts.add_stacked_column_chart,
    "grouped_column_chart": extra_charts.add_grouped_column_chart,
    "grouped_column": extra_charts.add_grouped_column_chart,
    "line_chart": extra_charts.add_line_chart,

    # Process / metric overview
    "process_flow_horizontal": process_extras.add_process_flow_horizontal,
    "process_flow": process_extras.add_process_flow_horizontal,
    "funnel": process_extras.add_funnel,
    "kpi_dashboard": process_extras.add_kpi_dashboard,
}


def infer_slide_type(spec: Dict[str, Any]) -> str:
    """Adaptive picker — choose a template by what payload shape was supplied."""
    # Structural / single-purpose
    if "stat" in spec and "stat_label" in spec:
        return "stat_hero"
    if "quote" in spec and "author" in spec:
        return "quote_slide"
    if "section_number" in spec and "section_title" in spec:
        return "section_divider"
    if "client" in spec and "title" in spec and "items" not in spec:
        return "cover_slide"
    if "items" in spec and isinstance(spec.get("items"), list) \
            and spec["items"] and isinstance(spec["items"][0], str):
        return "agenda"

    # Comparison
    if "options" in spec and "criteria" in spec:
        return "comparison_table"
    if "pros" in spec and "cons" in spec:
        return "pros_cons"
    if "left_items" in spec and "right_items" in spec:
        return "two_column_compare"

    # KPIs / funnels / process flow
    if "kpis" in spec:
        return "kpi_dashboard"
    if "stages" in spec:
        return "funnel"

    # Extra charts (series-shaped data)
    if "series" in spec and "categories" in spec:
        first = spec["series"][0] if spec["series"] else {}
        if spec.get("chart") == "line" or "values" in first \
                and spec.get("kind") == "line":
            return "line_chart"
        if spec.get("chart") == "stacked":
            return "stacked_column_chart"
        if spec.get("chart") == "grouped":
            return "grouped_column_chart"
        # default for series + categories: stacked
        return "stacked_column_chart"

    if "body" in spec and len(spec) <= 4:
        return "dark_navy_summary"
    if "paragraphs" in spec and "sections" not in spec:
        return "executive_summary_paragraph"
    if "sections" in spec:
        return "executive_summary_takeaways"
    if "categories" in spec and isinstance(spec["categories"], list) \
            and spec["categories"] and isinstance(spec["categories"][0], dict) \
            and "rows" in spec["categories"][0]:
        return "assessment_table"
    if "main_drivers" in spec:
        return "issue_tree"
    if "branches" in spec:
        return "org_chart"
    if "leader" in spec and "members" in spec:
        return "project_team_circles"
    if "functions" in spec:
        return "team_chart"
    if "weeks" in spec and "workstreams" in spec:
        return "gantt_timeline"
    if "waves" in spec:
        return "waves_timeline_4"
    if "phases" in spec:
        first = spec["phases"][0] if spec["phases"] else {}
        if "outcomes" in first or "activities" in first:
            return "phases_table_4"
        return "phases_chevron_3"
    if "steps" in spec:
        return "process_activities"
    if "areas" in spec:
        first = spec["areas"][0] if spec["areas"] else {}
        if "bullets" in first:
            return "overview_areas"
        return "five_key_areas"
    if "trends" in spec:
        first = spec["trends"][0] if spec["trends"] else {}
        if "examples" in first:
            return "three_trends_table"
        if spec.get("numbered"):
            return "three_trends_numbered"
        return "three_trends_icons"
    if "bus" in spec:
        return "growth_share"
    if "items" in spec and spec["items"] and "x_band" in spec["items"][0]:
        return "prioritization_matrix"
    if "bubbles" in spec:
        return ("bubble_chart_takeaways" if spec.get("takeaways")
                else "bubble_chart")
    if "values" in spec and "categories" in spec:
        if "forecast_from_index" in spec:
            return "column_historic_forecast"
        if "split_index" in spec:
            return "column_split_growth"
        if spec.get("growth_pct"):
            return "column_simple_growth"
        return "column_comparison"
    raise ValueError(f"Cannot infer slide type from spec keys: {list(spec.keys())}")


# Templates without the standard title band (no kicker above a title).
_FULL_BLEED = {"cover_slide", "dark_navy_summary", "section_divider", "quote_slide"}


def add_kicker(slide, text, theme):
    """Small letter-spaced label above the slide title ("OPTION 1 | LEASING")."""
    from .base import add_textbox, write_paragraph
    from .components import letter_space
    layout, pal = theme.layout, theme.palette
    tb = add_textbox(slide, layout.margin_left_in, 0.16,
                     layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
                     - layout.section_marker_w_in - 0.3, 0.26)
    p = write_paragraph(tb.text_frame, str(text).upper(), size=10, bold=True,
                        color=pal.mid_blue, family=theme.typography.family, first=True)
    letter_space(p, 200)


def add_nav(slide, sections, current, theme):
    """Section breadcrumb at the top-left: one small chevron per section, the
    current one dark (where the slide sits in the deck's storyline)."""
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Emu
    from .base import write_paragraph
    from .design import tint
    from .metrics import fit_one_line, text_width_pt
    layout, pal = theme.layout, theme.palette
    avail = (layout.slide_width_in - layout.margin_left_in - layout.margin_right_in
             - layout.section_marker_w_in - 0.3)
    n = len(sections)
    cur = current if isinstance(current, int) else (
        list(sections).index(current) if current in sections else -1)
    if cur < 0:
        import sys
        print(f"[mckinsey_pptx] WARNING nav: {current!r} is not one of {list(sections)}",
              file=sys.stderr)
    size = 10
    ws = [text_width_pt(s, size, True) / 72 / 0.9 + 0.45 for s in sections]
    if sum(ws) > avail:
        k = avail / sum(ws)
        ws = [w * k for w in ws]
        size = min(fit_one_line(s, w - 0.4, 10, 7, True) for s, w in zip(sections, ws))
    x, y, h = layout.margin_left_in, 0.13, 0.26
    for i, (s, w) in enumerate(zip(sections, ws)):
        shp = slide.shapes.add_shape(MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON,
                                     Inches(x), Inches(y), Inches(w + 0.08), Inches(h))
        shp.adjustments[0] = 0.4
        shp.shadow.inherit = False
        shp.line.fill.background()
        shp.fill.solid()
        on = i == cur
        shp.fill.fore_color.rgb = pal.mid_blue if on else tint(pal.mid_blue, 0.88)
        tf = shp.text_frame
        tf.margin_left, tf.margin_right = Inches(0.18), Inches(0.08)
        tf.margin_top = tf.margin_bottom = Emu(0)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = False
        write_paragraph(tf, s, size=size, bold=on, color=pal.white if on else pal.footer_gray,
                        family=theme.typography.family, align=PP_ALIGN.CENTER, first=True)
        x += w + 0.02


# ---------- focus check ----------

def _labels(v):
    if isinstance(v, str):
        return [v]
    if isinstance(v, dict):
        return [v.get(k) for k in ("title", "label", "name", "head") if v.get(k)][:1]
    return []


def focus_candidates(name: str, kw: Dict[str, Any]) -> List[str]:
    """Item labels of a focus-capable template (None: template has no focus)."""
    L: List[str] = []
    if name == "growth_share":
        for b in kw.get("bus", []):
            L += _labels(b)
    elif name == "matrix_2x2":
        for q in kw.get("quadrants", []):
            L += _labels(q)
        for p in kw.get("points", []):
            L += _labels(p)
    elif name == "prioritization_matrix":
        for it in kw.get("items", []):
            L += _labels(it)
    elif name == "cycle":
        for st in kw.get("steps") or [x for p in kw.get("paths", []) for x in p]:
            L += _labels(st)
    elif name == "risk_heatmap":
        for r in kw.get("risks", []):
            L += _labels(r)
    elif name in ("process_flow_horizontal", "funnel"):
        for st in kw.get("steps", kw.get("stages", [])):
            L += _labels(st)
    elif name == "issue_tree":
        for m in kw.get("main_drivers", []):
            L += _labels(m)
            for s2 in m.get("secondaries", []) or []:
                L += _labels(s2)
                for u in s2.get("underlying", []) or []:
                    L += _labels(u)
    elif name == "org_chart":
        for b in kw.get("branches", []):
            L += _labels(b) + list(b.get("reports", []) or [])
    elif name == "hub_spoke":
        for sp in kw.get("spokes", []):
            L += _labels(sp)
    else:
        return None
    return [str(x) for x in L if x]


def title_names(title: str, labels: Sequence[str]) -> List[str]:
    """Labels the action title mentions (whole words for Latin, substrings for CJK)."""
    import re
    from .metrics import _CJK, plain
    t = plain(title).lower()
    hits = []
    for lab in labels:
        l_ = plain(lab).strip().lower()
        if not l_:
            continue
        if _CJK.search(l_):
            if len(l_) >= 2 and l_ in t:
                hits.append(lab)
        elif len(l_) >= 3 and re.search(r"(?<!\w)" + re.escape(l_) + r"(?!\w)", t):
            hits.append(lab)
    return hits


def _check_title_focus(name, kw):
    labels = focus_candidates(name, kw)
    if labels is None or kw.get("focus") is not None or kw.get("highlight") is not None:
        return
    hits = title_names(kw.get("title", ""), labels)
    if hits:
        import sys
        from .metrics import plain
        t = plain(kw.get("title", "")).lower()
        # the item named first is usually the subject; longer label wins a tie
        hits = sorted(set(hits), key=lambda h: (t.find(plain(h).lower()), -len(h)))
        also = f" (also matches {', '.join(map(repr, hits[1:]))})" if hits[1:] else ""
        print(f"[mckinsey_pptx] WARNING {name} \"{str(kw.get('title', ''))[:50]}\": the title "
              f"names {hits[0]!r}{also} — pass focus={hits[0]!r} so that item carries the "
              f"accent, or focus=[] if the word is incidental and no item is focal.",
              file=sys.stderr)


def template_name(fn) -> str:
    """Canonical template name for a registry callable (aliases collapse)."""
    canon = {v: k for k, v in reversed(list(_REGISTRY.items()))}
    return canon.get(fn, fn.__name__)


class PresentationBuilder:
    """Compose a full deck of McKinsey-style slides."""

    def __init__(self, theme: Theme = DEFAULT_THEME, *,
                 auto_page_numbers: bool = True,
                 default_section_marker: Optional[str] = None,
                 nav: Optional[Sequence[str]] = None):
        """nav: the deck's chapters (["Overview", "Situation", ...]); a slide
        added with nav="Situation" (or an index) shows the breadcrumb bar."""
        self.theme = theme
        self.nav = list(nav) if nav else None
        self.auto_page_numbers = auto_page_numbers
        self.default_section_marker = default_section_marker
        self.prs = init_presentation(theme)
        self._page = 0

    # Direct add by type
    def add(self, slide_type: str, **kwargs):
        fn = _REGISTRY.get(slide_type)
        if fn is None:
            raise ValueError(f"Unknown slide type: {slide_type}. "
                             f"Available: {sorted(_REGISTRY)}")
        if self.auto_page_numbers:
            self._page += 1
            kwargs.setdefault("page_number", self._page)
        if (self.default_section_marker is not None
                and "section_marker" not in kwargs):
            kwargs["section_marker"] = self.default_section_marker
        kwargs.setdefault("theme", self.theme)
        kicker = kwargs.pop("kicker", None)
        group = kwargs.pop("group", None)
        nav = kwargs.pop("nav", None)
        name = template_name(fn)
        _check_title_focus(name, kwargs)
        out = fn(self.prs, **kwargs)
        slide = self.prs.slides[-1]
        if nav is not None and self.nav and name not in _FULL_BLEED:
            # one line of space above the title: the breadcrumb replaces the kicker
            add_nav(slide, self.nav, nav, kwargs["theme"])
        elif kicker and name not in _FULL_BLEED:
            add_kicker(slide, kicker, kwargs["theme"])
        # Record template (+ parallel group) on the slide (<p:cSld name>) so
        # scripts/deck_check.py can check layout variety and consistency.
        slide._element.cSld.set("name", "mp:" + name + (f"|{group}" if group else ""))
        return out

    # Adaptive add (type optional)
    def add_spec(self, spec: Dict[str, Any]):
        spec = dict(spec)  # copy
        slide_type = spec.pop("type", None) or infer_slide_type(spec)
        return self.add(slide_type, **spec)

    def add_specs(self, specs: Iterable[Dict[str, Any]]):
        return [self.add_spec(s) for s in specs]

    def save(self, path: str):
        ea = self.theme.typography.east_asian_family
        if ea:
            apply_east_asian_font(self.prs, ea)
        self.prs.save(path)
        return path


def build_from_spec(specs: Sequence[Dict[str, Any]], output_path: str, *,
                    theme: Theme = DEFAULT_THEME,
                    auto_page_numbers: bool = True,
                    default_section_marker: Optional[str] = None) -> str:
    """Convenience function: spec list in, .pptx out."""
    b = PresentationBuilder(theme=theme,
                            auto_page_numbers=auto_page_numbers,
                            default_section_marker=default_section_marker)
    b.add_specs(specs)
    return b.save(output_path)
