# -*- coding: utf-8 -*-
"""'프롬프트로 직접 만들어 보기'의 B 결과 그림 요청 꾸러미(docs/image_requests_make) 생성. A 결과를 먼저 받은 뒤 요청한다."""
import os, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_make import MAKE
from make_requests import PROMPTS, ATTACH_OF, CONV_OF
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests_make")
os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
HEAD = ("해설 페이지의 '직접 만들어 보기' 비교 그림을 만들어 줘.\n- 첨부한 그림(이미 만든 A 결과)과 똑같은 캐릭터·구도·빛을 유지하고, 아래 'Change only'에 적힌 것만 바꿀 것\n"
        "- 비율은 첨부한 A 결과와 같게\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·교복 느낌·어려 보이는 얼굴 금지\n- 그림 안에 글자·숫자·글씨·도장·로고 금지")
PAGES = ["", "01_era", "02_line", "03_mono", "04_proportion", "05_expression", "06_media_outfit", "07_failure_lab"]
rows = []; n = 0
for no in range(1, 8):
    cid = f"M0{no}_part{no}"
    md = f"# {cid[:3]} · {no}부 '직접 만들어 보기' 비교 그림\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD}\n```\n"
    for t in MAKE[no]:
        for k in t["b_imgs"]:
            n += 1; a = PROMPTS[t["key"]]; ratio = "16:9" if "16:9" in a[4].split("\n")[0] else "2:3"
            if k in ("f1_fixed", "f8_fixed"):
                att = f"{t['key']}.png (A 결과)"; how = "그림 생성이 아니라 '부분 수정(영역 칠하기)' 기능으로 — " + ("머리 부분만 칠하기" if k == "f1_fixed" else "글씨·도장 부분만 칠하기")
            else:
                att = f"{t['key']}.png (A 결과) + {ATTACH_OF[CONV_OF[t['key']]]}"; how = "A 결과를 첨부하고 Change only 문장으로"
            rows.append([n, cid[:3], k, f"{PAGES[no]}.html#make", ratio, how, ""])
            md += f"\n---\n## {k} — {t['title']}\n첨부: {att}\n방법: {how}\n```\n{t['b_text']}\n```\n"
    open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "ratio", "how", "status"]); w.writerows(rows)
open(os.path.join(D, "README.md"), "w").write(f"""# 그림 요청 꾸러미 2 — '프롬프트로 직접 만들어 보기' 비교 그림 ({n}장)

부마다 '프롬프트로 직접 만들어 보기' 실습의 **B 결과**(원리를 빼거나 바꾼 비교 그림)입니다. **꾸러미 1(docs/image_requests)의 A 결과를 먼저 받은 뒤** 요청합니다.

## 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 장수 | 방법 |
|---|---|---|---|
| 1~6 | prompts/M01~M06 | 부마다 2 | A 결과를 첨부하고 Change only 문장 |
| 7 | prompts/M07_part7.md | 2 | f1·f8은 **부분 수정(영역 칠하기)** |

## 주의
- 'Change only' 문장만 바꾸고 나머지(캐릭터·구도·빛)는 A와 같아야 비교가 됩니다. 구도가 흔들리면 'keep the same framing'을 덧붙입니다.
- 비교 그림이 A와 거의 같게 나오면 새 대화에서 처음부터 한 번 더 시도해 주세요. 그래도 같으면 그대로 주셔도 됩니다(페이지에 있는 그대로 적습니다).
""")
print("make images", n)
