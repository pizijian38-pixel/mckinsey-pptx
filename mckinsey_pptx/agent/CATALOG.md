# McKinsey Slide Template Catalog

This catalog enumerates every slide template the `mckinsey_pptx` plugin can produce.
The McKinsey Slide Agent reads this file to **decide which template fits a given
intent** and to learn the exact API for each template.

For every template you'll find:
- **Use when** — the situations this template is the right tool for
- **Don't use when** — common mistakes / nearby templates that might be better
- **Required inputs** — keyword arguments that must be supplied
- **Optional inputs** — what you can add for polish
- **Example** — minimal working call

All templates accept these common optional kwargs (omit unless useful):
`title`, `page_number`, `section_marker`, `source`, `footnote`, `theme`.

---

## 1. Executive summary — paragraph (`executive_summary_paragraph`)

**Category:** Executive summary
**Use when:** The summary is a flowing narrative of 2–4 short paragraphs and the
audience expects a written argument rather than scannable bullets. Best for
written reports rather than spoken decks.
**Don't use when:** The summary naturally breaks into 2–4 distinct takeaways with
supporting bullets — use `executive_summary_takeaways` instead.
**Required inputs:**
- `paragraphs: list[str]` — 2–4 paragraphs, each 1–4 sentences.
**Optional inputs:**
- `subtitle: str` — dashed-box subtitle below the title.
**Example:**
```python
b.add("executive_summary_paragraph",
      title="Executive summary",
      paragraphs=[
          "Market grew 22% per year and is expected to grow further.",
          "Korean players are losing 2 pts of share annually due to ...",
      ])
```

---

## 2. Executive summary — takeaways + bullets (`executive_summary_takeaways`)

**Category:** Executive summary
**Use when:** The summary is structured as 2–4 bold takeaways, each backed by 2–4
bullets, optionally ending with a final recommendation. This is the most common
McKinsey executive-summary pattern.
**Don't use when:** You only have one takeaway (use `dark_navy_summary` for a
single impact statement) or have prose paragraphs (`executive_summary_paragraph`).
**Required inputs:**
- `sections: list[{takeaway: str, bullets: list[str]}]`
**Optional inputs:**
- `final_conclusion: str` — bold concluding line at the bottom.
**Example:**
```python
b.add("executive_summary_takeaways",
      sections=[
          {"takeaway": "Market is growing 22% YoY",
           "bullets": ["NA share rising", "Europe stagnating"]},
          {"takeaway": "Korean players need to reposition",
           "bullets": ["Cost gap widening", "OEM mix shifting to LFP"]},
      ],
      final_conclusion="Recommend immediate action on 5 areas.")
```

---

## 3. Dark-navy impact summary (`dark_navy_summary`)

**Category:** Summary / divider
**Use when:** A single impact statement deserves its own slide — typically a
key finding, section divider, or "if you remember one thing..." moment. Renders
as a full-bleed deep navy slide with bold white text.
**Don't use when:** You have multiple takeaways (use `executive_summary_takeaways`).
**Required inputs:**
- `body: str` — the headline. If it starts with `"[Label]: "`, the label is bolded.
**Optional inputs:**
- `eyebrow: str` — small text in the top-right (e.g. report name).
- `corner_text: str` — bottom-right brand mark, defaults to the theme's `brand_text` (blank by default).
**Example:**
```python
b.add("dark_navy_summary",
      body="[Bottom line]: The next 5 years will determine global leadership in EV batteries.",
      eyebrow="K-battery global strategy")
```

---

## 4. Assessment table with traffic-light status (`assessment_table`)

**Category:** Status overview
**Use when:** You're showing KPIs grouped by category/BU with target vs. actual
values and a green/amber/red status per row. Standard for QBR or progress slides.
**Don't use when:** You just need a list of status items without category grouping
or numeric target/actual columns — consider `three_trends_table` or `overview_areas`.
**Required inputs:**
- `categories: list[{name: str, rows: list[{kpi, target, actual, status_label, status: "green"|"amber"|"red"}]}]`
**Optional inputs:**
- `columns: tuple[str, ...]` — header labels (default KPI/Target/Actual/Status).
**Example:**
```python
b.add("assessment_table",
      categories=[
          {"name": "EV BU",
           "rows": [
               {"kpi": "NA utilization", "target": "85%", "actual": "78%",
                "status_label": "Close", "status": "amber"},
           ]},
      ])
```

---

## 5. Bubble chart — full canvas (`bubble_chart`)

**Category:** Scatter / matrix
**Use when:** You want to position 5–15 entities on two continuous dimensions
with bubble size encoding a third dimension. Optional diagonal reference line.
Use when there is no separate takeaway pane needed.
**Don't use when:** You also need bullets explaining the chart (use
`bubble_chart_takeaways`), or you have categorical 2x2/3x3 quadrants
(use `growth_share` or `prioritization_matrix`).
**Required inputs:**
- `bubbles: list[{label: str, x: float, y: float, size: float, group: "blue_light"|"blue_dark"|"blue_royal"|"navy", label_pos?: "right"|"left"|"top"|"bottom"}]`
  - `label_pos` controls where the bubble's label renders relative to the bubble — defaults to `"right"`. Use `"left"`/`"top"`/`"bottom"` to break cluster overlaps when multiple bubbles are close together.
**Optional inputs:**
- `x_max, y_max: float`, `x_label, y_label, x_unit, y_unit: str`
- `groups: list[(color, label)]` — legend
- `diagonal: bool` — show 45° dashed reference (default True)
- `state_top_left, state_bottom_right: str | None` — italic quadrant captions
**Example:**
```python
b.add("bubble_chart",
      bubbles=[{"label": "P1", "x": 200, "y": 1500, "size": 2, "group": "blue_dark"}, ...])
```

---

## 6. Bubble chart with takeaways (`bubble_chart_takeaways`)

**Category:** Scatter / matrix
**Use when:** Same scatter use case as `bubble_chart` but you also want a
right-side bullet pane explaining what to read from the chart. Good for
exec audiences.
**Don't use when:** The chart speaks for itself; or you need quadrant labels —
then use `growth_share` or `prioritization_matrix`.
**Required inputs:**
- `bubbles: list[...]` (same shape as `bubble_chart`)
- `takeaways: list[str]` — bullets in the right pane
**Example:**
```python
b.add("bubble_chart_takeaways",
      bubbles=[...],
      takeaways=["Cluster of products ...", "Outlier P4 deserves attention"])
```

---

## 7. Growth-share matrix / BCG (`growth_share`, alias `bcg_matrix`)

**Category:** 2x2 matrix
**Use when:** Classic BCG portfolio analysis — market share (x) × growth rate (y)
with four quadrants (Star / Question mark / Cash cow / Dog). Bubbles are
business units sized by revenue/value.
**Don't use when:** Your axes aren't market share × growth, or you have 3x3
bands rather than a 2x2 split — use `prioritization_matrix`.
**Required inputs:**
- `bus: list[{name: str, x: float (0-100, share %), y: float (0-50, growth %), size: float}]`
**Optional inputs:**
- `x_max, y_max` — defaults 100 and 50
**Example:**
```python
b.add("growth_share",
      bus=[{"name": "[BU1]", "x": 12, "y": 37, "size": 4}, ...])
```

---

## 8. Prioritization / assessment matrix (`prioritization_matrix`)

**Category:** 3x3 matrix
**Use when:** Plotting initiatives on Time-to-impact (Long/Medium/Short) ×
Level-of-impact (Low/Medium/High), with color-coded status (green/amber/red)
per item. Top-right cell is highlighted.
**Don't use when:** You have continuous axes — use `bubble_chart`. You have
2x2 BCG axes — use `growth_share`.
**Required inputs:**
- `items: list[{name: str, x_band: 0|1|2, y_band: 0|1|2, status: "green"|"amber"|"red"}]`
  - `x_band` 0=Low, 1=Medium, 2=High
  - `y_band` 0=Short (top), 1=Medium, 2=Long (bottom)
**Optional inputs:**
- `ox, oy: float (0-1)` — within-cell offset for tighter layout
- `d: float` — bubble diameter override
- `description: str` — bold label above the matrix (top-left)
- `legend: (str, str, str)` — labels for the green / amber / red dots
**Example:**
```python
b.add("prioritization_matrix",
      items=[{"name": "[A]", "x_band": 2, "y_band": 0, "status": "green"}, ...])
```

---

## 9. Column comparison with focus (`column_comparison`)

**Category:** Categorical column chart
**Use when:** Comparing one metric across 5–12 categorical groups, sorted from
high to low, with one bar highlighted in bright blue (the "focus") and the rest
in deep navy. Right-side takeaway pane.
**Don't use when:** Your x-axis is time — use one of the time-series column
charts (`column_simple_growth`, `column_split_growth`, `column_historic_forecast`).
**Required inputs:**
- `categories: list[str]` — segment labels
- `values: list[float]` — one per category
**Optional inputs:**
- `focus_index: int` — which bar to highlight
- `takeaways: list[str]`
**Example:**
```python
b.add("column_comparison",
      categories=["A","B","C","D","E"], values=[670,623,580,514,421],
      focus_index=1, takeaways=["B is our focus segment"])
```

---

## 10. Column chart, simple growth (`column_simple_growth`)

**Category:** Time-series column chart
**Use when:** Showing one metric across 5–10 time periods with a single overall
growth-rate callout (e.g. "10% CAGR"). All bars same color.
**Don't use when:** Growth has a structural break mid-period (use
`column_split_growth`); you need to distinguish actuals vs forecast (use
`column_historic_forecast`).
**Required inputs:**
- `categories: list` — time labels
- `values: list[float]`
- `growth_pct: str` — label on the arrow oval
**Optional inputs:**
- `takeaways`, `data_label`, `data_unit`
**Example:**
```python
b.add("column_simple_growth",
      categories=[2020,2021,2022,2023,2024],
      values=[100,115,120,135,150], growth_pct="10.7%")
```

---

## 11. Column chart, split growth (`column_split_growth`)

