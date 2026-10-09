---
name: mckinsey-pptx
description: Builds consulting-style business presentations as real, editable .pptx files from a brief, a deck outline, or Excel/Word/PDF/CSV data, choosing from 80 templates and a composite layout (marimekko, treemap, sankey, slopegraph, dumbbell, bump charts, heat maps, radar, venn, swimlanes, layer stacks, fishbone, customer journey, logic grids, strategic-challenge and storyline summary pages, flywheels, risk heat maps, positioning scales, value chains, phase grids, evaluation matrices, business model canvas, strategic triangle, hub-and-spoke, option profiles, decision matrices, risk registers, card grids, data tables, native charts, waterfalls, scorecards, roadmaps, timelines, 2x2 matrices, SWOT, flows, org charts). Use when the user asks to make a PPT, deck, presentation, slides or PowerPoint for any business purpose — performance reviews / QBRs, board or steering updates, strategy and market entry, strategy cases and strategic analyses, options evaluations and proposals, project status, investment cases, operations improvement, marketing or product plans — or to turn an outline document into a deck, e.g. "做一份麦肯锡风格的PPT", "根据大纲做演示文稿", "做个季度业务回顾", "build a board update deck", "맥킨지 슬라이드 만들어줘".
---

# McKinsey PPTX skill

You compose McKinsey-style decks with the `mckinsey_pptx` Python package
that ships inside this skill folder, and turn the user's material into a real
`.pptx` in which **every slide uses the right template for what it
communicates**, and you can defend each choice.

## Working rules (read first)

1. **Two commands do the mechanics** — use them instead of ad-hoc
   `python -c` one-liners (each one-off command may need the user's
   approval; these two are the approved path):
   - `python SKILL_DIR/scripts/catalog.py` — one-line index of all templates;
     `python SKILL_DIR/scripts/catalog.py sankey slopegraph venn` — the full
     entries (arguments + runnable example) for just those templates.
   - `python SKILL_DIR/scripts/run_deck.py output/build_<slug>.py --source <file>`
     — builds, checks and renders in one go (finds LibreOffice on Windows,
     waits for the PDF, writes PNGs + `contact_sheet.png`).
2. **Attachments are files on disk — read them, never retype them.** When the
   user attaches or names a file, find its path in the conversation context
   (Antigravity keeps uploads in the conversation's `.user_uploaded/` folder;
   other hosts give an absolute path) and pass that path to `--source`. A
   hand-typed copy loses tables and numbers, and the checker then compares
   the deck against your copy instead of the real source. Can't find it? Ask
   the user for the path — don't search the whole disk, don't reconstruct it.
3. **The checker is a reviewer, not a score.** Don't open `deck_check.py` or
   the package source to learn how findings are computed; read the report and
   fix the deck. Coverage ([2]) exists to show source facts you missed —
   never add numbers, words or phrases (e.g. "10-slide") to raise it or to
   shorten the vocabulary list. Advisory sections ([2] [3] [5c] [11]) never
   require changing a correct slide. If a finding is wrong, say so in the
   report.
4. **Pick the template from the relationship, not the topic** (table below).

## Pick the template by the relationship

Ask of every content slide: *what relationship does it show?* Then start
from this table (newest templates first). Get the API with `catalog.py <name>`.

