# gsk2026 — 학회 프로그램 로컬 웹앱 만들기 실습

## 목적
GSK 2026 AI 워크숍 학생 실습 자료 (GitHub: `jikhanjung/gsk2026-aiworkshop`, public).
**AI 활용 수업**: 학생은 빈 Colab 노트북에서 **Gemini 에게 프롬프트를 입력하며** 미리 만든 학회 JSON 으로
**단일 HTML 파일** 학회 시간표 앱을 만들고 → 내려받아 → 자기 PC 브라우저에서 쓴다.
- 학생용: `docs/gemini_practice_guide.md` (완성 기준 9개·프롬프트 예시·Gemini 실수 패턴). 강사용: `docs/instructor_guide.md`.
- 이 저장소의 템플릿·노트북(`gsk2026_practice.ipynb`)은 **모범 답안** — 수업 마지막에 공개해 비교용으로 쓴다
  (`docs/reference_notebook_guide.md`). 노트북을 처음부터 주지 않는다.
(PDF 파싱은 실습 범위 밖 — 강사 준비 작업. 데이터는 대한지질학회 프로그램북 PDF 를 파싱해 사용.)

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
- **지금 `data/conference.json` 은 2025 추계학술대회 프로그램북**(`data/src/gsk2025_program_book.pdf`)을
  `scripts/parse_program_book.py`(pymupdf)로 파싱한 것. 프로그램북엔 초록 본문이 없어 abstract/keywords/affiliations 는 빈 값,
  포스터는 일정 없는 abstracts 로 들어간다. (초록집 PDF 는 회원 로그인 필요)
  (`scripts/prepare_data.py` 는 이전 임시 데이터(strati2026) 변환기 — 참고용)
  GSK 2026 프로그램북이 나오면(10월 중순 예상) 같은 파서로 **같은 스키마**로 다시 만든다.
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
- [x] `scripts/parse_program_book.py` → `data/conference.json` (2025 프로그램북: 구두 382, 포스터 229, 세션 38)
- [x] `steps/step2_list.html`, `step3_filter.html`, `step4_bookmark.html`, `app.html`(Step 5 완성본)
- [x] `build.py` — `python build.py steps/app.html data/conference.json dist/conference.html`
- [x] `scripts/make_notebook.py` → `gsk2026_practice.ipynb` (`docs/reference_notebook_guide.md` 와 단계명·파일명 일치).
      템플릿 원본은 steps/*.html — 고치면 노트북 재생성.
- [x] 검증 `scripts/check.py` (+ `scripts/smoke_test.js`, jsdom 은 NODE_PATH 로)
- [x] `README.md` (강사용)
- [ ] Colab 실제 실행 확인, GSK 2026 데이터로 교체