**Category:** Time-series column chart
**Use when:** A single time series has two distinct growth phases (e.g. flat
then accelerating) and you want **two** growth-arrow annotations to highlight
the inflection.
**Don't use when:** Growth is uniform (use `column_simple_growth`); split is
forecast vs actuals (use `column_historic_forecast`).
**Required inputs:**
- `categories`, `values`
- `split_index: int` — which bar separates phase 1 from phase 2
- `growth_pct_first: str`, `growth_pct_second: str`
**Example:**
```python
b.add("column_split_growth",
      categories=[2014,...,2022], values=[1035,...,1535],
      split_index=4, growth_pct_first="2%", growth_pct_second="8%")
```

---

## 12. Column chart, historic + forecast (`column_historic_forecast`)

**Category:** Time-series column chart
**Use when:** Showing actuals vs forecast. Historic bars in deep navy, forecast
bars in bright blue, with two growth-rate arrows (historic and forecast).
**Don't use when:** All values are actuals — use `column_simple_growth` or
`column_split_growth`.
**Required inputs:**
- `categories`, `values`
- `forecast_from_index: int` — first index that is forecast
- `historic_growth: str`, `forecast_growth: str`
**Example:**
```python
b.add("column_historic_forecast",
      categories=[2018,...,2026], values=[1035,...,1535],
      forecast_from_index=5,
      historic_growth="3%", forecast_growth="6%")
```

---

## 13. Three trends with icons (`three_trends_icons`)

**Category:** Trends / themes
**Use when:** Presenting exactly three trends/areas, each with a circular icon
and 3–4 bullet points. Storytelling-style; less data, more narrative.
**Don't use when:** You have exactly five themes (use `five_key_areas`), more
than three (use `overview_areas`), or want examples per theme
(use `three_trends_table`).
**Required inputs:**
- `trends: list[{label: str, bullets: list[str], icon: str}]`
  - `icon` is a single Unicode glyph (e.g. "💡", "$", "🚀")
**Optional inputs:**
- `subtitle: str`
**Example:**
```python
b.add("three_trends_icons",
      trends=[
          {"label": "Tech disruption", "icon": "🤖",
           "bullets": ["AI accelerating", "..."]},
          {"label": "Regulation",     "icon": "⚖",
           "bullets": ["IRA", "CRMA", "..."]},
          {"label": "Customer shift", "icon": "👥",
           "bullets": ["..."]},
      ])
```

---

## 14. Three trends — name/description/examples table (`three_trends_table`)

**Category:** Trends / themes
**Use when:** Three trends, each with a name pill, description bullets, and
example bullets in a third column.
**Don't use when:** You don't have concrete examples — use `three_trends_icons`
or `three_trends_numbered`.
**Required inputs:**
- `trends: list[{name: str, description: list[str], examples: list[str]}]`
**Example:**
```python
b.add("three_trends_table",
      trends=[{"name":"Trend 1","description":["..."], "examples":["Example A"]}, ...])
```

---

## 15. Three trends numbered (`three_trends_numbered`)

**Category:** Trends / themes
**Use when:** Three trends shown as numbered rows with a bright blue label pill
and bullet points. Good for sequenced/prioritized trends.
**Don't use when:** Not exactly three items, or icons would be more visual.
**Required inputs:**
- `trends: list[{label: str, bullets: list[str]}]`
**Example:** like `three_trends_icons` but without `icon` keys.

---

## 16. Five key areas (`five_key_areas`)

**Category:** Areas / categories
**Use when:** Presenting exactly five (or six) areas, each with a name pill,
a right-arrow connector, and a one-line description in alternating gray rows.
Best for compact "5 strategic areas" slides.
**Don't use when:** Three items (use `three_trends_*`), or seven-ish (use
`overview_areas`).
**Required inputs:**
- `areas: list[{name: str, description: str}]` — 5 items recommended
**Example:**
```python
b.add("five_key_areas",
      areas=[{"name":"[Area 1]", "description":"..."}, ...])
```

---

## 17. Overview of areas — vertical cards (`overview_areas`)

**Category:** Areas / categories
**Use when:** 5–7 columns of "areas" with a header pill, lettered badge (A–G),
and bullet content. Optional bottom-left blue call-out tag.
**Don't use when:** Just five items with one-line descriptions — use
`five_key_areas`. You have three items — use `three_trends_*`.
**Required inputs:**
- `areas: list[{name: str, bullets: list[str]}]`
**Optional inputs:**
- `call_out: str` — bottom-left blue tag
**Example:**
```python
b.add("overview_areas",
      areas=[{"name":"[A1]", "bullets":["b1", "b2"]}, ...],
      call_out="Short-term focus")
```

---

## 18. Issue tree (`issue_tree`)

**Category:** Hierarchy / decomposition
**Use when:** Decomposing one root issue into hierarchical drivers (Main →
Secondary → Underlying). Standard problem-solving framework slide.
**Don't use when:** Hierarchy is reporting structure (use `org_chart`).
**Required inputs:**
- `root: str` — the main issue
- `main_drivers: list[{label: str, secondaries: list[{label: str, underlying: list[str]}]}]`
**Example:** see demo_korean.py slide 12.

---

## 19. Organizational chart (`org_chart`)

**Category:** Hierarchy / org
**Use when:** Showing reporting structure: CEO → N heads → reports per head.
Boxes with names/titles.
**Don't use when:** Need icon-based team rendering — use `project_team_circles`.
**Required inputs:**
- `ceo: str`
- `branches: list[{head: str, reports: list[str]}]`

---

## 20. Project team or functions — circles (`project_team_circles`)

**Category:** Org / team
**Use when:** Highlighting one leader with N teammates rendered as labeled
circles (with optional Unicode icons). Best for staffing slides.
**Don't use when:** You need a function × role grid — use `team_chart`.
**Required inputs:**
- `leader: {name: str, description: str, icon: str}`
- `members: list[{name: str, description: str, icon: str}]`

---

## 21. Team chart — function columns × roles (`team_chart`)

**Category:** Org / staffing
**Use when:** Showing a project team broken down by function (columns) with
multiple roles per function (filled or outline circles).
**Don't use when:** You only need a list of N teammates — use
`project_team_circles`.
**Required inputs:**
- `project_name: str`
- `functions: list[{name: str, description: str, roles: list[{name: str, kind: "filled"|"outline"}]}]`

---

## 22. Phases — three chevron arrows (`phases_chevron_3`)

**Category:** Timeline / roadmap
**Use when:** Project breaks naturally into exactly three phases shown as
chevron arrows (Discover → Design → Deliver style), each with deliverables
and people lists below.
**Don't use when:** Four phases — use `phases_table_4` or `waves_timeline_4`.
**Required inputs:**
- `phases: list[{label: str, timeframe: str, deliverables: list[str], people: list[str]}]` — exactly 3 entries

---

## 23. Phases — four-column text table (`phases_table_4`)

**Category:** Timeline / roadmap
**Use when:** Four phases laid out as parallel columns (Phase 1–4) with
description + Key activities + Outcomes per column. More text than chevron.
**Don't use when:** Three phases — use `phases_chevron_3`.
**Required inputs:**
- `phases: list[{name, description, activities: list[str], outcomes: list[str]}]`

---

## 24. Waves — four on a horizontal arrow (`waves_timeline_4`)

**Category:** Timeline / roadmap
**Use when:** Project rolls out in four sequential waves on a single horizontal
arrow (with circle markers). Each wave has a headline, key activities, and
deliverables.
**Don't use when:** You're showing parallel workstreams over weeks (use
`gantt_timeline`); only three phases (use `phases_chevron_3`).
**Required inputs:**
- `waves: list[{name, headline, timeframe, activities: list[str], deliverables: list[str]}]`

---

## 25. Gantt-style weekly timeline (`gantt_timeline`)

**Category:** Timeline / project plan
**Use when:** Multiple parallel workstreams across many weeks (rows × week
columns), with milestones marked at specific weeks. The right tool for
detailed project plans.
**Don't use when:** Only 3–4 phases (use `phases_chevron_3` /
`phases_table_4` / `waves_timeline_4`).
**Required inputs:**
- `weeks: list[int]` — column headers
- `workstreams: list[{name, start_week, end_week, color: "blue_light"|"blue_dark"|"royal"}]`
**Optional inputs:**
- `milestones: list[{week: int, label: str}]`

---

## 26. Process activities table (`process_activities`)

**Category:** Project plan / process
**Use when:** A short project plan with 3–4 time blocks (e.g. Week 1–4, 5–8…)
showing per-block Activities + Mgmt. interaction (diamond marker) +
Deliverables (diamond marker).
**Don't use when:** Long plans across 10+ weeks (use `gantt_timeline`).
**Required inputs:**
- `steps: list[{name: str, subtitle: str, activities: list[str], interaction: str | None, deliverable: str | None}]`

---

## 27. Cover slide (`cover_slide`, alias `cover`)

**Category:** Structural — first page
**Use when:** Every standalone deck. Renders the deck title, subtitle, client,
and date with a deep navy stripe down the right edge and an optional
"CONFIDENTIAL" tag in the top-right.
**Don't use when:** This is an internal section divider — use `section_divider`.
**Required inputs:**
- `title: str` — main title
**Optional inputs:**
- `subtitle: str`, `client: str`, `date: str`, `confidentiality: str`
**Example:**
```python
b.add("cover_slide",
      title="K-Battery Strategic Review",
      subtitle="Global market entry assessment",
      client="Acme Corp", date="2026 Q2")
```

---

## 28. Section divider (`section_divider`)

**Category:** Structural — chapter break
**Use when:** Decks of more than ~10 slides need clear section breaks. Renders
a left navy panel with a giant chapter number and a right title block with
accent line + subtitle.
**Don't use when:** A single agenda slide is enough (use `agenda`).
**Required inputs:**
- `section_number: str` — e.g. "01"
- `section_title: str`
**Optional inputs:**
- `subtitle: str`
**Example:**
```python
b.add("section_divider", section_number="02",
      section_title="Competitive landscape",
      subtitle="Where rivals are moving and why")
```

---

## 29. Agenda (`agenda`)

**Category:** Structural — table of contents
**Use when:** Up-front roadmap of the deck (or before each major section).
Numbered chapter list with optional active highlight.
**Don't use when:** The deck is short enough that an agenda is overhead.
**Required inputs:**
- `items: list[str]` — chapter names
**Optional inputs:**
- `active_index: int` — highlights the current section in bright blue
- `title: str` — defaults to "Agenda"
**Example:**
```python
b.add("agenda",
      items=["Market context", "Competitive landscape",
             "Strategic options", "Recommendation", "Next steps"],
      active_index=2)
```

