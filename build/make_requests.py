# -*- coding: utf-8 -*-
"""Genspark 그림 요청 꾸러미(docs/image_requests) 생성. python3 build/make_requests.py
페이지의 '프롬프트로 직접 만들어 보기' A 프롬프트도 여기서 가져간다(이 파일이 원본).
화풍은 작품·작가 이름이 아니라 특징(선·명암·색·비율)으로만 적는다."""
import os, csv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "docs", "image_requests")
PIX = "Art style (required, always): 16-bit RPG style pixel art with clearly visible square pixels, limited palette, bold dark outline, 2–3 tone shading, small highlights; no smooth gradients, no painterly, vector, watercolor or 3D look.\nMatch the characters' proportions and colors of the attached reference images exactly, drawn in this same pixel-art style.\nBright daytime laboratory mood, soft natural sunlight through large windows, clean white walls, light lavender, mint and pink accents."
KEEP = "Match the attached reference images exactly for identity (hair shape and color, eye color, accessories). All characters are adults in their twenties (the Professor is an adult man in his thirties); modest outfits exactly as described. Only the drawing style changes between panels; the person stays the same."
END = "No text, no letters, no numbers, no calligraphy, no seals or stamps, no logos, no watermark, no revealing clothing, not childlike, no school uniform, not resembling any existing anime, comic or game character, do not imitate any specific artist or studio."
ENDC = "No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands."
SAFE = "Composition: every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom); bottom-left corner plain and bright."
CH = {
 "haru": "Haru (adult lab assistant, long straight pink hair with navy streaks and a thick navy streak down the center of the bangs, two round hair buns on top, small ahoge, big blue eyes)",
 "sia": "Sia (adult maid intern, long straight jet-black hair, no headdress, gray eyes, small silver earrings)",
 "moa": "Moa (adult maid intern, long ash-beige wavy hair, white frilled maid headband with a white ribbon over her LEFT ear, amber eyes)",
 "doctor": "the Professor (adult male scientist in his thirties, dark charcoal spiky hair with a white streak at the front, very thick black eyebrows, teal rectangular glasses)",
 "fly": "the Fruit Fly researcher (tiny cartoon fruit fly, large red compound eyes, retro dark blue helmet with a yellow-white stripe, colorful dangling cables, tiny white lab coat, translucent wings)",
 "bot": "AbaBot (boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, small tank treads)",
 "judges": "three small cute dark navy silhouette judges with white dot eyes (one with a pink side-ponytail bow, one with a beret and teal round glasses, one with a cat-ear hood and yellow pompoms) holding blank score paddles",
}
OUT = {"haru": "lavender hoodie with white drawstrings over a white t-shirt, open white knee-length lab coat",
       "sia": "charcoal-black long-sleeved maid dress, large gray bow at the collar, long white frilled apron",
       "moa": "camel knit cardigan over a white blouse, red and navy plaid bow tie, white frilled apron",
       "doctor": "white lab coat over a black vest, white shirt and black tie"}
def who(k, outfit=None): return CH[k] + ", wearing " + (outfit or OUT[k])
def cover(file, page, part, alt, scene, chars, meta, mood):
    p = f"Website top cover illustration, wide 16:9.\n{PIX}\nScene: {scene}\nCharacters:\n  " + ";\n  ".join(chars) + f".\nVisual metaphor: {meta}\n{SAFE}\nMood: {mood}\n{ENDC}"
    return (file, page, part, alt, p, "pixel")
def body(file, page, part, alt, ratio, scene, style, extra=""):
    p = ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\nArt style: {style}\n{KEEP}\n{scene}\n" + (extra + "\n" if extra else "") + "Plain white background behind the panels.\n" + END)
    return (file, page, part, alt, p, "variation")
ANIME = "clean modern anime illustration, confident lineart, two-tone cel shading, natural adult proportions"

