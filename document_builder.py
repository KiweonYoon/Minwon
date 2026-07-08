from collections import defaultdict
from datetime import datetime
from typing import Iterable

from yonhap_rss import NewsItem


def group_by_topic(items: Iterable[NewsItem]) -> dict[str, list[NewsItem]]:
    grouped: dict[str, list[NewsItem]] = defaultdict(list)
    for item in items:
        grouped[item.topic].append(item)
    return dict(grouped)


def build_admin_document(items: list[NewsItem]) -> str:
    today = datetime.now().strftime("%Y년 %m월 %d일")
    grouped = group_by_topic(items)

    lines: list[str] = []
    lines.append("# 과수 화상병 관련 언론동향 보고")
    lines.append("")
    lines.append(f"- 작성일: {today}")
    lines.append("- 수집대상: 연합뉴스 RSS")
    lines.append("- 검색주제: 과수 화상병")
    lines.append("")
    lines.append("## 1. 수집 개요")
    lines.append("")
    lines.append(f"연합뉴스 RSS에서 과수 화상병 관련 기사를 수집한 결과 총 {len(items)}건이 확인되었습니다.")
    lines.append("")
    lines.append("## 2. 주제별 주요 내용")
    lines.append("")

    if not items:
        lines.append("현재 수집된 관련 기사가 없습니다.")
    else:
        for topic, topic_items in grouped.items():
            lines.append(f"### {topic}")
            lines.append("")
            for idx, item in enumerate(topic_items, start=1):
                lines.append(f"{idx}. [{item.title}]({item.link})")
                if item.published:
                    lines.append(f"   - 보도시각: {item.published}")
                if item.summary:
                    lines.append(f"   - 요약: {item.summary}")
                lines.append("")

    lines.append("## 3. 검토 의견")
    lines.append("")
    lines.append("- 발생 지역, 농가 피해 규모, 방제 조치, 농가 지원 사항을 중심으로 후속 확인이 필요합니다.")
    lines.append("- 동일 사안에 대한 반복 보도 여부를 확인하고, 지자체·관계기관 발표자료와 교차검증해야 합니다.")
    lines.append("")
    lines.append("## 4. 향후 조치")
    lines.append("")
    lines.append("- 관련 부서 공유")
    lines.append("- 추가 보도 모니터링")
    lines.append("- 필요 시 보도자료 또는 설명자료 작성")
    lines.append("")

    return "\n".join(lines)


def build_press_release(items: list[NewsItem]) -> str:
    today = datetime.now().strftime("%Y년 %m월 %d일")
    grouped = group_by_topic(items)

    lines: list[str] = []
    lines.append("# 보도자료 초안")
    lines.append("")
    lines.append(f"배포일: {today}")
    lines.append("")
    lines.append("## 제목")
    lines.append("")
    lines.append("과수 화상병 확산 방지를 위한 예찰·방제 대응 강화")
    lines.append("")
    lines.append("## 본문")
    lines.append("")
    lines.append("농업 관련 기관은 과수 화상병 확산 방지를 위해 발생 동향을 면밀히 모니터링하고, 농가 예찰과 방제 안내를 강화하고 있습니다.")
    lines.append("")

    if items:
        lines.append("최근 언론 보도에서 확인된 주요 내용은 다음과 같습니다.")
        lines.append("")
        for topic, topic_items in grouped.items():
            lines.append(f"### {topic}")
            for item in topic_items[:5]:
                lines.append(f"- {item.title}")
            lines.append("")
    else:
        lines.append("현재 RSS에서 확인된 관련 보도는 없습니다.")
        lines.append("")

    lines.append("관계 기관은 농가 피해 최소화를 위해 의심 증상 신고, 현장 예찰, 방제수칙 홍보를 지속 추진할 예정입니다.")
    lines.append("")
    lines.append("## 문의")
    lines.append("")
    lines.append("- 담당부서: 농업기술센터")
    lines.append("- 담당자: ○○○")
    lines.append("- 연락처: 000-0000-0000")
    lines.append("")

    return "\n".join(lines)
