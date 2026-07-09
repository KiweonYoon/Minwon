import json
import re
from typing import Any

from yonhap_rss import NewsItem, classify_topic


DEFAULT_MODEL = "gemini-2.5-flash"


def _extract_json_array(text: str) -> list[dict[str, Any]]:
    """Gemini 응답에서 JSON 배열만 안전하게 추출합니다."""
    if not text:
        return []

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", cleaned)
        if not match:
            return []
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return []

    if isinstance(data, dict):
        data = data.get("articles", [])
    if not isinstance(data, list):
        return []

    return [item for item in data if isinstance(item, dict)]


def _item_from_article(article: dict[str, Any]) -> NewsItem | None:
    title = str(article.get("title", "")).strip()
    link = str(article.get("link", article.get("url", ""))).strip()
    published = str(article.get("published", article.get("date", ""))).strip()
    summary = str(article.get("summary", article.get("description", ""))).strip()
    source = str(article.get("source", "Gemini 웹 검색")).strip() or "Gemini 웹 검색"

    if not title:
        return None

    return NewsItem(
        source=source,
        title=title,
        link=link,
        published=published,
        summary=summary,
        topic=classify_topic(title, summary),
    )


def search_news_with_gemini(
    api_key: str,
    query: str,
    limit: int = 10,
    model: str = DEFAULT_MODEL,
) -> list[NewsItem]:
    """Gemini API의 Google Search grounding 기능으로 관련 기사 후보를 검색합니다."""
    if not api_key.strip():
        raise ValueError("Gemini API 키가 필요합니다.")
    if not query.strip():
        raise ValueError("검색어가 필요합니다.")

    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError(
            "google-genai 패키지가 설치되어 있지 않습니다. `pip install -r requirements.txt`를 다시 실행하세요."
        ) from exc

    client = genai.Client(api_key=api_key.strip())
    prompt = f"""
다음 조건에 맞는 한국어 뉴스 기사 후보를 웹에서 찾아 JSON 배열로만 반환해줘.

검색어: {query.strip()}
우선순위:
1. 연합뉴스(yna.co.kr) 기사
2. 농촌진흥청, 지자체, 농업기술센터 등 공신력 있는 출처
3. 최근 기사

반환 개수: 최대 {limit}개
반환 형식:
[
  {{
    "title": "기사 제목",
    "source": "언론사 또는 기관명",
    "published": "게시일 또는 보도시각, 알 수 없으면 빈 문자열",
    "summary": "핵심 내용 1~2문장",
    "link": "원문 URL"
  }}
]

주의사항:
- JSON 외의 설명 문장은 쓰지 마.
- URL이 확인되지 않는 항목은 제외해.
- 검색어와 직접 관련 없는 기사는 제외해.
""".strip()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.2,
        ),
    )

    articles = _extract_json_array(getattr(response, "text", ""))
    items: list[NewsItem] = []
    seen: set[str] = set()

    for article in articles:
        item = _item_from_article(article)
        if not item:
            continue
        key = item.link or item.title
        if key in seen:
            continue
        seen.add(key)
        items.append(item)

    return items