| The content is… | Use | Instead of |
|---|---|---|
| A whole split into parts (one split) | `treemap`; ≤ 5 parts → `chart` doughnut | cards listing segments |
| A whole split two ways (segment × player, region × channel) | `marimekko` | a numeric `data_table` |
| Volume moving through stages, splitting or merging | `sankey` | `process_flow`, `funnel` |
| Several items at two points in time — direction of change | `slopegraph` | before/after table |
| Several items — the gap between two values (now vs target, us vs best) | `dumbbell` | two-column text |
| Rank order over 3–6 periods | `bump` | a table of ranks |
| One measure over two categorical dimensions | `heatmap` | a numeric `data_table` |
| Options profiled on 3–8 criteria on one scale | `radar`; with weights → `decision_matrix` | cards per option |
| Causes of one observed problem | `fishbone` | cards of causes |
| Steps across several actors / hand-offs | `swimlane` | `process_flow` |
| Customer steps with feelings or pain points | `journey` | `process_flow` |
| Layers that build on each other (stack, operating model) | `layer_stack` | `card_rows` |
| 2–3 overlapping conditions or groups | `venn` | cards |
| Trend or magnitude by period / category | `chart` (line / column / bar) | a numeric `data_table` |
| A change between two totals, explained by drivers | `waterfall` | cards of drivers |
| Reinforcing loop, flywheel, vicious cycle | `cycle` | `card_rows` |
| One concept and its 3–6 parts or stakeholders | `hub_spoke` | `card_grid` |
| Positioning / prioritising on two dimensions | `matrix_2x2`, `growth_share`, `prioritization_matrix` | cards |
| Risks by probability × impact | `risk_heatmap` (owners → `risk_register`) | `card_rows` |
| Factor → impact → implication, per topic | `logic_grid` | cards |
| Decomposing a goal or question | `issue_tree` | bullets |
| Sequence of steps, one actor; narrowing quantity | `process_flow`; `funnel` | `card_rows` |
| Plan over time; KPIs vs target | `roadmap` / `timeline` / `phase_grid`; `scorecard` | tables |
| **Really a list** of parallel points with detail | `card_grid` / `card_rows` — the right choice | — |
| A text table (options × facets, as-is / to-be) | `data_table` | — |

Text layouts are correct when the content is a list. The checker's section
[11] reminds you when they fill more than half of the content slides — a
prompt to look at those slides again, not a rule to satisfy.

## Paths

- `SKILL_DIR` = the absolute path of the folder containing this `SKILL.md`
  (you just read it from the filesystem, so you know it). Resolve it once and
  use the absolute path everywhere below.
- Python package: `SKILL_DIR/mckinsey_pptx/`
- Template catalog (API of every template): `SKILL_DIR/mckinsey_pptx/agent/CATALOG.md`
- Template lookup: `SKILL_DIR/scripts/catalog.py` (index / named entries)
- Build + check + render: `SKILL_DIR/scripts/run_deck.py`
- Deck checker (run by `run_deck.py`): `SKILL_DIR/scripts/deck_check.py`
- Working example of a Chinese deck: `SKILL_DIR/examples/demo_chinese.py`
- Output: the user's **workspace** under `output/`. Never write into `SKILL_DIR`.

## First-run setup

Use `python3` on macOS/Linux and `python` on Windows (whichever exists).

```bash
python -m pip install -r "SKILL_DIR/requirements.txt"
```

(Safe to re-run: pip skips what is installed.) Write every command as a single
command — Windows PowerShell 5 rejects `&&` and `||`; run two commands as two
steps instead of chaining them.

The only dependency is `python-pptx`. The package itself is not installed
with pip — build scripts add `SKILL_DIR` to `sys.path` (see step 5).

Optional, for visual verification: LibreOffice, plus poppler (`pdftoppm`)
or PyMuPDF (`pip install pymupdf`) for the PNGs. `run_deck.py` finds them
itself (including `C:\Program Files\LibreOffice\program\soffice.exe`) and
says what is missing. Don't block the build on these; the `.pptx` doesn't
need them.

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
4. **No invented sources.** `source=` names a publisher or dataset the input
   actually cites ("Nielsen Retail Audit", "Kantar Household Panel"). A
   table's caption, a section name or "the outline" is **not** a source —
   use `source=""` then.
