# 008. README 두 실습 구성, KIGAM 지질도 오버레이(심화) 추가

- 날짜: 2026-10-06
- 상태: 완료 (KIGAM WMS 는 실제 키로 미검증)

## 한 일

- `README.md` 를 **실습 1(학회 시간표 앱) / 실습 2(브이월드 지도 앱)** 두 가지 기준으로 재구성.
  맨 위 비교표(만드는 것·주는 것·인터넷·배우는 것·심화·학생/강사 안내서·모범 답안/예시), 실습 2 요약 단락,
  기존 실습 1 내용은 "실습 1 — …" 섹션으로.
- `docs/vworld_map_practice_guide.md` §9 **(심화) KIGAM 지질도 오버레이** 추가:
  인증키 신청 절차(지오빅데이터 오픈플랫폼 가입 → OpenAPI 신청 → 승인), WMS 주소·파라미터·레이어,
  프롬프트 예시, 안 될 때 표. §1 "더 하면 좋은 것" 에 항목 추가.
- `examples/vworld_map_sample.html`: `KIGAM_KEY` 변수 추가 — 키가 있으면 `L.tileLayer.wms` 로 1:5만/1:25만 지질도
  오버레이와 켜기·끄기 메뉴(투명도 0.6). 비어 있으면 기존과 동일하게 동작. `node --check` 통과.

## 핵심 발견

- KIGAM 공식 안내(`/guide/openapi`, `openapiLayerList.html`, `openlayersSample.html`) 기준:
  - WMS 주소 `https://data.kigam.re.kr/openapi/wms`, 인증 파라미터 `key`, 표준 WMS GetMap 파라미터(`srs`/`crs`, `bbox`, `format=image/png`, `transparent`).
  - 지질도 레이어 `L_50K_Geology_Map`, `L_250K_Geology_Map`, `L_1M_Geology_Map` (+ 도폭 경계 `l_50k_geology_frame_latest`).
  - 공식 OpenLayers 예제가 Web Mercator(EPSG:3857) 지도 위에 이 WMS 를 겹침 → Leaflet 기본 좌표계와 같음.
  - 과도한 호출 시 이용 제한 가능하다고 명시.
- 가짜 키로 curl 요청 시 `400 Request Blocked`(HTML) 응답 — 키 오류인지 방화벽(User-Agent 등)인지 구분 못 함.
- 사용자 확인: KIGAM 은 가입 즉시, **키는 승인 필요라 당일 발급이 어려울 수 있음**. 브이월드 키는 즉시 발급.
  → 지질도는 본 실습 완성 기준에서 빼고 사전 신청/수업 후 과제로.

## 다음

- 강사가 KIGAM 키를 발급받아 샘플의 `KIGAM_KEY` 로 `file://` 에서 지질도가 겹쳐지는지 확인 (도메인 제한 여부 포함).
- 확인되면 안내서 §9 의 "실제 키로는 아직 시험하지 않았습니다" 문구 제거.
