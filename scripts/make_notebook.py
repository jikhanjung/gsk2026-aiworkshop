"""실습용 Colab 노트북(gsk2026_practice.ipynb)을 만든다.

    python scripts/make_notebook.py

단계별 HTML 템플릿은 steps/*.html 을 그대로 읽어 %%writefile 셀에 넣는다 (단일 진실 원천).
템플릿을 고쳤으면 이 스크립트를 다시 돌리면 된다. nbformat 없이 JSON 을 직접 쓴다.
설명 셀과 코드 주석은 한국어·영어를 함께 쓴다 (md(ko, en), 주석은 "# EN:" 줄).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "gsk2026_practice.ipynb"
cells = []


def md(ko, en=None):
    """설명 셀: 한국어 다음에 영어. / Markdown cell: Korean first, then English."""
    text = ko.strip("\n")
    if en:
        text += "\n\n---\n\n🇬🇧 **English**\n\n" + en.strip("\n")
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
# Conference Organizer(학회 시간표 앱) 만들기 실습 / Building the Conference Organizer

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
""", """
You put conference program data (JSON) into an HTML template with **Python** and build a **single-file HTML web app**
that opens in your PC browser even without internet.

| Stage | What you do | What you learn |
|---|---|---|
| Setup | define helper functions, load the data | file upload, reading JSON |
| Step 0 | explore the data | JSON structure, pandas tables |
| Step 1 | make HTML with Python only | f-strings, `html.escape` |
| Step 2 | draw the talk list with JS | array → HTML, `innerHTML`, escaping |
| Step 3 | date/room filters, search | state + `render()` pattern, events |
| Step 4 | ☆ bookmarks and My Schedule | `localStorage`, finding time clashes |
| Step 5 | finished app | tabs, detail view (`#` hash routing), bookmark export |
| Assignment | add your own features | |

Every step follows the same order:

```
run the template cell (%%writefile)  →  build()  →  preview()  →  download()  →  open it on your PC
```

> ⚠️ First do **File → Save a copy in Drive** and work in the copy.
> Run the cells in order from the top (`Ctrl + Enter` or ▶). **Chrome on a PC** is recommended.
""")

