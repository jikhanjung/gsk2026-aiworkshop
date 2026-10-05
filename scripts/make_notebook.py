"""실습용 Colab 노트북(gsk2026_practice.ipynb)을 만든다.

    python scripts/make_notebook.py

단계별 HTML 템플릿은 steps/*.html 을 그대로 읽어 %%writefile 셀에 넣는다 (단일 진실 원천).
템플릿을 고쳤으면 이 스크립트를 다시 돌리면 된다. nbformat 없이 JSON 을 직접 쓴다.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "gsk2026_practice.ipynb"
cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": _lines(text)})


def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                  "outputs": [], "source": _lines(text)})


def _lines(text):
    text = text.strip("\n")
    lines = text.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def template(name):
    return (ROOT / "steps" / name).read_text(encoding="utf-8")


# ───────────────────────────── 소개 ─────────────────────────────
md("""
# 학회 프로그램 웹앱 만들기 실습

학회 프로그램 데이터(JSON)를 **파이썬**으로 HTML 템플릿에 넣어서,
인터넷 없이도 내 PC 브라우저에서 열리는 **HTML 파일 하나짜리 웹앱**을 만듭니다.

| 단계 | 하는 일 | 배우는 것 |
|---|---|---|
| 준비 | 도우미 함수 정의, 데이터 불러오기 | 파일 업로드, JSON 읽기 |
| Step 0 | 데이터 살펴보기 | JSON 구조, pandas 표 |
| Step 1 | 파이썬만으로 HTML 만들기 | f-string, `html.escape` |
| Step 2 | JS 로 발표 목록 그리기 | 배열 → HTML, `innerHTML`, 이스케이프 |
| Step 3 | 날짜·장소 필터, 검색 | 상태(state) + `render()` 패턴, 이벤트 |
| Step 4 | ☆ 북마크와 내 일정 | `localStorage`, 시간 겹침 계산 |
| Step 5 | 완성본 | 탭·상세 화면(주소 `#` 라우팅), 북마크 내보내기 |
| 과제 | 직접 기능 추가 | |

모든 단계는 같은 순서로 진행합니다.

```
템플릿 셀(%%writefile) 실행  →  build()  →  preview()  →  download()  →  내 PC 에서 열기
```

> ⚠️ **파일 → 드라이브에 사본 저장** 을 먼저 하고, 사본에서 작업하세요.
> 셀은 위에서부터 순서대로 실행합니다 (`Ctrl + Enter` 또는 ▶).
> 브라우저는 **PC 의 Chrome** 을 권장합니다.
""")

# ───────────────────────────── 준비 ─────────────────────────────
md("""
## 준비 1. 도우미 함수

아래 셀을 실행하면 함수 세 개가 만들어집니다. 내용은 몰라도 되지만, 이름과 하는 일은 알아 두세요.

| 함수 | 하는 일 |
|---|---|
| `build("템플릿.html", "결과.html")` | 템플릿의 `__DATA__` 자리에 데이터를 넣어 결과 HTML 을 만든다 |
| `preview("결과.html")` | Colab 화면 안에서 결과 HTML 을 띄워 본다 |
| `download("결과.html")` | 결과 HTML 을 내 PC 로 내려받는다 |
""")
code('''
import json, os, html, subprocess, sys, time

DATA = None

def load_data(path):
    """conference.json 을 읽어 DATA 에 넣고 개수를 보여 준다."""
    global DATA
    with open(path, encoding="utf-8") as f:
        DATA = json.load(f)
    meta = DATA["meta"]
    print(f"{meta['name']} · {meta.get('place', '')} · {meta['days'][0]} ~ {meta['days'][-1]}")
    print(f"sessions {len(DATA['sessions'])}, talks {len(DATA['talks'])}, abstracts {len(DATA['abstracts'])}")

def build(template_path, out_path):
    """템플릿의 __DATA__ 자리에 JSON 데이터를 넣어 HTML 파일 하나를 만든다."""
    if DATA is None:
        raise RuntimeError("데이터가 없습니다. 위의 '준비 2. 데이터 불러오기' 셀을 먼저 실행하세요.")
    with open(template_path, encoding="utf-8") as f:
        page = f.read()
    n = page.count("__DATA__")
    if n == 0:
        raise ValueError(f"{template_path} 에 __DATA__ 자리가 없습니다. "
                         "템플릿에 const DATA = __DATA__; 줄이 그대로 있는지 확인하세요.")
    if n > 1:
        raise ValueError(f"{template_path} 에 __DATA__ 가 {n}번 있습니다. 한 번만 있어야 합니다 "
                         "(주석에 써 둔 __DATA__ 도 지우세요).")
    # 데이터 안에 "</script>" 같은 글자가 있으면 <script> 가 거기서 끝나 버린다.
    # 그래서 </ 를 <\\/ 로 바꿔 둔다 (JS 에서는 둘 다 같은 문자열이다).
    js = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\\\/")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page.replace("__DATA__", js))
    print(f"{out_path} 완성 ({os.path.getsize(out_path) / 1e6:.1f} MB)")

PORT = 8000
_server = None

def preview(path, height=650):
    """Colab 안에 작은 웹 서버를 띄우고 그 화면을 아래에 보여 준다."""
    global _server
    try:
        from google.colab import output
    except ImportError:
        print("Colab 이 아니면 이 파일을 브라우저로 직접 여세요:", os.path.abspath(path))
        return
    if _server is None:
        _server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    # 뒤에 ?v=시각 을 붙여 브라우저가 예전 파일을 다시 쓰지 않게 한다
    output.serve_kernel_port_as_iframe(PORT, path=f"/{path}?v={int(time.time())}", height=height)

def download(path):
    """내 PC 로 내려받기. 반응이 없으면 왼쪽 📁 파일 패널에서 파일 → ⋮ → 다운로드."""
    try:
        from google.colab import files
        files.download(path)
    except ImportError:
        print("Colab 이 아닙니다. 파일 위치:", os.path.abspath(path))

print("준비 완료: build, preview, download")
''')

md("""
## 준비 2. 데이터 불러오기

