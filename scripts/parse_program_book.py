"""대한지질학회 추계학술대회 프로그램북 PDF → data/conference.json (실습 데이터 스키마).

    python scripts/parse_program_book.py [프로그램북.pdf]
    (기본: data/src/gsk2025_program_book.pdf, 필요: pip install pymupdf)

프로그램북에는 초록 본문이 없다. 그래서
  talks      구두발표 (날짜·시간·발표장·세션·제목·저자)
  abstracts  구두발표 + 포스터의 제목·저자 목록 (abstract/keywords/affiliations 는 빈 값)
             포스터는 발표 일정이 없는 초록으로 들어간다.

PDF 구조 (2025 프로그램북 기준):
  - 쪽 위 "10. 28.화" (20pt) = 날짜, x≈62 의 큰 글씨 = 세션 머리 "S15: …", x≈421 "제1발표장" = 발표장
  - x≈58 "10:00-10:15" = 발표 시작, 그 아래 x≈123 줄들: 9.5pt 이상 = 제목, 그보다 작은 글씨 = 저자(제목 뒤) 또는 꼬리표(제목 앞)
  - 포스터는 x≈58 "P001"/"Y001", 줄은 x≈95
  - 오른쪽 가장자리(x>500)의 색인 탭과 쪽 아래(y>680) 쪽번호는 버린다
"""
import datetime
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data/src/gsk2025_program_book.pdf"
OUT = ROOT / "data/conference.json"
YEAR = 2025
WEEKDAYS = "월화수목금토일"

RE_DAY = re.compile(r"^(\d{1,2})\.\s*(\d{1,2})\.\s*([월화수목금토일])$")
RE_TIME = re.compile(r"^(\d{1,2}:\d{2})\s*[-~]\s*(\d{1,2}:\d{2})$")
RE_POSTER = re.compile(r"^([PY]\d{3})$")
RE_SESSION = re.compile(r"^([A-Z]\d{2})\s*:\s*(.+)$")
RE_ROOM = re.compile(r"^제\s*(\d+)\s*발표장$")
PLENARY_LABELS = {"특별강연", "기조강연", "기조연설"}


def hhmm(s):
    h, m = s.split(":")
    return f"{int(h):02d}:{m}"