# ───────────────────────────── 준비 ─────────────────────────────
md("""
## 준비 1. 도우미 함수 / Setup 1. Helper functions

아래 셀을 실행하면 함수 세 개가 만들어집니다. 내용은 몰라도 되지만, 이름과 하는 일은 알아 두세요.

| 함수 | 하는 일 |
|---|---|
| `build("템플릿.html", "결과.html")` | 템플릿의 `__DATA__` 자리에 데이터를 넣어 결과 HTML 을 만든다 |
| `preview("결과.html")` | Colab 화면 안에서 결과 HTML 을 띄워 본다 |
| `download("결과.html")` | 결과 HTML 을 내 PC 로 내려받는다 |
""", """
Running the cell below creates three functions. You don't need to understand their code, but remember their names and what they do.

| Function | What it does |
|---|---|
| `build("template.html", "result.html")` | puts the data into the template's `__DATA__` spot and writes the result HTML |
| `preview("result.html")` | shows the result HTML inside Colab |
| `download("result.html")` | downloads the result HTML to your PC |
""")
code('''
import json, os, html, subprocess, sys, time

DATA = None

def load_data(path):
    """conference.json 을 읽어 DATA 에 넣고 개수를 보여 준다.
    Reads conference.json into DATA and prints the counts."""
    global DATA
    with open(path, encoding="utf-8") as f:
        DATA = json.load(f)
    meta = DATA["meta"]
    print(f"{meta['name']} · {meta.get('place', '')} · {meta['days'][0]} ~ {meta['days'][-1]}")
    print(f"sessions {len(DATA['sessions'])}, talks {len(DATA['talks'])}, abstracts {len(DATA['abstracts'])}")

def build(template_path, out_path):
    """템플릿의 __DATA__ 자리에 JSON 데이터를 넣어 HTML 파일 하나를 만든다.
    Puts the JSON data into the template's __DATA__ spot and writes one HTML file."""
    if DATA is None:
        raise RuntimeError("데이터가 없습니다. 위의 '준비 2. 데이터 불러오기' 셀을 먼저 실행하세요. / "
                           "No data loaded. Run the 'Setup 2. Load the data' cell above first.")
    with open(template_path, encoding="utf-8") as f:
        page = f.read()
    n = page.count("__DATA__")
    if n == 0:
        raise ValueError(f"{template_path} 에 __DATA__ 자리가 없습니다. "
                         "템플릿에 const DATA = __DATA__; 줄이 그대로 있는지 확인하세요. / "
                         f"{template_path} has no __DATA__ spot. Check that the line const DATA = __DATA__; is still there.")
    if n > 1:
        raise ValueError(f"{template_path} 에 __DATA__ 가 {n}번 있습니다. 한 번만 있어야 합니다 "
                         "(주석에 써 둔 __DATA__ 도 지우세요). / "
                         f"{template_path} contains __DATA__ {n} times; it must appear exactly once "
                         "(also remove any __DATA__ written in comments).")
    # 데이터 안에 "</script>" 같은 글자가 있으면 <script> 가 거기서 끝나 버린다.
    # 그래서 </ 를 <\\/ 로 바꿔 둔다 (JS 에서는 둘 다 같은 문자열이다).
    # EN: If the data contains text like "</script>", the <script> block would end right there,
    # EN: so we turn </ into <\\/ (both mean the same string in JS).
    js = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\\\/")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page.replace("__DATA__", js))
    print(f"{out_path} 완성 / done ({os.path.getsize(out_path) / 1e6:.1f} MB)")

PORT = 8000
_server = None

def preview(path, height=650):
    """Colab 안에 작은 웹 서버를 띄우고 그 화면을 아래에 보여 준다.
    Starts a small web server inside Colab and shows the page below the cell."""
    global _server
    try:
        from google.colab import output
    except ImportError:
        print("Colab 이 아니면 이 파일을 브라우저로 직접 여세요 / Not in Colab — open this file in your browser:", os.path.abspath(path))
        return
    if _server is None:
        _server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    # 뒤에 ?v=시각 을 붙여 브라우저가 예전 파일을 다시 쓰지 않게 한다
    # EN: add ?v=<time> so the browser doesn't reuse an old cached file
    output.serve_kernel_port_as_iframe(PORT, path=f"/{path}?v={int(time.time())}", height=height)

def download(path):
    """내 PC 로 내려받기. 반응이 없으면 왼쪽 📁 파일 패널에서 파일 → ⋮ → 다운로드.
    Download to your PC. If nothing happens, use the 📁 Files panel on the left → the file → ⋮ → Download."""
    try:
        from google.colab import files
        files.download(path)
    except ImportError:
        print("Colab 이 아닙니다. 파일 위치 / Not in Colab. File location:", os.path.abspath(path))

print("준비 완료 / ready: build, preview, download")
''')

md("""
## 준비 2. 데이터 불러오기 / Setup 2. Load the data

강사가 안내한 방법 **하나만** 실행하세요.
`sessions …, talks …, abstracts …` 처럼 개수가 출력되면 성공입니다.

> 런타임이 초기화되면(오래 쉬었을 때 등) 업로드한 파일이 사라집니다. 그때는 준비 1 부터 다시 실행하세요.

### 방법 A — 파일 업로드
셀을 실행하면 **파일 선택** 버튼이 나옵니다 → 받아 둔 `conference.json` 을 고르세요.
""", """
Run **only one** of the two methods, whichever your instructor tells you.
It worked if you see counts like `sessions …, talks …, abstracts …`.

> When the runtime is reset (e.g. after a long break), uploaded files disappear. Then run again from Setup 1.

### Method A — upload the file
Running the cell shows a **Choose Files** button → pick the `conference.json` you received.
""")
code('''
from google.colab import files

uploaded = files.upload()            # 파일 선택 버튼이 나타난다 / a "Choose Files" button appears
name = next(iter(uploaded))          # 이름이 달라도(conference (1).json 등) 그대로 쓴다 / works even if renamed (e.g. "conference (1).json")
if name != "conference.json":
    os.replace(name, "conference.json")
load_data("conference.json")
''')
md("""
### 방법 B — 구글 드라이브 연결
1. 강사가 공유한 `conference.json` 을 **내 드라이브에 바로가기 추가**(또는 사본)해 둡니다.
2. 셀을 실행하면 권한 창이 뜹니다 → 내 계정 선택 → **허용**.
3. `DATA_PATH` 를 내 파일 위치에 맞게 고칩니다 (왼쪽 📁 파일 패널 → `drive/MyDrive` 에서 파일 → ⋮ → **경로 복사**).
""", """
### Method B — connect Google Drive
1. Add a **shortcut to My Drive** (or a copy) of the `conference.json` your instructor shared.
2. Running the cell opens a permission window → choose your account → **Allow**.
3. Change `DATA_PATH` to where your file is (📁 Files panel on the left → `drive/MyDrive` → the file → ⋮ → **Copy path**).
""")
code('''
from google.colab import drive
drive.mount("/content/drive")

DATA_PATH = "/content/drive/MyDrive/conference.json"   # ← 내 파일 위치로 고치기 / change to your file's location
load_data(DATA_PATH)
''')

