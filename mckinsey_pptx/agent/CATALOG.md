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

## Rich text, tones and icons (templates 41–51)

- `**bold**` → bold; `{red|text}` → bold in that tone (`navy`, `blue`,
  `mid_blue`, `light_blue`, `red`, `green`, `amber`, `gray`). Use red for
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

# Choosing between similar templates

Quick decision rules to avoid common confusions:

- **New decks default to the rich templates (41–51):** structured points →
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