---

## 30. Stat hero / big number (`stat_hero`, alias `big_number`)

**Category:** Impact / data point
**Use when:** A single statistic is *the* point — e.g., "82% of CEOs say…",
"$50B addressable market", "1.5 billion users by 2030". Renders the number
huge in deep navy with a label and optional supporting paragraph.
**Don't use when:** You have multiple numbers (use `kpi_dashboard`); the
number is part of a chart.
**Required inputs:**
- `stat: str` — the big number
- `stat_label: str` — what it represents
**Optional inputs:**
- `context: str`, `title: str`, `source_text: str`
**Example:**
```python
b.add("stat_hero",
      stat="$1.2B", stat_label="Annual revenue impact by 2030",
      context="If all five strategic actions are executed on schedule.")
```

---

## 31. Quote slide (`quote_slide`, alias `quote`)

**Category:** Impact / voice-of-customer
**Use when:** Showcasing a single interview quote, customer voice, or expert
opinion. Big quotation mark + italic quote + accent line + attribution.
**Don't use when:** Many quotes — pick one and put the rest in an appendix.
**Required inputs:**
- `quote: str`, `author: str`
**Optional inputs:**
- `author_title: str`, `title: str`
**Example:**
```python
b.add("quote_slide",
      quote="Speed of execution will outweigh strategic perfection.",
      author="Industry CEO", author_title="Top 5 EV OEM, NA")
```

---

## 32. Comparison table — Harvey balls (`comparison_table`, alias `option_compare`)

**Category:** Option assessment
**Use when:** Comparing 2–4 options across 3–6 criteria with Harvey-ball
ratings (0–4 quartile fills). Optional `recommended_index` highlights the
chosen column in bright blue with a "★ Recommended" tag.
**Don't use when:** You have only one option (use `pros_cons`); criteria are
all numeric (use a `comparison_table`-style chart in `column_comparison`).
**Required inputs:**
- `options: list[str]` — column headers
- `criteria: list[{name: str, scores: list[int 0-4 | str], notes?: list[str]}]`
  - `scores` accepts ints 0–4 OR semantic strings like "high"/"med"/"low".
**Optional inputs:**
- `recommended_index: int`, `subtitle: str`
**Example:**
```python
b.add("comparison_table",
      options=["Build","Buy","Partner"],
      criteria=[
          {"name":"Time to market","scores":[1,4,3]},
          {"name":"Capital required","scores":[1,2,4]},
          {"name":"Strategic fit","scores":[4,2,3]},
      ],
      recommended_index=2)
```

---

## 33. Pros and cons (`pros_cons`)

**Category:** Option assessment
**Use when:** Two-column +/− analysis of ONE option (or as a quick check on
recommendations). Green ✓ pros / red ✗ cons.
**Don't use when:** Multiple options (use `comparison_table`).
**Required inputs:**
- `pros: list[str]`, `cons: list[str]`
**Optional inputs:**
- `pros_label: str` (default "Pros"), `cons_label: str` (default "Cons")
**Example:**
```python
b.add("pros_cons",
      pros=["Faster to market", "Lower capex"],
      cons=["Less control", "Margin sharing"])
```

---

## 34. Two-column compare (`two_column_compare`, alias `before_after`)

**Category:** Side-by-side comparison
**Use when:** Before/After, As-is/To-be, Current/Future state visualization.
Two cards with header bands and a connecting arrow between them.
**Don't use when:** You have 3+ options (use `comparison_table`); you have
+/- analysis (use `pros_cons`).
**Required inputs:**
- `left_label: str`, `right_label: str`
- `left_items: list[str]`, `right_items: list[str]`
**Optional inputs:**
- `left_color, right_color: "navy"|"gray"|"blue"|"amber"`
- `show_arrow: bool` (default True)
**Example:**
```python
b.add("two_column_compare",
      left_label="As-is", right_label="To-be",
      left_items=["Single market","Reactive supply chain"],
      right_items=["Three-region presence","Strategic sourcing"])
```

---

## 35. Stacked column chart (`stacked_column_chart`, alias `stacked_column`)

**Category:** Chart — composition over time/category
**Use when:** Decomposing a total into 2–5 segments per category (e.g.
revenue by region across years). Per-segment values labeled inside, total
labeled above each bar.
**Don't use when:** Showing growth of a single value (use `column_simple_growth`)
or comparing two scenarios per category (use `grouped_column_chart`).
**Required inputs:**
- `categories: list` — x-axis labels
- `series: list[{name: str, values: list[float]}]` — one entry per stack segment
**Optional inputs:**
- `takeaways: list[str]`, `data_label`, `data_unit`, `show_totals: bool`
**Example:**
```python
b.add("stacked_column_chart",
      categories=[2022,2023,2024,2025,2026],
      series=[
          {"name":"NA",   "values":[100,140,180,230,290]},
          {"name":"EU",   "values":[80,100,130,160,200]},
          {"name":"APAC", "values":[60,75,95,120,150]},
      ])
```

---

## 36. Grouped column chart (`grouped_column_chart`, alias `grouped_column`)

**Category:** Chart — side-by-side category comparison
**Use when:** Comparing 2–4 series across the same set of categories
(e.g. two years per country, before/after per business unit).
**Don't use when:** Showing parts-of-whole (use `stacked_column_chart`).
**Required inputs:**
- `categories: list` — group labels
- `series: list[{name: str, values: list[float]}]` — one bar per series, per group
**Example:**
```python
b.add("grouped_column_chart",
      categories=["Korea","Japan","China","US","EU"],
      series=[{"name":"2023","values":[120,80,150,200,140]},
              {"name":"2024","values":[140,90,180,220,160]}])
```

---

## 37. Line chart (`line_chart`)

**Category:** Chart — time series, multi-series
**Use when:** 1–4 lines tracking a metric over time or sequence (monthly
sales, regional KPIs). Markers at every data point, configurable per-series
value labels.
**Don't use when:** Discrete categorical comparison (use `column_comparison`
or `grouped_column_chart`).
**Required inputs:**
- `categories: list` — x-axis points
- `series: list[{name: str, values: list[float], color?: str}]`
  - Optional `color`: "navy"|"blue"|"mid_blue"|"light_blue"|"royal"|"amber"|"green"|"red"
**Optional inputs:**
- `show_markers: bool` (default True), `show_values_for: list[str]` — series
  whose values should be label-printed at every point.
**Example:**
```python
b.add("line_chart",
      categories=["Jan","Feb","Mar","Apr","May","Jun"],
      series=[
          {"name":"NA",   "values":[100,108,115,118,124,130]},
          {"name":"EU",   "values":[80,82,85,88,92,98]},
          {"name":"APAC", "values":[60,66,72,80,90,100]},
      ])
```

---

## 38. Process flow horizontal (`process_flow_horizontal`, alias `process_flow`)

**Category:** Process / sequence
**Use when:** A 4–6 step sequential process with a one-line description per
step. Numbered chevron tiles in alternating navy/bright-blue.
**Don't use when:** Phases need full sub-content (use `phases_chevron_3` or
`phases_table_4`); process is iterative not linear.
**Required inputs:**
- `steps: list[{name: str, description: str}]`
**Example:**
```python
b.add("process_flow_horizontal",
      steps=[
          {"name":"Discover","description":"Market & customer research"},
          {"name":"Design",  "description":"Strategy & operating model"},
          {"name":"Build",   "description":"Capability & infrastructure"},
          {"name":"Launch",  "description":"Go-to-market execution"},
          {"name":"Scale",   "description":"Continuous optimization"},
      ])
```

---

## 39. Funnel (`funnel`)

**Category:** Top-down hierarchy / conversion
**Use when:** TAM/SAM/SOM market sizing, marketing funnel (awareness →
consideration → purchase → loyalty), or any quantity that shrinks down a
sequence. Each band shows name + headline value; descriptions on the right.
**Don't use when:** No clear narrowing logic (use `process_flow_horizontal`).
**Required inputs:**
- `stages: list[{name: str, value: str | None, description: str | None}]`
**Example:**
```python
b.add("funnel",
      stages=[
          {"name":"TAM","value":"$50B","description":"Total addressable market"},
          {"name":"SAM","value":"$20B","description":"Realistic serve set"},
          {"name":"SOM","value":"$3B", "description":"5-year capture"},
      ])
```

---

## 40. KPI dashboard (`kpi_dashboard`)

**Category:** Multi-metric overview
**Use when:** 4–8 KPIs at a glance, each with a big value, small delta
(▲ green / ▼ red / ▬ flat), and optional context line. Standard for QBRs
and ops reviews.
**Don't use when:** A single metric (use `stat_hero`); KPIs need full
target/actual context (use `assessment_table`).
**Required inputs:**
- `kpis: list[{label, value, delta?, delta_dir: "up"|"down"|"flat", context?}]`
**Optional inputs:**
- `columns: int` — tile grid columns (default 4)
**Example:**
```python
b.add("kpi_dashboard",
      kpis=[
          {"label":"Revenue","value":"$1.2B","delta":"+12% YoY","delta_dir":"up"},
          {"label":"Margin", "value":"18%",  "delta":"+200 bps","delta_dir":"up"},
          {"label":"Util.",  "value":"78%",  "delta":"-7 pts",  "delta_dir":"down"},
          {"label":"NPS",    "value":"42",   "delta":"flat",    "delta_dir":"flat"},
      ])
```

---

## 41. Data table (`data_table`, alias `table`)

**Category:** Table — any rows × columns
**Use when:** The source has a table (P&L by region, option × criteria,
risk × owner × status, feature × competitor) or any grid of text /
numbers that no specialised template fits. Native PowerPoint table, so the
user can edit it. Optional Key-insight panel on the right.
**Don't use when:** The data is a single series that reads better as a chart
(use a column/line chart), or cells are ratings (use `comparison_table`).
Never force a text table into `comparison_table` Harvey balls.
**Required inputs:**
- `columns: list[str]` — header labels
- `rows: list[list[str | number]]` — body rows, same order as the source
**Optional inputs:**
- `subtitle: str` — bold label above the table (e.g. "Market share, %")
- `col_widths: list[float]` — relative column widths (default: first column wider)
- `highlight_rows: list[int]` — 0-based body rows to tint + bold (e.g. "us")
- `highlight_col: int` — column to tint (e.g. the proposed option)
- `insight: str`, `insight_bullets: list[str]`, `insight_title: str` — right panel
- `font_size: int` — default 14 for ≤ 7 rows, else 12
- Cells, `insight` and `insight_bullets` accept `**bold**` spans (this
  template only — other templates print the asterisks literally).