# ───────────────────────────── Step 0 ─────────────────────────────
md("""
## Step 0. 데이터 살펴보기 / Explore the data

`DATA` 는 파이썬 **딕셔너리**입니다. 네 부분으로 되어 있어요.

| 키 | 내용 | 주요 필드 |
|---|---|---|
| `meta` | 학회 정보 | `name`(학회명), `place`, `days`(날짜 목록) |
| `sessions` | 세션 | `code`, `title` |
| `talks` | 발표 일정 | `id`, `date`, `day_label`, `time_start`, `time_end`, `room`, `session`, `title`, `first_author`, `kind`(`talk`/`plenary`), `abstract_id` |
| `abstracts` | 초록 | `id`, `session`, `title`, `authors[]`, `affiliations[]`, `abstract`, `keywords[]` |

발표와 초록은 `talks[i].abstract_id` ↔ `abstracts[j].id` 로 연결됩니다.
`abstract_id` 가 비어 있는(`None`) 발표도 있습니다(워크숍 등). 포스터처럼 발표 일정이 없는 초록도 있고,
데이터에 따라 초록 본문(`abstract`)이 비어 있을 수 있습니다. 표로 보면 훨씬 알아보기 쉽습니다.
""", """
`DATA` is a Python **dictionary** with four parts.

| Key | Contents | Main fields |
|---|---|---|
| `meta` | conference info | `name`, `place`, `days` (list of dates) |
| `sessions` | sessions | `code`, `title` |
| `talks` | talk schedule | `id`, `date`, `day_label`, `time_start`, `time_end`, `room`, `session`, `title`, `first_author`, `kind` (`talk`/`plenary`), `abstract_id` |
| `abstracts` | abstracts | `id`, `session`, `title`, `authors[]`, `affiliations[]`, `abstract`, `keywords[]` |

Talks and abstracts are linked by `talks[i].abstract_id` ↔ `abstracts[j].id`.
Some talks have an empty (`None`) `abstract_id` (workshops etc.). Some abstracts have no scheduled talk (posters),
and depending on the data the abstract text (`abstract`) may be empty. A table makes all this much easier to see.
""")
code('''
import pandas as pd

talks = pd.DataFrame(DATA["talks"])
abstracts = pd.DataFrame(DATA["abstracts"])
talks.head()
''')
code('''
# 날짜별·장소별 발표 수
# EN: number of talks per day and per room
pd.crosstab(talks["day_label"], talks["room"], margins=True)
''')
code('''
# 발표 하나와, 그 발표에 연결된 초록 하나를 그대로 출력해 보기
# EN: print one talk and the abstract linked to it, as they are
t = next(t for t in DATA["talks"] if t["abstract_id"])
a = next(a for a in DATA["abstracts"] if a["id"] == t["abstract_id"])
print(json.dumps(t, ensure_ascii=False, indent=2))
print(json.dumps({**a, "abstract": a["abstract"][:200] + "…"}, ensure_ascii=False, indent=2))
''')
md("""
**해 볼 것**: 초록이 가장 많은 세션은? 키워드 중 가장 많이 나오는 것은?
(힌트: `abstracts["session"].value_counts()`, `abstracts["keywords"].explode().value_counts()`)
""", """
**Try it**: Which session has the most abstracts? Which keyword appears most often?
(Hint: `abstracts["session"].value_counts()`, `abstracts["keywords"].explode().value_counts()`)
""")
code('''
# 여기에 직접 해 보세요
# EN: try it yourself here

''')

