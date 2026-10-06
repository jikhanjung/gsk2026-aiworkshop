# 007. 실습 2 — 브이월드 지도 앱 문서, Gemini 패널 위치 안내

- 날짜: 2026-10-06
- 상태: 완료 (문서) / 실제 인증키 점검 필요

## 한 일

- 사용자가 Gemini + Colab 으로 만든 지도 앱(`examples/vworld_map_sample.html`)을 바탕으로, 같은 방식의 두 번째 실습 문서 작성.
  - `docs/vworld_map_practice_guide.md` (학생): 완성 기준 8개(파일 하나, 내 키로 브이월드 지도, 배경 전환, 클릭해 지점 추가,
    정보·삭제, localStorage 유지, JSON 내보내기/불러오기, **키를 노트북에 적지 않기**), 인증키 발급(수업 전 과제),
    단계 0–6 프롬프트 예시(보안 비밀 `VWORLD_KEY` → 타일 한 장 요청으로 키 확인 → 첫 지도 → 레이어 → 지점 → 내보내기 → 다듬기),
    인증키 오류 표, Gemini 실수 표(f-string 과 `{z}/{y}/{x}`, 지도 높이 0, leaflet.css 누락, x/y 순서, Hybrid 겹치기, folium, 이스케이프, 좌표로 삭제 등).
  - `docs/vworld_map_instructor_guide.md` (강사): 서비스 URL 사전 점검 표(파이썬 / Colab 미리보기 / file://)와 막힐 때 대안,
    학생 사전 과제, 진행 예시, 개입 힌트, 평가 기준, 샘플 리뷰 포인트.
- Gemini 패널 위치: 새 노트북에선 패널이 닫혀 있고 **화면 맨 아래 가운데 파란 ✦ (Toggle Gemini)** 로 연다 —
  `gemini_practice_guide.md` §2·§7-1, `instructor_guide.md` 점검 목록, 새 안내서에 반영 (사용자 스크린샷 기준).
- README·CLAUDE.md·HANDOFF 에 실습 2 추가.

## 핵심 발견

- 브이월드 공식 WMTS: `https://api.vworld.kr/req/wmts/1.0.0/{키}/{레이어}/{z}/{y}/{x}.{png|jpeg}` — **y 가 x 보다 먼저**.
  잘못된 키는 HTTP 200 + `ExceptionReport` XML(`등록되지 않은 인증키입니다.`) → 이미지 대신 XML 이 오므로 타일이 회색.
- 샘플이 쓰는 키 없는 옛 주소 `https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png` 는 2026-10-06 현재 동작(비공식).
- 인증키는 발급 때 등록한 도메인으로 검사된다는 사례(데이터 API, `INCORRECT_KEY`)가 있음. WMTS 타일도 그런지,
  도메인이 없는 `file://` 에서 되는지는 **키가 없어 확인 못 함** → 강사 안내서에 사전 점검으로 넣음.
- Colab AI 기능 조건(공식 FAQ): 계정 18세 이상, 지원 지역. Workspace 계정은 관리자 설정에 따름.

## 다음

- 실제 브이월드 키로 사전 점검 표 채우기 → 학생에게 줄 서비스 URL 확정, 필요하면 완성 기준 #2 수정.
- 강사가 Gemini 로 지도 앱 전 과정을 한 번 해 보고 프롬프트·실수 표 보정.
