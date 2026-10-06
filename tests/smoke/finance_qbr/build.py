"""Smoke test 1 — quarterly business review from an Excel source (source mode, English)."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme("Acme Industrial", brand="1F4E79"),
                            default_section_marker="Q3 2024 review")
    N = dict(source="", footnote="")
    b.add("cover_slide", title="Q3 2024 business review", subtitle="Revenue up 4.9%, EBIT down $14M on freight and wages",
          date="October 2024", confidentiality=None)
    b.add("card_grid", title="Revenue grew 4.9%, but EBIT fell as costs outran price",
          cards=[{"title": "Revenue", "icon": "trend_up", "tone": "green", "value": "$870M",
                  "body": "Up from **$822M**; APAC **+17%**"},
                 {"title": "EBIT", "icon": "trend_down", "tone": "red", "value": "$106M",
                  "body": "Down from **$120M**: freight and wages"},
                 {"title": "EMEA margin", "icon": "alert", "tone": "red", "value": "31%",
                  "body": "Down from 34%; freight cost up 104%"}],
          insight="The margin problem is concentrated in EMEA freight", **N)
    b.add("scorecard", title="Three of five KPIs are off target; churn needs action",
          metrics=[{"metric": "Revenue growth", "target": "+5%", "actual": "+5.3%", "status": "green", "comment": "APAC ahead"},
                   {"metric": "Gross margin", "target": "37%", "actual": "36.4%", "status": "amber", "comment": "EMEA freight"},
                   {"metric": "Customer churn", "target": "<5%", "actual": "6.8%", "status": "red", "comment": "Two key accounts lost in EMEA"},
                   {"metric": "On-time delivery", "target": "95%", "actual": "96%", "status": "green"},
                   {"metric": "Cash conversion", "target": "90%", "actual": "88%", "status": "amber", "comment": "Inventory build in Q3"}],
          **N)
    b.add("chart", chart_type="column", title="Monthly revenue rose from $268M to $295M",
          subtitle="Revenue by month, 2024, $M",
          categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
          series=[{"name": "Revenue", "values": [268, 271, 279, 282, 286, 290, 284, 291, 295]}],
          highlight={"point": 8}, number_format="#,##0",
          insight="Only July dipped; September was the strongest month", **N)
    b.add("waterfall", title="EBIT fell $14M as freight and wages outweighed price",
          subtitle="EBIT bridge Q3 2023 → Q3 2024, $M",
          steps=[{"label": "Q3 2023", "value": 120, "total": True}, {"label": "Price", "value": 18},
                 {"label": "Volume", "value": 6}, {"label": "Freight", "value": -22},
                 {"label": "Wages", "value": -11}, {"label": "FX", "value": -5},
                 {"label": "Q3 2024", "value": 106, "total": True}],
          insight="Cost items (−38) more than offset commercial gains (+24)",
          insight_bullets=["Freight alone is larger than the price gain"], **N)
    b.add("data_table", title="EMEA is the only region where revenue and margin both fell",
          subtitle="Results by region",
          columns=["Region", "Revenue Q3 2024 ($M)", "Revenue Q3 2023 ($M)", "Gross margin Q3 2024", "Gross margin Q3 2023", "Comment"],
          rows=[["North America", 412, 389, "38%", "37%", "Price increase held"],
                ["EMEA", 268, 271, "{red|31%}", "34%", "Freight cost up 104%"],
                ["APAC", 190, 162, "41%", "39%", "Mix shift to services"]],
          highlight_rows=[1], **N)
    b.add("card_rows", title="Three actions target the cost and churn gaps",
          rows=[{"title": "Renegotiate EMEA freight", "icon": "truck", "body": "Owner **COO** · due Nov 2024"},
                {"title": "Win back lost accounts", "icon": "handshake", "body": "Owner **CCO** · due Dec 2024"},
                {"title": "Cut safety stock by 10 days", "icon": "package", "body": "Owner **CFO** · due Q1 2025"}],
          **N)
    out = out_dir / "finance_qbr.pptx"
    b.save(str(out))
    return out

SOURCES = [HERE / "source.xlsx"]
# Figures computed from the source (sums / growth rates) — declared, not invented.
DERIVED = {"870", "822", "4.9", "17", "38", "24", "14"}

if __name__ == "__main__":
    print(build(HERE))