강사가 안내한 방법 **하나만** 실행하세요.
`sessions …, talks …, abstracts …` 처럼 개수가 출력되면 성공입니다.

> 런타임이 초기화되면(오래 쉬었을 때 등) 업로드한 파일이 사라집니다. 그때는 준비 1 부터 다시 실행하세요.

### 방법 A — 파일 업로드
셀을 실행하면 **파일 선택** 버튼이 나옵니다 → 받아 둔 `conference.json` 을 고르세요.
""")
code('''
from google.colab import files

uploaded = files.upload()            # 파일 선택 버튼이 나타난다
name = next(iter(uploaded))          # 이름이 달라도(conference (1).json 등) 그대로 쓴다
if name != "conference.json":
    os.replace(name, "conference.json")
load_data("conference.json")
''')
md("""
### 방법 B — 구글 드라이브 연결
1. 강사가 공유한 `conference.json` 을 **내 드라이브에 바로가기 추가**(또는 사본)해 둡니다.
2. 셀을 실행하면 권한 창이 뜹니다 → 내 계정 선택 → **허용**.
3. `DATA_PATH` 를 내 파일 위치에 맞게 고칩니다 (왼쪽 📁 파일 패널 → `drive/MyDrive` 에서 파일 → ⋮ → **경로 복사**).
""")
code('''
from google.colab import drive
drive.mount("/content/drive")

DATA_PATH = "/content/drive/MyDrive/conference.json"   # ← 내 파일 위치로 고치기
load_data(DATA_PATH)
''')

# ───────────────────────────── Step 0 ─────────────────────────────
md("""
## Step 0. 데이터 살펴보기

`DATA` 는 파이썬 **딕셔너리**입니다. 네 부분으로 되어 있어요.

| 키 | 내용 | 주요 필드 |
|---|---|---|
| `meta` | 학회 정보 | `name`(학회명), `place`, `days`(날짜 목록) |
| `sessions` | 세션 | `code`, `title` |
| `talks` | 발표 일정 | `id`, `date`, `day_label`, `time_start`, `time_end`, `room`, `session`, `title`, `first_author`, `kind`(`talk`/`plenary`), `abstract_id` |
| `abstracts` | 초록 | `id`, `session`, `title`, `authors[]`, `affiliations[]`, `abstract`, `keywords[]` |

발표와 초록은 `talks[i].abstract_id` ↔ `abstracts[j].id` 로 연결됩니다.
`abstract_id` 가 비어 있는(`None`) 발표도 있습니다(기조강연 등). 표로 보면 훨씬 알아보기 쉽습니다.
""")
code('''
import pandas as pd

talks = pd.DataFrame(DATA["talks"])
abstracts = pd.DataFrame(DATA["abstracts"])
talks.head()
''')
code('''
# 날짜별·장소별 발표 수
pd.crosstab(talks["day_label"], talks["room"], margins=True)
''')
code('''
# 발표 하나와, 그 발표에 연결된 초록 하나를 그대로 출력해 보기
t = next(t for t in DATA["talks"] if t["abstract_id"])
a = next(a for a in DATA["abstracts"] if a["id"] == t["abstract_id"])
print(json.dumps(t, ensure_ascii=False, indent=2))
print(json.dumps({**a, "abstract": a["abstract"][:200] + "…"}, ensure_ascii=False, indent=2))
''')
md("""
**해 볼 것**: 초록이 가장 많은 세션은? 키워드 중 가장 많이 나오는 것은?
(힌트: `abstracts["session"].value_counts()`, `abstracts["keywords"].explode().value_counts()`)
""")
code('''
# 여기에 직접 해 보세요

''')

# ───────────────────────────── Step 1 ─────────────────────────────
md("""
## Step 1. 파이썬만으로 HTML 만들기

