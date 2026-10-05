# HANDOFF

- 갱신: 2026-10-06 (003·004 반영)

## 현재 상태

- 실습 자료 1차 완성 (devlog 003, 004). CLAUDE.md 의 작업 1~6 완료.
  - 템플릿 `steps/step2_list` · `step3_filter` · `step4_bookmark` · `app`(Step 5 완성본)
  - `build.py`, `scripts/make_notebook.py` → `gsk2026_practice.ipynb` (docs/colab_guide.md 와 단계명·파일명 일치)
  - 검증 `python scripts/check.py` 전부 통과 (jsdom 스모크 테스트 31개 포함, `NODE_PATH` 필요)
  - `README.md` 강사용 안내
- 데이터는 여전히 임시본(strati2026). `prepare_data.py` 가 시간을 `HH:MM` 두 자리로 정규화하도록 고침.

## 다음 할 일

1. **Colab 실제 실행 확인** — 노트북을 드라이브에 올려 처음부터 끝까지: `preview()` iframe, `files.download()`,
   방법 B(드라이브 마운트). 로컬에선 Colab 전용 부분을 검증할 수 없었음.
2. 내려받은 `out_step5.html` 을 PC Chrome 에서 열어 북마크 유지·내보내기/불러오기 수동 확인.
3. GSK 2026 프로그램이 나오면 같은 스키마로 `data/conference.json` 재생성 → `make_notebook.py` → `check.py`.
   (시간 두 자리, talks 정렬, room 비우지 않기 — README "데이터" 참고)
4. 템플릿을 고치면 반드시 `python scripts/make_notebook.py` 다시 실행 (노트북 셀은 steps/*.html 복사본).

## 결정 사항

- git 저장소: **public** `github.com/jikhanjung/gsk2026` (main). `data/`, `dist/` 는 `.gitignore` — 학회 데이터는 절대 커밋하지 말 것.
- 학생은 Colab 에서 바로 열 수 있음: `https://colab.research.google.com/github/jikhanjung/gsk2026/blob/main/gsk2026_practice.ipynb`
- 지금 데이터는 strati2026 로 만든 **임시본**. GSK 2026 프로그램이 나오면 그걸로 다시 만든다.

## 열린 질문

- 학생들에게 JSON(또는 완성 데이터)을 어떻게 배포할지 (드라이브 공유 링크 / GitHub / 직접 업로드).
- GSK 프로그램 PDF 파싱: 형식을 보고 strati2026 파서를 재사용할 수 있을지 판단 (파싱은 학생 실습 범위 밖, 강사 준비 작업).
