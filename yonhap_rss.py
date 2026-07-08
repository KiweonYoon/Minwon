import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List

import feedparser


@dataclass
class NewsItem:
    source: str
    title: str
    link: str
    published: str
    summary: str
    topic: str = "기타"


KEYWORDS = [
    "과수화상병",
    "과수 화상병",
    "화상병",
    "사과",
    "배",
    "농가",
    "방제",
    "예찰",
    "매몰",
    "폐원",
    "보상",
]


TOPIC_RULES = {
    "발생·확산 현황": ["발생", "확산", "확진", "감염", "농가", "면적", "지역"],
    "방제·예찰": ["방제", "예찰", "소독", "검사", "차단", "방역", "매몰"],
    "농가 지원·보상": ["지원", "보상", "손실", "피해", "생계", "자금"],
    "지자체·기관 대응": ["농촌진흥청", "농진청", "도청", "시청", "군청", "농업기술센터", "지자체"],
}


def load_sources(path: str = "rss_sources.json") -> list[dict]:
    source_path = Path(path)
    if not source_path.exists():
        return [{"name": "연합뉴스 최신뉴스", "url": "https://www.yna.co.kr/rss/news.xml"}]
    return json.loads(source_path.read_text(encoding="utf-8"))


def classify_topic(title: str, summary: str) -> str:
    text = f"{title} {summary}"
    for topic, words in TOPIC_RULES.items():
        if any(word in text for word in words):
            return topic
    return "기타"


def is_fire_blight_related(title: str, summary: str) -> bool:
    text = f"{title} {summary}"
    return any(keyword in text for keyword in KEYWORDS)


def fetch_feed(source: dict) -> list[NewsItem]:
    parsed = feedparser.parse(source["url"])
    items: list[NewsItem] = []

    for entry in parsed.entries:
        title = getattr(entry, "title", "").strip()
        link = getattr(entry, "link", "").strip()
        published = getattr(entry, "published", getattr(entry, "updated", "")).strip()
        summary = getattr(entry, "summary", "").strip()

        if not title:
            continue

        if is_fire_blight_related(title, summary):
            items.append(
                NewsItem(
                    source=source.get("name", ""),
                    title=title,
                    link=link,
                    published=published,
                    summary=summary,
                    topic=classify_topic(title, summary),
                )
            )

    return items


def fetch_all_news(sources: Iterable[dict]) -> list[NewsItem]:
    merged: list[NewsItem] = []
    seen_links: set[str] = set()

    for source in sources:
        for item in fetch_feed(source):
            key = item.link or item.title
            if key in seen_links:
                continue
            seen_links.add(key)
            merged.append(item)

    return merged


def to_dicts(items: list[NewsItem]) -> list[dict]:
    return [asdict(item) for item in items]
