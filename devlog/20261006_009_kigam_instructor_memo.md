# 009. 실습 2 강사 안내서 — KIGAM 지질도(심화) 강사 메모

- 날짜: 2026-10-06
- 상태: 완료 (실제 KIGAM 키 점검은 남음)

## 한 일

- `docs/vworld_map_instructor_guide.md` 에 "1-1) (심화) KIGAM 지질도 WMS" 점검 목록 추가 (학생 안내서 §9, devlog 008 과 짝):
  강사 키 사전 신청·승인(2주 전), 파이썬 / Colab 미리보기 / `file://` 세 곳 시험과 도메인 제한 확인, 레이어·좌표계·투명 PNG 확인,
  샘플 `KIGAM_KEY` 로 데모 후 키 지운 파일 배포, 수업 중 동시 호출 자제.
- 개입 힌트 표에 "지질도 안 겹쳐짐 — `openapi/wms` 500" 한 줄 추가.

## 핵심 발견

- `https://data.kigam.re.kr/openapi/wms` 에 키 없이 또는 잘못된 키로 `GetMap` → **HTTP 500 + HTML "서비스에 일시적인 오류가 발생했습니다."**
  (브이월드는 HTTP 200 + 오류 XML). 서버 장애처럼 보이므로 키 문제를 먼저 의심하도록 안내.
- 같은 주소의 `GetCapabilities` 는 404 XML.

## 다음

- 강사 KIGAM 키로 위 점검 표 채우기 (도메인 제한, file:// 동작, EPSG:3857, 투명 PNG).