Numeric tables (numbers by year / category) go to `chart` first; use
`data_table` for text tables or as the full-detail companion of a chart.
Insight bullets synthesise (≤ 3) — don't restate each row.
**Example:**
```python
# Finance — quarterly results by region (text + numbers table)
b.add("data_table",
      title="EMEA margin fell 3 pts as freight costs doubled",
      subtitle="Q3 results by region",
      columns=["Region", "Revenue ($M)", "Gross margin", "Main driver"],
      rows=[["North America", "412", "38%", "Price increase held"],
            ["EMEA", "268", "{red|31%}", "Freight cost +104%"],
            ["APAC", "190", "41%", "Mix shift to services"]],
      highlight_rows=[1],
      insight="Freight explains almost all of the EMEA margin gap",
      insight_bullets=["EMEA is the only region below 35%", "APAC margin rose with services mix"],
      source="Company management accounts")
```

---

## 42. Card grid (`card_grid`, alias `cards`) — preferred for structured content

**Category:** Layout — 2–8 cards
**Use when:** A slide has 2–8 parallel items, each with a header and 1–4
supporting points: executive-summary blocks (situation / problem / answer /
ask), workstream status, initiatives, risks, drivers, principles, options,
customer segments, capabilities.
Also KPI / objective cards via `value`. Text is fitted to the space (up to
18pt) and cards shrink to their content, so short content doesn't leave
empty boxes. Preferred over `executive_summary_takeaways`,
`three_trends_*`, `five_key_areas` and `kpi_dashboard` for new decks.
**Don't use when:** The content is a table (use `data_table`) or numbers to
chart (use `chart`).
**Required inputs:**
- `cards: list[{title, body?, bullets?, icon?, tone?, value?}]`
  - `icon`: a bundled icon name (list below) or 1–2 characters (`"1"`, `"A"`)
  - `tone`: `navy` | `blue` | `mid_blue` | `light_blue` | `red` (problem / risk)
    | `green` (opportunity / target met) | `amber` (watch) | `gray`
  - `value`: big number at the top of the card (objectives, KPIs)
