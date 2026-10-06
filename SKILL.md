---
name: mckinsey-pptx
description: Builds McKinsey-style consulting slide decks as real, editable .pptx files from a brief, a deck outline, or Excel/Word/PDF/CSV data, choosing from 41 templates (executive summary, data table, KPI dashboard, BCG matrix, prioritization matrix, historic+forecast charts, roadmap, Gantt, org chart, issue tree). Use when the user asks to make a PPT, deck, presentation, slides or PowerPoint, especially consulting-style business reviews, marketing or strategy plans, or turning an outline document into a deck — e.g. "做一份麦肯锡风格的PPT", "根据大纲做演示文稿", "build a McKinsey deck from this outline", "맥킨지 슬라이드 만들어줘".
---

# McKinsey PPTX skill

You compose McKinsey-style decks with the `mckinsey_pptx` Python package
that ships inside this skill folder, and turn the user's material into a real
`.pptx` in which **every slide uses the right template for what it
communicates**, and you can defend each choice.

## Paths

- `SKILL_DIR` = the absolute path of the folder containing this `SKILL.md`
  (you just read it from the filesystem, so you know it). Resolve it once and
  use the absolute path everywhere below.
- Python package: `SKILL_DIR/mckinsey_pptx/`
- Template catalog (API of every template): `SKILL_DIR/mckinsey_pptx/agent/CATALOG.md`
- Deck checker: `SKILL_DIR/scripts/deck_check.py`
- Working example of a Chinese deck: `SKILL_DIR/examples/demo_chinese.py`
- Output: the user's **workspace** under `output/`. Never write into `SKILL_DIR`.

## First-run setup

Use `python3` on macOS/Linux and `python` on Windows (whichever exists).

```bash
python3 -c "import pptx" || python3 -m pip install -r "SKILL_DIR/requirements.txt"
```

The only dependency is `python-pptx`. The package itself is not installed
with pip — build scripts add `SKILL_DIR` to `sys.path` (see step 5).

Optional, for visual verification: LibreOffice (`soffice`) and poppler
(`pdftoppm`). On Windows `soffice` usually lives at
`C:\Program Files\LibreOffice\program\soffice.exe`. Don't block the build on
these; the `.pptx` doesn't need them.

---

## Step 0 — Pick the mode. Everything else depends on it.

**Source mode** — the user gives you material the deck must be built from:
a deck outline ("Slide 1: … Slide 2: …"), a report, a plan, a spreadsheet,
or says "based on the file / framework in the folder". Most real requests
with files are source mode.

