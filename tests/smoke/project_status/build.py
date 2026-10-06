"""Smoke test 2 — programme status update from a short brief (brief mode, no source file).

Brief: "ERP programme steering update: design done, build 60% complete, data
migration 3 weeks late, go-live wave 1 in October and wave 2 in December,
budget $8.2M with $5.1M spent; need decisions on extra data engineers and on
freezing scope."
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme(), default_section_marker="ERP steering")
    N = dict(source="", footnote="")
    b.add("dark_navy_summary", body="[Bottom line]: Go-live wave 1 in October holds only if data "
          "migration recovers 3 weeks; two decisions are needed today.")
    b.add("scorecard", title="Build is on track; data migration is 3 weeks late",
          metrics=[{"metric": "Design", "target": "Complete", "actual": "Complete", "status": "green"},
                   {"metric": "Build", "target": "60%", "actual": "60%", "status": "green"},
                   {"metric": "Data migration", "target": "On plan", "actual": "3 weeks late", "status": "red",
                    "comment": "Recovery needs extra data engineers"},
                   {"metric": "Budget", "target": "$8.2M", "actual": "$5.1M spent", "status": "green"}], **N)
    b.add("roadmap", title="Two go-live waves: October and December",
          periods=["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          lanes=[{"name": "Build", "items": [{"label": "Build (60% done)", "start": 0, "end": 2}]},
                 {"name": "Data migration", "items": [{"label": "Migration (3 wks late)", "start": 0, "end": 3, "tone": "amber"}]},
                 {"name": "Go-live", "items": [{"label": "Wave 1", "start": 3, "end": 3, "tone": "green"},
                                               {"label": "Wave 2", "start": 5, "end": 5, "tone": "green"}]}],
          milestones=[{"label": "Wave 1 go-live", "at": 4, "tone": "green"},
                      {"label": "Wave 2 go-live", "at": 6, "tone": "green"}],
          insight="Migration is the critical path for wave 1", **N)
    b.add("card_rows", title="Two decisions are needed from the steering committee",
          rows=[{"title": "Add data engineers", "icon": "users", "tone": "amber",
                 "body": "Recover the **3-week** migration delay before wave 1"},
                {"title": "Freeze scope", "icon": "lock", "tone": "blue",
                 "body": "Protect the October and December go-live dates"}], **N)
    out = out_dir / "project_status.pptx"
    b.save(str(out))
    return out

SOURCES = []          # brief mode
DERIVED = set()

if __name__ == "__main__":
    print(build(HERE))
