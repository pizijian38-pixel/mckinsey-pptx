"""Smoke test 4 — 5-slide live pitch from a short brief (brief mode, live talk).

Brief: "5-minute pitch to the investment committee: invest $3.0M in warehouse
automation. Saves $1.4M a year (labour $0.9M, picking errors $0.3M, space
$0.2M), payback about 2 years. Pilot in Q1, full rollout by Q3. Ask: approve
$3.0M."
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme(), default_section_marker="Investment case")
    N = dict(source="", footnote="")
    b.add("dark_navy_summary", body="[The ask]: Approve $3.0M for warehouse automation — "
          "it saves $1.4M a year and pays back in about 2 years.")
    b.add("card_grid", title="$3.0M in, $1.4M a year back",
          cards=[{"value": "$3.0M", "title": "Investment", "tone": "navy", "body": "One-off"},
                 {"value": "$1.4M", "title": "Annual saving", "tone": "green", "body": "From year one"},
                 {"value": "~2 yrs", "title": "Payback", "tone": "blue", "body": "Pilot first, then rollout"}], **N)
    b.add("waterfall", title="Labour drives two-thirds of the $1.4M saving",
          subtitle="Annual saving by source, $M", number_format="0.0",
          steps=[{"label": "Labour", "value": 0.9}, {"label": "Picking errors", "value": 0.3},
                 {"label": "Space", "value": 0.2}, {"label": "Total", "value": 1.4, "total": True}], **N)
    b.add("timeline", title="Pilot in Q1, full rollout by Q3",
          events=[{"date": "Q1", "title": "Pilot", "body": "Prove the saving"},
                  {"date": "Q2", "title": "Rollout", "body": "Remaining sites"},
                  {"date": "Q3", "title": "Full rollout", "body": "All sites live", "tone": "green"}], **N)
    b.add("card_rows", title="The ask: approve $3.0M today",
          rows=[{"title": "Approve $3.0M", "icon": "check", "tone": "green",
                 "body": "Releases the pilot in Q1 and full rollout by Q3"}], **N)
    out = out_dir / "live_pitch.pptx"
    b.save(str(out))
    return out

SOURCES = []
DERIVED = set()

if __name__ == "__main__":
    print(build(HERE))
