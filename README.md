# GSK 2026 AI 워크숍 — Gemini 와 함께 HTML 앱 만들기

학생들이 **Google Colab 의 Gemini 에게 프롬프트를 입력하며** 노트북을 구성하고,
그 결과로 **HTML 파일 하나짜리 앱**을 만들어 내려받아 내 PC 브라우저에서 쓰는 실습 자료입니다.
코드를 처음부터 주지 않고, **원하는 것을 정확히 말하고 → 결과를 확인하고 → 고쳐 달라고 하는 과정**을 연습합니다.

실습은 두 가지입니다.

| | 실습 1. 브이월드 지도 앱 | 실습 2. 학회 시간표 앱 |
|---|---|---|
| 만드는 것 | 브이월드 배경지도 위에 **답사·시료 지점**을 찍고 기록하기 | 학회 발표를 날짜·발표장별로 보고, 북마크해서 **내 일정** 만들기 |
| 학생에게 주는 것 | 없음 — 학생이 **브이월드 인증키**를 미리 발급 | 학회 프로그램 데이터 `conference.json` |
| 인터넷 | **필요** (지도 타일, Leaflet CDN 허용) | **필요 없음** (데이터를 HTML 안에 넣음, 외부 라이브러리 금지) |
| 새로 배우는 것 | 지도 라이브러리, 외부 API, **인증키를 안전하게 다루기**(Colab 보안 비밀), `localStorage`, 내보내기·불러오기 | 데이터 파일 → HTML 에 넣기, 필터·검색, 화면 상태 관리, 시간 겹침 계산 |
| 심화 | **KIGAM 지질도 오버레이** (키 승인 필요 → 사전 신청 또는 수업 후 과제) | 세션별 보기, 상세 화면, 북마크 내보내기 등 |
| 학생용 안내서 | [`docs/vworld_map_practice_guide.md`](docs/vworld_map_practice_guide.md) | [`docs/gemini_practice_guide.md`](docs/gemini_practice_guide.md) |
| 강사용 안내서 | [`docs/vworld_map_instructor_guide.md`](docs/vworld_map_instructor_guide.md) | [`docs/instructor_guide.md`](docs/instructor_guide.md) |
| 모범 답안 / 예시 | [`examples/vworld_map_sample.html`](examples/vworld_map_sample.html) (인증키 미포함) | 노트북 `gsk2026_practice.ipynb` + [`docs/reference_notebook_guide.md`](docs/reference_notebook_guide.md) (수업 마지막 공개) |

두 실습 모두 진행 방식은 같습니다 — 완성 기준표를 보며 **단계별로 Gemini 에게 요청 → 실행 → 다운로드해서 열어 보기 → 기준과 비교**.
**실습 1(지도 앱)을 먼저** 합니다. 화면 구성이 단순하고(지도 + 지점 기록), 다룰 데이터가 없어 Gemini 와 일하는 방식에 익숙해지기 좋습니다.
실습 2(시간표 앱)에서는 큰 데이터 파일을 HTML 에 넣고, 필터·검색·겹침 계산처럼 로직이 더 많은 앱을 만듭니다.
지도 앱과 달리 **외부 라이브러리(CDN)를 쓰지 않는다**는 조건이 바뀌는 점을 학생에게 꼭 짚어 주세요.

- 모범 답안 노트북 Colab 링크(실습 2): https://colab.research.google.com/github/jikhanjung/gsk2026-aiworkshop/blob/main/gsk2026_practice.ipynb
- 설계 결정·규칙: [`CLAUDE.md`](CLAUDE.md) · 진행 상황: [`HANDOFF.md`](HANDOFF.md) · 개발 기록: [`devlog/`](devlog/README.md)

## 실습 1 (브이월드 지도 앱) 요약

