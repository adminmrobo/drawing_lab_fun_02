# -*- coding: utf-8 -*-
"""구조 먼저 그리기 연구실 · 웃음 편 2 · 베리에이션 — 공유 미리보기(og) 그림. 표지 그림(assets/img/cover_*.webp)이 들어오면 그것을 잘라 쓰고, 없으면 글자+캐릭터로 만든다."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
ITEMS = [("og_index", "cover_index", "구조 먼저 그리기 연구실 · 베리에이션", "같은 캐릭터, 다른 그림", ["fruitfly", "haru", "sia", "moa", "doctor"]),
 ("og_01", "cover_01", "1부 시대 베리에이션", "그림자 단계·눈·정보량·색보정", ["doctor", "moa", "fruitfly"]),
 ("og_02", "cover_02", "2부 선과 지역 베리에이션", "굵기 비·칠·단순화·효과선", ["doctor", "sia", "fruitfly"]),
 ("og_03", "cover_03", "3부 흑백·선화 베리에이션", "움직임 선·망점·여백·회색값", ["moa", "sia", "haru"]),
 ("og_04", "cover_04", "4부 등신 베리에이션", "8등신에서 SD·마스코트까지", ["doctor", "haru", "fruitfly"]),
 ("og_05", "cover_05", "5부 표정·과장 베리에이션", "무너짐·한 곳 과장·기호", ["doctor", "sia", "jupanbot"]),
 ("og_06", "cover_06", "6부 매체·옷 베리에이션", "재료·카메라·옷·설정 시트", ["haru", "sia", "moa"]),
 ("og_07", "cover_07", "7부 베리에이션 실패 실험실", "실패 8종과 나이 신호", ["jupanbot", "fruitfly", "x2"]),
 ("og_08", "cover_08", "8부 실전 연습장", "작업대·분류판·공방·진단", ["haru", "doctor", "x1"])]
os.makedirs(os.path.join(ROOT, "assets", "og"), exist_ok=True)
for key, cover, t1, t2, cast in ITEMS:
    cp = os.path.join(ROOT, "assets", "img", cover + ".webp")
    if os.path.exists(cp):
        im = Image.open(cp).convert("RGB"); w, h = im.size; nh = int(w * 630 / 1200)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh)).resize((1200, 630))
    else:
        im = Image.new("RGB", (1200, 630), "#ffffff"); d = ImageDraw.Draw(im)
        for x in range(0, 1200, 40):
            for y in range(0, 630, 40):
                if (x // 40 + y // 40) % 2 == 0: d.rectangle([x, y, x + 39, y + 39], fill="#f3f6fa")
        d.rectangle([0, 0, 1200, 8], fill="#0f8f84")
        d.text((60, 70), t1, font=ImageFont.truetype(F, 54), fill="#16212b")
        d.text((60, 160), t2, font=ImageFont.truetype(F, 36), fill="#0f8f84")
        d.text((60, 560), "안상선 · ahnboat lab", font=ImageFont.truetype(F, 24), fill="#5b6874")
        for i, c in enumerate(cast):
            f = Image.open(os.path.join(ROOT, "assets", "chars", f"{c}_e01.webp")).convert("RGBA").resize((220, 220), Image.NEAREST)
            im.paste(f, (1200 - 60 - 230 * (len(cast) - i), 330), f)
    im.save(os.path.join(ROOT, "assets", "og", key + ".jpg"), quality=82)
print("og done")