def lines_of(page):
    """쪽의 글줄을 (x, y, 크기, 글자) 로. 색인 탭·쪽번호는 뺀다."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            text = "".join(s["text"] for s in l["spans"]).strip()
            x0, y0, x1, y1 = l["bbox"]
            if not text or x0 > 500 or y0 > 680:
                continue
            size = max(s["size"] for s in l["spans"] if s["text"].strip())
            out.append({"x": x0, "y": y0, "size": size, "text": re.sub(r"\s+", " ", text)})
    # 같은 높이(±2pt)는 왼쪽부터
    out.sort(key=lambda l: (round(l["y"] / 2), l["x"]))
    return out


def split_authors(s):
    """쉼표로 나누되 괄호 안의 쉼표는 무시한다: "김복철 (前 NST이사장, 前 KIGAM원장)"."""
    s = re.sub(r"\s+and\s+", ", ", s)
    names, depth, cur = [], 0, ""
    for ch in s:
        depth += (ch == "(") - (ch == ")")
        if ch == "," and depth == 0:
            names.append(cur); cur = ""
        else:
            cur += ch
    names.append(cur)
    names = [n.strip().rstrip("*").strip() for n in names]
    return [n for n in names if n]


def finish_item(item, sink):
    """시간/포스터 번호 아래 모아 둔 줄들 → 제목·저자·꼬리표."""
    if not item:
        return
    title, authors, labels = [], [], []
    for l in item["lines"]:
        if l["size"] >= 9.4:
            title.append(l["text"])
        elif title:
            authors.append(l["text"])
        else:
            labels.append(l["text"])
    if not title:           # 휴식·중식·개회식처럼 제목 없는 칸은 버린다
        return
    item["title"] = " ".join(title).replace(" :", ":").strip()
    item["authors"] = split_authors(", ".join(authors))
    item["labels"] = labels
    sink.append(item)


def parse(pdf):
    doc = pymupdf.open(pdf)
    orals, posters, sessions = [], [], {}
    date = room = None
    session = None          # (code, title) 또는 None
    item = None
    header_open = False     # 세션 머리가 두 줄로 이어지는지

    for page in doc:
        for l in lines_of(page):
            t, x, size = l["text"], l["x"], l["size"]

            if size >= 19 and l["y"] < 80:                    # 날짜 머리 "10. 28.화" / "10. 28.화 - 30.목"
                m = RE_DAY.match(t)
                date = f"{YEAR}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else None
                continue
            if x > 400 and RE_ROOM.match(t):                  # 발표장
                room = f"제{RE_ROOM.match(t).group(1)}발표장"
                continue
            if t.startswith("좌장"):
                continue
            if 55 <= x < 75 and size >= 11:                   # 세션 머리
                finish_item(item, orals if item and "time_start" in item else posters); item = None
                m = RE_SESSION.match(t)
                if m:
                    session = (m.group(1), m.group(2).strip())
                elif "차세대" in t:
                    session = ("Y", t)
                else:
                    session = None                            # 특별강연·개회식 등
                header_open = True
                continue
            if header_open and size >= 11 and 75 <= x < 120 and session:   # 세션 머리 둘째 줄
                session = (session[0], f"{session[1]} {t}")
                continue
            header_open = False
            if session:
                sessions.setdefault(session[0], session[1])

            m_time, m_post = RE_TIME.match(t), RE_POSTER.match(t)
            if x < 90 and (m_time or m_post):
                finish_item(item, orals if item and "time_start" in item else posters)
                if m_time:
                    item = {"date": date, "time_start": hhmm(m_time.group(1)), "time_end": hhmm(m_time.group(2)),
                            "room": room, "session": session[0] if session else None, "lines": []}
                else:
                    item = {"poster": m_post.group(1), "session": session[0] if session else None, "lines": []}
                continue
            if item is not None and x >= 90:
                item["lines"].append(l)
        # 발표 하나가 다음 쪽으로 이어지는 일은 없으므로 쪽 끝에서 마무리
        finish_item(item, orals if item and "time_start" in item else posters); item = None
    return orals, posters, sessions


def build_data(orals, posters, sessions):
    abstracts, talks = [], []

    def add_abstract(it):
        abstracts.append({
            "id": len(abstracts) + 1,
            "session": it["session"],
            "title": it["title"],
            "authors": it["authors"],
            "affiliations": [],
            "abstract": "",
            "keywords": [],
        })
        return abstracts[-1]["id"]

    orals.sort(key=lambda t: (t["date"], t["time_start"], int(re.sub(r"\D", "", t["room"]) or 0)))
    # 원문 오타 보정: 같은 발표장에서 다음 발표 시작보다 늦게 끝나면 다음 시작으로 자른다
    # (2025: "12:00-15:15" → 12:00-12:15)
    by_room = {}
    for t in orals:
        by_room.setdefault((t["date"], t["room"]), []).append(t)
    for group in by_room.values():
        for a, b in zip(group, group[1:]):
            if a["time_end"] > b["time_start"]:
                print(f"  시간 보정: {a['date']} {a['room']} {a['time_start']}-{a['time_end']} → -{b['time_start']}  {a['title'][:30]}")
                a["time_end"] = b["time_start"]
    for i, t in enumerate(orals, 1):
        plenary = any(lbl in PLENARY_LABELS for lbl in t["labels"])
        y, mo, d = map(int, t["date"].split("-"))
        wd = WEEKDAYS[datetime.date(y, mo, d).weekday()]
        talks.append({
            "id": i,
            "date": t["date"],
            "day_label": f"{mo}월 {d}일({wd})",
            "time_start": t["time_start"],
            "time_end": t["time_end"],
            "room": t["room"],
            "session": t["session"],
            "title": t["title"],
            "first_author": t["authors"][0] if t["authors"] else "",
            "kind": "plenary" if plenary else "talk",
            "abstract_id": add_abstract(t) if t["authors"] else None,
        })
    for p in sorted(posters, key=lambda p: p["poster"]):
        p["title"] = f"[{p['poster']}] {p['title']}"
        add_abstract(p)

    used = {t["session"] for t in talks} | {a["session"] for a in abstracts}
    order = lambda c: (c[0], int(c[1:]) if c[1:].isdigit() else 0)
    session_list = [{"code": c, "title": sessions[c]} for c in sorted(sessions, key=order) if c in used]
    return talks, abstracts, session_list


def main():
    orals, posters, sessions = parse(SRC)
    talks, abstracts, session_list = build_data(orals, posters, sessions)
    days = sorted({t["date"] for t in talks})
    data = {
        "meta": {
            "name": f"{YEAR} 추계지질과학연합학술대회",
            "full_name": f"{YEAR} 추계지질과학연합학술대회 및 대한지질학회 제80차 정기총회",
            "place": "해비치 호텔&리조트 제주",
            "days": days,
            "note": "실습용 데이터 — 대한지질학회 프로그램북 PDF에서 자동 추출(초록 본문 없음). 재배포 금지.",
        },
        "sessions": session_list,
        "talks": talks,
        "abstracts": abstracts,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{OUT}: sessions {len(session_list)}, talks {len(talks)} "
          f"(plenary {sum(t['kind'] == 'plenary' for t in talks)}), abstracts {len(abstracts)} "
          f"(posters {len(posters)}), {OUT.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