**Optional inputs:**
- `intro: str` — dark banner above the cards (the slide's key message)
- `insight: str`, `insight_label: str` — highlighted bar below the cards
- `subtitle: str`, `columns: int` (auto: 2→2, 3→3, 4→2×2 or 1×4 for value
  cards, 5–6→3, 7–8→4)
**Example:**
```python
# Project status — four workstreams
b.add("card_grid", title="Two of four workstreams are behind plan",
      cards=[
        {"title": "Data migration", "icon": "database", "tone": "red",
         "bullets": ["{red|3 weeks late}: legacy schema gaps", "Recovery plan due 15 May"]},
        {"title": "Process redesign", "icon": "settings", "tone": "green",
         "bullets": ["On track — 6 of 8 processes signed off"]},
        {"title": "Training", "icon": "users", "tone": "amber",
         "bullets": ["Trainer hiring 2 weeks behind"]},
        {"title": "Go-live readiness", "icon": "check", "tone": "green",
         "bullets": ["Cut-over plan approved"]},
      ],
      insight="Go-live date holds only if migration recovers by end of May")

# Targets as value cards
b.add("card_grid", title="2025 targets: grow revenue while cutting cost to serve",
      cards=[{"value": "+12%", "title": "Revenue", "tone": "green", "body": "Driven by renewals and upsell"},
             {"value": "-8%", "title": "Cost to serve", "tone": "blue", "body": "Self-service and automation"},
             {"value": "95%", "title": "On-time delivery", "tone": "navy", "body": "Up from **91%**"}])
```

---

## 43. SWOT (`swot`)

**Category:** Framework — 2×2
**Use when:** Strengths / weaknesses / opportunities / threats. Fixed colours
and icons (S blue, W red, O green, T amber).
**Required inputs:** any of `strengths`, `weaknesses`, `opportunities`,
`threats: list[str]` (an empty quadrant shows "—"; never invent items to fill it)
**Optional inputs:** `labels` (4 headers, e.g. Chinese), `insight`, `subtitle`
**Example:**
```python
# Market entry assessment
b.add("swot", title="Strong product fit, but no local sales channel yet",
      strengths=["Product rated best-in-class by pilot customers", "Cost base 20% below incumbents"],
      weaknesses=["No local sales team", "Brand unknown in the region"],
      opportunities=["Regulation opens public tenders from 2026"],
      threats=["Two incumbents bundling at discount"])
```

---

## 44. Native chart with insight (`chart`, alias `native_chart`) — preferred for data

**Category:** Chart — editable PowerPoint chart
**Use when:** Any numeric series the user may want to edit later. Real
PowerPoint chart ("Edit Data" works), with an optional key-insight panel.
Preferred over the shape-drawn chart templates (`column_*`, `line_chart`,
`grouped_column_chart`, `stacked_column_chart`) for new decks.
**Required inputs:**
- `chart_type`: `column` | `grouped_column` | `stacked_column` |
  `stacked_column_100` | `bar` | `stacked_bar` | `line` | `pie` | `doughnut`
- `categories: list`, `series: list[{name, values, tone?}]`
**Optional inputs:**
- `highlight`: `{"series": "Services"}` (that series red, others gray — line/bar)
  or `{"point": 2}` (that bar red — single series)
- `number_format`: label format, e.g. `'0.0'`, `'0"%"'`, `'#,##0'`
- `insight: str`, `insight_bullets: list[str]`, `insight_title: str`
- `subtitle: str` (put the unit here: "Market share, %"), `show_values`, `y_max`
- Line charts with 3+ series label only the highlighted / toned series.
**Example:**
```python
# Revenue trend with the focus segment highlighted
b.add("chart", chart_type="line", title="Services overtook hardware as the largest revenue line",
      subtitle="Revenue by segment, $M", categories=["2021", "2022", "2023", "2024"],
      series=[{"name": "Hardware", "values": [520, 505, 480, 455]},
              {"name": "Software", "values": [210, 240, 275, 300]},
              {"name": "Services", "values": [380, 430, 470, 515]}],
      highlight={"series": "Services"}, number_format="#,##0",
      insight="Services grew 36% while hardware declined every year",
      insight_bullets=["Services **380 → 515**", "Hardware {red|520 → 455}"])
```

---

## 45. Tier ladder (`tier_ladder`, alias `price_ladder`)

**Category:** Framework — ascending tiers
**Use when:** 2–5 tiers that step up: price or service tiers, capability
maturity levels, portfolio tiers, escalation levels.
**Required inputs:**
- `tiers` (lowest first): `[{name, value?, lines?, label?, details?, tone?}]`
  - `value`: big text, e.g. `"$45 / user"`; `lines`: bold lines (what's included);
    `label` + `details`: a captioned list (e.g. "Target channel")
**Optional inputs:** `insight`, `subtitle`
**Example:**
```python
# Service tiers (works the same for price tiers, maturity levels, SLAs)
b.add("tier_ladder", title="Three service tiers move customers up the value curve",
      tiers=[{"name": "Basic", "value": "$20 / user", "lines": ["Core features"],
              "label": "Support", "details": ["Email, 48h"]},
             {"name": "Professional", "value": "$45 / user", "lines": ["Analytics, integrations"],
              "label": "Support", "details": ["Chat, 8h"]},
             {"name": "Enterprise", "value": "Custom", "lines": ["SSO, dedicated environment"],
              "label": "Support", "details": ["Named manager, 1h"]}],
      insight="Most upgrades happen when customers need integrations")
```

---

## Rich text, tones and icons (templates 41–55)

- `**bold**` → bold; `{red|text}` → bold in that tone (`navy`, `blue`,
  `mid_blue`, `light_blue`, `red`, `green`, `amber`, `gray`, `gold` = neutral
  emphasis such as best-in-row). Use red for
  problems / declines, green for growth / targets, sparingly (1–3 spans per
  card). Older templates (1–40) print the markup literally.
- Bundled icons (white on a tone circle): `alert`, `arrow_right`, `arrows`, `atom`, `award`, `bag`, `book`, `bot`, `box`, `building`, `calculator`, `calendar`, `cart`, `chart`, `check`, `clipboard`, `clock`, `coins`, `compass`, `cpu`, `cross`, `crown`, `database`, `dna`, `droplet`, `eye`, `factory`, `file`, `filter`, `flag`, `gem`, `globe`, `handshake`, `heart`, `home`, `info`, `key`, `lab`, `layers`, `leaf`, `lightbulb`, `line_chart`, `link`, `lock`, `mail`, `map`, `medal`, `megaphone`, `message`, `microscope`, `money`, `moon`, `package`, `palette`, `pen`, `percent`, `phone`, `pie`, `pill`, `price`, `puzzle`, `question`, `refresh`, `rocket`, `scale`, `search`, `settings`, `share`, `shield`, `smile`, `sparkles`, `star`, `stethoscope`, `store`, `sun`, `target`, `team`, `thumbs_up`, `tooth`, `trend_down`, `trend_up`, `trophy`, `truck`, `user`, `users`, `video`, `wallet`, `zap`.
  Unknown names fall back to the first letter and print a warning.
- Theme: `make_theme(company, lang="en"|"zh"|"ko"|"ja", brand="0B4DA2",
  accent=None)` sets slide language (CJK font + footer "Source:" label),
  attribution and brand colours in one call.

---

## 46. Card rows (`card_rows`)

**Category:** Layout — horizontal list
**Use when:** 2–6 items that each need a sentence or two (decisions needed,
risks and mitigations, principles, recommendations). Icon + header on the
left, text on the right. Same item shape as `card_grid`; use it to vary the
layout when several card slides would otherwise follow each other.
**Required inputs:** `rows: list[{title, body?, bullets?, icon?, tone?, value?}]`
**Optional inputs:** `subtitle`, `insight`, `label_width` (default 3.4")
**Example:**
```python
b.add("card_rows", title="Four decisions are needed from the steering committee",
      rows=[{"title": "Approve budget", "icon": "money", "body": "Release **$2.4M** phase-2 budget"},
            {"title": "Confirm go-live", "icon": "calendar", "body": "Hold **1 Oct** or move to January"},
            {"title": "Accept risk", "icon": "alert", "tone": "red", "body": "{red|3-week slip} in migration"}])
```

---

## 47. Waterfall / bridge (`waterfall`, alias `bridge`)

**Category:** Chart — bridge from start to end value (native, editable)
**Use when:** Explaining a change between two totals by its drivers:
revenue / EBIT / cost / cash / headcount bridges, budget vs. actual
variance, price-volume-mix. Increases green, decreases red, totals navy.
**Required inputs:** `steps: list[{label, value, total?}]` — `total=True` for
start / subtotal / end bars (drawn from zero); other values are deltas.
**Optional inputs:** `subtitle` (put the unit here), `number_format`,
`insight`, `insight_bullets`
**Rule:** only use deltas the source gives; start + deltas must equal the end total.
**Example:**
```python
b.add("waterfall", title="EBIT fell $14M as freight and wages outweighed price",
      subtitle="EBIT bridge, $M",
      steps=[{"label": "2023", "value": 120, "total": True}, {"label": "Price", "value": 18},
             {"label": "Volume", "value": 6}, {"label": "Freight", "value": -22},
             {"label": "Wages", "value": -11}, {"label": "FX", "value": -5},
             {"label": "2024", "value": 106, "total": True}],
      insight="Cost inflation (-38) more than offset commercial gains (+24)")
```

---

## 48. Scorecard — target vs. actual (`scorecard`)

**Category:** Performance — KPI status
**Use when:** 3–8 KPIs with target, actual and a status (QBR, project
health, OKR review, operating review). Status pill: `green` / `amber` /
`red` (or "on track" / "at risk" / "off track").
**Required inputs:** `metrics: list[{metric, target, actual, status, status_label?, comment?}]`
**Optional inputs:** `columns` (header labels, e.g. Chinese), `subtitle`
**Rule:** show values as given; don't compute variances the source doesn't state.
**Example:**
```python
b.add("scorecard", title="Four of six KPIs on track; churn and NPS need action",
      metrics=[{"metric": "Revenue growth", "target": "+10%", "actual": "+12%", "status": "green"},
               {"metric": "Customer churn", "target": "<5%", "actual": "7.2%", "status": "red",
                "comment": "Two large accounts lost"}])
```

---

## 49. Roadmap — workstreams × periods (`roadmap`)

**Category:** Plan — bars on a time grid
**Use when:** A plan with several workstreams over months / quarters /
years, with milestones (programme plan, product roadmap, transformation
plan, implementation plan).
**Required inputs:**
- `periods: list[str]` — e.g. `["Q1", "Q2", "Q3", "Q4"]`
- `lanes: list[{name, items: [{label, start, end, tone?}]}]` — `start` / `end`
  are 0-based period indices; the bar runs from the start of `start` to the
  end of `end` (`start=1, end=2` = Q2–Q3); add `.5` to begin mid-period.
  Overlapping items in one lane stack automatically.
**Optional inputs:** `milestones: [{label, at, tone?}]` (`at` = position on the
axis: 2 = boundary between period 2 and 3), `subtitle`, `insight`
**Example:**
```python
b.add("roadmap", title="ERP rollout completes in Q4 with two go-live waves",
      periods=["Q1", "Q2", "Q3", "Q4"],
      lanes=[{"name": "Design", "items": [{"label": "Process design", "start": 0, "end": 0}]},
             {"name": "Build", "items": [{"label": "Configuration", "start": 1, "end": 2},
                                          {"label": "Data migration", "start": 1, "end": 2, "tone": "amber"}]},
             {"name": "Deploy", "items": [{"label": "Go-live", "start": 3, "end": 3, "tone": "green"}]}],
      milestones=[{"label": "Design sign-off", "at": 1}, {"label": "Go-live", "at": 4, "tone": "green"}])
```

---

## 50. Timeline (`timeline`)

**Category:** Plan — dated events
**Use when:** 3–7 dated events in sequence (history, launch plan, regulatory
calendar, deal timeline). Text alternates above and below the line.
**Required inputs:** `events: list[{date, title, body?, tone?}]`
**Optional inputs:** `subtitle`, `insight`
**Example:**
```python
b.add("timeline", title="From pilot to national rollout in 18 months",
      events=[{"date": "Jan 2024", "title": "Pilot", "body": "3 stores"},
              {"date": "Oct 2024", "title": "Wave 1", "body": "40 stores"},
              {"date": "Jun 2025", "title": "National", "body": "All 310 stores", "tone": "green"}])
```

---

## 51. 2×2 matrix (`matrix_2x2`, alias `matrix`)

**Category:** Framework — two dimensions, four quadrants
**Use when:** Sorting options, initiatives, customers or risks on two
dimensions (impact × effort, likelihood × severity, attractiveness ×
ability to win, value × complexity). Quadrants with item lists, and/or
plotted points.
**Required inputs:** `x_label`, `y_label`, and `quadrants` (order: top-left,
top-right, bottom-left, bottom-right: `[{title, items?, tone?}]`) and/or
`points: [{label, x: 0-1, y: 0-1, tone?}]`
**Optional inputs:** `x_ends`, `y_ends` (default Low / High), `highlight`
(quadrant index to tint), `subtitle`, `insight`
**Example:**
```python
b.add("matrix_2x2", title="Automate high-volume, rule-based processes first",
      x_label="Process volume", y_label="Rule-based",
      quadrants=[{"title": "Standardise first", "items": ["Vendor onboarding"]},
                 {"title": "Automate now", "tone": "green", "items": ["Invoice matching", "Expense audit"]},
                 {"title": "Leave as is", "tone": "gray", "items": ["Board reporting"]},
                 {"title": "Assist with tools", "items": ["Credit decisions"]}],
      highlight=1)
```

---

## 52. Composite — regions of components (`composite`)

**Category:** Layout — build your own slide from parts
**Use when:** One slide must show several kinds of content together — the
typical consulting "deep dive": how it works (flow) + the numbers (key
values) + why / how / pros / cons (cards) + a verdict. Use it for an
option, initiative, product, market or business-model page. Prefer a
dedicated template when one fits the whole slide.
**Required inputs:**
- `columns: list` — each column is a region (dict) or a list of regions
  stacked top to bottom. Each region: `{"type": <component>, "heading"?: str,
  "weight"?: float (height share in its column), "panel"?: bool, ...args}`
**Optional inputs:** `widths: list[float]` (column width shares), `subtitle`,
`insight`, `insight_label`
**Components** (region `type` → arguments):
- `flow` — `steps: [{title, body?, tone?}]`, `highlight: int`, `caption: str`
  (value chain, business model, operating model, process)
- `kv_table` — `rows: [[label, value], ...]` or `[{label, value, tone?, total?}]`
  (unit economics, key facts, assumptions)
- `metrics` — `items: [{value, label, tone?}]` (2–4 big numbers)
- `cards` — `cards: [...]` as in `card_grid`, `columns: int`
- `pros_cons` — `pros: [str]`, `cons: [str]`, `labels`, `layout: stacked | columns`
- `list` — `items: [{title, body?, tone?}]` numbered (priorities, steps, criteria)
- `phases` — `phases: [{name, period?, goal?, bullets?, tone?}]` (compact roadmap)
- `bullets` — `items: [str]`; `text` — `text: str | [str]`
- `chart` — same arguments as `chart` (`chart_type`, `categories`, `series`, ...)
- `table` — same arguments as `data_table` (`columns`, `rows`, ...)
- `callout` — `text`, `label?`, `style: outline | solid | tint`, `tone?` — one
  highlighted statement: the new value proposition, the option in one line,
  the "so what" at the end of a column
- `pyramid` — `levels: [str]` (top first), `highlight: int | [int]`,
  `note?: str` (beside the highlighted level) or `notes: [str per level]` —
  positioning (high / mid / low end), hierarchy, maturity
- `sections` — `sections: [{title, bullets? | body?, tone?, mark?}]`,
  `boxed: bool` — stacked titled groups with a ruled header, e.g.
  Feasibility / Pros / Cons; `tone: green` → ✓ marks, `red` → ✗ marks
  (`mark: check | cross | dot` to override). Use `boxed: False` inside a `panel`.

**Logic options** — for pages that read left to right as one argument
("current situation → strategy → advantages → disadvantages", "how it
addresses the challenge → key activities → impact"):
- `headers: [str | {text, dark}]` — one header per column (`None` skips one)
- `header_style: chevron | rule | bar` (default: chevron with connectors, else rule)
- `connectors: bool` — an arrow between consecutive columns
- region `"arrow": True` — a down arrow from the region above it in the same
  column (bullets → arrow → `callout` with the resulting value proposition)
- region `"panel": True | "outline" | "tint"` — gray, outlined or tinted backdrop
**Example:**
```python
b.add("composite", kicker="Option 2 | Outsource to a 3PL partner", group="options",
      title="A 3PL partner cuts capex to zero but adds $0.40 per order",
      columns=[
        [{"type": "flow", "heading": "Operating model", "highlight": 1,
          "steps": [{"title": "Retailer", "body": "Owns stock"},
                    {"title": "3PL partner", "body": "Runs 4 DCs"},
                    {"title": "Customer", "body": "Next-day delivery"}],
          "caption": "Fee per order; 3-year volume commitment"},
         {"type": "kv_table", "heading": "Cost per order (base case)",
          "rows": [["Pick, pack & ship", "$4.10"], ["Transport", "$2.30"],
                   {"label": "Total (in-house $6.20)", "value": "$6.60", "tone": "red", "total": True}]}],
        [{"type": "cards", "columns": 2, "cards": [
            {"title": "Why", "icon": "lightbulb", "bullets": ["Capex freed for stores"]},
            {"title": "How", "icon": "settings", "bullets": ["3-year contract, 98% SLA"]},
            {"title": "Advantages", "icon": "check", "tone": "green", "bullets": ["$0 capex"]},
            {"title": "Disadvantages", "icon": "cross", "tone": "red", "bullets": ["+$0.40 per order"]}]}]],
      widths=[1.15, 1], insight="Worth it only below 2M orders a year", insight_label="Verdict")

# Option deep dive that reads as one argument (same frame for every option)
b.add("composite", kicker="Option 1 | Sell through retail channels", group="options",
      title="Option 1: sell the house brands through retail as a second growth engine",
      headers=["How it addresses the challenge", "Key activities", "Advantages and risks"],
      connectors=True,
      columns=[
        [{"type": "bullets", "items": ["**Bigger market:** category worth $15B, growing fast",
                                       "**Builds the brand** outside our own stores"]},
         {"type": "callout", "arrow": True, "label": "New value proposition",
          "text": "Our signature products, wherever customers shop"}],
        [{"type": "sections", "sections": [
            {"title": "Product", "bullets": ["Two current SKUs already suit retail"]},
            {"title": "Sales", "bullets": ["Channel team for e-commerce and convenience stores"]}]}],
        [{"type": "pros_cons", "pros": ["Second growth engine", "Scale lowers unit cost"],
          "cons": ["Competes with category leaders", "May cannibalise store visits"]}]])

# Positioning + evaluation (option elaboration | option evaluation)
b.add("composite", title="Option A: keep the mid-market position and partner for the new segment",
      headers=[{"text": "Option elaboration", "dark": True}, {"text": "Option evaluation", "dark": True}],
      header_style="bar",
      columns=[
        [{"type": "pyramid", "levels": ["High-end", "Mid-end", "Low-end"], "highlight": 1,
          "note": "**Keep the current position:** premium, not luxury", "panel": "tint", "weight": 1.6},
         {"type": "callout", "label": "New segment", "text": "**Partner** with a specialist brand"}],
        {"type": "sections", "sections": [
            {"title": "Feasibility", "mark": "dot", "bullets": ["Already strong in the mid-market"]},
            {"title": "Pros", "tone": "green", "bullets": ["Closes the product gap fast"]},
            {"title": "Cons", "tone": "red", "bullets": ["Depends on the partner"]}]}])
```

---

## 53. Option profiles (`option_profiles`)

**Category:** Evaluation — options side by side
**Use when:** Introducing 2–4 options, products, vendors, scenarios or
markets with the **same facets** (name, tagline, one-line summary, 1–3 key
numbers, pros, cons). Neutral by default — use it for "here are the
options" before any recommendation.
**Required inputs:** `options: [{name, tagline?, summary?, icon?, metrics?: [{value, label, tone?}], pros?, cons?}]`
**Optional inputs:** `recommended: int` (only after the evaluation has been
shown), `insight`, `insight_label` (default "Preliminary view"),
`pros_label`, `cons_label`, `subtitle`
**Notes:** pros / cons switch to side-by-side inside each card when stacked
text would drop below 12pt; keep 2–3 short items each.
**Example:**
```python
b.add("option_profiles", title="Three ways to meet 2026 volume; each trades capex for control",
      options=[{"name": "Build own DCs", "tagline": "Full control", "icon": "building",
                "metrics": [{"value": "$180M", "label": "capex"}],
                "pros": ["Lowest unit cost at scale"], "cons": ["24 months to open"]},
               {"name": "Outsource to 3PL", "tagline": "Zero capex", "icon": "truck",
                "metrics": [{"value": "$0", "label": "capex"}],
                "pros": ["Live in 6 months"], "cons": ["+$0.40 per order"]}],
      insight="No option wins on every dimension; the scorecard follows")
```

---

## 54. Decision matrix — weighted scoring (`decision_matrix`, alias `scoring_matrix`)

**Category:** Evaluation — criteria × weights × options
**Use when:** Options scored against weighted criteria (vendor selection,
strategic option scoring, site selection, investment prioritisation).
Shows raw score and weighted score, highlights the best score per row in
gold, and adds a weighted-total row. A table, never a chart.
**Required inputs:** `options: [str]`, `criteria: [{name, weight (25 | 0.25 | "25%"), scores: [num per option]}]`
**Optional inputs:** `recommended: int` (tints that column), `show_weighted`,
`highlight_best`, `decimals`, `scale_note`, `insight`, `insight_bullets`,
`insight_title` (default "What drives the result")
**Rule:** totals are computed from the given scores × weights — report them
as derived; if the user changed scores, say which and why.
**Example:**
```python
b.add("decision_matrix", title="The hybrid model scores highest overall",
      options=["Build own", "3PL", "Hybrid"],
      criteria=[{"name": "Capital efficiency", "weight": 40, "scores": [1, 5, 3]},
                {"name": "Unit cost", "weight": 35, "scores": [5, 2, 4]},
                {"name": "Time to capacity", "weight": 25, "scores": [1, 5, 4]}],
      scale_note="1 = poor, 5 = excellent; weighted score in brackets")
```

---

## 55. Risk register (`risk_register`)

**Category:** Evaluation — risks and mitigations
**Use when:** 2–6 risks, each with a severity (high / medium / low /
critical), a one-line description and mitigations (and optionally an owner).
**Required inputs:** `risks: [{title, severity, description?, mitigations?: [str], owner?}]`
**Optional inputs:** `columns`, `mitigation_label`, `insight`, `insight_label`, `subtitle`
**Example:**
```python
b.add("risk_register", title="Two high risks need owners before approval",
      risks=[{"title": "Partner service failure", "severity": "high",
              "description": "Peak-season misses hit NPS",
              "mitigations": ["SLA with penalties", "Dual-source two regions"], "owner": "COO"},
             {"title": "Contract lock-in", "severity": "low",
              "mitigations": ["Break clause after 18 months"]}])
```

---

## 56. Logic grid (`logic_grid`, alias `logic_chain`)

**Category:** Logic — one page that carries an argument
**Use when:** Each topic must be followed through the same chain of
reasoning, and the reader should see the chain: *external situation →
our capability → competitive advantage*; *what customers need → what we do
→ performance → implication*; *factor → impact on performance →
relevance → implication*; *new entrant → definition → their advantages →
challenge for us*. Situation-analysis pages of a strategy case, KSF
analyses, competitor moves and their impact.
`direction="down"` turns it into one column per topic with stages as bands
from top to bottom — the frame for PEST, five forces or stakeholder pages
("Political | Economic" × "Current situation → Influence on us").
**Don't use when:** The cells hold numbers to compare (use `data_table` or
`chart`); items are parallel with no chain between columns (use
`card_grid` / `card_rows`); one column needs a chart or a different kind of
content (use `composite` with `headers` + `connectors`).
**Required inputs:**
- `stages: [str]` — headers of the analysis columns, in reasoning order
- `rows: [{label?, icon?, cells: [cell per stage], conclusion?, tone?}]`;
  `cell` = str | [bullets] | `{body?, bullets?}`; `conclusion` = str or [bullets]
**Optional inputs:** `conclusion_label` (header of the dark conclusion column,
default "Implication"), `conclusion` (one shared conclusion for all rows
instead of one per row), `direction: across | down`, `arrows: conclusion |
all | none`, `header_style: chevron | rule | bar`, `label_header`,
`subtitle`, `insight`, `insight_label`
**Rules:** 2–4 rows (across) or 2–4 topics (down), 2–3 stages, 2–3 short
bullets per cell. The conclusion is a consequence the reader can check
against the cells on its left — not a new fact.
**Example:**
```python
b.add("logic_grid", kicker="Situation analysis (1/3)",
      title="Local fit and efficient production made us the market leader",
      stages=["External situation", "Our capability"],
      conclusion_label="Competitive advantage",
      rows=[{"label": "Local market", "icon": "globe",
             "cells": [["Regional differences make a local database a KSF",
                        "Price sensitivity is higher than in Europe"],
                       ["Largest regional database", "Price well below the global leader"]],
             "conclusion": "Products fit local customers better"},
            {"label": "Production", "icon": "factory",
             "cells": [["Scale is needed to carry R&D cost"],
                       ["**41%** of market volume", "Plants **20%** more efficient than average"]],
             "conclusion": "High standard at lower cost"}])

# PEST / five forces: topics as columns, stages top -> bottom
b.add("logic_grid", direction="down", title="High barriers protect us; substitutes still matter",
      stages=["Current situation"], conclusion_label="Influence on us",
      rows=[{"label": "New entrants", "cells": [["Barrier built on users and qualified partners"]],
             "conclusion": "High barrier from the community"},
            {"label": "Substitutes", "cells": [["Offline channels still used by **42%** of users"]],
             "conclusion": "Integrate offline channels"}])
```

---

## 57. Strategic challenge (`strategic_challenge`, alias `key_question`)

**Category:** Logic — convergence on the key question
**Use when:** The page that turns the situation analysis into the one
question the rest of the deck answers: 2–4 drivers (competitors, new
entrants, customers, regulation …) → what each could do to us → the one
threat they converge on → "How can <company> <goal>, given <constraint>?".
Optionally 2–4 `directions` that lead into the options.
**Don't use when:** There is no single question (use `card_grid`), or the
drivers need data to be believed (show the data first, then this page).
**Required inputs:** `drivers: [{title?, body, result?}]`, `question: str`
**Optional inputs:** `threat`, `labels` (3 column headers, default
"Drivers", "Possible results", "Key threat"), `question_label` (default
"Strategic challenge"), `directions: [str | {title, body}]`,
`directions_label`, `subtitle`
**Example:**
```python
b.add("strategic_challenge", kicker="Strategic challenge",
      title="The challenge is to defend the customer base on two fronts",
      drivers=[{"title": "Competitors", "body": "The global leader is investing heavily",
                "result": "We may fall behind when the duopoly breaks"},
               {"title": "New entrants", "body": "Device giants and online players may enter",
                "result": "We may lose on production scale and channels"}],
      threat="We may lose our advantages and, with them, future customers",
      question="How can we secure our lead in customers, given competition in existing and new markets?")
```

---

## 58. Storyline summary (`storyline_summary`)

**Category:** Logic — executive summary as a story
**Use when:** The executive summary of a problem-solving deck (strategy
case, options paper, board proposal): situation blocks → the key question
→ the options considered, with the chosen one(s) marked → the
recommendation. The reader gets the whole argument on one page, in the
order the deck tells it.
**Don't use when:** The deck has no question / options structure (use
`card_grid` 2×2 or `executive_summary_takeaways`). Do not mark a
recommended option the source doesn't recommend.
**Required inputs:** `situation: [{title, body? | bullets?}]` (1–4),
`question: str`
**Optional inputs:** `options: [str | {name?, body, badge?}]` (names default
to "Option A, B …"; `option_prefix` to change), `recommended: int | [int]`,
`badge` (default "Recommended"; per option via `badge`),
`recommendation: str | [str] | [{title, body}]`, `labels` (left band labels;
`None` hides them), `subtitle`
**Example:**
```python
b.add("storyline_summary", title="Partner now in the kids' segment, build our own line later",
      situation=[{"title": "Key success factors", "bullets": ["Local fit", "Efficient production"]},
                 {"title": "Current challenges", "bullets": ["Leader expanding", "New entrants"]}],
      question="How can we secure our lead in customers, given competition in existing and new markets?",
      options=[{"body": "Keep position; partner for kids' products", "badge": "Top priority"},
               {"body": "Keep position; build a kids' line in-house", "badge": "2nd priority"},
               {"body": "Move to the low end via direct-to-consumer"}],
      recommended=[0, 1],
      recommendation=[{"title": "Short term", "body": "partner to close the gap fast"},
                      {"title": "Long term", "body": "build our own line on our database"}])
```

---

## 59. Cycle / flywheel (`cycle`, alias `flywheel`)

**Category:** Logic — causal loop
**Use when:** Effects reinforce each other. *Branch* form (default): one
driver → 2–4 parallel chains of effects → one result, with a dashed
feedback arrow back to the driver (virtuous cycle, flywheel, network
effect). *Loop* form (`steps`): 3–6 steps around a centre — a vicious
cycle (`kind="vicious"`, red) or a self-reinforcing loop.
**Don't use when:** The steps happen once, in order (use
`process_flow_horizontal`); causes of one problem (use `issue_tree`).
**Required inputs:** branch: `start`, `paths: [[step, step], ...]`, `end`
(each str or `{title, body?, icon?}`); loop: `steps: [str | {title, body?}]`
**Optional inputs:** `connector_label` ("leads to …"), `feedback: bool | str`,
`center` (loop), `kind: virtuous | vicious`, `conclusion` (bold statement
under the diagram), `subtitle`, `insight`
**Example:**
```python
b.add("cycle", title="A larger customer base starts a virtuous cycle",
      start="Customer base grows",
      paths=[[{"title": "Fixed cost spread", "icon": "coins"}, "Cost leadership"],
             [{"title": "Database grows", "icon": "database"}, "Better treatment results"]],
      end="Sales grow", connector_label="leads to …",
      conclusion="Losing the customer base stops the flywheel")
b.add("cycle", title="Falling bookings may set off a revenue spiral", kind="vicious",
      steps=["Revenue depends on ad fees", "Fewer customers book", "Advertisers cut budgets"],
      center="Revenue decline")
```

---

## 60. Risk heat map (`risk_heatmap`, alias `risk_matrix`)

**Category:** Evaluation — risks on probability × impact
**Use when:** 3–7 risks the reader should see by severity, with one
mitigation each: graded zones (low → high), numbered risk boxes placed by
probability and impact, mitigations listed by number on the right.
**Don't use when:** Risks need owners and several mitigations each (use
`risk_register`); no probability / impact view exists in the source.
**Required inputs:** `risks: [{title, probability, impact, mitigation?}]` —
levels as `"low" | "medium" | "high"`, 1–3, 1–5 or 0–1
**Optional inputs:** `zones: blue | traffic`, `x_label`, `y_label`, `ends`,
`map_label`, `mitigation_label`, `insight`
**Example:**
```python
b.add("risk_heatmap", title="Two of five risks need action before launch",
      risks=[{"title": "Leader cuts prices", "probability": "high", "impact": "high",
              "mitigation": "Strengthen cost leadership"},
             {"title": "New segment grows slowly", "probability": "medium", "impact": "medium",
              "mitigation": "Educate customers"},
             {"title": "Cost overrun", "probability": "low", "impact": "medium",
              "mitigation": "Phase the investment"}])
```

