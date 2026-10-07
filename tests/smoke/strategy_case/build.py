"""Smoke test 6 — strategy case from a markdown outline (source mode,
English): storyline summary, logic grids (firm analysis; five forces with
direction="down"), strategic challenge, option deep dives as composite
logic chains (headers + connectors + callout + sections), scorecard,
recommendation."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

OPTIONS = [
    dict(name="Retail channels", kicker="Option A | Retail channels", icon="cart",
         title="Option A: bottled drinks in retail add a second growth engine",
         what="Sell own-brand bottled tea drinks through e-commerce and convenience stores",
         how=["A second growth engine that does not depend on opening stores",
              "The brand reaches customers outside the bar"],
         vp="Northwind drinks wherever young customers shop",
         activities=[("Product", ["Adapt two existing drinks for bottling"]),
                     ("Sales", ["Build a channel team for e-commerce and convenience stores"])],
         pros=["Second growth engine", "Scale lowers unit cost"],
         cons=["Competes with beverage leaders", "May reduce store visits"]),
    dict(name="Premium sub-brand", kicker="Option B | Premium sub-brand", icon="gem",
         title="Option B: a premium sub-brand opens a segment with less direct rivalry",
         what="Open a quieter, premium tea-bar format in tier-1 business districts",
         how=["A new segment with less direct rivalry",
              "Moves from the mid-price tier into the premium tier"],
         vp="A quiet, premium place to meet at night",
         activities=[("Product", ["Premium drinks menu"]),
                     ("Stores", ["Pilot stores in business districts"])],
         pros=["Higher spend per visit", "Less direct rivalry"],
         cons=["The new brand starts with low awareness", "Higher fit-out cost"]),
    dict(name="Partner network", kicker="Option C | Partner network", icon="handshake",
         title="Option C: a partner network adds reasons to visit at low investment",
         what="A membership alliance with board-game cafes and cinemas",
         how=["More reasons to visit through shared membership"],
         vp="One membership for a night out",
         activities=[("Partners", ["Sign board-game cafes and cinemas"]),
                     ("Membership", ["One shared card and joint offers"])],
         pros=["Low investment", "Shared marketing"],
         cons=["Weak control over partners", "Benefits are mostly short-term"]),
]


def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme("Northwind"), default_section_marker="Strategy case")
    N = dict(source="", footnote="")
    b.add("cover_slide", title="Northwind Tea House", subtitle="Strategic analysis", date="2025")

    b.add("storyline_summary", kicker="Executive summary",
          title="Grow through retail channels first, then a premium sub-brand",
          situation=[{"title": "Firm analysis", "bullets": [
                          "Cozy social space with no table charge: **93%** satisfaction",
                          "Own-brand drinks at RMB 15-25; revenue RMB 210M → 540M"]},
                     {"title": "Competition", "bullets": [
                          "Low entry barrier; two rivals copy the format",
                          "Substitutes serve the same night-time need"]}],
          question="How can Northwind keep revenue growth sustainable, given rivals copying its format?",
          options=[{"body": "Sell bottled drinks through retail channels", "badge": "Recommended first"},
                   {"body": "Open a premium sub-brand", "badge": "Recommended second"},
                   {"body": "Build a partner network"}],
          recommended=[0, 1],
          recommendation=[{"title": "Short term", "body": "two bottled drinks on e-commerce in 2025"},
                          {"title": "Long term", "body": "pilot the premium sub-brand with 5 stores in 2026"}],
          **N)

    b.add("logic_grid", kicker="Situation (1/3) | Firm analysis",
          title="Northwind wins young customers on social space and value, but both are easy to copy",
          stages=["Customer need", "What Northwind does", "Performance"],
          conclusion_label="Implication",
          rows=[{"label": "Social space", "icon": "users",
                 "cells": ["A cozy place to meet friends at night: **62%** name social needs",
                           ["Relaxed tea-bar format", "No table charge, music events"],
                           ["Satisfaction **93%**", "Repeat-visit rate **88%**"]],
                 "conclusion": "Attracts the target customers, but the format is easy to copy"},
                {"label": "Value for money", "icon": "money",
                 "cells": ["**58%** say price matters when they choose a place",
                           "Own-brand drinks at RMB 15-25, below most rivals",
                           "Revenue RMB **210M** (2021) → **540M** (2023)"],
                 "conclusion": "Customers are price sensitive: raising prices is hard"}],
          **N)

    b.add("chart", chart_type="column", kicker="Situation (2/3) | Store growth",
          title="Store count more than tripled in two years, funded by a 24% store margin",
          subtitle="Store count", categories=["2021", "2022", "2023"],
          series=[{"name": "Stores", "values": [120, 260, 410]}], highlight={"point": 2},
          insight="Cost control funds fast expansion, but it is not a lasting barrier",
          insight_bullets=["Store-level net margin **24%** vs **16%** for the peer average"],
          **N)

    b.add("logic_grid", direction="down", kicker="Situation (3/3) | Five forces",
          title="A low entry barrier and zero switching cost put the format under pressure",
          stages=["Current situation"], conclusion_label="Influence on Northwind",
          rows=[{"label": "New entrants",
                 "cells": [["Low capital needs", "Rent and fit-out are the main costs"]],
                 "conclusion": "Low entry barrier: expect more copycats"},
                {"label": "Rivals",
                 "cells": [["Top 5 chains hold **6%** of the market",
                            "Two rivals copy the format in tier-2 cities"]],
                 "conclusion": "Price competition in tier-1 and tier-2 cities"},
                {"label": "Substitutes",
                 "cells": [["KTV, board-game cafes and restaurants serve the same night-time need",
                            "Switching cost is zero"]],
                 "conclusion": "Loyalty must come from the experience, not from price"}],
          **N)

    b.add("strategic_challenge", kicker="Strategic challenge",
          title="Copying, low loyalty and a store-only model converge on slowing growth",
          drivers=[{"body": "The format is easy to copy", "result": "Rivals erode the differentiation"},
                   {"body": "Customers have low loyalty", "result": "Visits move to whatever is new"},
                   {"body": "Revenue comes from store operation only",
                    "result": "Growth is tied to opening stores"}],
          threat="Revenue growth per store slows as rivals open nearby",
          question="How can Northwind keep revenue growth sustainable, given rivals copying its format?",
          **N)

    b.add("option_profiles", kicker="Options | overview",
          title="Three ways to grow beyond the store format",
          options=[{"name": o["name"], "icon": o["icon"], "summary": o["what"],
                    "pros": o["pros"][:1], "cons": o["cons"][:1]} for o in OPTIONS],
          insight=None, **N)

    for o in OPTIONS:
        b.add("composite", kicker=o["kicker"], group="options", title=o["title"],
              headers=["How it addresses the challenge", "Key activities",
                       "Advantages and disadvantages"],
              connectors=True,
              columns=[[{"type": "bullets", "items": o["how"]},
                        {"type": "callout", "arrow": True, "label": "New value proposition",
                         "text": o["vp"]}],
                       [{"type": "sections", "sections": [{"title": t, "bullets": bl}
                                                         for t, bl in o["activities"]]}],
                       [{"type": "pros_cons", "pros": o["pros"], "cons": o["cons"]}]],
              **N)

    b.add("decision_matrix", kicker="Evaluation | weighted scorecard",
          title="Retail channels score highest; the premium sub-brand is second",
          options=["A: Retail channels", "B: Premium sub-brand", "C: Partner network"],
          criteria=[{"name": "Market size", "weight": 30, "scores": [5, 3, 2]},
                    {"name": "Fit with capabilities", "weight": 25, "scores": [4, 4, 3]},
                    {"name": "Competitive intensity", "weight": 25, "scores": [2, 4, 3]},
                    {"name": "Risk", "weight": 20, "scores": [4, 3, 3]}],
          scale_note="1 = poor, 5 = excellent; weighted score in brackets; gold = best in row",
          insight="Option A leads on market size; Option B on competitive intensity", **N)

    b.add("card_grid", kicker="Recommendation",
          title="Recommend Option A first and Option B second",
          cards=[{"title": "Short term: retail channels", "icon": "cart", "tone": "blue",
                  "bullets": ["Launch two bottled drinks on e-commerce in **2025**",
                              "Then convenience stores in tier-1 cities"]},
                 {"title": "Long term: premium sub-brand", "icon": "gem", "tone": "navy",
                  "bullets": ["Pilot the premium sub-brand with **5** stores in **2026**"]}],
          **N)
    out = out_dir / "strategy_case.pptx"
    b.save(str(out))
    return out


SOURCES = [HERE / "source.md"]
# weighted scores / totals computed from the scorecard
DERIVED = {"3.8", "3.5", "2.7", "100", "1.5", "1", "0.5", "0.8", "0.9", "0.6", "0.75"}

if __name__ == "__main__":
    print(build(HERE))
