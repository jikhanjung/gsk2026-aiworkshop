# P01. Colab 학회 웹앱 만들기 실습 계획

- 날짜: 2026-10-06
- 상태: 진행 중

## 배경

strati2026 프로젝트에서 학회 핸드북·초록집 PDF를 파싱해 Django 웹앱(발표 탐색 → 북마크 → 내 타임테이블)을
만들었다. 같은 결과물을 **서버 없이 HTML 파일 하나**로 만드는 과정을 학생 실습으로 구성한다.

## 범위 결정

- **PDF 파싱은 실습에서 제외.** 학회마다 PDF 형식이 달라(strati2026도 -29 시프트 인코딩, 상첨자 소속번호 등
  특수 처리 필요) 수업 시간 안에 다루기 어렵다. 파싱된 JSON 을 미리 만들어 나눠 준다.
- 실습의 초점은 **JSON → 웹앱**: 데이터를 HTML 에 넣고, JS 로 그리고, 상태·이벤트·localStorage 를 다루는 것.

## 실습 흐름

1. Colab 에서 JSON 을 불러와 살펴본다 (pandas).
2. 파이썬에서 HTML 템플릿의 `__DATA__` 자리에 JSON 을 넣어 **단일 HTML 파일**을 만든다.
3. Colab 안에서 미리 본 뒤(`http.server` + `serve_kernel_port_as_iframe`) `files.download()` 로 내려받는다.
4. 자기 PC 브라우저에서 열어 북마크·타임테이블을 직접 써 본다.

## 단계 구성

| 단계 | 파일 | 배우는 것 |
|------|------|-----------|
| Step 1 | (노트북 안 파이썬 코드) | f-string 만으로 정적 HTML 생성 — 데이터가 HTML 이 되는 원리 |
| Step 2 | `steps/step2_list.html` | JS 로 배열 → HTML 렌더, 이스케이프 |
| Step 3 | `steps/step3_filter.html` | state + render() 패턴, 날짜·장소 칩, 검색·하이라이트 |
| Step 4 | `steps/step4_bookmark.html` | localStorage 북마크, 내 일정(시간순·겹침 표시) |
| 완성본 | `steps/app.html` | 탭 구성, 상세 화면(hash 라우팅), 초록 검색, 북마크 내보내기·불러오기 |

## 설계 원칙

- `file://` 에서는 `fetch()` 가 막히므로 데이터를 HTML 안에 넣는다. 외부 파일 의존 없음(data.js 분리 금지 —
  학생들이 두 파일을 같은 폴더에 두지 않아 깨지는 일을 막기 위해).
- 바닐라 JS, 라이브러리 없음. localStorage 접근은 try/catch.
- 실습 환경은 PC 크롬 기준. 휴대폰에서 내려받은 HTML 은 JS·localStorage 가 불안정하다.

## 주의

- 실습 데이터(초록 본문 포함)는 수업 내부용. 재배포 금지.
