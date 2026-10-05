# 학회 프로그램 웹앱 만들기 실습

학회 프로그램 데이터(JSON)를 **Google Colab** 에서 파이썬으로 HTML 템플릿에 넣어
**HTML 파일 하나짜리 웹앱**을 만들고, 내려받아 내 PC 브라우저에서 쓰는 실습 자료입니다.
대상은 프로그래밍 초보~중급 학생입니다.

- 학생용 안내서: [`docs/colab_guide.md`](docs/colab_guide.md)
- 실습 노트북: `gsk2026_practice.ipynb` (`scripts/make_notebook.py` 로 생성)
- 설계 결정·규칙: [`CLAUDE.md`](CLAUDE.md) · 진행 상황: [`HANDOFF.md`](HANDOFF.md) · 개발 기록: [`devlog/`](devlog/README.md)

## 구성

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
docs/colab_guide.md        학생용 Colab 안내서
```

템플릿은 모두 `const DATA = __DATA__;` 한 자리를 가지고 있고, 파이썬이 그 자리에 JSON 을 넣습니다
(`</` 는 `<\/` 로 이스케이프). `file://` 로 열면 `fetch` 가 막히기 때문에 데이터를 HTML 안에 넣는 방식입니다.
템플릿은 학회명·날짜·장소·세션을 전부 `DATA` 에서 읽으므로, 같은 스키마의 다른 학회 데이터를 넣어도 그대로 동작합니다.

## 데이터

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

## 수업 전 준비 (강사)

1. 데이터 만들기: 프로그램북 PDF 를 `data/src/` 에 두고
   `python scripts/parse_program_book.py [PDF]` → `data/conference.json` (`pip install pymupdf` 필요)
2. 노트북 만들기: `python scripts/make_notebook.py` → `gsk2026_practice.ipynb`
3. 검증: `python scripts/check.py` (아래 "검증" 참고)
4. 노트북을 드라이브에 올리고 Colab 으로 열어 **위에서부터 끝까지 한 번 실행**해 봅니다.
   특히 `preview()` 미리보기가 실습실 네트워크에서 뜨는지, `download()` 가 되는지 확인.
5. 노트북 공유 링크는 **보기 전용**으로. 학생은 "드라이브에 사본 저장" 후 작업합니다.
6. 데이터 배포 방법을 정합니다 (`docs/colab_guide.md` §3-2).
   - **방법 A 업로드**: `conference.json` 을 메신저·LMS 로 나눠 주고 학생이 업로드. 가장 단순.
   - **방법 B 드라이브**: 공유 폴더에 두고 학생이 "내 드라이브에 바로가기 추가" → 노트북의 `DATA_PATH` 수정.
     드라이브 권한 창이 한 번 더 나오므로 시간이 조금 더 걸립니다.
   - 어느 쪽이든 **링크 공유 범위를 수강생으로 제한**하고, 재배포 금지를 공지합니다.
7. 실습실 PC 에서 *Chrome 다운로드 → 로컬 HTML 더블클릭 → 북마크 후 다시 열기* 를 미리 해 봅니다
   (보안 정책으로 다운로드나 로컬 파일 JS 가 막힌 곳이 있음).

`docs/colab_guide.md` 끝의 강사용 체크리스트도 함께 보세요.

## 수업 진행 (예: 3시간)

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

## 주의점

- **런타임 초기화**: 오래 쉬면 업로드한 파일·만든 HTML 이 사라집니다. "런타임 → 이전 셀 모두 실행" 후 데이터를 다시 올리면 됩니다.
- **`%%writefile` 첫 줄과 `__DATA__`** 를 학생이 지우는 일이 흔합니다. `build()` 가 한국어 오류로 알려 줍니다.
- **미리보기가 안 바뀜**: 템플릿 셀을 다시 실행하지 않은 경우가 대부분입니다.
- **하얀 화면**: 내려받은 파일을 Chrome 으로 열고 `F12` → Console. 백틱·괄호 짝 오류가 대부분입니다.
- **북마크 저장 공간**: Colab 미리보기와 내려받은 파일은 따로 저장됩니다. Chrome 에서는 로컬 HTML 파일끼리 공유되므로
  Step 4 와 Step 5 파일의 북마크가 같이 보이는 것은 정상입니다(같은 키 `gsk2026.bookmarks`).
- **폰 비권장**: 폰의 파일 앱 미리보기는 JS·`localStorage` 가 잘 동작하지 않습니다. PC Chrome 기준으로 진행하세요.
- 결과 HTML(약 2MB)에는 **초록 본문까지 전부** 들어 있습니다. 공개 장소에 올리지 않도록 안내하세요.

## 개발 (템플릿을 고칠 때)

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
