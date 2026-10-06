---
name: mckinsey-pptx
description: Builds McKinsey-style consulting slide decks as real, editable .pptx files from a brief, notes, or Excel/Word/PDF/CSV data, choosing from 40 templates (executive summary, KPI dashboard, BCG matrix, prioritization matrix, historic+forecast charts, roadmap, Gantt, org chart, issue tree). Use when the user asks to make a PPT, deck, presentation, slides or PowerPoint, especially consulting-style business reviews, strategy reports or kickoff decks — e.g. "做一份麦肯锡风格的PPT", "帮我做个业务汇报演示文稿", "build a McKinsey deck for ...", "맥킨지 슬라이드 만들어줘".
---

# McKinsey PPTX skill

You compose McKinsey-style decks with the `mckinsey_pptx` Python package
that ships inside this skill folder. Take a brief from the user — a sentence,
a paragraph, rough data or source files — and turn it into a real `.pptx`
in which **every slide uses the right template for what it communicates**,
and you can defend each choice.

## Paths

- `SKILL_DIR` = the absolute path of the folder containing this `SKILL.md`
  (you just read it from the filesystem, so you know it). Resolve it once and
  use the absolute path everywhere below.
- Python package: `SKILL_DIR/mckinsey_pptx/`
- Template catalog (API of every template): `SKILL_DIR/mckinsey_pptx/agent/CATALOG.md`
- Working example of a Chinese deck: `SKILL_DIR/examples/demo_chinese.py`
- Output: the user's **workspace** under `output/`. Never write into `SKILL_DIR`.

## First-run setup

Use `python3` on macOS/Linux and `python` on Windows (whichever exists).

```bash
python3 -c "import pptx" || python3 -m pip install -r "SKILL_DIR/requirements.txt"
```

The only dependency is `python-pptx`. The package itself is not installed
with pip — build scripts add `SKILL_DIR` to `sys.path` (see step 6).

Optional, for visual verification: LibreOffice (`soffice`) and poppler
(`pdftoppm`). On Windows `soffice` usually lives at
`C:\Program Files\LibreOffice\program\soffice.exe`. Don't block the build on
these; the `.pptx` doesn't need them.

## Workflow — every time

1. **Understand the brief.** Identify:
   - Audience (executives, working team, board?) and purpose (decision
     request, status update, kickoff, education).
   - Real data given (numbers, lists, names) vs. what you must make up as
     illustrative placeholders. If the user points to files in the workspace
     (`.xlsx`, `.csv`, `.docx`, `.pdf`, `.md`), read them and record which
     number came from which sheet/page.
   - Language. Chinese brief → Chinese slides + Chinese theme. Korean brief →
     Korean slides + Korean theme. Otherwise English + default theme.
   - Attribution: the company/team name for the footer. Use it only if the
     user gave one (or it is in their files). Never invent one.

2. **Read the catalog.** Load `SKILL_DIR/mckinsey_pptx/agent/CATALOG.md`.
   It is the source of truth for every template's name, arguments, *Use
   when* and *Don't use when*. Never invent template names or argument shapes.

3. **Plan the story arc.** A common consulting arc:
   - `cover_slide`, or `dark_navy_summary` for the bottom line
   - `executive_summary_takeaways` for the structured argument
   - 1–3 supporting analysis slides (charts, matrices)
   - 1–2 implication slides (areas, trends, prioritization)
   - 1 roadmap or process slide (phases, waves, gantt)
   - 1 closing recommendation
   Aim for 5–10 slides unless told otherwise. McKinsey decks are tight.

4. **Pick a template per slide and write a one-line rationale** naming the
   template and why it beats the nearby alternatives, e.g.:
   - `column_historic_forecast` — actuals + forecast over 9 years; not
     `column_simple_growth` because history must be distinguished from projection.
   - `prioritization_matrix` — 9 initiatives on time-to-impact × impact; not
     `growth_share` because the axes aren't market share.
   - `phases_chevron_3` — exactly three sequential phases; not `phases_table_4`.

5. **Fill content with judgment.** Use the user's real numbers. Otherwise
   write plausible, illustrative content for the topic — don't leave generic
   `[Insert ...]` markers. Bullets short, parallel, takeaway-driven.

   **Layout / overflow rules — non-negotiable:**
   - Titles ≤ 70 chars (English), ≤ 25 Chinese characters, ≤ 50 chars Korean.
   - Bullets ≤ 15 words. In dense templates (`overview_areas`,
     `phases_table_4`, `waves_timeline_4`, `gantt_timeline`) ≤ 10 English
     words / ≤ 12 Chinese characters per bullet — columns are < 2" wide.
   - CJK text is ~1.3× wider than Latin: keep it ~25% shorter.
   - Literal `[...]` text renders as gray placeholder styling on purpose —
     never leave it in a real deck. Where a template accepts `subtitle`,
     `description` or `takeaway_header`, supply a real value.
   - Column / stacked / grouped / line / bubble charts: **always pass**
     `description=` and `takeaway_header=`.
   - Templates default to `source="xx"` / `footnote="1. xx"` in the footer.
     Always pass a real `source=` (or `source=""`) and `footnote=""` unless
     there is a real footnote.
   - `prioritization_matrix`: pass `description=` and
     `legend=(green_label, amber_label, red_label)`.
   - `three_trends_icons` / `five_key_areas` / `three_trends_table`: labels
     render as-is — write `"成本竞争力"`, not `"[成本竞争力]"`.

