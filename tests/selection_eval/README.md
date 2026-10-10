# Template-selection eval

Four outlines written so that most slides carry a clear relationship (split,
flow, gap, rank, causes, loop, layers, overlap …), plus a few slides that really
are lists and one trap (issues with no stated effect → not a fishbone). Each
`answers.json` gives the preferred / acceptable / trap templates per outline
slide. All companies and numbers are fictional.

| Case | Slides | Tests |
|---|---|---|
| `market_entry` | 11 | marimekko, multi-series line, dumbbell, funnel, sankey, journey, weighted decision matrix, risk heat map, list, roadmap |
| `operations` | 11 | trend vs target, fishbone (stated effect), waterfall, swimlane, heatmap, bump, slopegraph + notes (composite), 2×2 priorities, scorecard, list |
| `strategy_options` | 11 | storyline summary, treemap, venn, 2×2 positioning, option profiles, radar, cycle, layer stack, hub-and-spoke, roadmap |
| `qbr` | 10 | multi-series chart, mix, waterfall, actual-vs-target gap, **trap** (issues ≠ fishbone), issue tree, text table, list, timeline |

## Running a case (plan only, ~5 minutes)

In Antigravity, new conversation, attach `<case>/outline.md`, and send:

> 使用 mckinsey-pptx skill，基于附件的大纲做一份演示文稿。只做到 slide plan（Step 3），运行 `catalog.py --plan` 校验通过后停止，不要构建 deck。

Then score the plan it wrote:

    python tests/selection_eval/score.py <case> <workspace>/output/<slug>_plan.md

or copy all four plans into one folder (file names containing the case name)
and run `score.py --all <folder>`. A built deck can be scored too
(`score.py <case> deck.pptx`): slides are matched by position.

## Reading the score

- **score**: 2 per preferred, 1 per acceptable, −1 per trap; % of the maximum.
- **relationship slides drawn as a diagram/chart**: the diagram rate on slides
  that are not lists — the main signal for "picks text layouts by default".
- **list slides over-diagrammed**: a diagram where a list was right.

Plan-only runs measure the choice before any checker feedback; a full build
may change a few slides. Run each case at least twice before comparing
versions: single runs varied by ±15% in the Crest tests.
