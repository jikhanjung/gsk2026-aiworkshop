# 011. 학생 안내서 프롬프트를 쉬운 말로 · 시간표 앱 이름 Conference Organizer

- 날짜: 2026-10-06
- 상태: 완료

## 한 일

- **프롬프트 예시를 비전공자 말투로** (사용자 요청: 기술을 잘 모르는 입력자가 원하는 것을 명확히 말하는 상황을 상정)
  - 두 학생 안내서 §4 머리에 원칙: ① 하고 싶은 것 ② 화면이 어떻게 보이면 좋겠는지 ③ 어떻게 확인할지 — 기술 선택은 Gemini 에게,
    **조건**(파일 하나, 더블클릭, 인터넷 없이 / 키 안 보이게)만은 꼭 말하기.
  - 단계별 프롬프트에서 Leaflet·WMTS·localStorage·이스케이프·fetch·f-string·템플릿 치환 같은 말을 빼고 목적·관찰로 다시 씀.
    단계 0 에 "나는 프로그래밍을 잘 몰라 — 단계마다 내가 할 일도 알려 줘" 를 넣음.
  - 지도 앱: 꼭 필요한 기술 정보(브이월드 타일 주소·레이어, KIGAM WMS)는 **참고 카드 A/B** 로 분리 —
    "이해하지 않아도 됨, Gemini 가 헤맬 때만 붙여 넣기". 보안 비밀은 "키를 안전하게 두려면?" 하고 Gemini 에게 묻게 함.
  - "Gemini 가 자주 하는 실수" 표: **이런 일이 생기면 / 이렇게 말하기(본 것 + 오류 붙여 넣기) / 왜 그런가(몰라도 됨)** 로 재구성.
  - §5 프롬프트 요령: 모르는 말은 물어보기, 실행 전 "한두 줄로 설명해 줘", 새 대화로 요약해 다시 시작.
- **시간표 앱 이름 = Conference Organizer** (사용자 요청)
  - `docs/gemini_practice_guide.md` → `docs/conference_organizer_practice_guide.md`,
    `docs/instructor_guide.md` → `docs/conference_organizer_instructor_guide.md` (지도 앱 문서와 이름 짝 맞춤).
  - README·CLAUDE.md·HANDOFF·모든 docs 의 참조와 "학회 시간표 앱" 표기를 Conference Organizer 로 (제목·첫 소개는 "(학회 시간표 앱)" 병기).
  - 모범 답안 노트북 제목도 변경 (`make_notebook.py` → 재생성, `check.py` 통과).
- 이전 devlog 의 옛 파일명·표기는 기록이므로 그대로 둠.

## 다음

- 강사가 실제 Gemini 로 쉬운 말 프롬프트를 써 보고, Gemini 가 조건을 놓치는 지점이 있으면 예시 보강.
