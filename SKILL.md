---
name: mckinsey-pptx
description: Builds consulting-style business presentations as real, editable .pptx files from a brief, a deck outline, or Excel/Word/PDF/CSV data, choosing from 80 templates and a composite layout (marimekko, treemap, sankey, slopegraph, dumbbell, heat maps, radar, swimlanes, fishbone, customer journey, logic grids, strategic-challenge and storyline summaries, risk heat maps, value chains, phase grids, evaluation and decision matrices, business model canvas, native charts, waterfalls, scorecards, roadmaps, 2x2 matrices, SWOT, org charts). Use when the user asks to make a PPT, deck, presentation, slides or PowerPoint for any business purpose — performance reviews / QBRs, board or steering updates, strategy and market entry, strategy cases, options evaluations and proposals, project status, investment cases, operations improvement, marketing or product plans — or to turn an outline document into a deck, e.g. "做一份麦肯锡风格的PPT", "根据大纲做演示文稿", "做个季度业务回顾", "build a board update deck", "맥킨지 슬라이드 만들어줘".
---

# McKinsey PPTX skill

You compose McKinsey-style decks with the `mckinsey_pptx` Python package
that ships inside this skill folder, and turn the user's material into a real
`.pptx` in which **every slide uses the right template for what it
communicates**, and you can defend each choice.

## Working rules (read first)