---

## 61. Positioning scale (`positioning_scale`)

**Category:** Comparison — players on indicator scales
**Use when:** 2–5 competitors compared on 3–8 indicators, where the point
is *relative position* (who is ahead on what): one row per indicator with
what it means, and a low → high scale with each player's marker. Optional
left panel with each player's keywords.
**Don't use when:** Exact values matter (use `data_table` or `chart`);
two dimensions at once (use `matrix_2x2` / `bubble_chart`).
**Required inputs:** `players: [str | {name, short?, tone?, keywords?}]`,
`indicators: [{name, note?, ends?, values: [num per player]}]`
**Optional inputs:** `focus` (index of the player to emphasise, default 0),
`scale: (min, max)`, `ends` (default Low / High), `headers`, `insight`
**Rule:** values are positions from the source (ranks, ratings, figures);
do not invent precise positions — if the source only says "higher" /
"lower", use a coarse 1–3 scale and say so in the report.
**Example:**
```python
b.add("positioning_scale", title="We lead on reach but trail on product range",
      players=[{"name": "Us", "short": "U"}, {"name": "Leader", "short": "L"},
               {"name": "Challenger", "short": "C"}],
      indicators=[{"name": "Case volume", "note": "More cases, richer data", "values": [3, 3, 1]},
                  {"name": "Product range", "note": "More choice for customers", "values": [2, 3, 1]}],
      scale=(1, 3))
```

