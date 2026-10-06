"""Smoke test 5 — options evaluation proposal from a markdown outline
(source mode, English): neutral overview, one parallel slide per option,
weighted scorecard, recommendation with roadmap, risk register."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

OPTIONS = [
    dict(n=1, name="Buy a SaaS CRM", short="Vendor A SaaS", icon="cart", kicker="Option 1 | Buy a SaaS CRM",
         title="Buying SaaS is fastest to value but limits credit workflows",
         flow=[{"title": "Harbor Bank", "body": "Owns data and process"},
               {"title": "Vendor A", "body": "SaaS CRM, upgrades included"},
               {"title": "Integrator", "body": "Certified, 3 waves"}],
         econ=[["Licence per year", "$2.1M"], ["Implementation", "$4.5M"],
               {"label": "5-year cost", "value": "$15.0M", "total": True}],
         why=["Covers **85%** of requirements out of the box", "Upgrades included"],
         how=["3 waves by region", "Retire the old CRM in month 15"],
         pros=["Fastest time to value: **9 months** to first wave", "Lowest delivery risk"],
         cons=["Limited customisation of credit workflows", "Data residency needs a dedicated region"],
         verdict="Best if speed matters more than credit-workflow fit"),
    dict(n=2, name="Extend in-house", short="In-house build", icon="settings", kicker="Option 2 | Extend the in-house platform",
         title="Extending in-house keeps control but delays any release by 18 months",
         flow=[{"title": "Harbor Bank", "body": "40 engineers"},
               {"title": "In-house platform", "body": "New front end, modern integration"},
               {"title": "Relationship managers", "body": "1,200 users"}],
         econ=[["Build", "$9.0M"], ["Run cost per year", "$1.2M"],
               {"label": "5-year cost", "value": "$15.0M", "total": True}],
         why=["Team knows the bank's processes", "Reuses the existing data model"],
         how=["Rebuild front end", "Modernise integration layer, 18 months"],
         pros=["Full control of credit workflows", "No licence dependency"],
         cons=["**18 months** before any release", "Key-person risk in a team of 40"],
         verdict="Best fit, but the timeline collides with the 18-month support deadline"),
    dict(n=3, name="Hybrid", short="SaaS core + credit module", icon="layers", kicker="Option 3 | SaaS core plus in-house credit module",
         title="The hybrid buys commodity functions and builds only the credit module",
         flow=[{"title": "SaaS core", "body": "Contact and pipeline"},
               {"title": "Platform API", "body": "Integration point"},
               {"title": "Credit module", "body": "Built in-house"}],
         econ=[["Licence per year", "$1.6M"], ["Implementation", "$5.5M"],
               {"label": "5-year cost", "value": "$13.5M", "total": True}],
         why=["Buy commodity sales functions", "Build only what differentiates the bank"],
         how=["SaaS for contact and pipeline management", "Credit module on the SaaS platform API"],
         pros=["Lowest 5-year cost", "Keeps credit workflows in-house"],
         cons=["Two teams to coordinate", "API limits of the SaaS platform"],
         verdict="Balances cost, speed and fit — if the platform API holds up"),
]


def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme("Harbor Bank"), default_section_marker="CRM options")
    N = dict(source="", footnote="")
    b.add("option_profiles", kicker="CRM replacement | three options",
          title="Three ways to replace the CRM before support ends in 18 months",
          options=[{"name": o["name"], "tagline": o["short"], "icon": o["icon"],
                    "metrics": [{"value": o["econ"][-1]["value"], "label": "5-year cost"}],
                    "pros": o["pros"][:1], "cons": o["cons"][:1]} for o in OPTIONS],
          insight="No option is best on time, cost and fit at once", **N)
    for o in OPTIONS:
        b.add("composite", kicker=o["kicker"], group="options", title=o["title"],
              columns=[[{"type": "flow", "heading": "Delivery model", "steps": o["flow"], "highlight": 1},
                        {"type": "kv_table", "heading": "Economics", "rows": o["econ"]}],
                       [{"type": "cards", "columns": 2, "cards": [
                           {"title": "Why", "icon": "lightbulb", "bullets": o["why"]},
                           {"title": "How", "icon": "settings", "bullets": o["how"]},
                           {"title": "Advantages", "icon": "check", "tone": "green", "bullets": o["pros"]},
                           {"title": "Disadvantages", "icon": "cross", "tone": "red", "bullets": o["cons"]}]}]],
              widths=[1.1, 1], insight=o["verdict"], insight_label="Verdict", **N)
    b.add("decision_matrix", kicker="Evaluation | weighted scorecard",
          title="The hybrid scores highest; buying SaaS is a close second",
          options=["Buy SaaS", "Extend in-house", "Hybrid"],
          criteria=[{"name": "Time to value", "weight": 30, "scores": [5, 2, 4]},
                    {"name": "5-year cost", "weight": 25, "scores": [3, 3, 4]},
                    {"name": "Fit with credit workflows", "weight": 20, "scores": [2, 5, 4]},
                    {"name": "Delivery risk", "weight": 15, "scores": [4, 2, 3]},
                    {"name": "Vendor dependency", "weight": 10, "scores": [2, 5, 3]}],
          scale_note="1 = poor, 5 = excellent; weighted score in brackets; gold = best in row",
          insight="The hybrid is never last and leads on cost",
          insight_bullets=["Buying SaaS wins on time to value only"], **N)
    b.add("composite", kicker="Recommendation (1/2) | rationale and roadmap",
          title="Recommend the hybrid, delivered in three phases over 18 months",
          columns=[[{"type": "cards", "heading": "Rationale", "weight": 0.9, "cards": [
                        {"title": "Lowest 5-year cost", "icon": "money", "body": "**$13.5M** vs. $15.0M for both alternatives"},
                        {"title": "Keeps differentiation", "icon": "shield", "body": "Credit workflows stay in-house"},
                        {"title": "Meets the deadline", "icon": "clock", "body": "Old CRM retired by month 18"}]},
                    {"type": "phases", "heading": "Roadmap", "phases": [
                        {"period": "Months 0–6", "name": "Core", "bullets": ["SaaS core for one region"]},
                        {"period": "Months 7–12", "name": "Extend", "bullets": ["Credit module", "Two more regions"]},
                        {"period": "Months 13–18", "name": "Retire", "bullets": ["Retire the old CRM"]}]}]],
          **N)
    b.add("risk_register", kicker="Recommendation (2/2) | risks and mitigation",
          title="One high risk must be tested before the contract is signed",
          risks=[{"title": "SaaS API limits", "severity": "high",
                  "mitigations": ["Proof of concept before contract signature"]},
                 {"title": "Team coordination", "severity": "medium",
                  "mitigations": ["One programme office", "Shared backlog"]},
                 {"title": "Data residency", "severity": "medium",
                  "mitigations": ["Contract a dedicated region"]}],
          insight="Run the API proof of concept first: it decides between hybrid and buy", insight_label="Decision needed", **N)
    out = out_dir / "options_eval.pptx"
    b.save(str(out))
    return out

SOURCES = [HERE / "source.md"]
# weighted scores / totals computed from the scorecard
DERIVED = {"3.8", "2.9", "3.75", "3.15", "3.45", "100",
           "1.5", "0.75", "0.6", "0.4", "0.3", "0.2", "1.2", "1", "0.45", "0.8", "0.5"}

if __name__ == "__main__":
    print(build(HERE))
