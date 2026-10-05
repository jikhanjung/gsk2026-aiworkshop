# 004. Colab 노트북 생성 · 검증 · README

- 날짜: 2026-10-06
- 상태: 완료

## 한 일

- `scripts/make_notebook.py` → `gsk2026_practice.ipynb` (셀 34개, nbformat 없이 JSON 직접 작성, 셀 id 부여).
  `docs/colab_guide.md`(002)에 맞춘 구성:
  - 준비 1 도우미 함수(`load_data`, `build`, `preview`, `download`) → 준비 2 데이터(방법 A 업로드 / 방법 B 드라이브 `DATA_PATH`)
    → Step 0 pandas → Step 1 f-string(`step1.html`) → Step 2~5(`%%writefile` 템플릿 셀 + build/preview 셀 + download 셀,
    결과 `out_step2.html` … `out_step5.html`) → 과제(안내서 §10 과 같은 목록).
  - 템플릿 셀은 `steps/*.html` 을 그대로 읽어 넣음(단일 진실 원천).
  - `build()`: 데이터 미로드 / `__DATA__` 없음 / 2번 이상일 때 한국어 오류.
  - `preview()`: 백그라운드 `http.server` + `serve_kernel_port_as_iframe`, `?v=시각` 으로 캐시 회피. Colab 밖이면 경로 출력.
- `scripts/smoke_test.js` — jsdom 렌더 스모크 테스트 31개 (step2~4, app: 필터, 검색 하이라이트, 북마크 저장, 겹침/비겹침,
  깨진 localStorage 값, 라우팅, 상세, 본문 검색 스니펫, 100건 제한, 불러오기 병합 등). 테스트 값도 데이터에서 고름.
- `scripts/check.py` — 빌드 → `node --check` → `</script>` 주입 데이터 → 노트북 JSON·파이썬 셀 문법·`%%writefile` == `steps/*.html`
  → (jsdom 있으면) 스모크 테스트.
- 노트북 코드 셀을 로컬에서 순서대로 실행(Colab 전용 셀은 `load_data` 로 대체)해 `out_step*.html` 이 `build.py` 결과와 같고
  스모크 테스트도 통과함을 확인.
- `README.md` — 구성, 데이터 스키마·규칙, 수업 전 준비, 3시간 진행 예시, 주의점, 개발·검증 방법.

## 핵심 발견

- `%%writefile` 셀 본문은 끝 줄바꿈이 없어서 결과 파일이 원본과 마지막 개행 하나 차이 — 동작에는 무관(검사는 rstrip 비교).
- 실제 Colab 에서의 `preview()`·`files.download()` 는 로컬에서 검증할 수 없음 → Colab 실행 확인은 남은 일.

## 다음

- Colab 에 올려 처음부터 끝까지 실행 확인 (미리보기 iframe, 다운로드, 드라이브 방법 B).
- GSK 2026 데이터로 교체 후 `python scripts/check.py`.
