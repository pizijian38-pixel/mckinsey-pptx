"""中文示例演示文稿 —「新能源汽车品牌出海战略回顾」。

保留麦肯锡风格版式，中文字形使用 ZH 主题（默认 微软雅黑）。

Run:  python -m examples.demo_chinese  -> writes output/demo_chinese.pptx
"""
from __future__ import annotations
from pathlib import Path

from mckinsey_pptx import PresentationBuilder, make_zh_theme


# 公司名会出现在页脚版权（ⓒ 2026 示例公司）和深蓝总结页右下角
ZH_DEMO_THEME = make_zh_theme("示例公司")


def build(output_path: str = "output/demo_chinese.pptx") -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    b = PresentationBuilder(theme=ZH_DEMO_THEME, default_section_marker="出海战略")

    # 1. 封面
    b.add("cover_slide",
          title="新能源汽车品牌出海战略回顾",
          subtitle="欧洲与东南亚市场进入评估",
          client="管理层汇报", date="2026 年第四季度")

    # 2. 核心结论
    b.add("dark_navy_summary",
          body="[核心结论]: 未来三年是品牌出海的窗口期，应优先布局欧洲高端市场，"
               "同时以东南亚为第二增长曲线。",
          eyebrow="出海战略回顾")

    # 3. 执行摘要
    b.add("executive_summary_takeaways",
          title="执行摘要",
          sections=[
              {"takeaway": "海外销量三年增长 4 倍，但利润率仍低于国内",
               "bullets": ["欧洲贡献 55% 海外营收", "物流与关税侵蚀 6 个百分点毛利"]},
              {"takeaway": "本地化生产是扭转利润率的关键",
               "bullets": ["匈牙利工厂 2027 年投产", "东南亚 CKD 组装降本 12%"]},
              {"takeaway": "品牌认知度仍是最大短板",
               "bullets": ["欧洲无提示认知度仅 18%", "需加大渠道与售后投入"]},
          ],
          final_conclusion="建议：批准 2027 年 30 亿元本地化投资方案。")

    # 4. KPI 仪表盘
    b.add("kpi_dashboard",
          title="2026 年海外业务核心指标",
          source="公司经营数据", footnote="",
          kpis=[
              {"label": "海外营收", "value": "286 亿", "delta": "同比 +42%", "delta_dir": "up"},
              {"label": "海外销量", "value": "21.5 万辆", "delta": "同比 +38%", "delta_dir": "up"},
              {"label": "海外毛利率", "value": "11.2%", "delta": "-1.5 个百分点", "delta_dir": "down"},
              {"label": "经销网点", "value": "640 家", "delta": "持平", "delta_dir": "flat"},
          ])

    # 5. 历史 + 预测柱状图
    b.add("column_historic_forecast",
          title="海外营收趋势：2021–2030 年",
          source="公司经营数据", footnote="",
          description="海外营收（亿元），2026 年起为预测",
          takeaway_header="关键结论",
          data_label="营收", data_unit="亿元",
          categories=[2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
          values=[35, 62, 118, 170, 201, 286, 360, 445, 530, 620],
          forecast_from_index=5,
          historic_growth="+56%", forecast_growth="+21%",
          takeaways=["预测期年均增长约 21%", "欧洲占比稳定在 50% 以上",
                     "东南亚 2028 年后成为第二增长极"])

    # 6. 三大趋势
    b.add("three_trends_numbered",
          title="影响出海的三大趋势",
          source="公司经营数据", footnote="",
          subtitle="未来五年将重塑行业格局",
          trends=[
              {"label": "贸易壁垒上升",
               "bullets": ["欧盟反补贴关税落地", "本地化率成为准入门槛"]},
              {"label": "价格战外溢",
               "bullets": ["国内价格竞争延伸至海外", "入门车型利润被压缩"]},
              {"label": "软件定义汽车",
               "bullets": ["智能座舱成为差异化核心", "OTA 能力影响复购"]},
          ])

    # 7. 优先级矩阵
    b.add("prioritization_matrix",
          title="出海举措优先级矩阵",
          description="按见效时间 × 影响程度排序",
          legend=("按计划推进", "存在风险", "建议暂缓"),
          source="公司战略部", footnote="",
          items=[
              {"name": "匈牙利工厂", "x_band": 2, "y_band": 0, "ox": 0.6, "oy": 0.5, "status": "green"},
              {"name": "欧洲直营店", "x_band": 1, "y_band": 0, "ox": 0.4, "oy": 0.5, "status": "green"},
              {"name": "泰国 CKD", "x_band": 1, "y_band": 1, "ox": 0.5, "oy": 0.5, "status": "amber"},
              {"name": "售后网络", "x_band": 2, "y_band": 1, "ox": 0.5, "oy": 0.4, "status": "amber"},
              {"name": "南美试点", "x_band": 0, "y_band": 2, "ox": 0.5, "oy": 0.5, "status": "red"},
          ])

    # 8. 三阶段路线图
    b.add("phases_chevron_3",
          title="出海战略分三个阶段推进",
          source="公司经营数据", footnote="",
          phases=[
              {"label": "夯实欧洲", "timeframe": "2027",
               "deliverables": ["工厂投产", "认知度达 30%"],
               "people": ["欧洲事业部"]},
              {"label": "拓展东南亚", "timeframe": "2028",
               "deliverables": ["CKD 规模化", "新增 3 国"],
               "people": ["亚太事业部"]},
              {"label": "全球化运营", "timeframe": "2029+",
               "deliverables": ["海外营收占比 40%", "全球研发协同"],
               "people": ["集团总部"]},
          ])

    b.save(output_path)
    return output_path


if __name__ == "__main__":
    out = build()
    print(f"wrote {out}")
