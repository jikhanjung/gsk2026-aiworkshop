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