# ───────────────────────────── Step 1 ─────────────────────────────
md("""
## Step 1. 파이썬만으로 HTML 만들기 / HTML with Python only

웹 페이지는 결국 **글자(텍스트) 파일**입니다. 파이썬 f-string 으로 HTML 글자를 만들어 파일에 쓰면 끝!

⚠️ 제목에 `<` 나 `&` 같은 글자가 있으면 HTML 이 깨집니다. 그래서 `html.escape()` 로 바꿔 넣습니다.
""", """
A web page is in the end just a **text file**. Build the HTML text with Python f-strings, write it to a file — done!

⚠️ Characters like `<` or `&` in a title break the HTML, so we pass them through `html.escape()`.
""")
code('''
# 첫날 발표만 골라 <li> 목록을 글자로 만든다
# EN: pick the first day's talks and build an <li> list as text
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
  <p>발표 {len(day_talks)}건 / {len(day_talks)} talks</p>
  <ul>{"".join(items)}</ul>
</body>
</html>"""

with open("step1.html", "w", encoding="utf-8") as f:
    f.write(page)
print("step1.html 완성 / done")
preview("step1.html", height=400)
''')
md("""
잘 나오죠? 그런데 **날짜를 바꿔 보거나, 검색하려면** 어떻게 해야 할까요?
파이썬은 파일을 만들 때 한 번만 실행되니, 날짜마다 · 검색어마다 파일을 따로 만들어야 합니다. 😵

→ 그래서 **데이터는 통째로 HTML 에 넣어 두고**, 화면은 브라우저 안의 **자바스크립트(JS)** 가 그리게 합니다.

**해 볼 것**: 둘째 날 목록으로 바꿔 보기, 기조강연(`kind == "plenary"`)만 굵게 표시하기.
""", """
Looks good? But how would you **switch the date or search**?
Python runs only once when it makes the file, so you'd need a separate file for every date and every search term. 😵

→ So we **put all the data into the HTML** and let **JavaScript (JS)** in the browser draw the screen.

**Try it**: switch to the second day's list; make only plenary talks (`kind == "plenary"`) bold.
""")
code('download("step1.html")      # 내려받아 더블클릭으로 열어 보기 / download it and open it by double-clicking')

# ───────────────────────────── Step 2~4, 완성본 ─────────────────────────────
STEPS = [
    ("step2_list.html", "Step 2. JS 로 목록 그리기 / Draw the list with JS", """
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
""", """
From here on we use a **template HTML**, and Python only inserts the data.

```html
<script>
const DATA = __DATA__;      ← build() replaces this spot with the JSON
</script>
```

JSON comes from JavaScript syntax, so pasted in as-is it becomes a JS object.
Then JS draws the screen: `DATA.talks.filter(...)` → `` `<div>${...}</div>` `` (template literal) → `innerHTML`.
Don't forget to escape with `esc()` in JS too.

The cell below creates the template file with `%%writefile`. **Edit the HTML in the cell and run it again** to save the changed template.
"""),
    ("step3_filter.html", "Step 3. 날짜·장소 필터와 검색 / Date & room filters, search", """
화면에 영향을 주는 값(고른 날짜, 고른 장소, 검색어)을 `state` 한곳에 모아 둡니다.

1. 사용자가 칩을 누르거나 글자를 입력하면 → **`state` 만 바꾸고**
2. **`render()`** 가 `state` 를 보고 화면 전체를 다시 그립니다.

이 **state → render** 패턴은 React 같은 큰 프레임워크도 똑같이 씁니다.
장소 칩 목록은 데이터에서 뽑아내므로(`new Set(DATA.talks.map(t => t.room))`) 다른 학회 데이터를 넣어도 그대로 동작합니다.
""", """
Keep every value that affects the screen (selected date, selected room, search term) together in one `state`.

1. When the user clicks a chip or types → **only change `state`**
2. **`render()`** looks at `state` and redraws the whole screen.

Big frameworks like React use exactly this **state → render** pattern.
The room chips are taken from the data (`new Set(DATA.talks.map(t => t.room))`), so it still works with another conference's data.
"""),
    ("step4_bookmark.html", "Step 4. 북마크와 내 일정 / Bookmarks and My Schedule", """
☆ 를 누르면 발표 id 를 `Set` 에 넣고 **`localStorage`** 에 저장합니다.
`localStorage` 는 브라우저가 사이트(파일)별로 주는 작은 저장 공간이라, 페이지를 닫았다 열어도 북마크가 남아 있어요.

- 저장은 **글자만** 됩니다 → `JSON.stringify` 로 바꿔 저장, `JSON.parse` 로 꺼내기
- 브라우저 설정에 따라 막힐 수 있으므로 `try / catch` 로 감쌉니다
- **내 일정** 탭: 날짜별로 모아 시간순으로 보여 주고, 시간이 겹치는 발표는 빨갛게 표시합니다.
  `"09:30" < "10:00"` 처럼 `HH:MM` 글자는 그대로 비교해도 시간 순서가 맞습니다.
- 목록은 계속 다시 그려지므로, 클릭 이벤트는 바깥(`main`)에 **한 번만** 걸고 무엇을 눌렀는지 확인합니다 (이벤트 위임).

⚠️ Colab 미리보기와 내려받은 파일은 **서로 다른 저장 공간**을 씁니다. 미리보기에서 찍은 북마크는 PC 파일에 없어요.
""", """
Clicking ☆ puts the talk id into a `Set` and saves it to **`localStorage`**.
`localStorage` is a small storage space the browser gives each site (file), so bookmarks survive closing and reopening the page.

- It stores **text only** → save with `JSON.stringify`, read back with `JSON.parse`
- It can be blocked by browser settings, so wrap it in `try / catch`
- **My Schedule** tab: groups bookmarks by date in time order and marks clashing talks in red.
  `HH:MM` strings compare correctly as text, e.g. `"09:30" < "10:00"`.
- The list keeps being redrawn, so attach the click listener **once** to the outer element (`main`) and check what was clicked (event delegation).

⚠️ The Colab preview and the downloaded file use **separate storage**. Bookmarks made in the preview are not in the file on your PC.
"""),
    ("app.html", "Step 5. 완성본 / The finished app", """
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
""", """
This combines everything so far and adds a few things.

- **Bottom tabs**: Program / Sessions / Search / My Schedule
- **Hash routing**: the end of the address (`#/talk/12`, `#/session/...`) decides which view to draw.
  Back and refresh work even when opened as a file (`file://`).
- **Talk detail**: abstract text, authors, affiliations, keywords (click a keyword to search)
- **Search**: title, authors, keywords and also the **abstract text**. If it matches only the text, the surrounding sentence is shown.
- **`Map` index**: `id → talk` lookups prepared in advance for speed.
- **Export/Import**: save bookmarks to a `bookmarks.json` file and load them on another PC.
- Uses the same storage key as Step 4. Chrome lets local HTML files on your PC share storage, so Step 4 bookmarks show up here too (this is normal).

The template is long, so it's handy to collapse the cell. When you're done, `download()` it and open it on your PC.
"""),
]

