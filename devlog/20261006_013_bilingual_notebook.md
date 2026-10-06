# 013. 모범 답안 노트북·템플릿 주석 한/영 병기

- 날짜: 2026-10-06
- 상태: 완료 (샘플 HTML 영어판은 다음 작업)

## 한 일

- `scripts/make_notebook.py`: `md(ko, en)` — 설명 셀은 한국어 다음 구분선과 "🇬🇧 English" 아래 영어. 제목은 "한국어 / English" 한 줄.
  코드 주석은 `# EN:` 줄 추가, docstring 두 언어, `print`·`build()` 오류 메시지 "한국어 / English".
- `steps/*.html` 4개: JS·CSS 설명 주석에 영어 병기 (줄 주석은 다음 줄 `// EN: …`, 줄 끝·CSS·구역 제목은 "한국어 / English").
  앱 화면 문구(버튼 등)는 한국어 그대로.
- 노트북 재생성, `check.py` 통과, 로컬에서 노트북 셀 전체 실행해 build 오류 메시지 확인.

## 다음

- `examples/vworld_map_sample.html` 영어판(`vworld_map_sample.en.html`).