5. **Elaborate, don't decide.** You may expand a terse source bullet into a
   header plus supporting points: restate it, explain what it means, connect
   it to another fact *in the source*, or say what follows from it for the
   decision. You may **not** add anything the source doesn't contain, in
   particular:
   - new targets, KPIs, rankings or superlatives ("#1 in the region",
     "fastest-growing", "market-leading");
   - new partners, customers, suppliers or deal types ("strategic
     partnership with …", "exclusive agreement");
   - new products, features, offers, tiers or pricing ("a premium
     subscription tier", "bundled packs");
   - new markets, channels, sites, regions, campaigns or dates;
   - new ownership, credential or regulatory claims ("proprietary",
     "patented", "certified", "FDA-cleared", "clinically proven");
   - new causes, mechanisms or customer / employee behaviour the source
     doesn't state, and invented colour ("driven by bureaucracy",
     "loved by Gen Z", "in every boardroom").
   Test for every supporting point: *can I point to the sentence in the
   source it comes from, or is it a plain logical consequence of two source
   facts?* If not, delete it. Two true points beat three padded ones; a card
   with one source bullet may stay short.
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

### The user's request is a spec too (both modes)

1. **Prescribed structure is binding.** If the request fixes the slide
   count, the order, or what each slide must contain ("slide 6: rationale,
   roadmap, risk & mitigation"; "each option: why, how, advantages,
   disadvantages"), every named element becomes a **visible, labelled
   block** on that slide, in that order. Don't drop, merge or rename
   elements; if space is tight, shorten each block rather than losing one.
2. **Constraints on a slide are binding.** "No preference yet", "neutral",
   "don't recommend", "facts only" → on that slide no `highlight_col` /
   `highlight_rows`, no favouring tones (green for one option), no
   evaluative insight; label the bottom bar neutrally ("Preliminary view").
3. **Thinking tasks come before layout.** When the request asks you to
   verify, stress-test, challenge, correct, complement or decide (not only to
   lay out), do that work in the plan first: list the questions the audience
   will ask (e.g. "what if utilisation is 12 h, not 16 h?"), answer each from
   the source, and record what you changed and why. The deck then shows the
   corrected position. You may complement the source when asked to — but
   flag every addition in "Inferences added", show how derived numbers are
   computed, and never present an addition as sourced fact.

---

## Step 1 — Understand the material and the use

- **Audience** (executives, working team, board, class/jury) and **use**:
  - *Live presentation* — fewer words per slide, one message per slide.
  - *Pre-read / leave-behind / plan document* — slides must carry the full
    argument on their own: denser, every claim backed on the slide.
  "给高管看" alone does not mean "cut content"; a plan, review or report built
  from a document is a pre-read unless the user says it is a short talk.
- **Slide count:**
  - Source mode: driven by the source — roughly one slide per section, plus
    a cover, an optional agenda / section dividers for 15+ slides, and a
    closing slide. Never fewer slides than source sections.
  - Brief mode: 5–10 slides unless told otherwise.
- **Attribution**: the company/team name for the footer — only if the user
  gave one or it is in their files.
- If the user points to or attaches files (`.xlsx`, `.csv`, `.docx`, `.pdf`,
  `.md`), read them fully from their real path, including tables (working
  rule 2). These paths are the `--source` files in step 6.

## Step 2 — Look up the templates

1. Run `python SKILL_DIR/scripts/catalog.py` once — the index of every
   template with its *Use when* line.
2. For each slide, name the relationship (table above) and 1–3 candidate
   templates; then run `catalog.py <candidates…>` for their full entries
   (arguments, *Don't use when*, a runnable example).
   `catalog.py --guide` prints "Choosing between similar templates".

The catalog (`CATALOG.md`) is the source of truth for names and arguments —
never invent template names or argument shapes. Don't page through
CATALOG.md by line ranges or grep it for templates you already know; the
newer diagram templates sit at the end and get missed that way.

## Step 3 — Write the slide plan first

Before writing any build code, write `output/<slug>_plan.md` — a table with
one row per slide:

| # | Source section | Required elements (from the request) | Message (action title) | Relationship | Template | Why not text cards | Source data used | Inferences added |
|---|---|---|---|---|---|---|---|---|

"Required elements" copies what the user asked that slide to contain
(or "—"); after building, tick each one off against the rendered slide.

"Relationship" names what the slide shows, in the words of the table above
("whole split two ways", "gap per item", "causes of one problem", "list").
"Why not text cards": for a diagram or chart, "—"; for `card_grid`,
`card_rows`, `data_table` or `swot`, say in a few words why the content is
really a list ("4 parallel initiatives, no order or quantity"). If you
can't, pick the diagram.

"Inferences added" lists every supporting point or insight that is a
consequence you drew rather than a sentence from the source — so the user
can check them. Keep it short; most rows should say "—".

In source mode, check the plan against the source before continuing:
every section is in the plan; every source table is in the "data used"
column of some slide. Fix the plan, not the source.

**Action titles.** Each title states the slide's takeaway as a claim
("EMEA margin fell 3 pts as freight costs doubled", "Two of five
workstreams are behind plan"), not a topic ("EMEA results", "Project
status"). Take the claim from the source's own key message;
keep the source's section name as the `section_marker` or subtitle if useful.

**Focus follows the title.** When the title singles out one item of a
diagram ("*Batteries* are the only question mark worth funding", "the
programme is in its *build* phase"), pass that item as `focus=` — on
`growth_share`, `matrix_2x2`, `prioritization_matrix`, `cycle`,
`risk_heatmap`, `process_flow`, `funnel`, `issue_tree`, `org_chart`,
`hub_spoke`, `marimekko`, `treemap`, `sankey`, `slopegraph`, `dumbbell`,
`fishbone`, `journey`, `heatmap`, `radar`, `venn`, `bump`, `swimlane`,
`layer_stack`. The focal item gets the accent and everything else turns
neutral; one or two focal items per slide, never more. Write the focal item
next to the template in the plan ("growth_share · focus Batteries"). If the
title makes no claim about one item, leave `focus` out (or `focus=[]` to
silence the build warning).

## Step 4 — Fill each slide to the right density

**Slide anatomy for content slides:** action title → optional subtitle →
2–4 content blocks → (analysis slides) a key insight.

- Each source bullet becomes a **block header**, followed by 1–3 supporting
  points drawn from the source (its details, its tables, and the logical
  "so what"). A slide with four one-line bullets and nothing else is too
  thin.
- Every analysis slide (market, competition, segments, channels, SWOT)
  carries a **key insight**. Every rich template has an `insight` slot
  (`card_grid`, `chart`, `data_table`, `swot`, `tier_ladder`); older chart
  templates use `takeaways`.
- **What a key insight is:** one sentence that *synthesises* — it combines
  two or more data points, or states what the data means for the decision
  ("Growth came entirely from new customers; the base shrank 4%"). It is
  **not** a restatement of the title, of one table row, or of the cards above.
  - Insight panels next to a table or chart: the insight sentence plus at
    most **3** bullets, each comparing or connecting data — never one bullet
    per table row (the table already shows the rows).
  - If you can't write an insight that adds something beyond the title, leave
    `insight` out. Not every slide needs one; objectives, roadmaps and
    reference tables often don't.
- **Analysis pages end in a "so what" for the company.** On situation pages
  (market, customers, competitors, PEST, five forces) the last column, band
  or bar says what the facts mean for the company — "Competitive
  advantage", "Impact on <company>", "Implication". In `logic_grid` that is
  the conclusion column; in `composite` the last column or a `callout`.
  The conclusion must follow from the cells beside it; in source mode,
  list it under "Inferences added" unless the source states it.
- **Show the chain, not just the list.** When a slide argues A → B → C
  (cause → effect → consequence), use a layout whose columns or rows carry
  that order (`logic_grid`, `composite` with `connectors`,
  `strategic_challenge`), with column headers that name each step.
- **Name the bottom bar for its role** (`insight_label=`): "Bottom line",
  "Verdict", "Implication", "What it takes", "Preliminary view", "Decision
  needed" — not "Key insight" on every slide.
- **Emphasis:** in the rich templates mark the 1–3 things the reader must
  see per card or panel — key numbers in `**bold**`, problems / declines in
  `{red|…}`, growth / targets in `{green|…}`. Don't colour whole sentences.
- **Icons:** give each `card_grid` card an `icon` that matches its meaning
  (names in CATALOG, e.g. `alert` for risks, `money` for cost, `users` for
  customers or people, `trend_up` for growth, `clock` for time,
  `settings` for operations). Use `tone` for meaning, not decoration.
- Use the source's numbers inside the text ("from 12.4% to 9.8% in two
  years"), not vague words ("declined slightly").

**Data → template rules:**

The relationship table at the top comes first; this table covers the
remaining cases. Default to the **rich templates** (41–80); they use larger type, fit text to
the space, support emphasis and icons, and produce editable tables and
charts. Use the older templates (1–40) for what they uniquely cover. When no
single template fits a slide that mixes content types, build it with
`composite` regions instead of forcing it into one template.

| Content | Template |
|---|---|
| **Scores, ratings or rankings against criteria** (weighted evaluation, vendor / option scoring, maturity ratings) | **table, not a chart**: `decision_matrix` (weights, raw + weighted scores, best per row, totals); plain ratings → `data_table` |
| 2–4 options / products / scenarios side by side, each with the same facets (summary, key numbers, pros, cons) | `option_profiles` |
| One option / initiative / product in depth (how it works + numbers + why / how / pros / cons + verdict) | `composite` (e.g. `flow` + `kv_table` on the left, 2×2 `cards` on the right) |
| One option read as an argument (current situation → strategy → advantages → disadvantages; how it addresses the challenge → key activities → impact) | `composite` with `headers` + `connectors=True`; `callout` for the value proposition, `pyramid` for positioning, `sections` for feasibility / pros / cons |
| **A chain of reasoning per topic** (external situation → capability → advantage; customer need → what we do → performance → implication; factor → impact → implication) | `logic_grid` — one row per topic, conclusion column on the right |
| PEST, five forces, stakeholders — each with "current situation" and "influence on us" | `logic_grid(direction="down")` |
| Drivers that converge on one threat and the key question of the deck | `strategic_challenge` |
| Executive summary of a problem-solving deck (situation → question → options → recommendation) | `storyline_summary` |
| Effects that reinforce each other (flywheel, network effect, vicious cycle) | `cycle` (branch with feedback, or `steps` loop; `kind="vicious"`) |
| Risks by probability × impact, one mitigation each | `risk_heatmap`; owners / several mitigations → `risk_register` |
| Competitors' relative position on several indicators | `positioning_scale` |
| Industry stages with KSFs, margins or prices; own stages marked | `value_chain` |
| Implementation plan: same row types per stage (partners / actions / resources), bars across years, KPI rows, risk panel | `phase_grid` |
| Option scores **with a reason per cell**, dot ratings, criteria grouped by dimension, or a "why these criteria" formula | `evaluation_matrix` (text-only with `rating=None`) |
| Business model | `business_model_canvas`; internal alignment around a goal → `strategic_triangle`; one concept and its 3–6 parts → `hub_spoke` |
| Risks with severity, owner or mitigation | `risk_register` |
| **Numeric** series where *magnitude or trend* is the point (by period or category) | `chart`: `line` = trend, `column` / `bar` = compare or rank, `grouped_column` = two periods side by side, `stacked_column` = composition, `doughnut` = share of one total. `highlight` the focus item, add an `insight`. Full `data_table` on a following slide only if the chart can't show every value |
| Change between two totals, explained by drivers (bridge, variance, price-volume-mix) | `waterfall` |
| KPIs with target vs. actual and status | `scorecard` |
| Headline numbers / targets (2–4) | `card_grid` with `value` per card |
| **Text** table, or mixed text and numbers | `data_table` (all rows and columns; `highlight_rows` / `highlight_col`) |
| Options × criteria, as-is vs. to-be, feature comparison | `data_table`; `comparison_table` only when the source gives ratings |
| Executive summary (situation / complication / resolution / ask) | `card_grid` (2×2) with `insight` = the bottom line |
| 2–8 parallel points with detail (drivers, initiatives, risks, segments, workstreams) | `card_grid` |
| 2–6 items needing a sentence each (decisions, recommendations, risks + mitigation) | `card_rows` |
| Two-dimension prioritisation (impact × effort, likelihood × severity) | `matrix_2x2`; market-share × growth → `growth_share` |
| SWOT or any S/W/O/T subset | `swot` |
| Tiers that step up (service / price tiers, maturity levels) | `tier_ladder` |
| Workstreams over time with milestones | `roadmap`; 3–7 dated events → `timeline`; weekly detail → `gantt_timeline` |
| Linear process (4–6 steps), funnel, issue tree, org chart | `process_flow_horizontal`, `funnel`, `issue_tree`, `org_chart` |
| Single bold statement / chapter break | `dark_navy_summary`, `section_divider` |

**Common deck types** — when the user has no outline (brief mode) or asks
for a type of deck, start from the matching spine and adapt it:

| Deck type | Typical spine |
|---|---|
| Performance review (QBR, monthly / annual results) | summary `card_grid` → `scorecard` → `chart`s of key trends → `waterfall` of the main variance → issues `card_rows` → actions / outlook |
| Strategy / market entry | summary → market `chart`s → competition `data_table` / `matrix_2x2` → options `data_table` → recommendation `card_grid` → `roadmap` |
| Project / programme status | status `scorecard` → `roadmap` with milestones → risks `card_rows` → decisions needed `card_rows` |
| Strategy case / strategic analysis (MBA case, strategy review) | `storyline_summary` → situation `logic_grid`s (firm: need → what we do → performance → implication; competition and new entrants) + `chart`s, `cycle` for a flywheel → `strategic_challenge` → `option_profiles` → one `composite` per option (`headers` + `connectors`, `group="options"`) → `evaluation_matrix` (or `decision_matrix`) → recommendation (`card_grid` rationale + `phase_grid` / `roadmap`) → `risk_heatmap` / `risk_register` → appendix: `business_model_canvas`, `strategic_triangle`, `logic_grid(direction="down")` for PEST / five forces, `positioning_scale`, `value_chain`, `swot`, `data_table`. With 10+ slides, set chapters with `PresentationBuilder(nav=[...])` and pass `nav=` per slide |
| Options evaluation / proposal | `option_profiles` (neutral) → one `composite` per option (`group="options"`, same regions each time) → `decision_matrix` → recommendation `card_grid` + `roadmap` → `risk_register` |
| Investment / business case | ask (`dark_navy_summary`) → problem / opportunity → options → financials `chart` / `waterfall` → risks → `timeline` |
| Operations / process improvement | baseline `chart` → root causes `issue_tree` / `card_grid` → initiatives `matrix_2x2` → impact `waterfall` → `roadmap` |
| Board / steering update | one-page summary → `scorecard` → decisions needed → appendix tables |
| Marketing / product plan | market & customer → positioning `data_table` → offer / `tier_ladder` → channels & campaigns `card_grid` → targets & budget `chart` |

These are starting points, not rules: in source mode the source's own
structure always wins.

**Parallel slides look alike.** When consecutive slides cover parallel items
(option 1 / 2 / 3, product A / B / C, region by region, one slide per
workstream), give them **the same template and the same block order**, and
pass the same `group=` to each (`b.add(..., group="options")`). Readers
compare them side by side; a different layout for one of them reads as a
different kind of content. Inside the shared frame, swap a block only when
that item lacks the data (e.g. no unit economics for one option → a
priority list in the same position).

**Vary the layouts** across different kinds of content. At most **three**
slides in a row with the same template unless they share a `group` (a
`swot` counts as a `card_grid`; `card_rows` is a different layout). If the source has numeric
series, the deck must contain at least one `chart`. When a run gets long,
re-express one slide differently — e.g. targets as `card_grid` values, a
list of drivers as a `chart` of their sizes, a profile or option set as a
`data_table` (aspect × detail). The checker (step 6) flags violations.

**Layout / overflow rules:**
- Titles must fit on **one line** (the underline sits right below it):
  ≤ ~75 characters English, ≤ ~34 Chinese characters. Put the rest of the
  message in the subtitle or the key insight.
- `kicker=` puts a small label above the title that says where the slide
  sits in the argument ("Option 2 | Outsource to 3PL", "Recommendation (1/2)
  | Roadmap"). Use it on every content slide of a structured deck; keep it
  under ~60 characters.
- `default_section_marker` / `section_marker` is a short label in a small
  top-right box: ≤ 20 characters ("Reignite 2026", "Market review").
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
- `**bold**` / `{tone|…}` markup works only in the rich templates (41–45);
  older templates print it literally.
- `three_trends_icons` / `five_key_areas` / `three_trends_table`: labels
  render as-is — write `"Cost leadership"`, not `"[Cost leadership]"`.

## Step 5 — Write the build script

`output/build_<slug>.py` in the workspace (slug = short lowercase-hyphen name):

```python
import sys
from pathlib import Path
sys.path.insert(0, r"SKILL_DIR")          # absolute path of this skill folder
from mckinsey_pptx import PresentationBuilder, make_theme

OUT = Path(__file__).resolve().parent
b = PresentationBuilder(theme=make_theme("Acme"),     # see Theme
                        default_section_marker="Marketing plan 2026")
b.add("cover_slide", title="...", subtitle="...", date="2026")
b.add("data_table", title="...", columns=[...], rows=[...],
      highlight_rows=[...], insight="...", source="")
# ... one b.add(<template>, **kwargs) per row of the plan, in order
b.save(str(OUT / "<slug>.pptx"))
```

Only use `b.add(<template>, ...)` — never draw PowerPoint shapes by hand,
and never edit files under `SKILL_DIR`.

## Step 6 — Build, check and render (one command)

```bash
python "SKILL_DIR/scripts/run_deck.py" output/build_<slug>.py --source <each source file>
```

It runs the build, prints build WARNINGs, runs the checker on the deck the
build wrote, renders PNGs into `output/preview_<slug>/` and ends with a
summary (build / check / render). Exit status 0 = nothing to fix. Brief mode:
no `--source`. Add `--no-render` while iterating on fixes.

The checker reports:
1. **Numbers not found in the sources** → in source mode, remove each one or
   trace it to the source (a derived figure like a difference is fine if you
   say so in the report). In brief mode, list them as illustrative.
2. **Source numbers used** → in source mode aim for ≥ 90%; for every unused
   number either add it or say in the report why it was left out.
3. **Thin text slides** (advisory, source mode only; charts, tables,
   roadmaps and other visual templates are exempt) → add supporting detail
   *if the source has it*. Never pad a slide with invented points to fill
   space — a short slide is better than a fabricated one, and live talks are
   meant to be light.
4. **Leftover placeholders** → fill or remove.
5. **Content not in the sources**
   - a) forbidden claim types (superlatives, exclusivity / ownership,
     credentials, partnerships, commitments — e.g. `#1`, `fastest`,
     `proprietary`, `certified`, `partnership`) and b) quoted terms that the source doesn't
     contain → delete the point, or trace it to the source sentence.
   - c) vocabulary not in the sources, per slide → re-read every slide with
     many new words and apply rule 5's test to each supporting point. Plain
     explanatory words are fine; new facts, features, places or behaviours
     are not.
6. **Layout variety** → more than three slides of the same template in a
   row (outside a `group`), a mostly numeric table shown with no chart in
   the deck, or a `group` whose slides use different templates → fix the
   layout (parallel slides share one template; other runs get re-expressed).
7. **Small body text (< 12pt)** → shorten the longest bullets, drop the
   subtitle or the insight bar, or split the slide. The build also prints
   `[mckinsey_pptx] WARNING ... text fitted at Npt` — treat it the same way.
   The build also warns when a title names a diagram item but `focus` is not
   set, or when `focus` matches no item — fix the call, don't ignore it.
8. **Footer source line** → wrong-language label (fix `make_theme(lang=)`)
   or a caption used as a source (use `source=""`).
9. **Insight restates a table row** → replace with a bullet that compares or
   connects rows, or drop it.
10. **English default labels in a CJK deck** → build the theme with
   `make_theme(lang=...)` (the slide language) so default labels are
   translated, or pass the labels yourself.
11. **Layout mix** (advisory, never fails) → text layouts on more than half
   of the content slides. Re-check those slides against the relationship
   table; keep the ones that really are lists.

Fix and rebuild until the checker is clean or every remaining item is
explained in the report. Fix the deck, not the report: never reword a
correct point or add words just to clear a finding (working rule 3).

## Step 7 — Inspect the previews (mandatory when they rendered)

`run_deck.py` wrote `output/preview_<slug>/contact_sheet.png` (every slide
on one image) and `slide-NN.png`. Look at the contact sheet first, then open
single slides that look wrong. If the summary says the render was not done,
install what it names (LibreOffice; `pip install pymupdf` if `pdftoppm` is
missing) once — don't write your own conversion commands.

Check: text running past boxes, labels hidden behind
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

Start from the relationship table at the top. For each slide list 1–3 candidate templates, eliminate with their *Don't use
when* clauses, then pick by item count (3 vs 5 vs 7), axis type (continuous
vs categorical) and audience. Common mistakes:

- Cutting a multi-year, multi-entity table down to one year → `data_table` / `line_chart`.
- Text features in `comparison_table` Harvey balls → `data_table`.
- `column_simple_growth` when forecast bars are needed → `column_historic_forecast`.
- `bubble_chart` when there are quadrant labels → `growth_share` / `prioritization_matrix`.
- `org_chart` for decomposing a problem → `issue_tree`.
- 5+ trends in `three_trends_*` → `overview_areas`.
- A market split by segment *and* by player → `marimekko`; split one way → `treemap`.
- Volume that splits into several outcomes → `sankey`; one narrowing quantity → `funnel`.
- Two points in time for several series → `slopegraph`; a gap per category → `dumbbell`.
- Causes of one observed problem → `fishbone`; decomposing a goal → `issue_tree`.
- Steps a customer goes through *and how they feel* → `journey`; without feelings → `process_flow`.
- Area and width charts take values >= 0 only; for gains and losses use `waterfall`.
- One measure over two categorical dimensions → `heatmap`; risks on probability × impact → `risk_heatmap`.
- Options profiled on 3–8 criteria of one scale → `radar`; with a reason per cell → `evaluation_matrix`.
- Rank over 3–6 periods → `bump`; a process across several actors → `swimlane`; stacked layers → `layer_stack`; 2–3 overlapping conditions → `venn`.

## Theme

Always build the theme with **`make_theme`** — one call sets the slide
language, the footer attribution and (optionally) brand colours:

```python
from mckinsey_pptx import make_theme
make_theme()                                         # English, no attribution
make_theme("Acme Corp")                              # English, footer "ⓒ 2026 Acme Corp"
make_theme("Acme Corp", brand="0B4DA2")              # + brand colour (accent= optional)
make_theme("某某公司", lang="zh")                     # Chinese slides: 微软雅黑, "资料来源："
make_theme("某某公司", lang="zh", font="PingFang SC") # 苹方 (or "Source Han Sans SC", "DengXian")
make_theme("<company>", lang="ko")                   # Korean slides
```

- `lang` is the language **of the slides** (step 0, rule 6), never the
  language the user chats in. Using `lang="zh"` for an English deck puts
  "资料来源：" in every footer — the checker flags it.
- `lang` also translates every **default label** templates draw ("Key
  insight" → "关键洞察", "Weighted total" → "加权总分", "Recommended" →
  "推荐", SWOT headers, "Low / High", "Option A" → "方案 A" …). A Chinese
  deck built without `lang="zh"` shows English labels — never do that.
  Labels you pass explicitly are drawn as given, so write them in the slide
  language.
- `company`: only if the user gave it or it is in their files. Footer
  attribution is blank otherwise (page number only).
- `brand`: when the user names a brand colour, or the brand has a well-known
  one. Semantic red / green / amber stay as they are.
- Older helpers (`make_zh_theme`, `make_brand_theme`) still work.

## Iterating

The first deck is a draft. When the user asks to change a slide ("第 4 页换个
版式", "把第 2 页第三条改成 …", "做一份英文版"), edit `output/build_<slug>.py`
and the plan, rebuild, and re-run the checker — don't start over.
