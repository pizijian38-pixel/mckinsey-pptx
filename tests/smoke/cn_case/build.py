"""Smoke test 7 — Chinese strategy case (source mode): every analysis /
framework template added from the strategy-case decks (cycle,
positioning_scale, value_chain, business_model_canvas, strategic_triangle,
hub_spoke, evaluation_matrix, phase_grid, risk_heatmap), the section nav
bar, and default labels localised by make_theme(lang="zh")."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from mckinsey_pptx import PresentationBuilder, make_theme

NAV = ["情境分析", "方案评估", "落地计划"]


def build(out_dir: Path) -> Path:
    b = PresentationBuilder(theme=make_theme("北辰茶馆", lang="zh"), nav=NAV)
    N = dict(source="", footnote="")
    b.add("cover_slide", title="北辰茶馆", subtitle="战略分析", date="")

    b.add("cycle", nav="情境分析", title="门店规模驱动成本、产品与品牌三条飞轮",
          start="门店数量增加",
          paths=[[{"title": "采购规模扩大", "icon": "cart"}, "单杯成本下降"],
                 [{"title": "会员数据积累", "icon": "database"}, "新品命中率提升"],
                 [{"title": "品牌曝光增加", "icon": "megaphone"}, "品牌认知提升"]],
          end="营收增长", feedback="营收增长支持继续开店",
          conclusion="门店规模是持续成功的关键，一旦失去规模，飞轮就会停转", **N)

    b.add("positioning_scale", nav="情境分析", title="北辰在门店数量和会员体系上领先，客单价居中",
          players=[{"name": "北辰茶馆", "short": "北", "keywords": ["性价比高", "门店多", "会员体系完善"]},
                   {"name": "南山茶社", "short": "南", "keywords": ["品牌高端", "单店营收高"]},
                   {"name": "西岭茶饮", "short": "西", "keywords": ["价格最低", "扩张最快"]}],
          indicators=[{"name": "门店数量", "note": "门店越多，覆盖越广", "values": [3, 1, 2]},
                      {"name": "平均客单价", "note": "客单价越高，触达人群越窄", "values": [2, 3, 1]},
                      {"name": "会员体系", "note": "会员越多，复购越稳", "values": [3, 2, 1]}],
          scale=(1, 3), **N)

    b.add("value_chain", nav="情境分析", title="北辰自营研发与门店两个环节，外卖环节受平台议价",
          stages=[{"name": "原料采购", "bullets": ["茶叶与乳制品", "供应商分散，替代容易"]},
                  {"name": "产品研发", "own": True, "bullets": ["新品研发速度", "口味本地化"]},
                  {"name": "门店运营", "own": True, "bullets": ["选址能力", "标准化出品"]},
                  {"name": "外卖与配送", "bullets": ["依赖平台", "平台议价能力强"]}],
          own_label="北辰自营环节", body_label="关键成功要素", **N)

    b.add("business_model_canvas", nav="情境分析", title="北辰以平价好喝的社交茶饮，通过门店与外卖获得收入",
          partners=["茶园", "乳制品供应商", "外卖平台"], activities=["新品研发", "门店运营"],
          resources=["会员数据", "门店网络"], value_proposition=["平价、好喝、适合社交的茶饮空间"],
          relationships=["会员积分", "社群运营"], channels=["直营门店", "外卖平台", "小程序"],
          segments=["18–30 岁城市年轻人"], costs=["原料 **35%**", "租金 **25%**", "人工 **20%**"],
          revenue=["门店销售", "外卖销售"], **N)

    b.add("strategic_triangle", nav="情境分析", title="资源、业务与组织围绕同一个目标",
          goal="成为年轻人首选的平价茶饮品牌",
          resources=[{"title": "资源与能力", "bullets": ["会员数据", "选址能力", "快速研发"]}],
          business=[{"title": "价值主张", "bullets": ["平价好喝的茶饮与社交空间"]}],
          structure=[{"title": "结构与系统", "bullets": ["统一的门店管理系统", "标准化出品流程"]},
                     {"title": "人员", "bullets": ["门店店长培训体系"]}], **N)

    b.add("hub_spoke", nav="情境分析", title="茶饮体验由四个环节共同决定，短板决定整体",
          center="茶饮产品",
          spokes=[{"title": "茶叶原料", "note": "决定基础口感"},
                  {"title": "配方研发", "note": "决定差异化"},
                  {"title": "出品标准", "note": "决定稳定性"},
                  {"title": "门店体验", "note": "决定复购"}],
          side={"title": "任何一个环节短板都会拖累整体体验",
                "bullets": ["需要供应链合作", "需要人才培养"]}, **N)

    b.add("evaluation_matrix", nav="方案评估", title="方案一在市场规模和能力匹配上领先，推荐方案一",
          options=["方案一：零售渠道", "方案二：高端子品牌"],
          criteria=[{"group": "吸引力", "name": "市场规模", "weight": 40, "scores": [5, 3],
                     "notes": ["市场规模大", "高端市场容量有限"]},
                    {"group": "吸引力", "name": "竞争强度", "weight": 20, "scores": [2, 4],
                     "notes": ["与饮料巨头竞争激烈", "直接竞争少"]},
                    {"group": "可行性", "name": "能力匹配", "weight": 40, "scores": [4, 3],
                     "notes": ["可复用现有研发能力", "需要新的门店能力"]}],
          recommended=0, scale_note="1 = 差，5 = 好；加权总分由得分与权重计算", **N)

    b.add("phase_grid", nav="落地计划", title="先电商、后便利店，逐个进入零售渠道",
          stages=["阶段一：电商渠道", "阶段二：便利店渠道"],
          rows=[{"label": "合作伙伴", "cells": ["天猫、京东", "全家、罗森"]},
                {"label": "行动", "cells": ["开设官方旗舰店", "谈判上架，先一线城市"],
                 "kpi": "第一年零售营收 2000 万元"}],
          side={"items": [{"title": "先进入新渠道", "bullets": ["避开与巨头正面竞争"]},
                          {"title": "保持门店体验差异化", "bullets": ["减少分流"]}]}, **N)

    b.add("risk_heatmap", nav="落地计划", title="降价竞争是唯一的高风险，需以差异化口味应对",
          risks=[{"title": "饮料巨头降价竞争", "probability": "high", "impact": "high",
                  "mitigation": "聚焦差异化口味"},
                 {"title": "零售分流门店客流", "probability": "medium", "impact": "medium",
                  "mitigation": "门店专供产品"},
                 {"title": "供应链成本上升", "probability": "low", "impact": "medium",
                  "mitigation": "与茶园签订长期协议"}], **N)
    out = out_dir / "cn_case.pptx"
    b.save(str(out))
    return out


SOURCES = [HERE / "source.md"]
# weighted totals computed from the scorecard: 0.4*5+0.2*2+0.4*4, 0.4*3+0.2*4+0.4*3
DERIVED = {"4", "3.2", "100"}

if __name__ == "__main__":
    print(build(HERE))
