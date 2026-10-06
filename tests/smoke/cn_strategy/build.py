"""Smoke test 3 — Chinese strategy deck from a Chinese markdown outline (source mode, zh)."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme("星海科技", lang="zh"), default_section_marker="东南亚策略")
    N = dict(source="", footnote="")
    b.add("cover_slide", title="智能家居业务东南亚进入策略", subtitle="优先进入越南和印尼", date="2025", confidentiality=None)
    b.add("dark_navy_summary", body="[结论]: 优先进入越南和印尼，2026 年实现海外营收 12 亿元。")
    b.add("chart", chart_type="column", title="东南亚智能家居市场持续扩大",
          subtitle="市场规模（亿元），2025 年为预计", categories=["2022", "2023", "2024", "2025 预计"],
          series=[{"name": "市场规模", "values": [180, 220, 270, 330]}], highlight={"point": 3},
          insight="市场从 180 亿元增至预计 330 亿元", insight_title="关键结论", **N)
    b.add("data_table", title="越南增长最快，印尼规模最大",
          columns=["国家", "市场规模（亿元）", "年增长率", "竞争强度"],
          rows=[["越南", 60, "{green|28%}", "中"], ["印尼", 95, "24%", "高"],
                ["泰国", 70, "15%", "高"], ["马来西亚", 45, "12%", "中"]],
          highlight_rows=[0, 1], insight="越南和印尼兼具规模与增长", insight_title="关键结论", **N)
    b.add("swot", title="成本与产品线是优势，品牌与售后是短板",
          labels=("优势", "劣势", "机会", "威胁"),
          strengths=["供应链成本低于当地品牌 20%", "产品线完整"],
          weaknesses=["品牌知名度低", "没有本地售后网络"],
          opportunities=["电商渗透率快速提升"], threats=["本地品牌价格战"], **N)
    b.add("matrix_2x2", title="越南优先进入，印尼通过合作进入",
          x_label="进入难度", y_label="市场吸引力", x_ends=("低", "高"), y_ends=("中", "高"),
          quadrants=[{"title": "优先进入", "tone": "green", "items": ["越南"]},
                     {"title": "合作进入", "items": ["印尼"]},
                     {"title": "电商试点", "items": ["马来西亚"]},
                     {"title": "暂缓", "tone": "gray", "items": ["泰国"]}],
          highlight=0, **N)
    b.add("roadmap", title="分三步推进：越南先行，2026 年覆盖三国",
          periods=["2025 上半年", "2025 下半年", "2026 年"],
          lanes=[{"name": "越南", "items": [{"label": "建立团队", "start": 0, "end": 0},
                                            {"label": "上市", "start": 1, "end": 1, "tone": "green"}]},
                 {"name": "印尼", "items": [{"label": "寻找合作方", "start": 1, "end": 1, "tone": "amber"},
                                            {"label": "上市", "start": 2, "end": 2, "tone": "green"}]},
                 {"name": "马来西亚", "items": [{"label": "电商试点", "start": 2, "end": 2, "tone": "mid_blue"}]}],
          **N)
    out = out_dir / "cn_strategy.pptx"
    b.save(str(out))
    return out

SOURCES = [HERE / "source.md"]
DERIVED = set()

if __name__ == "__main__":
    print(build(HERE))
