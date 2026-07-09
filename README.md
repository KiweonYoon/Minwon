# 연합뉴스 RSS 과수화상병 뉴스 문서화 도구

연합뉴스 RSS를 수집해 `과수 화상병` 관련 뉴스를 자동으로 모으고, Gemini API 키가 있을 경우 웹 검색으로 관련 기사 후보를 추가 수집한 뒤 주제별로 분류하여 행정문서 초안과 보도자료 초안을 생성하는 Streamlit 웹앱입니다.

## 주요 기능

- 연합뉴스 RSS 피드 수집
- 과수 화상병 관련 기사 필터링
- Gemini API 키 입력 시 웹 검색 기능 활성화
- Gemini Google Search grounding 기반 관련 기사 후보 검색
- RSS 기사와 Gemini 검색 기사 중복 제거
- 주제별 자동 분류
  - 발생·확산 현황
  - 방제·예찰
  - 농가 지원·보상
  - 지자체·기관 대응
  - 기타
- 화면에서 새로고침 버튼으로 최신 RSS 재수집
- 표준 행정문서 초안 생성
- 보도자료 초안 생성
- Markdown 파일 다운로드

## 설치 방법

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux에서는 다음처럼 가상환경을 활성화합니다.

```bash
source .venv/bin/activate
```

## 실행 방법

```bash
streamlit run app.py
```

실행 후 브라우저에서 표시되는 주소로 접속하면 됩니다.

## Gemini 검색 사용 방법

1. 앱 왼쪽 사이드바의 `Gemini API 키` 칸에 본인의 Gemini API 키를 입력합니다.
2. API 키가 입력되면 `Gemini로 관련 기사 검색` 버튼이 활성화됩니다.
3. 검색어를 입력한 뒤 버튼을 누르면 Gemini 웹 검색 결과가 기존 RSS 결과와 합쳐집니다.
4. 입력한 API 키는 Streamlit 세션에서만 사용되며 파일에 저장하지 않습니다.

## RSS 목록 수정

RSS 주소는 `rss_sources.json` 파일에서 수정할 수 있습니다.

```json
[
  {
    "name": "연합뉴스 최신뉴스",
    "url": "https://www.yna.co.kr/rss/news.xml"
  }
]
```

## 출력물

웹 화면에서 다음 문서를 생성할 수 있습니다.

- `행정문서_초안.md`
- `보도자료_초안.md`

## 주의사항

- 연합뉴스 RSS 주소는 사이트 정책에 따라 변경될 수 있습니다.
- Gemini 검색 결과는 AI가 웹 검색을 바탕으로 구성한 기사 후보이므로, 행정문서나 보도자료로 사용하기 전 원문 링크를 반드시 확인하세요.
- API 키는 코드에 직접 넣지 말고 화면 입력칸 또는 별도 비밀 관리 방식을 사용하세요.