C1 = [
 cover("cover_index", "index.html", "목차", "낮의 연구실 갤러리 벽에 같은 하루·시아·모아의 초상이 서로 다른 화풍(셀화·수묵·SD·3D·흑백 만화)으로 걸려 있고, 초파리가 벽에 점을 찍어 군집을 묶는 장면",
   "a bright laboratory gallery wall covered with many small framed portraits of the same three women in different drawing styles, grouped in loose clusters with soft colored circles drawn around each group on the wall.",
   [who("haru") + ", in the center pointing at one cluster", who("sia") + ", on the left looking at a black-and-white framed portrait", who("moa") + ", on the right holding a tiny round mascot figure", who("doctor") + ", at the back with a clipboard",
    CH["fly"] + ", hovering near the wall drawing a colored circle around a group of frames", CH["bot"] + ", at the bottom right holding a stack of blank frames", CH["judges"] + " sitting on a bench in the back"],
   "many variations of one character, grouped into loose clusters like dots on a map.", "cheerful, playful, a gallery opening."),
 cover("cover_01", "01_era.html", "1부 시대 베리에이션", "연구실 사진 벽에 같은 모아의 초상이 연대별 화풍으로 나란히 걸리고, 모아가 그 앞에서 고개를 갸웃하는 장면",
   "a hallway of the lab with a row of framed portraits of the same woman from left to right, each frame a little more modern (from warm faded tones to bright crisp colors).",
   [who("moa") + ", in the center facing the viewer, tilting her head with curiosity", CH["fly"] + ", on the left facing right, holding a small paint palette with only two colors", CH["bot"] + ", on the right facing left, holding a yellowed photo filter sheet", who("doctor") + ", at the back nodding"],
   "a timeline of the same face.", "warm, nostalgic and bright."),
 cover("cover_02", "02_line.html", "2부 선과 지역 베리에이션", "연구실 펜 작업대에서 시아가 모델로 앉고, 초파리와 주판봇이 굵기가 다른 펜과 붓으로 같은 얼굴을 그리는 장면",
   "a long drawing table with many pens of different thickness, a brush, an ink stone and a screentone sheet.",
   [who("sia") + ", sitting on a stool in the center as the model, calm", CH["fly"] + ", on the left facing right, drawing with a thin even pen", CH["bot"] + ", on the right facing left, drawing with a big brush", who("doctor") + ", at the back holding a magnifier"],
   "one face, many kinds of lines.", "calm, focused."),
 cover("cover_03", "03_mono.html", "3부 흑백·선화 베리에이션", "연구실 먹 작업대에서 모아가 움직임 선 위에 연필 러프를 그리고, 시아가 망점 시트를 대고, 하루가 흑백 엽서를 들고 있는 장면",
   "a bright lab drawing table with pencil rough sketch sheets, a screentone sheet, an ink stone and a brush, and a black-and-white printed postcard; one wall poster shows only a curved pink line.",
   [who("moa") + ", sketching quick pencil poses on a large sheet", who("sia") + ", holding a dotted screentone sheet up to the light", who("haru") + ", holding a black-and-white postcard of herself", CH["fly"] + ", hovering with a tiny brush", CH["bot"] + ", at the back with a stack of paper"],
   "color removed, only lines and gray dots remain.", "calm, crafty."),
 cover("cover_04", "04_proportion.html", "4부 등신 베리에이션", "연구실 키 재기 벽 앞에 하루가 서고, 옆에 같은 하루 인형이 큰 것부터 작은 둥근 마스코트까지 줄지어 선 장면",
   "a lab wall with a tall height chart, a shelf of dolls of the same woman from realistic proportions to tiny round mascot figures.",
   [who("haru") + ", standing in the center next to the height chart, smiling", CH["fly"] + ", on the left measuring a doll's head with a tiny ruler", CH["bot"] + ", on the right holding the smallest round mascot figure", who("doctor") + ", at the back"],
   "the same character shrinking from tall to round.", "fun, cute."),
]
C2 = [
 cover("cover_05", "05_expression.html", "5부 표정·과장 베리에이션", "연구실 거울 앞에서 시아가 표정 카드 아홉 장을 들고, 박사가 지친 얼굴과 평소 얼굴 카드를 비교하는 장면",
   "a mirror corner in the lab with a corkboard of nine expression cards of the same woman (blank card frames with simple faces, no text).",
   [who("sia") + ", in the center holding up an expression card with a surprised face", who("doctor") + ", on the right comparing two cards, one cheerful and one tired", CH["fly"] + ", on the left holding a magnifier", CH["bot"] + ", at the back with a big sweat drop on its screen"],
   "one face, many expressions.", "funny, light."),
 cover("cover_06", "06_media_outfit.html", "6부 매체·옷 베리에이션", "연구실 스튜디오에서 세 사람이 옷걸이 앞에 서고, 뒤쪽 액자에 같은 세 사람이 3D·흑백·픽셀 버전으로 걸린 장면",
   "a bright lab studio with a clothing rack (knit vest, beret, plaid scarf, black tank top), a small 3D printer with a round figure, and three framed pictures on the wall.",
   [who("haru") + ", on the left holding a small round 3D figure of herself", who("sia") + ", in the center holding a black-and-white printed card", who("moa") + ", on the right holding a beret and a plaid scarf", CH["fly"] + ", hovering over the rack", CH["bot"] + ", at the back"],
   "same people, different materials and outfits.", "lively, creative."),
 cover("cover_07", "07_failure_lab.html", "7부 베리에이션 실패 실험실", "검수 책상 위에 어색한 베리에이션 카드 여덟 장이 놓이고, 초파리가 돋보기로 살피며 주판봇이 머리를 긁는 장면",
   "an inspection desk in the lab with eight blank picture cards (simple sketches only, no text), a magnifier and a checklist board with five blank rows.",
   [CH["fly"] + ", in the center holding a big magnifier over a card", CH["bot"] + ", on the right scratching its head with a gray arm", who("doctor") + ", at the back pointing at the checklist", CH["judges"] + " peeking from the left"],
   "find the first thing that went wrong.", "curious, a little comic."),
 cover("cover_08", "practice/index.html", "8부 실전 연습장", "연구실 조종 책상의 큰 모니터에 점들이 군집을 이룬 지도가 뜨고, 하루가 다이얼을 돌리는 장면",
   "the lab control desk with a big monitor showing a scatter of colored dots in loose clusters, dials and sliders on the desk.",
   [who("haru") + ", in the center turning a dial", who("doctor") + ", on the right watching", CH["fly"] + ", hovering near the monitor", CH["bot"] + ", typing"],
   "moving a dot from one cluster to another.", "focused, hopeful."),
]
B1 = [
 body("p1_moa_era_grid", "01_era.html", "1부 1단계", "같은 모아의 가슴 위 초상 네 장 — 80년대 셀화풍, 90년대풍, 2000년대 디지털풍, 지금의 애니풍", "16:9",
   "Four chest-up portraits of the same " + who("moa") + ", side by side in a row, gentle smile, same pose and framing in all four.",
   "four panels from left to right: (1) 1980s-like cel animation look — one hard-edged shadow tone, one small round eye highlight, heavy upper lashes, thick outlines, warm slightly faded colors; (2) 1990s-like look — two hard shadow tones, sharper chin, glossy hair highlights; (3) 2000s-like early digital look — clean thin lines, soft airbrushed shading; (4) present-day anime look — large eyes with several highlights, soft gradient shading, bright crisp colors"),
 body("p1_moa_detail_pair", "01_era.html", "1부 3단계", "같은 모아 두 장 — 왼쪽은 가닥 선이 적고 굵은 단순한 그림, 오른쪽은 가닥 선과 주름 선이 많은 정교한 그림", "16:9",
   "Two chest-up portraits of the same " + who("moa") + ", same pose, side by side.",
   "left: simple TV-animation line art with thick outlines and only a few hair strand lines; right: detailed feature-film illustration with many fine hair strand lines and fabric fold lines, thinner outlines"),
 body("p2_sia_line_styles", "02_line.html", "2부 1단계", "같은 시아 네 장 — 클리어 라인풍, 미국 코믹스풍, 그래픽 노블풍, 수묵풍", "16:9",
   "Four chest-up portraits of the same " + who("sia") + ", calm expression, same pose, side by side.",
   "four panels: (1) uniform-weight clean lines, flat colors, no shading (European adventure-comic look); (2) bold thick outlines, saturated primary colors, halftone dot shading (classic American comic-book look); (3) thin pen lines with cross-hatching shadows, muted realistic colors (realistic graphic-novel look); (4) black ink brush strokes with broken lines and large empty white space (East Asian ink painting look)"),
 body("p3_sia_brush", "02_line.html", "3부 3단계", "수묵풍 시아 한 장 — 머리카락은 굵은 먹, 얼굴은 최소한의 끊긴 선, 넓은 여백. 글씨·도장 없음", "2:3",
   "Chest-up portrait of " + who("sia") + ", looking slightly to the side, calm.",
   "black ink brush painting on white paper: bold sweeping brush strokes for the hair, only a few broken thin lines for the face outline and features, about two thirds of the picture left empty white; no calligraphy, no seals"),
 body("p2_sia_paint", "02_line.html", "2부 2단계", "같은 시아 세 장 — 평면 색, 원색 망점 칠, 번지는 수채 칠", "16:9",
   "Three chest-up portraits of the same " + who("sia") + ", calm expression, same pose, side by side.",
   "three panels with the same clean line drawing but different coloring: (1) flat even colors with crisp edges, medium saturation; (2) bold saturated primary colors with halftone dot shading; (3) soft bleeding watercolor washes, low saturation, thin light pencil-like lines"),
 body("p3_moa_gesture", "03_mono.html", "3부 1단계", "모아의 흑백 러프 동작 시트 — 찌르기·막기·물러서기 등 다섯 동작", "16:9",
   "A black-and-white rough pencil sketch sheet of " + CH["moa"] + " in five different action poses (lunging forward, blocking, stepping back, turning, leaping), wearing a simple long-sleeved blouse and long skirt.",
   "black and white pencil gesture sketches: quick overlapping rough lines, a strongly curved line of action through each body, no color, no shading except a few light strokes; her headband and the ribbon over her LEFT ear kept as simple lines; hands empty or holding a plain wooden stick, no weapons"),
 body("p4_haru_heads", "04_proportion.html", "4부 1단계", "같은 하루 다섯 장 — 7.5·6·4·3·2.5등신, 키를 맞춰 나란히", "16:9",
   "Five full-body standing figures of the same " + who("haru") + ", side by side with their total heights equal, friendly pose.",
   ANIME + "; proportions from left to right: 7.5 heads tall, 6 heads tall, 4 heads tall, 3 heads tall, 2.5 heads tall comedy SD — every figure is the same adult woman drawn in a different proportion style, not a child"),
 body("p4_haru_mascot", "04_proportion.html", "4부 3단계", "2등신 마스코트 피규어 하루와 일반 애니풍 하루 카드", "16:9",
   "A smooth round 2-head-tall mascot figure of " + who("haru") + " standing on a white desk, next to a small card showing the same adult woman drawn in normal anime proportions.",
   "the figure: smooth vinyl toy rendering, simple rounded shapes, no outlines, only key symbols kept bold (pink hair with navy streaks, two round buns, lavender hoodie, white lab coat); the card: " + ANIME),
]
B2 = [
 body("p5_sia_collapse", "05_expression.html", "5부 1단계", "같은 시아 다섯 장 — 예쁜 놀람에서 개그 작화로 무너지는 단계", "16:9",
   "Five face close-ups of the same " + who("sia") + " reacting with surprise, in a row from left to right.",
   ANIME + "; step by step from a pretty surprised face (left) to a comical collapsed face (right): eyes become simple, then dot eyes and white circle eyes, mouth grows, vertical shock lines over the upper face; her long black hair and small silver earrings stay exactly the same in all five"),
 body("p5_sia_one_place", "05_expression.html", "5부 2단계", "같은 시아 세 장 — 눈만 / 입만 / 땀 한 방울만 크게 과장", "16:9",
   "Three face close-ups of the same " + who("sia") + ", surprised.",
   ANIME + "; left: only the eyes are exaggerated (much larger), everything else normal; middle: only the mouth is exaggerated (wide open), everything else normal; right: only one big sweat drop on the forehead, everything else normal"),
 body("p6_haru_media", "06_media_outfit.html", "6부 1단계", "같은 하루 네 장 — 셀 애니·부드러운 3D·먹선·16비트 픽셀", "16:9",
   "Four chest-up portraits of the same " + who("haru") + ", cheerful smile, same pose, side by side.",
   "four panels: (1) " + ANIME + "; (2) soft 3D render like a smooth vinyl figure, no outlines; (3) black and white ink line drawing with screentone dots; (4) 16-bit pixel art with visible square pixels. The silhouette, hair color, two buns and lavender hoodie stay the same in all four"),
 body("p6_moa_outfits", "06_media_outfit.html", "6부 3단계", "같은 모아의 잡지풍 포스터 세 장 — 펑크·프레피·가을 코디", "16:9",
   "Three magazine-style character posters of the same " + CH["moa"] + ", each poster combining a large face close-up, a full-body outfit pose and a themed pattern background, with an empty blank area for a title (no text).",
   ANIME + "; outfits: (1) punk — black sleeveless top with a black-and-red striped tie, checkered cargo shorts to the knee, sneakers; (2) preppy — argyle knit vest over a white shirt, below-the-knee pleated gray skirt, loafers, small handbag; (3) autumn outfit — cream cable-knit sweater, teal plaid scarf, beige beret, long plaid skirt, leather backpack, autumn leaves pattern. She keeps the white frilled headband and the white ribbon over her LEFT ear in all three. Adult woman in her twenties, not a school uniform"),
]
F = [
 body("f1_identity", "07_failure_lab.html", "7부 f1", "수묵풍 모아 — 머리띠와 리본이 사라지고 머리가 생머리로 바뀐 의도적 실패", "2:3",
   "Intentional failure example. Chest-up ink brush painting of an adult woman who is supposed to be Moa, but the white frilled headband and the ribbon are missing and her wavy hair has become straight.", "black ink brush painting, broken lines, large empty space; no calligraphy, no seals"),
 body("f2_two_axes", "07_failure_lab.html", "7부 f2", "80년대 셀화와 3D 피규어 질감이 섞인 시아 — 의도적 실패", "2:3",
   "Intentional failure example. Chest-up portrait of " + who("sia") + ", awkwardly mixing a 1980s-like cel look (thick outlines, one hard shadow) with a glossy 3D vinyl-figure rendering on the same face.", "mixed cel and 3D rendering"),
 body("f3_muddy", "07_failure_lab.html", "7부 f3", "셀·수채·3D 사이 어중간한 질감의 하루 — 의도적 실패", "2:3",
   "Intentional failure example. Chest-up portrait of " + who("haru") + ", rendered in a muddy in-between texture: blurry outlines, half watercolor bleeding, half soft 3D shading, dull colors.", "muddy mixed rendering"),
 body("f4_age_drift", "07_failure_lab.html", "7부 f4", "2.5등신 하루가 아이처럼 어려 보이는 의도적 실패", "2:3",
   "Intentional failure example to teach what to avoid: a 2.5-head-tall SD figure of Haru (pink hair with navy streaks, two round buns) whose face reads too young: very round cheeks, oversized eyes, a childish outfit. Keep it wholesome and fully clothed.", ANIME),
 body("f5_sd_face", "07_failure_lab.html", "7부 f5", "SD 몸에 8등신 얼굴을 얹은 시아 — 의도적 실패", "2:3",
   "Intentional failure example. A 2.5-head-tall SD body of " + who("sia") + " but with a realistic 8-head-tall face placed in the large head: eyes exactly in the middle so the forehead looks huge, and tiny hands with five detailed fingers.", ANIME),
 body("f6_overexag", "07_failure_lab.html", "7부 f6", "눈·입·땀·눈물·기호를 모두 키운 시아 — 의도적 실패", "2:3",
   "Intentional failure example. Face close-up of " + who("sia") + " where everything is exaggerated at once: huge eyes, huge open mouth, many big sweat drops, tears, a heart symbol and an anger mark all together, confusing.", ANIME),
 body("f7_mocking", "07_failure_lab.html", "7부 f7", "박사의 개그 그림이 외모를 놀리는 쪽으로 간 의도적 실패", "2:3",
   "Intentional failure example to teach what to avoid: a comedy drawing of " + who("doctor") + " where, instead of a funny reaction, his nose and chin are distorted in an unflattering way. Keep it mild and not grotesque.", ANIME),
 body("f8_fake_text", "07_failure_lab.html", "7부 f8", "수묵풍 시아 옆에 뜻 없는 글씨와 붉은 도장이 들어간 의도적 실패", "2:3",
   "Intentional failure example. Ink brush painting of " + who("sia") + " with meaningless pseudo-calligraphy columns and a red seal stamp beside her (this failure image intentionally includes fake writing).", "black ink brush painting", "Exception for this failure image only: the pseudo-calligraphy and seal are allowed."),
]
CONV = [
 ("C01_covers_A", "표지 A", "16:9", "refs 전부(haru·sia·moa anime_base, doctor_sheet, fruitfly_sprites_6, jupanbot_ref_genspark_v0, pixel_style_ref_prev_cover)", C1),
 ("C02_covers_B", "표지 B", "16:9", "refs 전부 + C01의 cover_index", C2),
 ("C03_part1_4", "1~4부 본문", "16:9", "moa·sia·haru anime_base와 sheet", B1),
 ("C04_part5_6", "5~6부 본문", "16:9", "sia·haru·moa anime_base와 sheet", B2),
 ("C05_fail", "7부 실패 8종", "2:3", "해당 캐릭터 anime_base", F),
]
PROMPTS = {it[0]: it for _c in CONV for it in _c[4]}
CONV_OF = {it[0]: _c[0] for _c in CONV for it in _c[4]}
ATTACH_OF = {_c[0]: _c[3] for _c in CONV}
HEAD_PIX = "웹사이트 표지 그림을 만들어 줘. 아래 프롬프트를 하나씩 순서대로 그려 줘.\n- 첨부한 기준 그림의 캐릭터 모습·색을 정확히 지킬 것\n- 16비트 RPG 픽셀아트, 16:9, 밝은 낮 연구실\n- 그림 안에 글자·숫자·로고 금지"
HEAD_VAR = "해설 페이지 본문 그림을 만들어 줘. 아래 프롬프트를 하나씩 순서대로 그려 줘.\n- 첨부한 기준 그림의 캐릭터(머리 모양·색·장식)를 정확히 지키고, 패널마다 '그림체'만 바꿀 것\n- 등장인물은 모두 20대 성인(박사는 30대 성인 남성). 노출·교복 느낌·어려 보이는 얼굴 금지\n- 실존 작품·작가·캐릭터를 닮게 하지 말 것\n- 그림 안에 글자·숫자·글씨·도장·로고 금지(f8 실패 그림만 예외)"

