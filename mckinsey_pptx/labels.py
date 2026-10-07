"""Default labels in the deck's language.

Templates keep English defaults in their signatures ("Key insight",
"Weighted total", ...). Every place that draws a label passes it through
`loc(theme, text)`: when the theme was built with make_theme(lang="zh" |
"ko" | "ja") and the text is a known default, the translation is drawn.
Labels the caller passes in (anything not in the table) are drawn as given.
"""
from __future__ import annotations

_T = {
    # bars, panels, headings
    "Key insight": ("关键洞察", "핵심 인사이트", "重要な示唆"),
    "Bottom line": ("结论", "결론", "結論"),
    "Verdict": ("评估结论", "판단", "評価"),
    "Implication": ("启示", "시사점", "示唆"),
    "Preliminary view": ("初步判断", "예비 판단", "暫定見解"),
    "Decision needed": ("待决策事项", "의사결정 필요", "要意思決定"),
    "What drives the result": ("结果的驱动因素", "결과를 좌우하는 요인", "結果を左右する要因"),
    "What it takes": ("所需条件", "필요 조건", "必要条件"),
    "Advantages": ("优势", "장점", "メリット"),
    "Disadvantages": ("劣势", "단점", "デメリット"),
    "Pros": ("优点", "장점", "長所"),
    "Cons": ("缺点", "단점", "短所"),
    "Feasibility": ("可行性", "실행 가능성", "実現可能性"),
    "Mitigation": ("应对措施", "대응 방안", "対応策"),
    "owner": ("负责人", "담당", "担当"),
    "Recommended": ("推荐", "추천", "推奨"),
    # evaluation tables
    "Criterion": ("评估标准", "평가 기준", "評価基準"),
    "Criteria": ("评估标准", "평가 기준", "評価基準"),
    "Weight": ("权重", "가중치", "ウェイト"),
    "Weighted total": ("加权总分", "가중 합계", "加重合計"),
    "Total": ("总分", "합계", "合計"),
    "Score": ("得分", "점수", "スコア"),
    "Average": ("平均分", "평균", "平均"),
    "Dimension": ("维度", "차원", "観点"),
    "Rationale": ("理由", "근거", "根拠"),
    "high": ("高", "높음", "高"), "medium": ("中", "중간", "中"),
    "low": ("低", "낮음", "低"), "critical": ("严重", "심각", "重大"),
    "High": ("高", "높음", "高"), "Medium": ("中", "중간", "中"),
    "Low": ("低", "낮음", "低"), "Critical": ("严重", "심각", "重大"),
    # scorecard / assessment
    "Metric": ("指标", "지표", "指標"),
    "Target": ("目标", "목표", "目標"),
    "Actual": ("实际", "실적", "実績"),
    "Status": ("状态", "상태", "状況"),
    "Comment": ("备注", "비고", "コメント"),
    "On track": ("正常", "정상", "順調"),
    "Key Performance Indicators": ("关键绩效指标", "핵심 성과 지표", "重要業績評価指標"),
    "Category": ("类别", "구분", "カテゴリー"),
    "Deliverables": ("交付成果", "산출물", "成果物"),
    "People": ("人员", "인력", "体制"),
    "Outcomes": ("成果", "성과", "成果"),
    "Week": ("周", "주", "週"),
    "Area": ("领域", "영역", "領域"),
    "Description": ("说明", "설명", "説明"),
    "TIME TO IMPACT": ("见效时间", "효과 발현 시점", "効果発現までの期間"),
    "LEVEL OF IMPACT": ("影响程度", "영향도", "影響度"),
    "At risk": ("有风险", "위험", "要注意"),
    "Off track": ("滞后", "지연", "遅延"),
    # SWOT
    "Strengths": ("优势", "강점", "強み"),
    "Weaknesses": ("劣势", "약점", "弱み"),
    "Opportunities": ("机会", "기회", "機会"),
    "Threats": ("威胁", "위협", "脅威"),
    # logic templates
    "Drivers": ("驱动因素", "동인", "要因"),
    "Possible results": ("可能后果", "예상 결과", "想定される結果"),
    "Key threat": ("核心威胁", "핵심 위협", "主要な脅威"),
    "Strategic challenge": ("战略挑战", "전략 과제", "戦略課題"),
    "Ways to address it": ("应对方向", "해결 방향", "対応の方向性"),
    "Situation": ("情境", "상황", "現状"),
    "Key question": ("关键问题", "핵심 질문", "主要論点"),
    "Options": ("备选方案", "대안", "選択肢"),
    "Recommendation": ("建议", "권고안", "提言"),
    "Option": ("方案", "대안", "案"),
    "Current situation": ("现状", "현황", "現状"),
    "Impact on us": ("对我们的影响", "우리에 대한 영향", "当社への影響"),
    # risk heat map / scales / canvases
    "Probability": ("发生概率", "발생 가능성", "発生確率"),
    "Impact": ("影响程度", "영향도", "影響度"),
    "Risk": ("风险", "리스크", "リスク"),
    "Risks and mitigation": ("风险与应对", "리스크 및 대응", "リスクと対応"),
    "KPI": ("KPI", "KPI", "KPI"),
    "Risk mapping": ("风险地图", "리스크 맵", "リスクマップ"),
    "Mitigations": ("应对措施", "대응 방안", "対応策"),
    "Indicator": ("指标", "지표", "指標"),
    "What it means": ("含义", "의미", "意味"),
    "Comparison": ("对比", "비교", "比較"),
    "Players": ("主要玩家", "주요 플레이어", "主要プレイヤー"),
    "Key success factors": ("关键成功要素", "핵심 성공 요인", "主要成功要因"),
    "Key partners": ("关键合作伙伴", "핵심 파트너", "主要パートナー"),
    "Key activities": ("关键业务", "핵심 활동", "主要活動"),
    "Key resources": ("核心资源", "핵심 자원", "主要リソース"),
    "Value proposition": ("价值主张", "가치 제안", "価値提案"),
    "Customer relationships": ("客户关系", "고객 관계", "顧客との関係"),
    "Channels": ("渠道", "채널", "チャネル"),
    "Customer segments": ("客户细分", "고객 세그먼트", "顧客セグメント"),
    "Cost structure": ("成本结构", "비용 구조", "コスト構造"),
    "Revenue streams": ("收入来源", "수익원", "収益の流れ"),
    "Goals": ("目标", "목표", "目標"),
    "Resources & capabilities": ("资源与能力", "자원과 역량", "資源と能力"),
    "Business & value proposition": ("业务与价值主张", "사업과 가치 제안", "事業と価値提案"),
    "Structure, systems & people": ("结构、系统与人员", "구조·시스템·인력", "組織・システム・人材"),
}
_IDX = {"zh": 0, "ko": 1, "ja": 2}


def loc(theme, text):
    """`text` in the theme's language if it is a known default label."""
    if text is None:
        return None
    i = _IDX.get(getattr(theme, "lang", "en"))
    if i is None:
        return text
    hit = _T.get(str(text))
    return hit[i] if hit else text


def is_cjk_theme(theme) -> bool:
    return getattr(theme, "lang", "en") in _IDX


def english_defaults():
    """Default English labels (for the checker)."""
    return set(_T) - {"KPI", "owner", "high", "medium", "low", "critical"}
