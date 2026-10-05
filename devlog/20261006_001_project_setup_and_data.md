# 001. 프로젝트 셋업 및 실습 데이터 준비

- 날짜: 2026-10-06
- 상태: 완료

## 한 일

- `~/projects/gsk2026` 생성 (`data/`, `scripts/`, `steps/`, `dist/`, `devlog/`).
- `scripts/prepare_data.py`: strati2026 산출물(`output/sessions.json`, `program.json`, `abstracts.json`)을
  실습용 단일 파일 `data/conference.json` 으로 재가공.
  - 날짜를 ISO(`2026-06-29`)로 바꾸고 원래 표기는 `day_label` 로 보존 → 정렬이 쉬워짐.
  - 기조강연(plenary)의 빈 `room` 은 `"Main Hall"` 로 채움 → 장소 필터에서 null 처리 불필요.
  - 초록의 저자는 이름 문자열 배열로 단순화(소속번호·교신저자 표시는 제외).
  - 결과: 세션 30, 발표 457(talk 448 + plenary 9), 초록 607, 2.0MB.
- **데이터는 임시본**: GSK 2026 프로그램 공개 전까지 strati2026 데이터로 개발. 나중에 GSK 프로그램 PDF 를
  파싱해 같은 스키마로 다시 만든다. `data/` 는 `.gitignore`(재배포 불가 데이터 + 재생성 가능).
- `git init` (커밋 전). `.gitignore`: `data/`, `dist/`.
- `steps/step2_list.html`, `steps/step3_filter.html` 작성.
- `CLAUDE.md` 에 설계 결정과 남은 작업 정리.
- 남은 작업은 tmux 세션 `gsk` 의 Claude 에 인계.

## 다음

- Step 4(북마크·내 일정), 완성본 앱, 로컬 빌드 스크립트, Colab 노트북 생성, 검증, README.
