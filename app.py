import pandas as pd
import streamlit as st

from document_builder import build_admin_document, build_press_release
from yonhap_rss import fetch_all_news, load_sources, to_dicts


st.set_page_config(
    page_title="연합뉴스 RSS 과수화상병 문서화",
    page_icon="📰",
    layout="wide",
)

st.title("연합뉴스 RSS 과수화상병 뉴스 문서화 도구")
st.caption("RSS를 다시 가져오는 버튼을 눌러 최신 기사를 수집하고, 행정문서·보도자료 초안을 생성합니다.")

with st.sidebar:
    st.header("수집 설정")
    keyword_help = "현재 코드는 과수화상병, 과수 화상병, 화상병, 방제, 예찰, 보상 등 관련 키워드를 기준으로 필터링합니다."
    st.info(keyword_help)
    refresh = st.button("RSS 다시 가져오기", type="primary", use_container_width=True)

if "items" not in st.session_state or refresh:
    with st.spinner("연합뉴스 RSS를 수집하는 중입니다."):
        sources = load_sources()
        st.session_state["sources"] = sources
        st.session_state["items"] = fetch_all_news(sources)

items = st.session_state["items"]
sources = st.session_state.get("sources", [])

col1, col2, col3 = st.columns(3)
col1.metric("등록 RSS", len(sources))
col2.metric("관련 기사", len(items))
col3.metric("분류 주제", len(set(item.topic for item in items)) if items else 0)

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
                st.markdown(f"- [{item.title}]({item.link})")
                if item.summary:
                    st.caption(item.summary)
else:
    st.warning("현재 수집된 과수 화상병 관련 기사가 없습니다. RSS 주소 또는 키워드를 확인하세요.")

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