1. **Run only these terminal commands** — anything else (a `python -c`
   snippet, `dir` / `ls` over folders, `Test-Path`, `pip list`, `New-Item`)
   stops the run for the user's approval. `SKILL_DIR` is the folder of this
   SKILL.md (don't search the disk for it); output goes to the workspace
   `output/`, never into `SKILL_DIR`. Write files with your file tool, view
   PNGs with your file viewer. Expect 6–10 commands for a whole deck.
   - `python "SKILL_DIR/scripts/read_source.py" "<attachment path>"` — the
     source as text, every table as a Markdown table (docx / xlsx / pptx /
     pdf / md / csv).
   - `python "SKILL_DIR/scripts/catalog.py"` — index of all templates; then
     **one** call per need: `catalog.py --plan output/<slug>_plan.md` (checks
     the plan, prints the entries it needs), or
     `catalog.py data_table fishbone --icons` for named templates; other
     flags: `--guide --options --focus --theme --spines`.
   - `python "SKILL_DIR/scripts/run_deck.py" output/build_<slug>.py --source "<path>" --plan output/<slug>_plan.md`
     — builds, checks and renders (PNGs + `contact_sheet.png`). Run
     `run_deck.py --env` once; only if it says `python-pptx : MISSING`:
     `python -m pip install -r "SKILL_DIR/requirements.txt"`.
   Use `python3` on macOS/Linux, `python` on Windows. One command per call:
   PowerShell 5 rejects `&&` and `||`.
2. **Attachments are files on disk — read them, never retype them.** Find the
   path in the conversation context (Antigravity: the attachment / media entry
   of the request, a path like `…\brain\<id>\.user_uploaded\media_….docx`),
   read it with `read_source.py`, and pass the same path to `--source`. **The
   attachment is the source even when a similar file already sits in the
   workspace** (an older copy, `source_outline.md`): a hand-typed copy loses
   tables and numbers, and the checker would compare against your copy. Can't
   find it? Ask for the path; don't search the disk.
3. **A new request builds a new deck.** New plan, new build script. Plans,
   scripts and decks already in `output/` are not your draft: don't open or
   reuse them; use a new slug if the name is taken. Edit an existing script
   only when the user asks to change that deck (see Iterating).
4. **Everything you need is in this file and `catalog.py`.** Don't read, grep
   or search the package source, `deck_check.py` or `assets/`. If something
   isn't there, say so in the report instead of reverse-engineering it.
5. **The checker is a reviewer, not a score.** Fix the deck, not the report;
   never add numbers or words to raise coverage or clear a finding. Advisory
   sections ([2] [3] [5c] [11]) never require changing a correct slide. If a
   finding is wrong, say so in the report.
6. **Pick the template from the relationship, not the topic** (table below).
   Optional for visual checks: LibreOffice + poppler or PyMuPDF; `run_deck.py`
   finds them and says what is missing. The `.pptx` doesn't need them.

## Pick the template by the relationship

Ask of every content slide: *what relationship does it show?* Then start
from this table (newest templates first). Get the API with `catalog.py <name>`.

| The content is… | Use | Instead of |
|---|---|---|
| A whole split into parts (one split) | `treemap`; ≤ 5 parts → `chart` doughnut | cards listing segments |
| A whole split two ways (segment × player, region × channel) | `marimekko` | a numeric `data_table` |
| Volume moving through stages, splitting or merging | `sankey` | `process_flow`, `funnel` |
| **Several players / segments over 3+ periods** (share, sales, price) | `chart` `line`, every series; `highlight={"series": <the one the title is about>}`; ≤ ~8 lines | the source table as a `data_table` |
| Several items at two points in time — direction of change | `slopegraph` | before/after table |
| Several items — the gap between two values (now vs target, us vs best) | `dumbbell` | two-column text |
| Rank order over 3–6 periods | `bump` | a table of ranks |
| One measure over two categorical dimensions | `heatmap` | a numeric `data_table` |
| Options profiled on 3–8 criteria on one scale | `radar`; with weights → `decision_matrix` | cards per option |
| Causes of one observed problem — **the source names the effect and says these cause it** | `fishbone` | cards of causes |
| Weaknesses, issues or barriers to address (no stated effect) | `logic_grid` (issue → evidence → what fixes it) or `card_rows` | a `fishbone` with a borrowed effect |
| Steps across several actors / hand-offs | `swimlane` | `process_flow` |
| Customer steps with feelings or pain points | `journey` | `process_flow` |
| Layers that build on each other (stack, operating model) | `layer_stack` | `card_rows` |
| 2–3 overlapping conditions or groups | `venn` | cards |
| Trend or magnitude of one series | `chart`: `line` trend · `column` / `bar` compare or rank · `grouped_column` two periods · `stacked_column` composition; `highlight` the focus item, add an `insight` | a numeric `data_table` |
| A change between two totals, explained by drivers | `waterfall` | cards of drivers |
| Reinforcing loop, flywheel, vicious cycle | `cycle` | `card_rows` |
| One concept and its 3–6 parts or stakeholders | `hub_spoke` | `card_grid` |
| Positioning / prioritising on two dimensions | `matrix_2x2`, `growth_share`, `prioritization_matrix` | cards |
| Risks by probability × impact | `risk_heatmap` (owners → `risk_register`) | `card_rows` |
| Factor → impact → implication, per topic | `logic_grid` | cards |
| Decomposing a goal or question | `issue_tree` | bullets |
| Sequence of steps, one actor; narrowing quantity | `process_flow`; `funnel` | `card_rows` |
| Plan over time; KPIs vs target | `roadmap` / `timeline` / `phase_grid`; `scorecard` | tables |
| One claim that needs two relationships (a diagram and what follows from it; a level and its change) | `composite` with a `diagram` or `chart` region beside cards / callout (rule below) | two crowded slides |
| **Really a list** of parallel points with detail | `card_grid` / `card_rows` — the right choice | — |
| A text table (options × facets, as-is / to-be) | `data_table` | — |

**A diagram asserts a relationship.** Cause → effect, sequence, flow,
overlap, hierarchy or one focal item: draw it only when the source states it.
If you infer it, list it under "Inferences added" in the plan or use a list
layout — never borrow an effect or a priority from another section.

**One slide, two relationships.** The title's claim is the *main*
relationship and decides the template. A second one shares the slide only
when it explains or qualifies the main one: `composite[diagram:radar + cards +
callout]` (profile + what follows), `composite[chart + diagram:slopegraph]`
(level + ranking shift), `composite[diagram:timeline + cards]` (plan + gates).
Region sizes and the 14 diagrams a region can hold: `catalog.py composite`; at
most two diagrams per slide. **Split into two slides** when each relationship
makes its own claim (it needs its own title), when the second needs a
full-slide diagram (cycle, swimlane, hub_spoke, risk_heatmap, venn), or when
three relationships compete.

Text layouts are correct when the content is a list; the checker's [11]
reminds you when they fill over half of the content slides — a prompt to look
again, not a rule. Mistakes the table doesn't cover: text features in
`comparison_table` Harvey balls → `data_table`; `column_simple_growth` with
forecast bars → `column_historic_forecast`; `bubble_chart` with quadrant
labels → `growth_share` / `prioritization_matrix`; `org_chart` for decomposing
a problem → `issue_tree`; 5+ trends in `three_trends_*` → `overview_areas`;
area and width charts take values >= 0 only (gains and losses → `waterfall`).

---

## Step 0 — Pick the mode. Everything else depends on it.

**Source mode** — material the deck must be built from:
a deck outline ("Slide 1: … Slide 2: …"), a report, a plan, a spreadsheet,
or "based on the file / framework in the folder".

**Brief mode** — only a short description ("make a Q4 review deck,
revenue 120bn, 2 KPIs late"), no document to follow.

If unsure: source mode whenever a document describes the deck's content.

### Source-mode rules (non-negotiable)

1. **The source is the spec, not inspiration.** Every section of the source
   gets at least one slide, in the source's order. Do not merge, drop or
   reorder sections on your own. If the source is clearly too long for the
   stated use (e.g. 40 sections for a 10-minute talk), ask the user before
   cutting.
2. **Every table and every number in the source appears in the deck** —
   as a chart, a `data_table`, a KPI tile or inside the text. A source
   table is data, not a layout: a 6-brand × 4-year table becomes a line
   chart with all 6 brands and all 4 years (don't reduce it to one year);
   a text table stays a `data_table`. Numbers inside a native chart count as
   shown — they are in the chart's data and the checker reads them — even
   when only the focal series carries value labels.
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
   decision. You may **not** add anything the source doesn't contain: new
   targets, KPIs, rankings or superlatives ("#1 in the region",
   "market-leading"); new partners, customers, deal types, products, tiers,
   prices, markets, channels, sites, campaigns or dates; new ownership,
   credential or regulatory claims ("proprietary", "certified",
   "clinically proven"); new causes, mechanisms or behaviour, and invented
   colour ("loved by Gen Z"). Test for every supporting point: *can I point
   to the source sentence, or is it a plain logical consequence of two source
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

- **Audience and use.** *Live presentation*: fewer words, one message per
  slide. *Pre-read / leave-behind / plan document*: slides carry the full
  argument, every claim backed on the slide. "给高管看" alone does not mean
  "cut content": a plan, review or report built from a document is a pre-read
  unless the user says it is a short talk.
- **Slide count.** Source mode: roughly one slide per section plus a cover, an
  optional agenda / dividers for 15+ slides and a closing slide — never fewer
  slides than sections. Brief mode: 5–10 unless told otherwise.
- **Footer attribution:** the company or team name, only if the user gave it
  or it is in their files.
- Attached or named files (`.xlsx`, `.csv`, `.docx`, `.pdf`, `.md`): read them
  fully, tables included, from their real path (working rules 1–2); those
  paths are the `--source` files in Step 6.

## Step 2 — Choose templates from the index

Run `catalog.py` once: the index lists every template with its *Use when*
line. For each slide name the relationship (table above) and pick the
template; two candidates → `catalog.py <a> <b> --guide`. Then write the plan
(Step 3) and run `catalog.py --plan output/<slug>_plan.md`: it rejects unknown
names, unjustified text layouts and unsupported composite regions, and prints
the entries (arguments, *Don't use when*, example) of exactly the templates
the plan uses — look a template up again only if the build reports an
argument error. The catalog is the source of truth for names and arguments;
never invent them, and don't page through `CATALOG.md` or grep it.

## Step 3 — Write the slide plan first

Before writing any build code, write `output/<slug>_plan.md` — a table with
one row per slide, in slide order:

| # | Source section | Required elements | Message (action title) | Relationship: main · secondary | Template(s) | Why not text cards | Source data used | Inferences added |
|---|---|---|---|---|---|---|---|---|

- **Required elements:** what the user asked that slide to contain, or "—";
  tick each off against the rendered slide.
- **Relationship:** the main relationship in the words of the table above
  ("whole split two ways", "gap per item", "causes of one problem", "list"),
  then the secondary one, if any ("gap per item · what drives it"), else "—".
- **Template(s):** the template name, nothing else but `· focus <item>` —
  or, for a composite, its regions: `composite[diagram:radar + cards +
  callout]` (diagram regions as `diagram:<template>`). `catalog.py --plan`
  and the checker's [12] read this column.
- **Why not text cards:** "—" for a diagram or chart; for `card_grid`,
  `card_rows`, `data_table` or `swot`, a few words on why the content is a
  list ("4 parallel initiatives, no order or quantity"). If you can't, pick
  the diagram.
- **Inferences added:** every supporting point or insight that is a
  consequence you drew rather than a source sentence. Most rows say "—".

Source mode: check the plan against the source before continuing — every
section is in the plan, every source table is in some slide's "data used".
Fix the plan, not the source.

**Action titles.** Each title states the slide's takeaway as a claim
("EMEA margin fell 3 pts as freight costs doubled", "Two of five
workstreams are behind plan"), not a topic ("EMEA results", "Project
status"). Take the claim from the source's own key message; the section
name can go in `section_marker` or the subtitle.

**Focus follows the title.** When the title singles out one item of a diagram
("*Batteries* are the only question mark worth funding", "the programme is in
its *build* phase"), pass it as `focus=` (the templates that take it:
`catalog.py --focus`) and write it in the plan ("growth_share · focus
Batteries"). The focal item gets the accent, everything else turns neutral;
one or two per slide. If the title makes no claim about one item — including
titles that name several items side by side ("A, B and C constrain growth") —
leave `focus` out (`focus=[]` silences the build warning). Never pick one of
several named items: that is a priority the source didn't give.

## Step 4 — Fill each slide to the right density

**Slide anatomy:** action title → optional subtitle → 2–4 content blocks →
(analysis slides) a key insight.

- Each source bullet becomes a **block header** plus 1–3 supporting points
  from the source (its details, its tables, the logical "so what"). Four
  one-line bullets and nothing else is too thin.
- **Key insight** (`insight=`; older chart templates `takeaways`): one sentence
  that *synthesises* — it combines two or more data points or states what they
  mean for the decision ("Growth came entirely from new customers; the base
  shrank 4%"). It is not a restatement of the title, one table row or the
  cards above. Beside a table or chart: the sentence plus at most 3 bullets
  that compare or connect data, never one bullet per row. If you can't write
  one that adds something, leave it out — objectives, roadmaps and reference
  tables often have none. Name the bar for its role (`insight_label=`: "Bottom
  line", "Verdict", "Implication", "Decision needed", "Preliminary view"), not
  "Key insight" everywhere.
- **Analysis pages end in a "so what" for the company** (market, customers,
  competitors, PEST, five forces): the last column, band or bar says what the
  facts mean ("Competitive advantage", "Impact on <company>"). It must follow
  from the cells beside it; in source mode list it under "Inferences added"
  unless the source states it.
- **Show the chain, not just the list.** A → B → C arguments use a layout
  whose columns or rows carry that order (`logic_grid`, `composite` with
  `connectors`, `strategic_challenge`), column headers naming each step.
- **Emphasis and icons:** where the template renders markup (`catalog.py
  --icons` lists them; elsewhere the characters print literally and the
  checker flags them), mark the 1–3 things per card the reader must see: key
  numbers `**bold**`, problems `{red|…}`, growth `{green|…}` — never whole
  sentences. Give each `card_grid` card an `icon` that matches its meaning;
  `tone` carries meaning, not decoration.
- Use the source's numbers in the text ("from 12.4% to 9.8% in two years"),
  not vague words ("declined slightly").

**Data → template** (the relationship table comes first; this covers the rest).
Prefer templates 41–80: larger type, text fitted to the space, editable tables
and charts; use 1–40 only for what they uniquely cover (org chart, BCG /
bubble chart, issue tree, funnel, process flow, cover, divider, agenda, quote,
stat_hero). When no single template fits a mixed slide, use `composite`. Templates
not named here (`swot`, `roadmap`, `timeline`, `org_chart`, `phase_grid`,
`positioning_scale`, `value_chain`, `business_model_canvas`, ...) are found by
their *Use when* line in the index.

| Content | Template |
|---|---|
| **Scores, ratings or rankings against criteria** (weighted evaluation, vendor scoring, maturity) | **a table, not a chart**: `decision_matrix` (weights, weighted scores, best per row, totals); plain ratings → `data_table` |
| Option scores **with a reason per cell**, dot ratings, criteria grouped by dimension | `evaluation_matrix` (text-only with `rating=None`) |
| 2–4 options / products / scenarios with the same facets (summary, key numbers, pros, cons) | `option_profiles` |
| One option / initiative in depth (how it works + numbers + why / how / pros / cons + verdict) | `composite` (`flow` + `kv_table`, 2×2 `cards`) |
| One option read as an argument (situation → strategy → advantages → disadvantages) | `composite` with `headers` + `connectors=True`; `callout` for the value proposition, `pyramid` for positioning, `sections` for feasibility / pros / cons |
| A chain of reasoning per topic (situation → capability → advantage; need → what we do → implication) | `logic_grid` — one row per topic, conclusion column right; PEST / five forces → `logic_grid(direction="down")` |
| Drivers converging on one threat and the key question | `strategic_challenge` |
| Executive summary of a problem-solving deck (strategy case, options paper, board proposal) | `storyline_summary` |
| Short summary (situation / complication / resolution / ask) | `card_grid` 2×2 with `insight` = the bottom line |
| Summary as prose; as 2–4 bold takeaways | `executive_summary_paragraph`; `executive_summary_takeaways` |
| KPIs target vs. actual with status; headline numbers (2–4) | `scorecard`; `card_grid` with `value` per card |
| **Text** or mixed text / number table; options × criteria, as-is vs. to-be | `data_table` (all rows and columns; `highlight_rows` / `highlight_col`); `comparison_table` only when the source gives ratings |
| 2–8 parallel *qualitative* points with detail (initiatives, principles, recommendations) | `card_grid` (sized drivers → `waterfall`; risks → `risk_heatmap` / `risk_register`; segments → `treemap` / `marimekko`) |
| 2–6 items needing a sentence each (decisions, risks + mitigation) | `card_rows` |

No outline (brief mode) or a deck "type" asked for → `catalog.py --spines`
lists the usual slide order per deck type; in source mode the source's own
structure always wins.

**Parallel slides look alike.** Consecutive slides on parallel items (option
1 / 2 / 3, region by region) get the same template, the same block order and
the same `group=` (`b.add(..., group="options")`). Swap a block only when
that item lacks the data. **Vary the layouts** otherwise: at most three
slides in a row with the same template unless they share a `group`; with
numeric series the deck needs at least one `chart`. When a run gets long,
re-express one slide (targets as `card_grid` values, drivers as a `chart`).

**Layout rules:**
- Titles fit on **one line**: ≤ ~75 characters English, ≤ ~34 Chinese; the
  rest goes in the subtitle or insight.
- `kicker=` (≤ ~60 characters) puts a label above the title saying where the
  slide sits in the argument ("Option 2 | Outsource to 3PL"); use it on every
  content slide of a structured deck. `section_marker` / `default_section_marker`
  ≤ 20 characters. `cover_slide`: `client` and `date` one short line each; a
  long key message goes in `subtitle`.
- Dense templates (`overview_areas`, `phases_table_4`, `waves_timeline_4`,
  `gantt_timeline`) have columns < 2" wide: one short line per bullet; detail
  goes to a `data_table` slide.
- Fit is checked by rendering (Step 7). If a slide overflows, pick a roomier
  template or split the slide before shortening wording, and never drop
  source data.
- Always pass `source=` (a real cited source, or `""`) and `footnote=""` —
  the defaults print `xx`. Chart templates: also `description=` and
  `takeaway_header=`; `prioritization_matrix`: `description=` and
  `legend=(green, amber, red)`. Literal `[...]` renders as gray placeholder
  styling on purpose; pass real values. `three_trends_icons` / `five_key_areas`
  / `three_trends_table` print labels as written — no brackets.

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
python "SKILL_DIR/scripts/run_deck.py" output/build_<slug>.py --source <each source file> --plan output/<slug>_plan.md
```

It builds (printing every failed slide at once), checks the deck, renders PNGs
into `output/preview_<slug>/` and ends with a summary. Exit 0 = nothing to
fix. Brief mode: no `--source`. Add `--no-render` while iterating.

Each flagged checker section prints what to do. The rules that don't fit on a
report line:
- **[1] numbers not in the sources:** source mode — delete or trace to the
  source; a derived figure is fine if the report says how it was computed.
  Brief mode — list as illustrative.
- **[2] coverage:** aim ≥ 90% of source numbers used; for each unused one,
  show it or say why it was left out. Never add numbers to raise it.
- **[5] content not in the sources:** apply rule 5's test to every point
  flagged; plain explanatory words are fine, new facts, features, places or
  behaviours are not.
- **[3] [11] advisory:** a short slide beats a padded one; [11] is a prompt to
  re-check text layouts against the relationship table.
- **[12] plan vs deck:** update the plan row or fix the slide so the report
  matches the deck.
- Build WARNINGs (`text fitted at Npt`, `focus` missing or matching nothing)
  count as findings: fix the call.

Fix and rebuild until the checker is clean or every remaining item is
explained in the report.

## Step 7 — Inspect the previews (mandatory when they rendered)

Open `output/preview_<slug>/contact_sheet.png` (every slide on one image),
then single `slide-NN.png` files that look wrong. If the summary says the
render was not done, install what it names once (LibreOffice; `pip install
pymupdf` if `pdftoppm` is missing) — don't write your own conversion commands.
Check: text running past boxes, labels hidden behind shapes, titles wrapping
into the underline, chart labels stacking, large empty areas, leftover `[...]`
/ `xx`. Fix and rebuild. If the tools are missing, say the deck was not
visually verified.

## Step 8 — Report back (in the user's language)

- The `.pptx` path and slide count; a numbered slide list: template + one-line
  rationale (from the plan).
- Source mode: section coverage ("20/20 sections, 7/7 tables"), every `[待补充]`
  slot, source data left out and why. Brief mode: which numbers came from the
  user and which are illustrative.
- The `== summary` lines of the last `run_deck.py` run, verbatim. If `check`
  is not `clean`, list each remaining item and why it stays; never describe a
  run with open items as passed.
- For each slide in a [11] reminder: the relationship it shows and why a text
  layout is still right (the plan's "Why not text cards"). Slides you can't
  justify get a diagram before you report.
- An offer to iterate ("要把第 4 页换成别的版式吗？").

## Theme

Always `make_theme(company, lang=<language of the slides>, brand=...)`:
`lang="zh"` / `"ko"` also translates every default label, so a Chinese deck
built without it shows English labels; `lang` follows the source (Step 0,
rule 6), never the chat language. `company` only if the user gave it;
`brand` (hex) only if they named a brand colour. Details and fonts:
`catalog.py --theme`.

## Iterating

The first deck is a draft. When the user asks — in this conversation, or by
naming the existing deck — to change a slide ("第 4 页换个版式", "把第 2 页第三条
改成 …", "做一份英文版"), edit `output/build_<slug>.py` and the plan, rebuild,
and re-run the checker — don't start over. A fresh request for a deck ("做一个
…演讲", "make a deck on …") is not an iteration, even if an older deck on the
same topic is in `output/` (working rule 3).
