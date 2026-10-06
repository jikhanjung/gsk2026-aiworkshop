# 015. 데이터 구글 드라이브 링크 배포

- 날짜: 2026-10-06
- 상태: 완료

## 한 일

- 강사가 `data/conference.json` 을 구글 드라이브에 "링크가 있는 모든 사용자" 로 공유
  (`1RIQlIQLFfPRQNLve4ZU9KyTKr1TMBvy4`). 로그인 없이 `uc?export=download&id=…` 로 받은 파일이 로컬과 바이트 동일함을 확인.
  JSON 자체는 저장소에 넣지 않음 (사용자 결정).
- 모범 답안 노트북(`scripts/make_notebook.py`) 준비 2: **방법 A — 링크로 바로 받기(권장)** 셀 추가
  (`urllib.request.urlretrieve(DATA_URL, "conference.json")` → `load_data`). 기존 업로드 → 방법 B, 드라이브 마운트 → 방법 C.
  노트북 재생성, 로컬에서 도우미 셀 + 방법 A 셀 실행 확인 (sessions 38, talks 382, abstracts 609).
- 학생 안내서 §2(한/영): 준비물에 링크, 데이터 가져오기 첫 번째 방법으로 `!wget -q -O conference.json "…"` 두 줄 셀. 런타임 끊김 안내도 맞춤.
- 모범 답안 안내서 §3-2·§8·문제 해결 표·강사 체크리스트(한/영), README 배포 방법(한/영) A/B/C 로 정리.

## 핵심 발견

- 저장소가 public 이라 링크도 사실상 공개. README 에 "수업 뒤 드라이브 공유를 '제한됨' 으로" 메모.
- 파일을 바꿀 때(GSK 2026 데이터) 드라이브에서 **같은 파일의 새 버전 업로드**(파일 관리 → 새 버전)를 하면 ID 가 유지되어 문서·노트북을 안 고쳐도 됨.

## 다음

- Colab 에서 방법 A 셀과 `!wget` 셀 실제 실행 확인.
