# 연합뉴스 RSS 과수화상병 뉴스 문서화 도구

연합뉴스 RSS를 수집해 `과수 화상병` 관련 뉴스를 자동으로 모으고, 주제별로 분류한 뒤 행정문서 초안과 보도자료 초안을 생성하는 Streamlit 웹앱입니다.

## 주요 기능

- 연합뉴스 RSS 피드 수집
- 과수 화상병 관련 기사 필터링
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

## GitHub 업로드

```bash
git init
git branch -M main
git add .
git commit -m "Initial commit: add Yonhap RSS document generator"
git remote add origin https://github.com/KiweonYoon/Minwon.git
git push -u origin main
```

이미 remote가 등록되어 있으면 아래처럼 실행하세요.

```bash
git remote set-url origin https://github.com/KiweonYoon/Minwon.git
git push -u origin main
```

## 주의사항

연합뉴스 RSS 주소는 사이트 정책에 따라 변경될 수 있습니다. 실행 중 RSS 수집이 되지 않으면 `rss_sources.json`의 주소를 최신 주소로 교체하세요.
