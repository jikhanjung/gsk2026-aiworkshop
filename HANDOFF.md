# HANDOFF

- 갱신: 2026-10-06 (003·004 반영)

## 현재 상태

- 실습 자료 1차 완성 (devlog 003, 004). CLAUDE.md 의 작업 1~6 완료.
  - 템플릿 `steps/step2_list` · `step3_filter` · `step4_bookmark` · `app`(Step 5 완성본)
  - `build.py`, `scripts/make_notebook.py` → `gsk2026_practice.ipynb` (docs/reference_notebook_guide.md 와 단계명·파일명 일치)
  - 검증 `python scripts/check.py` 전부 통과 (jsdom 스모크 테스트 31개 포함, `NODE_PATH` 필요)
  - `README.md` 강사용 안내
- **데이터를 2025 GSK 추계학술대회 프로그램북으로 교체** (devlog 005): `scripts/parse_program_book.py` →
  구두 382 / 포스터 229 / 세션 38. 초록 본문 없음(초록집은 회원 로그인 필요). 원본 PDF 는 `data/src/`(git 미추적).

## 수업 방식 변경 (devlog 006)

- **AI 활용 수업**: 학생은 Colab Gemini 에게 프롬프트로 노트북을 구성. 모범 답안 노트북은 마지막에 공개.
- 문서: `docs/conference_organizer_practice_guide.md`(학생), `docs/conference_organizer_instructor_guide.md`(강사),
  `docs/reference_notebook_guide.md`(구 colab_guide — 모범 답안 안내서로 전환).

## 실습 1 — 브이월드 지도 앱 (devlog 007; 순서 변경 devlog 010)

- 문서: `docs/vworld_map_practice_guide.md`(학생), `docs/vworld_map_instructor_guide.md`(강사), 샘플 `examples/vworld_map_sample.html`(사용자가 Gemini 로 만든 것).
- **미확인 — 수업 전 반드시 실제 키로 점검**: 브이월드 WMTS 가 서비스 URL(도메인)을 검사하는지,
  `file://` 로 연 HTML 과 Colab 미리보기에서 타일이 나오는지. 결과에 따라 학생에게 줄 "서비스 URL" 값과 완성 기준 #2 를 확정
  (강사 안내서 "수업 전 점검 1)" 표). 키 없는 옛 주소 `xdworld.vworld.kr/2d/…/{z}/{x}/{y}` 는 2026-10-06 현재 동작(비공식).
- Gemini 패널: 새 노트북에선 닫혀 있음 → 화면 맨 아래 가운데 ✦ **Toggle Gemini**. 두 학생 안내서·강사 안내서에 반영.

## 다음 할 일

0. **강사가 Gemini in Colab 으로 전 과정을 직접 한 번 해 보기** — 안내서의 UI 설명·프롬프트 예시·"Gemini 가 자주 하는 실수" 표가
   실제와 맞는지 확인 (현재 내용은 실제 Gemini 로 검증하지 않은 예상치).

1. **Colab 실제 실행 확인** — 노트북을 드라이브에 올려 처음부터 끝까지: `preview()` iframe, `files.download()`,
   방법 B(드라이브 마운트). 로컬에선 Colab 전용 부분을 검증할 수 없었음.
2. 내려받은 `out_step5.html` 을 PC Chrome 에서 열어 북마크 유지·내보내기/불러오기 수동 확인.
3. GSK 2026 프로그램북이 나오면(공지 게시판, 10월 중순 예상) `data/src/` 에 받아 `parse_program_book.py` → `check.py`.
   (시간 두 자리, talks 정렬, room 비우지 않기 — README "데이터" 참고)
4. 템플릿을 고치면 반드시 `python scripts/make_notebook.py` 다시 실행 (노트북 셀은 steps/*.html 복사본).

## 결정 사항

- git 저장소: **public** `github.com/jikhanjung/gsk2026-aiworkshop` (main). `data/`, `dist/` 는 `.gitignore` — 학회 데이터는 절대 커밋하지 말 것.
- 학생은 Colab 에서 바로 열 수 있음: `https://colab.research.google.com/github/jikhanjung/gsk2026-aiworkshop/blob/main/gsk2026_practice.ipynb`
- 지금 데이터는 2025 프로그램북. GSK 2026 프로그램북이 나오면 같은 파서로 다시 만든다.

## GSK 2026 학술대회 정보 (2026-10-06 조사)

- 2026 추계지질과학연합학술대회 및 대한지질학회 제81차 정기총회 — **2026-10-27(화) ~ 10-30(금), 여수엑스포컨벤션센터**
  (10/27~29 구두발표, 10/29 포스터·KIGAM 포럼, 10/30 야외답사). 학회 페이지: https://www.gskorea.or.kr/html/?pmode=inputList&smode=view&part=1&intAcSeq=40
- **상세 프로그램북은 아직 미공개** (10/6 기준). 공개된 건 `2026_추계안내서_v2.pdf`(40쪽, 일정 개요·세션 목록·강연자)뿐.
  세션: 일반세션 17개 분야 + 특별세션 13개(주제 7, 현안 6) + 기조강연 1·특별강연 2.
- 참고: 2025 프로그램북은 2025-10-17(개막 약 10일 전)에 공지 게시판(`pmode=BBBS0002700002`)에 `2025_Program_book.pdf` 로 첨부됨
  → 2026 도 10월 중순 게시 예상. 초록집은 `pmode=BBBS0002700007`(온라인 ISSN 3058-6054) 에 연도별로 올라옴.

## 열린 질문

- 학생들에게 JSON(또는 완성 데이터)을 어떻게 배포할지 (드라이브 공유 링크 / GitHub / 직접 업로드).
- 초록 본문을 넣을지: 2025 초록집(회원 전용 다운로드)을 받아 파싱하면 abstract/keywords/affiliations 를 채울 수 있음.
