import pandas as pd
import streamlit as st

from document_builder import build_admin_document, build_press_release
from gemini_news_search import search_news_with_gemini
from yonhap_rss import NewsItem, fetch_all_news, load_sources, to_dicts


def merge_news_items(*groups: list[NewsItem]) -> list[NewsItem]:
    merged: list[NewsItem] = []
    seen: set[str] = set()

    for group in groups:
        for item in group:
            key = item.link or item.title
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)

    return merged


st.set_page_config(
    page_title="연합뉴스 RSS 과수화상병 문서화",
    page_icon="📰",
    layout="wide",
)

st.title("연합뉴스 RSS 과수화상병 뉴스 문서화 도구")
st.caption(
    "RSS를 다시 가져오거나 Gemini API 키를 입력해 웹 검색을 실행한 뒤, "
    "행정문서·보도자료 초안을 생성합니다."
)

with st.sidebar:
    st.header("수집 설정")
    keyword_help = (
        "RSS 수집은 과수화상병, 과수 화상병, 화상병, 방제, 예찰, 보상 등 "
        "관련 키워드를 기준으로 필터링합니다."
    )
    st.info(keyword_help)

    refresh = st.button("RSS 다시 가져오기", type="primary", use_container_width=True)

    st.divider()
    st.header("Gemini 검색 설정")
    gemini_api_key = st.text_input(
        "Gemini API 키",
        type="password",
        help="입력한 API 키는 현재 실행 중인 Streamlit 세션에서만 사용되며 파일에 저장하지 않습니다.",
    )
    gemini_enabled = bool(gemini_api_key.strip())

    if gemini_enabled:
        st.success("Gemini 검색 기능이 활성화되었습니다.")
    else:
        st.warning("Gemini API 키를 입력하면 웹 검색 기능이 활성화됩니다.")

    search_query = st.text_input("검색어", value="과수 화상병 연합뉴스")
    search_limit = st.slider("검색 결과 수", min_value=3, max_value=20, value=10)
    search_with_gemini = st.button(
        "Gemini로 관련 기사 검색",
        disabled=not gemini_enabled,
        use_container_width=True,
    )

if "rss_items" not in st.session_state or refresh:
    with st.spinner("연합뉴스 RSS를 수집하는 중입니다."):
        sources = load_sources()
        st.session_state["sources"] = sources
        st.session_state["rss_items"] = fetch_all_news(sources)

if "gemini_items" not in st.session_state:
    st.session_state["gemini_items"] = []

if search_with_gemini:
    with st.spinner("Gemini로 관련 기사를 검색하는 중입니다."):
        try:
            st.session_state["gemini_items"] = search_news_with_gemini(
                api_key=gemini_api_key,
                query=search_query,
                limit=search_limit,
            )
        except Exception as exc:
            st.error(f"Gemini 검색 중 오류가 발생했습니다: {exc}")

rss_items = st.session_state.get("rss_items", [])
gemini_items = st.session_state.get("gemini_items", [])
items = merge_news_items(rss_items, gemini_items)
sources = st.session_state.get("sources", [])

col1, col2, col3, col4 = st.columns(4)
col1.metric("등록 RSS", len(sources))
col2.metric("RSS 관련 기사", len(rss_items))
col3.metric("Gemini 검색 기사", len(gemini_items))
col4.metric("전체 기사", len(items))

st.subheader("수집 결과")

if items:
    df = pd.DataFrame(to_dicts(items))
    st.dataframe(
        df[["topic", "published", "title", "source", "link"]],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("주제별 기사")
    for topic in sorted(df["topic"].unique()):
        with st.expander(f"{topic} ({len(df[df['topic'] == topic])}건)", expanded=True):
            for item in [x for x in items if x.topic == topic]:
                if item.link:
                    st.markdown(f"- [{item.title}]({item.link})")
                else:
                    st.markdown(f"- {item.title}")
                if item.summary:
                    st.caption(item.summary)
else:
    st.warning("현재 수집된 관련 기사가 없습니다. RSS 주소, 키워드 또는 Gemini API 키를 확인하세요.")

st.divider()
st.subheader("문서 생성")

admin_doc = build_admin_document(items)
press_release = build_press_release(items)

tab1, tab2 = st.tabs(["행정문서 초안", "보도자료 초안"])

with tab1:
    st.markdown(admin_doc)
    st.download_button(
        "행정문서 초안 다운로드",
        data=admin_doc.encode("utf-8"),
        file_name="행정문서_초안.md",
        mime="text/markdown",
        use_container_width=True,
    )

with tab2:
    st.markdown(press_release)
    st.download_button(
        "보도자료 초안 다운로드",
        data=press_release.encode("utf-8"),
        file_name="보도자료_초안.md",
        mime="text/markdown",
        use_container_width=True,
    )
