"""Score how well a slide plan (or a built deck) picks templates.

    python tests/selection_eval/score.py <case> <plan.md | deck.pptx>
    python tests/selection_eval/score.py --all <folder>   # <folder>/<case>_plan.md for each case

<case> is a folder name here (market_entry, operations, strategy_options, qbr).
Each slide of the case has reference answers in <case>/answers.json:
  preferred  2 points   the template the relationship calls for
  acceptable 1 point    a defensible second choice
  trap      -1 point    a known wrong reading (e.g. fishbone with a borrowed effect)
  anything else 0
A composite counts as each diagram it holds ("composite:slopegraph"), and a
plan row is matched to the outline by "Slide N" in its Source section column.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import plan_check  # noqa: E402

CASES = ("market_entry", "operations", "strategy_options", "qbr")


def _canon(name: str) -> str:
    if name.startswith("composite:"):
        return "composite:" + (plan_check.canonical(name[10:]) or name[10:])
    return plan_check.canonical(name) or name


def choices_from_plan(path: Path) -> dict:
    """{source slide number: (template, [diagram templates], has_chart)}"""
    rows = plan_check.parse_plan(path.read_text(encoding="utf-8-sig"))
    out = {}
    for i, r in enumerate(rows, start=1):
        m = re.search(r"slide\s*(\d+)", r.get("section", ""), re.I)
        n = int(m.group(1)) if m else (r["n"] or i)
        diagrams = [p.partition(":")[2] for p in r["parts"] if p.startswith("diagram:")]
        out.setdefault(n, (r["template"], diagrams, "chart" in r["parts"]))
    return out


def choices_from_deck(path: Path) -> dict:
    import deck_check
    from pptx import Presentation
    prs = Presentation(str(path))
    return {i: (deck_check.template_of(s) or "", deck_check.diagrams_of(s), False)
            for i, s in enumerate(prs.slides, start=1)}


def candidates(template: str, diagrams, has_chart) -> set:
    c = {_canon(template)} if template else set()
    for d in diagrams:
        c |= {_canon("composite:" + d), _canon(d)}
    if has_chart:
        c.add("chart")
    return c


def score_case(case: str, path: Path):
    answers = json.loads((HERE / case / "answers.json").read_text(encoding="utf-8"))["slides"]
    chosen = choices_from_deck(path) if path.suffix == ".pptx" else choices_from_plan(path)
    text_layouts = plan_check._text_layouts()
    rows, total, best = [], 0, 0
    stats = {"preferred": 0, "acceptable": 0, "zero": 0, "trap": 0, "missing": 0,
             "diagram_slides": 0, "diagram_hits": 0, "list_slides": 0, "over_diagram": 0}
    for key, ans in answers.items():
        n = int(key)
        if ans["preferred"] == ["cover_slide"]:
            continue
        pref = {_canon(t) for t in ans["preferred"]}
        acc = {_canon(t) for t in ans.get("acceptable", [])}
        trap = {_canon(t) for t in ans.get("trap", [])}
        best += 2
        is_list = ans.get("list", False)
        if n not in chosen:
            stats["missing"] += 1
            rows.append((n, "—", 0, ans["relationship"], ans["preferred"]))
            continue
        tpl, diagrams, has_chart = chosen[n]
        cand = candidates(tpl, diagrams, has_chart)
        pts = 2 if cand & pref else 1 if cand & acc else -1 if cand & trap else 0
        stats[{2: "preferred", 1: "acceptable", 0: "zero", -1: "trap"}[pts]] += 1
        total += pts
        textual = _canon(tpl) in text_layouts and not diagrams and not has_chart
        if is_list:
            stats["list_slides"] += 1
            stats["over_diagram"] += int(not textual and pts <= 0)
        else:
            stats["diagram_slides"] += 1
            stats["diagram_hits"] += int(not textual)
        shown = tpl + (f"[{', '.join(diagrams)}]" if diagrams else "")
        rows.append((n, shown, pts, ans["relationship"], ans["preferred"]))
    return rows, total, best, stats


def report(case, path):
    rows, total, best, st = score_case(case, path)
    print(f"== {case}: {total}/{best} ({total / best:.0%})  — {path.name}")
    for n, shown, pts, rel, pref in rows:
        mark = {2: "✓", 1: "~", 0: "✗", -1: "✗✗"}[pts]
        print(f"  {n:>2} {mark:2} {shown:34.34} {rel[:44]:44}  ref: {', '.join(pref)}")
    print(f"  preferred {st['preferred']} · acceptable {st['acceptable']} · other {st['zero']} · "
          f"trap {st['trap']} · missing {st['missing']}")
    print(f"  relationship slides drawn as a diagram/chart: {st['diagram_hits']}/{st['diagram_slides']}"
          f" · list slides over-diagrammed: {st['over_diagram']}/{st['list_slides']}")
    return total, best, st


def main(argv) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    if len(argv) == 2 and argv[0] == "--all":
        folder, grand, gbest = Path(argv[1]), 0, 0
        for case in CASES:
            hits = sorted(folder.glob(f"*{case}*plan*.md")) or sorted(folder.glob(f"*{case}*.pptx"))
            if not hits:
                print(f"== {case}: no plan or deck found in {folder}\n")
                continue
            t, b, _ = report(case, hits[-1])
            grand, gbest = grand + t, gbest + b
            print()
        if gbest:
            print(f"TOTAL {grand}/{gbest} ({grand / gbest:.0%})")
        return 0
    if len(argv) != 2 or argv[0] not in CASES:
        print(__doc__)
        return 1
    report(argv[0], Path(argv[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