TIPS = """
> **템플릿 셀 규칙** — 첫 줄 `%%writefile …` 과 `const DATA = __DATA__;` 의 `__DATA__` 는 그대로 두세요.
> 템플릿을 고쳤다면 **템플릿 셀 → 아래 build 셀** 순서로 둘 다 다시 실행해야 반영됩니다.
> 화면이 하얗게 나오면 내려받은 파일을 Chrome 으로 열고 `F12` → **Console** 에서 빨간 오류를 확인하세요.
"""
TIPS_EN = """
> **Template cell rules** — leave the first line `%%writefile …` and the `__DATA__` in `const DATA = __DATA__;` as they are.
> After editing a template, re-run **the template cell, then the build cell below it** for the change to take effect.
> If the page comes out blank white, open the downloaded file in Chrome and look for red errors in `F12` → **Console**.
"""
for i, (name, title, intro, intro_en) in enumerate(STEPS, start=2):
    out = f"out_step{i}.html"
    md(f"## {title}\n{intro}{TIPS if i == 2 else ''}", f"{intro_en}{TIPS_EN if i == 2 else ''}")
    code(f"%%writefile {name}\n" + template(name))
    code(f'build("{name}", "{out}")\npreview("{out}")')
    code(f'download("{out}")')

# ───────────────────────────── 과제 ─────────────────────────────
md("""
## 과제 아이디어 / Assignment ideas

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
""", """
In order of difficulty. Edit the Step 5 template cell (`app.html`), then re-run the build cell to check.

1. Show a summary like "N talks · M sessions" at the top of the first screen
2. Show the session title when hovering over a talk card (`title` attribute)
3. Show the bookmark count as a badge next to the My Schedule tab name
4. A dark-mode button (switch CSS variables)
5. A clean **printable** My Schedule (`@media print`)
6. Keyword cloud: collect abstract keywords by frequency; click one to search
7. Export My Schedule as a calendar file (`.ics`)

Python-side assignment: make a small HTML with just one session (filter `DATA`, then `build()`).
If you get stuck, look for similar parts in the finished app's code.

> ⚠️ The HTML you made contains the whole dataset, including abstract text. Don't post it anywhere public (web, GitHub, social media).
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
