# 014. 지도 앱 샘플 HTML 영어판

- 날짜: 2026-10-06
- 상태: 완료

## 한 일

- `examples/vworld_map_sample.en.html`: 한국어 샘플과 같은 코드·동작, 화면 문구·주석·alert/confirm·기본 필드
  (`장소명/방문일/메모` → `Place/Visit date/Notes`)만 영어로. `lang="en"`, 맨 위에 한국어판과의 관계 주석.
  강사 안내서의 샘플 리뷰 포인트(이스케이프 없음, 좌표로 삭제, 옛 타일 주소)가 그대로 성립하도록 로직은 손대지 않음.
  저장 키(`standalone_map_markers_v1`)도 같게 둬서 내보낸 JSON 을 두 버전이 서로 불러올 수 있음.
- 두 파일 `<script>` `node --check` 통과.
- 영어 문서(README.en, 지도 앱 학생·강사 안내서 영어판)는 영어 샘플을 가리키고, 한국어 문서에는 영어판도 표기. CLAUDE.md 에 "샘플 고치면 둘 다".

## 다음

- 없음.