---

## 62. Value chain (`value_chain`)

**Category:** Framework — industry stages
**Use when:** The industry's stages left → right with what matters in each
(key success factors, activities, margins) and which stages the company
performs (`own`). `value` adds a second line per stage (cost, price,
margin); `groups` add ruled headers spanning stages (Suppliers / Buyers).
**Don't use when:** A company's own process steps (use `process_flow`).
**Required inputs:** `stages: [{name, value?, bullets? | body?, own?}]` (3–6)
**Optional inputs:** `own_label` (legend, e.g. "Activities of Acme"),
`groups: [{label, start, end}]`, `body_label` ("Key success factors"), `insight`
**Example:**
```python
b.add("value_chain", title="We own the two stages that hold most of the margin",
      stages=[{"name": "Materials", "value": "~$150", "bullets": ["Low differentiation"]},
              {"name": "Design", "own": True, "bullets": ["AI treatment planning"]},
              {"name": "Production", "own": True, "bullets": ["3D printing at scale"]},
              {"name": "Clinics", "value": "$5,000+", "bullets": ["Doctors steer decisions"]}],
      own_label="Activities of Acme", body_label="Key success factors")
```

---

## 63. Phase grid (`phase_grid`, alias `implementation_grid`)

**Category:** Plan — rows × stages
**Use when:** An implementation plan where each stage has the same kinds of
content (partners, actions, resources, goals) — rows are those kinds,
columns are stages or years. Cells can `span` several stages (a bar across
years); a row can carry a full-width `kpi` band; `side` adds a risk
mitigation panel on the right.
**Don't use when:** Workstreams with dated bars and milestones (use
`roadmap`); only 3 phases with a few bullets (use `phases` in `composite`).
**Required inputs:** `stages: [str]`, `rows: [{label, cells: [cell per stage], kpi?}]`;
cell = None | str | [bullets] | `{body? | bullets?, span?, tone?}`
(`tone: navy` draws a solid bar)
**Optional inputs:** `side: {title, items: [str | {title, bullets}]}`,
`timeline: bool` (dots on a line under the stage headers), `insight`
**Example:**
```python
b.add("phase_grid", title="Enter channels one by one, online first",
      stages=["Stage 1: E-commerce", "Stage 2: Convenience stores"],
      rows=[{"label": "Partners", "cells": ["Tmall, JD", "7-11, FamilyMart"]},
            {"label": "Actions", "cells": [["Open official stores"], ["Negotiate shelf space"]],
             "kpi": "RMB 2M revenue in year 1"}],
      side={"title": "Risk mitigation", "items": [{"title": "Avoid head-on competition",
                                                   "bullets": ["Start where giants are weak"]}]})
```

---

## 64. Evaluation matrix (`evaluation_matrix`)

**Category:** Evaluation — scores *with reasons*
**Use when:** Options compared on criteria where each cell needs its
reason, or ratings are shown as dots, or criteria are grouped into
dimensions (attractiveness / feasibility / risk), or a banner states why
these criteria (`basis`: "Profit = users × pay rate × ARPU − cost − risk").
Works text-only (`rating=None`) for a qualitative (+) / (−) comparison.
**Don't use when:** Plain weighted numbers with no reasons (use
`decision_matrix`); feature check-marks (use `data_table`).
**Required inputs:** `options: [str | {name, badge?}]`,
`criteria: [{name, group?, weight?, scores?, notes?}]`
**Optional inputs:** `rating: number | dots | None`, `scale_max` (dots),
`total: auto | weighted | average | sum | None | [given]`, `total_label`,
`basis`, `recommended: int | [int]`, `scale_note`, `decimals`, `insight`
**Rules:** totals are computed from the scores (and weights) — report them as
derived. Weights must add up to 100% (the build warns otherwise). Mark
`recommended` / badges only when the source recommends.
**Example:**
```python
b.add("evaluation_matrix", title="Option A scores highest on profitability",
      basis="Why these criteria: Profit = Users × Pay rate × ARPU − Cost",
      options=["A: new user groups", "B: own clinics"],
      criteria=[{"name": "User base", "scores": [2, 1], "notes": ["Adds men and 40+ users", "No direct impact"]},
                {"name": "ARPU", "scores": [3, 3], "notes": ["Higher-priced services", "Service fees"]},
                {"name": "Cost", "scores": [-2, -3], "notes": ["Marketing to new groups", "Clinics need capex"]}],
      total="sum", recommended=0)
b.add("evaluation_matrix", title="Partner first, build second", rating="dots", scale_max=4,
      options=[{"name": "Partner", "badge": "Top priority"}, {"name": "Build", "badge": "2nd priority"}],
      criteria=[{"name": "Speed", "scores": [4, 1]}, {"name": "Control", "scores": [2, 4]}])
```

---

## 65. Business model canvas (`business_model_canvas`, alias `bmc`)

