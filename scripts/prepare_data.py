"""strati2026 파싱 산출물(output/*.json)을 실습용 JSON 한 파일로 합친다.

    python scripts/prepare_data.py [strati2026_output_dir]

결과: data/conference.json
  meta      학회 이름·장소·날짜 목록
  sessions  [{code, title}]
  talks     [{id, date, day_label, time_start, time_end, room, session, title, first_author, kind, abstract_id}]
  abstracts [{id, session, title, authors, affiliations, abstract, keywords}]
"""
import json
import sys
from datetime import datetime
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "projects/strati2026/output")
OUT = Path(__file__).resolve().parent.parent / "data/conference.json"
YEAR = 2026


def iso_date(label):  # "June 29" -> "2026-06-29"
    return datetime.strptime(f"{label} {YEAR}", "%B %d %Y").strftime("%Y-%m-%d")


def hhmm(s):  # "8:50" -> "08:50" (문자열 비교로 시간 순서를 맞추려고 두 자리로 통일)
    if not s:
        return s
    h, m = s.split(":")
    return f"{int(h):02d}:{m}"


def load(name, key):
    return json.loads((SRC / f"{name}.json").read_text(encoding="utf-8"))[key]


sessions = [{"code": s["code"], "title": s["title"]} for s in load("sessions", "sessions")]

talks = []
for t in load("program", "talks"):
    talks.append({
        "id": t["id"],
        "date": iso_date(t["date"]),
        "day_label": t["date"],
        "time_start": hhmm(t["time_start"]),
        "time_end": hhmm(t["time_end"]),
        "room": t["room"] or "Main Hall",  # 기조강연(plenary)은 room 이 비어 있음
        "session": t["session"],
        "title": t["title"],
        "first_author": t["first_author"],
        "kind": t["kind"],
        "abstract_id": t["abstract_id"],
    })
talks.sort(key=lambda t: (t["date"], t["time_start"], t["room"]))

abstracts = []
for a in load("abstracts", "abstracts"):
    abstracts.append({
        "id": a["id"],
        "session": a["session"],
        "title": a["title"],
        "authors": [au["name"] for au in a["authors"]],
        "affiliations": a["affiliations_raw"],
        "abstract": a["abstract"],
        "keywords": a["keywords"],
    })

days = sorted({t["date"] for t in talks})
data = {
    "meta": {
        "name": "STRATI 2026",
        "full_name": "5th International Congress on Stratigraphy",
        "place": "Suzhou, China",
        "days": days,
        "note": "실습용 데이터 — 학회 핸드북·초록집 PDF에서 자동 추출. 재배포 금지.",
    },
    "sessions": sessions,
    "talks": talks,
    "abstracts": abstracts,
}
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{OUT}: sessions {len(sessions)}, talks {len(talks)}, abstracts {len(abstracts)}, "
      f"{OUT.stat().st_size / 1e6:.1f} MB")
