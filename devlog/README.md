# devlog 인덱스

개발 로그·계획 문서 색인. **파일명 slug 자체가 요약**이라 디렉터리 listing 이 1차 인덱스이고,
이 문서는 **번호 규칙 + 라운드 그룹핑**을 더한다.

## 명명 규칙 (CLAUDE.md §문서 규칙)

- **작업 결과**: `YYYYMMDD_{nnn}_{title}.md` (001, 002, … 단조 증가 시퀀스)
- **계획 문서**: `YYYYMMDD_P{nn}_{title}.md` (P01, P02, …)
- 새 문서를 쓰면 아래 표에 한 줄 추가한다.

## 라운드

| 라운드 | devlog | 날짜 |
|---|---|---|
| **실습 설계 + 데이터 준비** | **P01** colab_webapp_practice_plan(계획: PDF 파싱 제외, JSON → 단일 HTML, 단계 구성) · 001 project_setup_and_data (strati2026 산출물 → `data/conference.json`, Step 2·3 템플릿) | 10/6 |
| **학생용 안내서** | 002 colab_guide (`docs/colab_guide.md`: 단계별 안내·주의사항·문제 해결·강사 체크리스트) | 10/6 |
| **실습 자료 완성** | 003 step4_app_build (Step 4 북마크·내 일정, 완성본 `steps/app.html`, `build.py`, 시간 두 자리 정규화) · 004 notebook_check_readme (노트북 생성기·안내서 정렬, `check.py`/jsdom 스모크 테스트, README) | 10/6 |
| **GSK 데이터** | 005 gsk2025_program_book_data (2026 프로그램북 미공개 → 2025 프로그램북 PDF 파싱 `scripts/parse_program_book.py`, 구두 382·포스터 229) | 10/6 |
| **AI 활용 수업으로 전환** | 006 gemini_class_docs_and_repo_rename (학생용 Gemini 안내서·강사 안내서 신설, 노트북은 모범 답안으로, 저장소 `gsk2026-aiworkshop`) | 10/6 |
| **실습 2 — 브이월드 지도 앱** | 007 vworld_map_practice_docs (학생·강사 안내서, 인증키·보안 비밀, 서비스 URL 사전 점검, Gemini 패널 = 맨 아래 ✦ Toggle Gemini) | 10/6 |
| **README 두 실습 · 지질도 심화** | 008 readme_two_practices_and_kigam_overlay (README 실습 1/2 비교표, 브이월드 안내서 §9 KIGAM 지질도 WMS 오버레이, 샘플 `KIGAM_KEY`) | 10/6 |
| **실습 2 — 지질도 심화** | 009 kigam_instructor_memo (강사 안내서에 KIGAM WMS 사전 점검, 무효 키 → HTTP 500 "일시적인 오류" 페이지) | 10/6 |
| **실습 순서 변경** | 010 practice_order_swap (실습 1 = 브이월드 지도 앱, 실습 2 = 학회 시간표 앱. README·안내서 4종·CLAUDE/HANDOFF 갱신) | 10/6 |
| **쉬운 말 프롬프트 · 앱 이름** | 011 plain_prompts_and_conference_organizer (학생 안내서 프롬프트를 비전공자 말투로, 참고 카드 분리, 실수 표 재구성 / 시간표 앱 = Conference Organizer, 안내서 파일명 변경) | 10/6 |
