# gsk2026 — 학회 프로그램 로컬 웹앱 만들기 실습

## 목적
학생 실습 자료. **미리 만든 학회 JSON** 을 주고, 학생들이 **Google Colab** 에서
파이썬으로 JSON 을 HTML 템플릿에 넣어 **단일 HTML 파일**을 만들고 → `files.download()` 로
내려받아 → 자기 PC 브라우저에서 열어 쓰는 과정을 단계별로 실습한다.
(PDF 파싱은 실습 범위 밖. 데이터는 strati2026 프로젝트 산출물을 재가공해 사용.)

## 설계 결정 (사용자와 합의됨)
- 결과물은 **HTML 파일 하나**. 데이터는 `<script>const DATA = __DATA__;</script>` 자리에
  파이썬이 JSON 을 넣는다 (`file://` 에선 fetch 가 막히므로 외부 data.js/JSON 로드 금지).
  넣을 때 `</` → `<\/` 이스케이프.
- 바닐라 JS, 외부 라이브러리 없음. 북마크는 localStorage (try/catch 로 감쌀 것).
- Colab 에서 미리보기: 백그라운드 `python -m http.server` + `google.colab.output.serve_kernel_port_as_iframe`.
  Colab 밖에서 실행하면 경로만 출력하는 fallback.
- 다운로드: `google.colab.files.download`. 크롬 권장, 막히면 드라이브 저장 안내.
- 노트북 설명·주석은 한국어. 대상은 프로그래밍 초보~중급 학생.
- PC 브라우저 기준 (폰에서 내려받은 HTML 은 JS/localStorage 가 불안정).

## 데이터 (git 미추적)
- `data/` 는 `.gitignore` 대상 — 초록 본문 등 재배포 불가 데이터. 스크립트로 다시 만든다.
- **지금 `data/conference.json` 은 임시 데이터**(strati2026 산출물 재가공, `scripts/prepare_data.py`).
  GSK 2026(대한지질학회) 프로그램이 나오면 그 PDF 를 파싱해 **같은 스키마**로 다시 만든다.
  → 템플릿·노트북은 특정 학회(STRATI)에 묶이지 않게 `DATA.meta` 와 스키마 필드만 쓸 것.
  (학회명·장소·날짜 하드코딩 금지, 장소/세션 목록도 데이터에서 뽑기)

## 문서 규칙 (다른 프로젝트와 동일)
- **계획 문서**: `devlog/YYYYMMDD_P{nn}_{title}.md` (P01, P02, ...)
- **작업 결과**: `devlog/YYYYMMDD_{nnn}_{title}.md` (001, 002, ...) — 작업 단위마다 하나.
  형식: `# NNN. 제목` / `- 날짜:` / `- 상태:` / `## 한 일` / `## 핵심 발견`(있으면) / `## 다음`.
- `devlog/README.md` — devlog 색인. 새 devlog 를 쓰면 라운드 표에 한 줄 추가.
- `HANDOFF.md` — 현재 작업 상태와 다음 할 일 (세션이 바뀌어도 이어받을 수 있게 작업 끝날 때 갱신).
- `README.md` — 프로젝트 소개와 사용법 (강사용 수업 안내 포함).
- 이 파일(CLAUDE.md)에는 설계 결정과 규칙만 둔다. 진행 상황은 HANDOFF.md 로.

## 현재 상태
(자세한 진행 상황·다음 할 일은 `HANDOFF.md`)
- [x] `scripts/prepare_data.py` → `data/conference.json` (임시본, 시간은 `HH:MM` 두 자리로 정규화)
- [x] `steps/step2_list.html`, `step3_filter.html`, `step4_bookmark.html`, `app.html`(Step 5 완성본)
- [x] `build.py` — `python build.py steps/app.html data/conference.json dist/conference.html`
- [x] `scripts/make_notebook.py` → `gsk2026_practice.ipynb` (`docs/colab_guide.md` 와 단계명·파일명 일치).
      템플릿 원본은 steps/*.html — 고치면 노트북 재생성.
- [x] 검증 `scripts/check.py` (+ `scripts/smoke_test.js`, jsdom 은 NODE_PATH 로)
- [x] `README.md` (강사용)
- [ ] Colab 실제 실행 확인, GSK 2026 데이터로 교체