웹 페이지는 결국 **글자(텍스트) 파일**입니다. 파이썬 f-string 으로 HTML 글자를 만들어 파일에 쓰면 끝!

⚠️ 제목에 `<` 나 `&` 같은 글자가 있으면 HTML 이 깨집니다. 그래서 `html.escape()` 로 바꿔 넣습니다.
""")
code('''
first_day = DATA["meta"]["days"][0]
day_talks = [t for t in DATA["talks"] if t["date"] == first_day]

items = []
for t in day_talks:
    items.append(f"""
    <li>
      <b>{t["time_start"]}–{t["time_end"]}</b> · {html.escape(t["room"])}<br>
      {html.escape(t["title"])}<br>
      <small>{html.escape(t["first_author"] or "")}</small>
    </li>""")

page = f"""<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><title>{html.escape(DATA["meta"]["name"])}</title></head>
<body>
  <h1>{html.escape(DATA["meta"]["name"])} — {html.escape(day_talks[0]["day_label"])}</h1>
  <p>발표 {len(day_talks)}건</p>
  <ul>{"".join(items)}</ul>
</body>
</html>"""

with open("step1.html", "w", encoding="utf-8") as f:
    f.write(page)
print("step1.html 완성")
preview("step1.html", height=400)
''')
md("""
잘 나오죠? 그런데 **날짜를 바꿔 보거나, 검색하려면** 어떻게 해야 할까요?
파이썬은 파일을 만들 때 한 번만 실행되니, 날짜마다 · 검색어마다 파일을 따로 만들어야 합니다. 😵

→ 그래서 **데이터는 통째로 HTML 에 넣어 두고**, 화면은 브라우저 안의 **자바스크립트(JS)** 가 그리게 합니다.

**해 볼 것**: 둘째 날 목록으로 바꿔 보기, 기조강연(`kind == "plenary"`)만 굵게 표시하기.
""")
code('download("step1.html")      # 내려받아 더블클릭으로 열어 보기')

# ───────────────────────────── Step 2~4, 완성본 ─────────────────────────────
STEPS = [
    ("step2_list.html", "Step 2. JS 로 목록 그리기", """
이제부터는 **템플릿 HTML** 을 쓰고, 파이썬은 데이터만 넣어 줍니다.

```html
<script>
const DATA = __DATA__;      ← build() 가 이 자리를 JSON 으로 바꾼다
</script>
```

JSON 은 원래 자바스크립트 문법에서 나온 것이라, 그대로 넣으면 JS 객체가 됩니다.
그다음은 JS 가 `DATA.talks.filter(...)` → `` `<div>${...}</div>` `` (템플릿 리터럴) → `innerHTML` 순서로 화면을 그립니다.
JS 에서도 `esc()` 로 이스케이프하는 것을 잊지 마세요.

아래 셀은 `%%writefile` 로 템플릿 파일을 만듭니다. **셀 안의 HTML 을 고친 뒤 다시 실행**하면 바뀐 템플릿이 저장됩니다.
"""),
    ("step3_filter.html", "Step 3. 날짜·장소 필터와 검색", """
화면에 영향을 주는 값(고른 날짜, 고른 장소, 검색어)을 `state` 한곳에 모아 둡니다.

1. 사용자가 칩을 누르거나 글자를 입력하면 → **`state` 만 바꾸고**
2. **`render()`** 가 `state` 를 보고 화면 전체를 다시 그립니다.

이 **state → render** 패턴은 React 같은 큰 프레임워크도 똑같이 씁니다.
장소 칩 목록은 데이터에서 뽑아내므로(`new Set(DATA.talks.map(t => t.room))`) 다른 학회 데이터를 넣어도 그대로 동작합니다.
"""),
    ("step4_bookmark.html", "Step 4. 북마크와 내 일정", """
☆ 를 누르면 발표 id 를 `Set` 에 넣고 **`localStorage`** 에 저장합니다.
`localStorage` 는 브라우저가 사이트(파일)별로 주는 작은 저장 공간이라, 페이지를 닫았다 열어도 북마크가 남아 있어요.

