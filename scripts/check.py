"""전체 검증: 빌드 → JS 문법 검사 → 노트북 검사 → (jsdom 이 있으면) 렌더 스모크 테스트.

    python scripts/check.py
    NODE_PATH=/path/to/node_modules python scripts/check.py   # jsdom 스모크 테스트까지

필요: node. 스모크 테스트는 `npm i jsdom` 한 node_modules 를 NODE_PATH 로 지정.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build import build  # noqa: E402

STEPS = ["step2_list", "step3_filter", "step4_bookmark", "app"]
DATA = ROOT / "data/conference.json"
DIST = ROOT / "dist"
failed = []


def check(name, ok, detail=""):
    print(f"{'  ok  ' if ok else '  FAIL'} {name}{' — ' + detail if detail else ''}")
    if not ok:
        failed.append(name)


def node_check(html_path):
    scripts = re.findall(r"<script>(.*?)</script>", Path(html_path).read_text(encoding="utf-8"), re.S)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write("\n".join(scripts))
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    return r.returncode == 0, r.stderr.strip().splitlines()[-1:] if r.returncode else ""


print("[1] 빌드 + JS 문법")
for s in STEPS:
    out = build(ROOT / f"steps/{s}.html", DATA, DIST / f"{s}.html")
    ok, err = node_check(out)
    check(f"{s}.html", ok, str(err))

# 데이터에 </script> 가 들어 있어도 <script> 가 끊기지 않는지 (</ → <\/ 이스케이프)
data = json.loads(DATA.read_text(encoding="utf-8"))
data["talks"][0]["title"] = "</script><b>깨짐?</b>"
with tempfile.TemporaryDirectory() as tmp:
    bad = Path(tmp) / "data.json"
    bad.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    out = build(ROOT / "steps/app.html", bad, Path(tmp) / "app.html")
    ok, err = node_check(out)
    check("</script> 이 든 데이터", ok, str(err))

print("[2] 노트북")
nb_path = ROOT / "gsk2026_practice.ipynb"
try:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    check("JSON 유효", nb.get("nbformat") == 4 and isinstance(nb.get("cells"), list))
    ids = [c.get("id") for c in nb["cells"]]
    check("셀 id 고유", len(set(ids)) == len(ids) and all(ids))
    written = {}
    for c in nb["cells"]:
        src = "".join(c["source"])
        if c["cell_type"] == "code" and src.startswith("%%writefile"):
            first, body = src.split("\n", 1)
            written[first.split()[1]] = body
        elif c["cell_type"] == "code" and not src.startswith("%"):
            compile(src, "cell", "exec")
    check("파이썬 셀 문법", True)
    for s in STEPS:
        same = written.get(f"{s}.html", "").rstrip() == (ROOT / f"steps/{s}.html").read_text(encoding="utf-8").rstrip()
        check(f"%%writefile {s}.html == steps/{s}.html", same, "" if same else "make_notebook.py 다시 실행")
except (OSError, ValueError, SyntaxError) as e:
    check("노트북 읽기", False, repr(e))

print("[3] 렌더 스모크 테스트 (jsdom)")
r = subprocess.run(["node", "-e", "require('jsdom')"], capture_output=True)
if r.returncode:
    print("  skip  jsdom 없음 (NODE_PATH 지정)")
else:
    r = subprocess.run(["node", "scripts/smoke_test.js", "dist"], cwd=ROOT, capture_output=True, text=True)
    print(r.stdout.rstrip())
    check("smoke_test.js", r.returncode == 0, r.stderr.strip()[-300:])

print("\n" + (f"{len(failed)}개 실패: {failed}" if failed else "모두 통과"))
sys.exit(1 if failed else 0)