README = """# 그림 요청 꾸러미 — 구조 먼저 그리기 연구실 · 웃음 편 2 · 베리에이션

저장소: `adminmrobo/drawing_lab_fun_02` (페이지는 완성 — 그림 자리는 '그림 준비 중'으로 비어 있음)
만드는 도구: Genspark 이미지 · 받은 그림은 zip으로 돌려주시면 됩니다(대화 단위로 나눠 여러 번 주셔도 됩니다).

## 1. 그림 규칙
| 항목 | 규칙 |
|---|---|
| 그림체 | **표지 9장은 16비트 픽셀아트**. 본문 그림은 **패널마다 그림체를 바꾸는 베리에이션**(셀화·클리어 라인·코믹스·그래픽 노블·흑백 러프·수묵·SD·3D·픽셀) |
| 화풍 지정 | 작품·작가 이름을 쓰지 않고 **특징(선·명암·색·비율)으로만** 적음 |
| 캐릭터 고정값 | 하루: 정수리 번 2개 + 앞머리 가운데 남색 줄 / 시아: 흑발·장식 없음·은 귀걸이 / 모아: 흰 프릴 머리띠 + **왼쪽** 귀 위 흰 리본 / 박사: 흰 줄 있는 짙은 머리, 굵은 눈썹, 청록 사각 안경 |
| 나이·노출 | 모두 20대 성인(박사는 30대 성인 남성). SD도 성인. **어려 보이는 얼굴·교복 느낌·노출 금지** |
| 글자 | 그림 안에 글자·숫자·글씨·도장·로고 금지(f8 실패 그림만 예외) |
| 참고 그림 | 연구실 캐릭터 기준 그림(`assets/refs/`)만 첨부. 다른 작품 그림·'AI 학습 금지' 표시가 있는 그림은 첨부하지 않음 |

## 2. 요청 순서 (Genspark 대화 하나 = 파일 하나)
| 순서 | 파일 | 그림 수 | 비율 | 첨부 |
|---|---|---|---|---|
| 1 | `prompts/C01_covers_A.md` | 5 | 16:9 픽셀 | refs 전부 |
| 2 | `prompts/C02_covers_B.md` | 4 | 16:9 픽셀 | refs 전부 + C01의 cover_index |
| 3 | `prompts/C03_part1_4.md` | 8 | 16:9 (p3_sia_brush만 2:3) | moa·sia·haru 기준 그림 |
| 4 | `prompts/C04_part5_6.md` | 4 | 16:9 | sia·haru·moa 기준 그림 |
| 5 | `prompts/C05_fail.md` | 8 | 2:3 | 해당 캐릭터 기준 그림 |

## 3. 저장 이름
`checklist.csv`의 `file` 열 이름 그대로(png·jpg). 받으면 WebP로 바꿔 `assets/img/`에 넣습니다(표지 1600×900, 가로 1200×675, 세로 600×900).

## 4. 실패 그림 주의
도구가 실수를 자동으로 고쳐 그리면 두 번까지만 다시 시도해 주세요. 그래도 안 되면 그대로 주셔도 됩니다(페이지에서 '결과는 매번 다르다'는 사례로 설명합니다).
"""

if __name__ == "__main__":
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for cid, title, ratio, att, items in CONV:
        pix = items[0][5] == "pixel"
        md = f"# {cid[:3]} · {title} — " + ", ".join(i[0] for i in items) + f"\n\n**첨부:** {att}\n\n**Genspark에 먼저 붙여 넣기 ↓**\n```\n{HEAD_PIX if pix else HEAD_VAR}\n```\n"
        for k, (file, page, part, alt, prompt, style) in enumerate(items):
            n += 1; rows.append([n, cid[:3], file, page, part, "16:9" if "16:9" in prompt.split("\n")[0] else "2:3", style, ""])
            md += f"\n---\n## {k+1}) {file} — {part}\nalt: {alt}\n```\n{prompt}\n```\n"
        open(os.path.join(D, "prompts", cid + ".md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "page", "part", "ratio", "style", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(README)
    print("prompts", len(CONV), "images", n)