- 저장은 **글자만** 됩니다 → `JSON.stringify` 로 바꿔 저장, `JSON.parse` 로 꺼내기
- 브라우저 설정에 따라 막힐 수 있으므로 `try / catch` 로 감쌉니다
- **내 일정** 탭: 날짜별로 모아 시간순으로 보여 주고, 시간이 겹치는 발표는 빨갛게 표시합니다.
  `"09:30" < "10:00"` 처럼 `HH:MM` 글자는 그대로 비교해도 시간 순서가 맞습니다.
- 목록은 계속 다시 그려지므로, 클릭 이벤트는 바깥(`main`)에 **한 번만** 걸고 무엇을 눌렀는지 확인합니다 (이벤트 위임).

⚠️ Colab 미리보기와 내려받은 파일은 **서로 다른 저장 공간**을 씁니다. 미리보기에서 찍은 북마크는 PC 파일에 없어요.
"""),
    ("app.html", "Step 5. 완성본", """
지금까지 배운 것을 모두 합치고 몇 가지를 더했습니다.

- **하단 탭**: 프로그램 / 세션 / 검색 / 내 일정
- **hash 라우팅**: 주소 끝의 `#/talk/12`, `#/session/...` 을 보고 어떤 화면을 그릴지 정합니다.
  파일로 열어도(`file://`) 뒤로가기·새로고침이 됩니다.
- **발표 상세**: 초록 본문, 저자, 소속, 키워드 (키워드를 누르면 검색)
- **검색**: 제목·저자·키워드에 더해 **초록 본문**까지. 본문에서만 찾으면 앞뒤 문장을 보여 줍니다.
- **`Map` 색인**: `id → 발표` 를 미리 만들어 두어 빠르게 찾습니다.
- **내보내기/불러오기**: 북마크를 `bookmarks.json` 파일로 저장하고, 다른 PC 에서 불러올 수 있습니다.
- Step 4 와 같은 저장 키를 씁니다. Chrome 은 내 PC 의 HTML 파일들이 저장 공간을 함께 쓰므로 Step 4 에서 한 북마크가 여기서도 보입니다 (정상).

템플릿이 길어서 셀을 접어 두는 게 편합니다. 다 만들었으면 `download()` 로 내려받아 PC 에서 열어 보세요.
"""),
]

TIPS = """
> **템플릿 셀 규칙** — 첫 줄 `%%writefile …` 과 `const DATA = __DATA__;` 의 `__DATA__` 는 그대로 두세요.
> 템플릿을 고쳤다면 **템플릿 셀 → 아래 build 셀** 순서로 둘 다 다시 실행해야 반영됩니다.
> 화면이 하얗게 나오면 내려받은 파일을 Chrome 으로 열고 `F12` → **Console** 에서 빨간 오류를 확인하세요.
"""
for i, (name, title, intro) in enumerate(STEPS, start=2):
    out = f"out_step{i}.html"
    md(f"## {title}\n{intro}{TIPS if i == 2 else ''}")
    code(f"%%writefile {name}\n" + template(name))
    code(f'build("{name}", "{out}")\npreview("{out}")')
    code(f'download("{out}")')

# ───────────────────────────── 과제 ─────────────────────────────
md("""
## 과제 아이디어

난이도 순서입니다. Step 5 템플릿 셀(`app.html`)을 고친 뒤 build 셀을 다시 실행해 확인하세요.

1. 첫 화면 위쪽에 "총 발표 N건 · 세션 M개" 요약 표시
2. 발표 카드에 세션 제목을 마우스를 올렸을 때 보이게(`title` 속성)
3. 내 일정에서 북마크 개수를 탭 이름 옆에 배지로 표시
4. 다크 모드 버튼 (CSS 변수 바꾸기)
5. 내 일정을 **인쇄용**으로 깔끔하게 (`@media print`)
6. 키워드 구름: 초록 키워드를 많이 나온 순서로 모아 보여 주고, 누르면 검색
7. 내 일정을 캘린더 파일(`.ics`)로 내보내기

파이썬 쪽 과제: 세션 하나만 담은 작은 HTML 만들기 (`DATA` 를 걸러서 `build()`).
막히면 완성본 코드에서 비슷한 부분을 찾아보세요.

> ⚠️ 만든 HTML 에는 초록 본문까지 데이터 전체가 들어 있습니다. 공개된 곳(웹·GitHub·SNS)에 올리지 마세요.
""")

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    },
    "cells": [{**c, "id": f"cell{i:02d}"} for i, c in enumerate(cells)],
}
OUT.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{OUT.relative_to(ROOT)}: 셀 {len(cells)}개")
