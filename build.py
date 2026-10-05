"""HTML 템플릿의 __DATA__ 자리에 학회 JSON 을 넣어 단일 HTML 파일을 만든다.

    python build.py steps/app.html data/conference.json dist/conference.html

Colab 노트북의 build() 헬퍼와 같은 일을 한다 (로컬 확인용).
"""
import json
import sys
from pathlib import Path


def build(template_path, data_path, out_path):
    template = Path(template_path).read_text(encoding="utf-8")
    if template.count("__DATA__") != 1:
        raise ValueError(f"{template_path}: __DATA__ 자리가 정확히 한 번 있어야 합니다")
    data = json.loads(Path(data_path).read_text(encoding="utf-8"))
    # 데이터 안의 "</script>" 가 <script> 태그를 끝내 버리지 않도록 </ 를 <\/ 로 바꾼다
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template.replace("__DATA__", js), encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    out = build(*sys.argv[1:])
    print(f"{out}: {out.stat().st_size / 1e6:.1f} MB")