**Brief mode** — the user gives only a short description ("make a Q4 review
deck, revenue 120bn, 2 KPIs late") and no document to follow.

If unsure, it is source mode whenever a document in the workspace describes
the deck's content.

### Source-mode rules (non-negotiable)

1. **The source is the spec, not inspiration.** Every section of the source
   gets at least one slide, in the source's order. Do not merge, drop or
   reorder sections on your own. If the source is clearly too long for the
   stated use (e.g. 40 sections for a 10-minute talk), ask the user before
   cutting.
2. **Every table and every number in the source appears in the deck** —
   as a `data_table`, a chart, a KPI tile or inside the text. A 6-brand ×
   4-year table stays 6 × 4; don't reduce it to one year.
3. **Numbers come only from the source.** No invented metrics, baselines,
   deltas, revenue splits, store counts, dates or rankings. If a template
   slot needs a number the source doesn't have, leave the slot out, or write
   `[待补充]` / `[TBD]` and list it in your report. A KPI tile without a
   source baseline gets no delta.
4. **No invented sources.** Pass `source=` only with a source the input
   actually cites ("Nielsen", "Table 1 of the outline"). Otherwise
   `source=""`.
5. **Elaborate in words, not in facts.** You may expand a terse source bullet
   into a header plus supporting points, explaining what it means, why it
   matters and what follows from it — using only facts already in the
   source. You may not add new brands, products, people, numbers or events.
6. **Language follows the source document**, not the language of the
   user's chat message. An English outline makes an English deck even if
   the user wrote to you in Chinese — unless the user explicitly asks for a
   translation ("做成中文版"). Keep product, brand and campaign names as the
   source writes them.

### Brief-mode rules

- Use the user's real numbers. Where the brief is thin you may write
  illustrative content, but **mark every made-up number as illustrative** in
  your report ("illustrative — replace with actuals"), never present it as
  fact, and never invent a source attribution.
- Language: the language the user writes in, unless they ask otherwise.

---

## Step 1 — Understand the material and the use

- **Audience** (executives, working team, board, class/jury) and **use**:
  - *Live presentation* — fewer words per slide, one message per slide.
  - *Pre-read / leave-behind / plan document* — slides must carry the full
    argument on their own: denser, every claim backed on the slide.
  "给高管看" alone does not mean "cut content"; a marketing or strategy *plan*
  is a pre-read unless the user says it is a short talk.
- **Slide count:**
  - Source mode: driven by the source — roughly one slide per section, plus
    a cover, an optional agenda / section dividers for 15+ slides, and a
    closing slide. Never fewer slides than source sections.
  - Brief mode: 5–10 slides unless told otherwise.
- **Attribution**: the company/team name for the footer — only if the user
  gave one or it is in their files.
- If the user points to files (`.xlsx`, `.csv`, `.docx`, `.pdf`, `.md`), read
  them fully, including tables.

## Step 2 — Read the catalog

Load `SKILL_DIR/mckinsey_pptx/agent/CATALOG.md`. It is the source of truth
for every template's name, arguments, *Use when* and *Don't use when*. Never
invent template names or argument shapes.

## Step 3 — Write the slide plan first

Before writing any build code, write `output/<slug>_plan.md` — a table with
one row per slide:

| # | Source section | Message (action title) | Template | Source data used |
|---|---|---|---|---|

In source mode, check the plan against the source before continuing:
every section is in the plan; every source table is in the "data used"
column of some slide. Fix the plan, not the source.

**Action titles.** Each title states the slide's takeaway as a claim
("Crest is losing share while local players gain"), not a topic
("Competitive landscape"). Take the claim from the source's own key message;
keep the source's section name as the `section_marker` or subtitle if useful.

## Step 4 — Fill each slide to the right density

**Slide anatomy for content slides:** action title → optional subtitle →
2–4 content blocks → (analysis slides) a key insight.

- Each source bullet becomes a **block header**, followed by 1–3 supporting
  points drawn from the source (its details, its tables, and the logical
  "so what"). A slide with four one-line bullets and nothing else is too
  thin.
- Every analysis slide (market, competition, segments, channels, SWOT)
  carries a **key insight**: one sentence on what the data means for the
  decision. Templates with a takeaway / insight slot: `data_table`
  (`insight`), chart templates (`takeaways`), `executive_summary_takeaways`
  (`final_conclusion`).
- Use the source's numbers inside the text ("from 8.8% in 2022 to 8.0% in
  2025"), not vague words ("declined slightly").

**Data → template rules:**

| Source content | Template |
|---|---|
| Any table (text or numbers) | `data_table` — all rows and columns, `highlight_rows` for "us", `insight` for the takeaway |
| One metric over time | `column_simple_growth`; with forecast → `column_historic_forecast` |
| 2–4 entities over time | `line_chart` (and the full table in `data_table` if there are more entities) |
| Shares by category, two periods | `grouped_column_chart` |
| Parts of a whole | `stacked_column_chart` |
| Target KPIs (2–8) | `kpi_dashboard` — delta only if the source gives a baseline |
| Legacy vs. new / as-is vs. to-be | `two_column_compare`, or `data_table` if the source is a table |
| Options × features (text) | `data_table` with `highlight_col` — never Harvey balls without source ratings |
| Strengths / weaknesses / SWOT | `data_table` (factor × impact) or `pros_cons` (S+O vs. W+T) |
| Audience persona (profile, psychographics, pain points, behaviour) | `executive_summary_takeaways` — one section per aspect |
| 3 / 5 / 7 parallel items with detail | `three_trends_*` / `five_key_areas` / `overview_areas` |
| Phases / roadmap | `phases_chevron_3`, `phases_table_4`, `waves_timeline_4`, `gantt_timeline` |

**Layout / overflow rules:**
- Titles must fit on **one line** (the underline sits right below it):
  ≤ ~75 characters English, ≤ ~34 Chinese characters. Put the rest of the
  message in the subtitle or the key insight.
- `cover_slide`: `client` and `date` are one short line each (e.g. "Group 8",
  "2026"); put a long key message in `subtitle`.
- In dense templates (`overview_areas`, `phases_table_4`, `waves_timeline_4`,
  `gantt_timeline`) columns are < 2" wide — keep each bullet to one short
  line there, and move detail to a `data_table` slide if needed.
- Fit is checked by rendering (step 7), not by cutting content in advance.
  If a slide overflows, first pick a roomier template or split the slide;
  shorten wording only after that, and never by dropping source data.
- Literal `[...]` text renders as gray placeholder styling on purpose. Where a
  template accepts `subtitle`, `description` or `takeaway_header`, pass a real
  value. Chart templates: **always pass** `description=` and `takeaway_header=`.
- Templates default to `source="xx"` / `footnote="1. xx"`. Always pass
  `source=` (a real cited source, or `""`) and `footnote=""`.
- `prioritization_matrix`: pass `description=` and `legend=(green, amber, red)`.
- `**bold**` markup works only in `data_table` cells and its insight panel;
  everywhere else it prints the asterisks.
- `three_trends_icons` / `five_key_areas` / `three_trends_table`: labels
  render as-is — write `"Cost leadership"`, not `"[Cost leadership]"`.

## Step 5 — Write the build script

`output/build_<slug>.py` in the workspace (slug = short lowercase-hyphen name):

```python
import sys
from pathlib import Path
sys.path.insert(0, r"SKILL_DIR")          # absolute path of this skill folder
from mckinsey_pptx import PresentationBuilder, DEFAULT_THEME, make_zh_theme

OUT = Path(__file__).resolve().parent
b = PresentationBuilder(theme=DEFAULT_THEME,          # see Theme
                        default_section_marker="Marketing plan 2026")
b.add("cover_slide", title="...", subtitle="...", date="2026")
b.add("data_table", title="...", columns=[...], rows=[...],
      highlight_rows=[...], insight="...", source="")
# ... one b.add(<template>, **kwargs) per row of the plan, in order
b.save(str(OUT / "<slug>.pptx"))
```

Only use `b.add(<template>, ...)` — never draw PowerPoint shapes by hand,
and never edit files under `SKILL_DIR`.

## Step 6 — Build and check against the source

```bash
python3 output/build_<slug>.py
python3 "SKILL_DIR/scripts/deck_check.py" output/<slug>.pptx --source <each source file>
```

The checker reports:
1. **Numbers not found in the sources** → in source mode, remove each one or
   trace it to the source (a derived figure like a difference is fine if you
   say so in the report). In brief mode, list them as illustrative.
2. **Source numbers used** → in source mode aim for ≥ 90%; for every unused
   number either add it or say in the report why it was left out.
3. **Sparse slides** (text fill < 12%; cover / divider / closing slides are
   exempt) → add the source's supporting detail, a key insight, or switch
   to a denser template.
4. **Leftover placeholders** → fill or remove.

Fix and rebuild until the checker is clean or every remaining item is
explained.

## Step 7 — Render and inspect (mandatory when the tools exist)

```bash
soffice --headless --convert-to pdf --outdir output/preview_<slug> output/<slug>.pptx
pdftoppm -png -r 80 output/preview_<slug>/<slug>.pdf output/preview_<slug>/slide
```

On Windows: wait for `soffice` to finish before reading the PDF (it may
return early; check the PDF exists and is non-empty, retry once). If
`pdftoppm` is missing, convert with PyMuPDF (`pip install pymupdf`;
`fitz.open(pdf)[i].get_pixmap(dpi=80).save(...)`).

Look at every PNG and check: text running past boxes, labels hidden behind
shapes, titles wrapping into the underline, chart labels stacking, large
empty areas, leftover `[...]` / `xx`. Fix and rebuild. If the tools are
missing, say the deck was not visually verified.

## Step 8 — Report back (in the user's language)

- The output `.pptx` path and slide count.
- Numbered slide list: template + one-line rationale (from the plan).
- Source mode: section coverage ("20/20 sections, 7/7 tables"), checker
  results, every `[待补充]` slot, any source data left out and why.
- Brief mode: which numbers came from the user and which are illustrative.
- An offer to iterate ("要把第 4 页换成别的版式吗？").

## Choosing between templates

For each slide list 1–3 candidate templates, eliminate with their *Don't use
when* clauses, then pick by item count (3 vs 5 vs 7), axis type (continuous
vs categorical) and audience. Common mistakes:

- Cutting a multi-year, multi-entity table down to one year → `data_table` / `line_chart`.
- Text features in `comparison_table` Harvey balls → `data_table`.
- `column_simple_growth` when forecast bars are needed → `column_historic_forecast`.
- `bubble_chart` when there are quadrant labels → `growth_share` / `prioritization_matrix`.
- `org_chart` for decomposing a problem → `issue_tree`.
- 5+ trends in `three_trends_*` → `overview_areas`.

## Theme

Footer attribution is blank by default (page number only).

**Chinese** — always use the Chinese theme for Chinese slides. Latin
text/numbers stay Arial; every run gets the East Asian font so Chinese
renders in 微软雅黑:

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
and the plan, rebuild, and re-run the checker — don't start over.