- **수업 전 과제**: 학생이 브이월드(https://www.vworld.kr) 가입 → 인증키 발급(배경지도 WMTS 포함) → 메일 인증 → 승인 확인.
  키는 신청 즉시 발급되지만 가입·메일 인증 단계가 있으므로 **수업 전에 미리** 받아 오게 합니다. 신청서의 **서비스 URL** 은 강사가 미리 시험해 본 값을 알려 줍니다.
- **인증키는 노트북 코드에 쓰지 않습니다.** Colab 왼쪽 🔑 **보안 비밀**에 `VWORLD_KEY` 로 넣고 코드에서 읽습니다.
  단, 완성 HTML 파일에는 키가 들어가므로 **HTML 은 강사에게만 제출**하고 공개하지 않습니다.
- 완성 기준: 내 키로 배경지도 표시, 배경지도 전환, 클릭해서 지점 추가·정보 보기·삭제, 다시 열어도 유지(`localStorage`),
  JSON 내보내기·불러오기, 키가 노트북에 노출되지 않음. 자세한 단계·프롬프트·주의사항은 안내서 참고.
- **(심화) 지질도 오버레이**: 한국지질자원연구원 지오빅데이터 오픈플랫폼(https://data.kigam.re.kr) OpenAPI 의 지질도 WMS
  (`https://data.kigam.re.kr/openapi/wms`, 레이어 `L_50K_Geology_Map` 등)를 브이월드 지도 위에 반투명하게 겹칩니다.
  가입은 바로 되지만 **인증키는 승인을 거쳐야 해서 당일 발급이 어려울 수 있습니다** (브이월드 키는 즉시 발급).
  → 본 실습 완성 기준에서 빼고, 미리 신청한 학생이나 수업 후 과제로 진행합니다. 안내서 §9.
- `examples/vworld_map_sample.html` 은 Leaflet + 브이월드 타일 + `localStorage` 로 만든 참고 예시입니다 (인증키 미포함).
  파일 안 `KIGAM_KEY` 에 키를 넣으면 1:5만 / 1:25만 지질도 켜기·끄기 메뉴가 생깁니다.
- 서비스 URL 사전 점검, 대안, 샘플 리뷰 포인트는 강사용 [`docs/vworld_map_instructor_guide.md`](docs/vworld_map_instructor_guide.md).

---

이 아래는 저장소 구성과 **실습 2(학회 시간표 앱)** 의 데이터·준비 절차입니다.

## 저장소 구성

```
data/conference.json       실습 데이터 (git 미추적, scripts/parse_program_book.py 로 생성)
data/src/                  원본 PDF (git 미추적) — gsk2025_program_book.pdf
steps/step2_list.html      Step 2  JS 로 목록 그리기
steps/step3_filter.html    Step 3  날짜·장소 필터, 검색 (state + render)
steps/step4_bookmark.html  Step 4  ☆ 북마크(localStorage), 내 일정, 시간 겹침
steps/app.html             Step 5  완성본: 하단 탭, 발표 상세(hash 라우팅), 세션, 초록 본문 검색, 북마크 내보내기/불러오기
build.py                   템플릿 + JSON → 단일 HTML (로컬용, 노트북의 build() 와 같은 일)
scripts/make_notebook.py   steps/*.html 을 %%writefile 셀로 넣어 노트북 생성
scripts/check.py           전체 검증 (빌드, JS 문법, 노트북, 렌더 스모크 테스트)
scripts/smoke_test.js      jsdom 렌더 스모크 테스트 (check.py 가 호출)
docs/gemini_practice_guide.md     학생용 Gemini 실습 안내서
docs/instructor_guide.md          강사용 수업 운영 안내
docs/reference_notebook_guide.md  모범 답안 노트북 안내서 (수업 마지막 공개)
docs/vworld_map_practice_guide.md 실습 1 학생용 안내서 (브이월드 지도 앱, §9 KIGAM 지질도 심화)
docs/vworld_map_instructor_guide.md 실습 1 강사용 안내
examples/vworld_map_sample.html   실습 1 참고 예시
```

템플릿은 모두 `const DATA = __DATA__;` 한 자리를 가지고 있고, 파이썬이 그 자리에 JSON 을 넣습니다
(`</` 는 `<\/` 로 이스케이프). `file://` 로 열면 `fetch` 가 막히기 때문에 데이터를 HTML 안에 넣는 방식입니다.
템플릿은 학회명·날짜·장소·세션을 전부 `DATA` 에서 읽으므로, 같은 스키마의 다른 학회 데이터를 넣어도 그대로 동작합니다.

## 실습 2 — 데이터

스키마 (`data/conference.json`):

| 키 | 필드 |
|---|---|
| `meta` | `name`, `full_name`, `place`, `days`(ISO 날짜 목록), `note` |
| `sessions[]` | `code`, `title` |
| `talks[]` | `id`, `date`(ISO), `day_label`, `time_start`, `time_end`(`HH:MM` 두 자리), `room`, `session`, `title`, `first_author`, `kind`(`talk`/`plenary`), `abstract_id` |
| `abstracts[]` | `id`, `session`, `title`, `authors[]`, `affiliations[]`, `abstract`, `keywords[]` |

- 시간은 반드시 `HH:MM` **두 자리**로 맞춥니다. 시간 겹침 계산과 정렬이 문자열 비교에 기대고 있습니다.
- `talks` 는 날짜·시작 시각 순으로 정렬해 둡니다 (내 일정·겹침 계산이 이 순서를 씁니다).
- `room` 은 비우지 않습니다 (장소 필터). 초록이 없는 발표는 `abstract_id: null`.
- 지금 데이터는 **2025 추계지질과학연합학술대회 프로그램북**(대한지질학회 공지 게시판 첨부 PDF)에서 뽑은 것입니다.
  구두발표 382건(특별강연 등 plenary 5), 포스터 229건(P001–P209, 차세대 Y001–Y020), 세션 38개, 3일 · 9개 발표장.
  - 프로그램북엔 **초록 본문이 없어서** `abstract`·`keywords`·`affiliations` 는 빈 값이고, 저자 목록만 있습니다.
    초록집 PDF 는 학회 회원 로그인이 있어야 내려받을 수 있습니다.
  - 포스터는 발표 시각이 없으므로 `talks` 가 아니라 **일정 없는 `abstracts`**(제목 앞 `[P001]`)로 넣었습니다.
  - 휴식·중식·개회식·총회처럼 제목 없는 칸은 뺐습니다. 원문 시간 오타 1건(`12:00-15:15`)은 다음 발표 시작으로 보정합니다.
- 2026 프로그램북이 나오면(10월 중순 예상) `data/src/` 에 넣고 같은 파서를 돌린 뒤 `python scripts/check.py` 로 확인하세요.
  쪽 배치가 바뀌었으면 `scripts/parse_program_book.py` 머리 주석의 좌표·글자 크기 규칙을 고칩니다.
- 학회 자료이므로 **공개 저장소·웹에 올리지 않습니다** (`data/`, `dist/` 는 `.gitignore`).

## 실습 2 — 수업 전 준비 (강사)

수업 운영·점검 항목은 [`docs/instructor_guide.md`](docs/instructor_guide.md). 아래는 자료를 만드는 절차와,
모범 답안 노트북을 학생들이 바로 따라 할 수 있게 준비하는 절차입니다.

1. 데이터 만들기: 프로그램북 PDF 를 `data/src/` 에 두고
   `python scripts/parse_program_book.py [PDF]` → `data/conference.json` (`pip install pymupdf` 필요)
2. 노트북 만들기: `python scripts/make_notebook.py` → `gsk2026_practice.ipynb`
3. 검증: `python scripts/check.py` (아래 "검증" 참고)
4. 노트북을 드라이브에 올리고 Colab 으로 열어 **위에서부터 끝까지 한 번 실행**해 봅니다.
   특히 `preview()` 미리보기가 실습실 네트워크에서 뜨는지, `download()` 가 되는지 확인.
5. 노트북 공유 링크는 **보기 전용**으로. 학생은 "드라이브에 사본 저장" 후 작업합니다.
6. 데이터 배포 방법을 정합니다 (`docs/reference_notebook_guide.md` §3-2, `docs/gemini_practice_guide.md` §2).
   - **방법 A 업로드**: `conference.json` 을 메신저·LMS 로 나눠 주고 학생이 업로드. 가장 단순.
   - **방법 B 드라이브**: 공유 폴더에 두고 학생이 "내 드라이브에 바로가기 추가" → 노트북의 `DATA_PATH` 수정.
     드라이브 권한 창이 한 번 더 나오므로 시간이 조금 더 걸립니다.
   - 어느 쪽이든 **링크 공유 범위를 수강생으로 제한**하고, 재배포 금지를 공지합니다.
7. 실습실 PC 에서 *Chrome 다운로드 → 로컬 HTML 더블클릭 → 북마크 후 다시 열기* 를 미리 해 봅니다
   (보안 정책으로 다운로드나 로컬 파일 JS 가 막힌 곳이 있음).

`docs/instructor_guide.md` 의 "수업 전 점검" 도 함께 보세요.

## 실습 2 — (대안) 모범 답안 노트북으로 강의식 진행 (예: 3시간)

기본 수업 방식(Gemini 실습)의 진행표는 `docs/instructor_guide.md`. 아래는 모범 답안 노트북을 처음부터 같이 따라가는 강의식 진행입니다.

| 시간 | 단계 | 포인트 |
|---|---|---|
| 0:00 | 소개, 사본 저장, 런타임 연결 | 완성본을 먼저 보여 주면 동기 부여가 됩니다 |
| 0:10 | 준비 — 도우미 함수, 데이터 불러오기 | 개수(`sessions …, talks …`)가 나오는지 전원 확인 |
| 0:20 | Step 0 — 데이터 살펴보기 (pandas) | `talks` ↔ `abstracts` 연결(`abstract_id`) |
| 0:35 | Step 1 — f-string 정적 HTML | `html.escape` 가 왜 필요한지. "날짜를 바꾸려면?" 으로 JS 의 필요성 유도 |
| 0:55 | Step 2 — JS 로 목록 | `__DATA__` 치환, 템플릿 리터럴, `esc()`, F12 콘솔 보는 법 |
| 1:20 | 휴식 | |
| 1:30 | Step 3 — 필터·검색 | **state → render()** 패턴을 칠판에 그려 설명 |
| 2:00 | Step 4 — 북마크·내 일정 | `localStorage`, `Set`, 이벤트 위임, 겹침 계산(문자열 시간 비교) |
| 2:30 | Step 5 — 완성본, 내려받아 PC 에서 열기 | hash 라우팅, 북마크 내보내기/불러오기. 북마크 유지 확인 |
| 2:45 | 과제 안내, 질의응답 | 노트북 끝 "과제 아이디어" |

시간이 부족하면 Step 3 의 "해 볼 것" 을 건너뛰고, Step 5 는 코드 설명 없이 기능만 보여 줘도 됩니다.

## 실습 2 — 주의점

- **런타임 초기화**: 오래 쉬면 업로드한 파일·만든 HTML 이 사라집니다. "런타임 → 이전 셀 모두 실행" 후 데이터를 다시 올리면 됩니다.
- **`%%writefile` 첫 줄과 `__DATA__`** 를 학생이 지우는 일이 흔합니다. `build()` 가 한국어 오류로 알려 줍니다.
- **미리보기가 안 바뀜**: 템플릿 셀을 다시 실행하지 않은 경우가 대부분입니다.
- **하얀 화면**: 내려받은 파일을 Chrome 으로 열고 `F12` → Console. 백틱·괄호 짝 오류가 대부분입니다.
- **북마크 저장 공간**: Colab 미리보기와 내려받은 파일은 따로 저장됩니다. Chrome 에서는 로컬 HTML 파일끼리 공유되므로
  Step 4 와 Step 5 파일의 북마크가 같이 보이는 것은 정상입니다(같은 키 `gsk2026.bookmarks`).
- **폰 비권장**: 폰의 파일 앱 미리보기는 JS·`localStorage` 가 잘 동작하지 않습니다. PC Chrome 기준으로 진행하세요.
- 결과 HTML(약 2MB)에는 **초록 본문까지 전부** 들어 있습니다. 공개 장소에 올리지 않도록 안내하세요.

## 실습 2 — 개발 (템플릿을 고칠 때)

```bash
# 템플릿 하나를 빌드해서 브라우저로 확인
python build.py steps/app.html data/conference.json dist/conference.html

# 템플릿을 고쳤으면 노트북을 다시 만든다 (steps/*.html 이 단일 진실 원천)
python scripts/make_notebook.py

# 전체 검증
python scripts/check.py
```

### 검증

`scripts/check.py` 가 하는 일:

1. 모든 템플릿을 `dist/` 로 빌드하고 `<script>` 를 뽑아 `node --check`
2. 데이터에 `</script>` 가 들어 있어도 스크립트가 끊기지 않는지 (`</` 이스케이프)
3. 노트북 JSON 유효성, 파이썬 셀 문법, `%%writefile` 셀이 `steps/*.html` 과 같은지
4. jsdom 이 있으면 `scripts/smoke_test.js` 로 렌더 스모크 테스트 (필터, 검색, 북마크 저장, 겹침, 상세, 내보내기/불러오기 등).
   테스트 값도 데이터에서 골라 쓰므로 데이터를 바꿔도 그대로 돌릴 수 있습니다.

jsdom 은 프로젝트 의존성이 아닙니다. 아무 곳에나 설치하고 `NODE_PATH` 로 알려 주세요.

```bash
mkdir -p /tmp/jsdom && (cd /tmp/jsdom && npm i jsdom)
NODE_PATH=/tmp/jsdom/node_modules python scripts/check.py
```