**Category:** Framework — nine blocks
**Use when:** Describing how a company creates, delivers and captures value
(strategy-case backup, company profile, new-business design).
**Required inputs:** any of `partners`, `activities`, `resources`,
`value_proposition`, `relationships`, `channels`, `segments`, `costs`,
`revenue` (each str | [bullets] | {body?, bullets?}; empty blocks show "—")
**Optional inputs:** `labels: {key: name}` (rename a block), `highlight`
(blocks with a dark header, default the value proposition), `insight`
**Example:**
```python
b.add("business_model_canvas", title="We earn from advertisers by giving users trusted information",
      partners=["Clinics", "Product brands"], activities=["Content moderation"],
      resources=["User community"], value_proposition=["Free, transparent reviews"],
      relationships=["Community"], channels=["Own app"], segments=["Young urban users"],
      costs=["Marketing **64%**"], revenue=["Advertising", "Booking fees"])
```

---

## 66. Strategic triangle (`strategic_triangle`)

**Category:** Framework — internal alignment
**Use when:** Internal analysis: goals in the centre; resources &
capabilities, business & value proposition, and structure / systems /
people around it — do they support the goal?
**Required inputs:** `goal: str` (one short sentence)
**Optional inputs:** `resources`, `business` (str | [str] | {title, bullets} |
[{title, bullets}]), `structure: [{title, bullets}]` (1–3 blocks along the
bottom), `labels` (3 corner names), `goal_label`, `insight`
**Example:**
```python
b.add("strategic_triangle", title="Resources, offer and organisation all serve one goal",
      goal="Lead the online market and expand into adjacent services",
      resources=[{"title": "Users", "bullets": ["Largest community"]}],
      business=[{"title": "For customers", "bullets": ["Reviews and booking"]}],
      structure=[{"title": "Systems", "bullets": ["App, website"]},
                 {"title": "People", "bullets": ["Advisory board"]}])
```

---

## 67. Hub and spoke (`hub_spoke`)

**Category:** Framework — one concept and its parts
**Use when:** One concept made of 3–6 elements (disciplines, capabilities,
stakeholders, ecosystem partners), each with a one-line note, and what
that means (`side` panel).
**Don't use when:** The parts are steps in order (use `process_flow`) or
need detail (use `card_grid`).
**Required inputs:** `center: str`, `spokes: [{title, note?, icon?}]` (3–6)
**Optional inputs:** `direction: in | out`, `heading` (caption above the
diagram), `side: {title, bullets}`, `insight`
**Rules:** spoke titles 1–2 words, notes one short line.
**Example:**
```python
b.add("hub_spoke", title="The product combines four disciplines; the weakest sets the limit",
      center="Clear aligners",
      spokes=[{"title": "Dentistry", "note": "Basis of treatment"},
              {"title": "Materials", "note": "Gentle, constant force"},
              {"title": "Software", "note": "AI treatment planning"},
              {"title": "Manufacturing", "note": "3D printing at scale"}],
      side={"title": "Partnerships and talent are critical",
            "bullets": ["A gap in one discipline weakens the whole product"]})
```

---

## Slide-level options (every template)

- `kicker="Option 1 | Leasing model"` — small letter-spaced label above the
  title (section / position in the argument). Not drawn on cover, divider
  and full-bleed slides.
- `group="options"` — marks parallel slides (one per option / product /
  region). They should use the same template; the checker treats a group as
  one series instead of flagging it as repetition.
- `insight_label=` — name the bottom bar for its role ("Verdict",
  "Bottom line", "Preliminary view", "Decision needed").
- `nav="Situation"` — section breadcrumb at the top-left (current chapter
  highlighted). Set the chapters once: `PresentationBuilder(..., nav=["Overview",
  "Situation", "Challenge", "Options", "Recommendation"])`. It takes the
  kicker's place: on a slide with `nav`, the kicker is not drawn.
- **Language of default labels:** build the theme with `make_theme(lang="zh" |
  "ko" | "ja")` and every default label ("Key insight", "Weighted total",
  "Recommended", "Strengths", "Low / High" …) is drawn in that language.
  Labels you pass yourself are drawn as given.

---

# Choosing between similar templates

Quick decision rules to avoid common confusions:

- **A chain of reasoning on one page** (situation → capability → advantage;
  need → what we do → performance → implication; factor → impact →
  implication) → `logic_grid`; PEST / five forces with "influence on us" →
  `logic_grid(direction="down")`; drivers converging on the key question →
  `strategic_challenge`; executive summary of a problem-solving deck →
  `storyline_summary`; one option / column needs a chart, pyramid or
  callout inside the chain → `composite` with `headers` + `connectors`.
- **Causal loops:** effects that reinforce each other → `cycle` (branch
  flywheel, or `steps` loop; `kind="vicious"` for a downward spiral).
- **Risks:** probability × impact picture with one mitigation each →
  `risk_heatmap`; owners and several mitigations per risk → `risk_register`.
- **Competitors on indicators:** relative position per indicator →
  `positioning_scale`; exact values → `data_table` / `chart`.
- **Industry structure:** stages with KSFs or margins, own stages marked →
  `value_chain`.
- **Implementation:** same row types per stage (partners / actions /
  resources), spans across years, KPI bands, risk panel → `phase_grid`;
  workstreams with dated bars and milestones → `roadmap`.
- **Scoring:** reasons per cell, dots, dimension groups or a formula banner
  → `evaluation_matrix`; plain weighted numbers → `decision_matrix`.
- **Frameworks:** business model → `business_model_canvas`; internal
  alignment around a goal → `strategic_triangle`; one concept and its parts →
  `hub_spoke`; PEST / five forces → `logic_grid(direction="down")`;
  SWOT → `swot`.
- **Options / evaluation decks:** options overview → `option_profiles`;
  one slide per option → `composite` (same regions for every option,
  `group="options"`); scoring → `decision_matrix`; risks → `risk_register`.
- **New decks default to the rich templates (41–55):** structured points →
  `card_grid` / `card_rows`; tables → `data_table`; numbers → `chart`;
  bridges → `waterfall`; KPIs vs. target → `scorecard`; plans → `roadmap`
  / `timeline`; 2×2 → `matrix_2x2`; SWOT → `swot`; tiers → `tier_ladder`.
  Use templates 1–40 for what these don't cover (org charts, issue trees,
  BCG / bubble charts, process flows, funnels, cover / dividers).

- **Deck structure:** First page → `cover_slide`; chapter break → `section_divider`;
  table of contents → `agenda`.
- **Single number is the point:** → `stat_hero`. Multiple numbers in tiles →
  `kpi_dashboard`. KPIs by BU with target/actual + status dots →
  `assessment_table`.
- **Voice / quote:** single quote → `quote_slide`; otherwise summarize and use
  bullets.
- **Three vs five vs seven items?** → `three_trends_*` / `five_key_areas` /
  `overview_areas`.
- **Time series (single metric):** flat trend + one growth label →
  `column_simple_growth`; inflection → `column_split_growth`; forecast →
  `column_historic_forecast`. Multi-series time series with continuous lines →
  `line_chart`.
- **Categorical bars:** sorted high-to-low with one focus → `column_comparison`.
  Two scenarios per category → `grouped_column_chart`. Parts-of-a-whole per
  category → `stacked_column_chart`.
- **Matrix / 2D:** two continuous axes → `bubble_chart` /
  `bubble_chart_takeaways`; market-share × growth quadrants → `growth_share`;
  impact × time bands → `prioritization_matrix`.
- **Any table from the source:** → `data_table` (keep every row and column).
  More than 4 series over time → `data_table` with `highlight_rows`, or a
  `line_chart` of the 4 most relevant series *plus* the full table elsewhere.
- **Comparison of options:** 2–4 options × criteria with Harvey balls →
  `comparison_table` (only when the source gives ratings); options × text
  features → `data_table` with `highlight_col`; one option's +/− → `pros_cons`; before/after or
  current/future → `two_column_compare`.
- **Hierarchy:** drivers of an issue → `issue_tree`; reporting lines →
  `org_chart`; one leader + N teammates → `project_team_circles`; function ×
  role grid → `team_chart`.
- **Roadmap:** 3 phases → `phases_chevron_3`; 4 phases (text) →
  `phases_table_4`; 4 waves on arrow → `waves_timeline_4`; 10+ weeks parallel
  streams → `gantt_timeline`; 3–4 time blocks with deliverables →
  `process_activities`; 4–6 generic linear steps → `process_flow_horizontal`.
- **Conversion / sizing:** TAM/SAM/SOM or marketing funnel → `funnel`.
- **Summary:** narrative → `executive_summary_paragraph`; structured
  takeaways → `executive_summary_takeaways`; single bold statement →
  `dark_navy_summary`.

---

# Common arguments

These work on every template (don't add them unless useful):

- `title: str` — slide title (bold, with bottom rule). Defaults to a placeholder.
- `section_marker: str` — small label in the top-right (e.g. "Strategy review").
- `page_number: int` — auto-numbered if `auto_page_numbers=True` on the builder.
- `source: str`, `footnote: str` — bottom-left small text.
- `theme: Theme` — build it with `make_theme(company, lang=..., brand=...)`.

# Building a deck

Chinese deck:

```python
from mckinsey_pptx import PresentationBuilder, make_theme

b = PresentationBuilder(theme=make_theme("某某公司", lang="zh"), default_section_marker="Q4 回顾")
b.add("dark_navy_summary", body="[核心结论]: ...")
b.save("output/deck.pptx")
```

Korean / custom theme:

```python
from mckinsey_pptx import PresentationBuilder, DEFAULT_THEME
from mckinsey_pptx.theme import Typography
from dataclasses import replace

KO_THEME = replace(
    DEFAULT_THEME,
    typography=replace(DEFAULT_THEME.typography, family="Apple SD Gothic Neo"),
    copyright_text="ⓒ 2026 Acme",
)

b = PresentationBuilder(theme=KO_THEME, default_section_marker="Q4 review")
b.add("dark_navy_summary", body="[Bottom line]: ...")
b.add("executive_summary_takeaways", sections=[...])
b.add("column_historic_forecast", categories=[...], values=[...], forecast_from_index=5,
      historic_growth="3%", forecast_growth="6%")
b.save("output/deck.pptx")
```
