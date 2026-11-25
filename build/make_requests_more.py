# -*- coding: utf-8 -*-
"""2차 본문 그림 13장 요청 꾸러미(docs/image_requests_more). 원본은 content_extra.py."""
import os, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_extra import EXTRA
from make_requests import HEAD_VAR
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests_more"); os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
CONV = [("C06_part1_3", "1~3부 추가 본문", "moa·sia·haru anime_base와 sheet", [b for no, _, b in EXTRA if no <= 3]),
        ("C07_part4_7", "4~7부 추가 본문", "haru·sia·moa anime_base와 sheet, doctor_sheet", [b for no, _, b in EXTRA if no >= 4])]
rows = []; n = 0
for cid, title, att, items in CONV:
    md = f"# {cid[:3]} · {title} — " + ", ".join(i[0] for i in items) + f"\n\n**첨부:** {att}\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD_VAR}\n```\n"
    for k, (file, page, part, alt, prompt, style) in enumerate(items):
        n += 1; rows.append([n, cid[:3], file, page, part, "16:9", style, ""])
        md += f"\n---\n## {k+1}) {file} — {part}\nalt: {alt}\n```\n{prompt}\n```\n"
    open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "ratio", "style", "status"]); w.writerows(rows)
open(os.path.join(D, "README.md"), "w").write(f"""# 그림 요청 꾸러미 4 — 2차 본문 그림 ({n}장)

1차에서 그림이 없던 단계에 넣는 본문 그림입니다. 모두 16:9, 패널 여러 장을 한 그림에 나란히 그립니다(1차에서 한 장에 나란히 요청한 비교가 가장 차이가 잘 나왔습니다).

| 순서 | 파일 | 장수 | 첨부 |
|---|---|---|---|
| 1 | prompts/C06_part1_3.md | 6 | moa·sia·haru 기준 그림 |
| 2 | prompts/C07_part4_7.md | 7 | haru·sia·moa 기준 그림, doctor_sheet |

저장 이름은 checklist.csv의 file 이름 그대로(png). 그림 안 글자·도장 금지, 모든 인물 성인.
""")
print("more images", n)