6. **Write the build script** at `output/build_<slug>.py` in the workspace
   (slug = short lowercase-hyphen name, e.g. `q4-business-review`):

   ```python
   import sys
   from pathlib import Path
   sys.path.insert(0, r"SKILL_DIR")          # absolute path of this skill folder
   from mckinsey_pptx import PresentationBuilder, make_zh_theme

   OUT = Path(__file__).resolve().parent
   b = PresentationBuilder(theme=make_zh_theme("某某公司"),   # see Theme
                           default_section_marker="Q4 回顾")
   b.add("cover_slide", title="...", subtitle="...", date="2026 年第四季度")
   b.add("executive_summary_takeaways", sections=[...], final_conclusion="...")
   # ... one b.add(<template>, **kwargs) per planned slide, in order
   b.save(str(OUT / "q4-business-review.pptx"))
   ```

   Only use `b.add(<template>, ...)` — never draw PowerPoint shapes by hand,
   and never edit files under `SKILL_DIR`.

7. **Build:** `python3 output/build_<slug>.py`. If it fails, fix the spec and
   rebuild.

8. **Render and inspect — mandatory when the tools exist:**
   ```bash
   soffice --headless --convert-to pdf --outdir output/preview_<slug> output/<slug>.pptx
   pdftoppm -png -r 80 output/preview_<slug>/<slug>.pdf output/preview_<slug>/slide
   ```
   Look at the PNGs and check for: text running past boxes, labels hidden
   behind shapes, titles wrapping into the underline, chart labels stacking,
   leftover `[...]` / `xx` placeholders. Shorten content and rebuild if any
   slide is broken. If the tools are missing, say the deck was not visually
   verified.

9. **Report back** in the user's language:
   - The output `.pptx` path.
   - Numbered slide list: template + one-line rationale.
   - Which numbers came from the user/files and which you made up.
   - An offer to iterate ("要把第 4 页换成别的版式吗？").

## Choosing between templates

For each slide list 1–3 candidate templates, eliminate with their *Don't use
when* clauses, then pick by item count (3 vs 5 vs 7), axis type (continuous
vs categorical) and audience. Common mistakes:

- `column_simple_growth` when forecast bars are needed → `column_historic_forecast`.
- `bubble_chart` when there are quadrant labels → `growth_share` / `prioritization_matrix`.
- `org_chart` for decomposing a problem → `issue_tree`.
- 5+ trends in `three_trends_*` → `overview_areas`.
- 15 slides when 6 would do.

## Theme

Footer attribution is blank by default (page number only).

**Chinese** — always use the Chinese theme. Latin text/numbers stay Arial;
every run gets the East Asian font so Chinese renders in 微软雅黑:

```python
from mckinsey_pptx import make_zh_theme
make_zh_theme("某某公司")                      # footer "ⓒ 2026 某某公司", brand mark "某某公司"
make_zh_theme()                                 # no company given → no attribution
make_zh_theme("某某公司", font="PingFang SC")    # user asks for 苹方
```
Other fonts on request: 思源黑体 `"Source Han Sans SC"`, 等线 `"DengXian"`.

**Korean:**
```python
from dataclasses import replace
from mckinsey_pptx import DEFAULT_THEME
KO = replace(DEFAULT_THEME,
             typography=replace(DEFAULT_THEME.typography,
                                family="Apple SD Gothic Neo",
                                east_asian_family="Apple SD Gothic Neo"),
             copyright_text="ⓒ 2026 <company>", brand_text="<company>")
```

**English:** `PresentationBuilder()` with the default theme; set attribution
with `replace(DEFAULT_THEME, copyright_text="ⓒ 2026 Acme", brand_text="Acme")`.

`copyright_text` = footer on content slides; `brand_text` = bottom-right mark
on `dark_navy_summary`; `source_label` = prefix of the footer source line.

## Iterating

The first deck is a draft. When the user asks to change a slide ("第 4 页换个
版式", "把第 2 页第三条改成 …", "做一份英文版"), edit `output/build_<slug>.py`
and rebuild — don't start over.
