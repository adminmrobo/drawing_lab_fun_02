# -*- coding: utf-8 -*-
"""구조 먼저 그리기 연구실 · 웃음 편 2 · 베리에이션 — 페이지 빌드.
python3 build/build.py 로 index.html, 01~06 페이지, practice/index.html 을 다시 만든다.
그림 파일(assets/img/{키}.webp)이 있으면 넣고, 없으면 '그림 준비 중' 자리만 둔다."""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_a import P1, P2, P4
from content_c import P3
from content_b import P5, P6, P7
from content_make import MAKE
from make_requests import PROMPTS, CONV_OF, ATTACH_OF
from img_notes import ALT, DRILL_RES, RETRY_RES, RETRY3_RES
from content_drill import DRILL, RETRY, BASE_OF, RETRY3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = "v1.0"
DATE = "2026-11-25"
SITE = "https://adminmrobo.github.io/drawing_lab_fun_02/"
PREV_SITE = "https://adminmrobo.github.io/drawing_lab_fun/"
FACE_SITE = "https://adminmrobo.github.io/drawing_lab_03/"
CLOSET_SITE = "https://adminmrobo.github.io/structure_first_drawing_lab_01/"
FIRST_SITE = "https://adminmrobo.github.io/adminmrobo-structure_first_drawing_lab/"
REPO = "https://github.com/adminmrobo/drawing_lab_fun_02"
AUTHOR_URL = "https://adminmrobo.github.io/who_am_i/who_am_i.html"
RENDER = "https://adminmrobo.github.io/ai_rendering/"
CHARREPO = "https://github.com/adminmrobo/fruitfly-lab-expressions"
SERIES = "구조 먼저 그리기 연구실 · 웃음 편 2 · 베리에이션"
E = html.escape
PARTS = [P1, P2, P3, P4, P5, P6, P7]

CH = {
 "doctor": ("박사", "해설 + 손님 모델(5부 지친 얼굴). 짙은 머리의 흰 줄, 굵은 눈썹, 청록 사각 안경"),
 "haru": ("조수 하루", "모델(4부 등신, 3·6부) + 수식 상자 담당. 정수리 번 2개와 앞머리 가운데 남색 줄"),
 "sia": ("시아", "인턴1 · 모델(2부 선, 3부 흑백, 5부 표정, 6부). 흑발, 머리 장식 없음, 은 귀걸이"),
 "moa": ("모아", "인턴2 · 모델(1부 시대, 3부 흑백 러프, 6부 옷). 흰 프릴 머리띠와 왼쪽 귀 위 흰 리본"),
 "jupanbot": ("주판봇", "화가 A. 결과부터 서두른다 — 색만 바꾸고, 통째로 줄이고, 전부 키운다"),
 "fruitfly": ("초파리 연구원", "화가 B. 무엇을 바꾸고 무엇을 남길지부터 나눈다. \"이걸 눌러 봐\""),
 "x1": ("X1", "평가단. 닮음(같은 캐릭터인가)을 본다"),
 "x2": ("X2", "평가단. 원리를 본다"),
 "x3": ("X3", "평가단. 자연스러움을 본다"),
}
COLOR = {"doctor": "doc", "haru": "asst", "fruitfly": "fly", "jupanbot": "robo", "sia": "sia", "moa": "moa", "x1": "x", "x2": "x", "x3": "x"}

def face(k, e="e13", pre="", cls=""):
    n = CH[k][0]
    return f'<img src="{pre}assets/chars/{k}_{e}.webp" alt="{E(n)}" width="96" height="96" loading="lazy"{(" class=%s" % cls) if cls else ""}>'

def has_img(key):
    return os.path.exists(os.path.join(ROOT, "assets", "img", key + ".webp"))

def art(key, alt, ar="16/9", cap=None, pre="", cls=""):
    if key in ALT:
        if cap == alt:
            cap = ALT[key]
        alt = ALT[key]
    cap_html = f"<figcaption>{E(cap)}</figcaption>" if cap else ""
    if has_img(key):
        return f'<figure class="art {cls}" data-img="{key}"><img src="{pre}assets/img/{key}.webp" alt="{E(alt)}" loading="lazy" decoding="async">{cap_html}</figure>'
    return (f'<figure class="art {cls}" data-img="{key}"><div class="ph-art" style="--ar:{ar}" role="img" aria-label="{E(alt)}">'
            f'<b>그림 준비 중 · {key}</b><span>{E(alt)}</span></div>{cap_html}</figure>')

def head(title, desc, og, path, pre=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}assets/og/{og}"><meta property="og:url" content="{SITE}{path}"><meta name="twitter:card" content="summary_large_image">
<meta name="author" content="안상선">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/lab.css">
</head>
<body data-root="{pre}">
<div id="prog"></div>
"""

def nav(links, pre=""):
    a = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in links)
    return f'<nav class="top"><div class="row"><a class="logo" href="{pre}index.html">구조 먼저 그리기 <i>· 베리에이션</i></a><div class="links">{a}</div></div></nav>\n'

def cover(key, cap, cast, pre=""):
    if has_img(key):
        return f'<div class="cover"><div class="frame" data-img="{key}"><img class="art" src="{pre}assets/img/{key}.webp" alt="{E(cap)}" width="1600" height="900" fetchpriority="high" decoding="async"></div></div>\n'
    # 그림이 오기 전 픽셀 대체 표지: 네모 격자 + 상자·원기둥 마네킹(픽셀 블록) + 픽셀 캐릭터
    cells = []
    for x in range(0, 1600, 40):
        for y in range(0, 900, 40):
            if (x // 40 + y // 40) % 2 == 0:
                cells.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="#f3f6fa"/>')
    px = []
    import math as _m
    for gx in range(1040, 1400, 20):
        for gy in range(120, 600, 20):
            dx, dy = gx + 10 - 1220, gy + 10 - 330
            if abs(_m.hypot(dx, dy * 1.0) - 170) < 11 and gy < 400 or (gy >= 400 and abs(abs(dx) - (170 - (gy - 400) * 0.85)) < 11 and gy < 580):
                px.append(f'<rect x="{gx}" y="{gy}" width="20" height="20" fill="#1e2f6e"/>')
    for gy in range(140, 580, 20): px.append(f'<rect x="1210" y="{gy}" width="20" height="20" fill="#e0337f" opacity=".55"/>')
    for gx in range(1060, 1380, 20): px.append(f'<rect x="{gx}" y="330" width="20" height="20" fill="#e0337f" opacity=".55"/>')
    bl = "".join(px)
    easel = '<rect x="240" y="180" width="300" height="380" fill="#ffffff" stroke="#8a5a2b" stroke-width="12"/><rect x="270" y="560" width="20" height="260" fill="#8a5a2b"/><rect x="490" y="560" width="20" height="260" fill="#8a5a2b"/>' + \
            "".join(f'<rect x="{300+i*40}" y="{240+j*40}" width="40" height="40" fill="{c}"/>' for i, j, c in [(1,0,"#d8c09a"),(2,0,"#d8c09a"),(0,1,"#d8c09a"),(1,1,"#f8e3d3"),(2,1,"#f8e3d3"),(3,1,"#d8c09a"),(1,2,"#4a3b5c"),(2,2,"#4a3b5c"),(0,2,"#f8e3d3"),(3,2,"#f8e3d3"),(1,3,"#f8e3d3"),(2,3,"#f8e3d3"),(1,4,"#f8e3d3"),(2,4,"#f8e3d3")])
    imgs = "".join(face(k, e, pre) for k, e in cast)
    return f"""<div class="cover"><div class="frame" data-img="{key}"><svg class="grid" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true" shape-rendering="crispEdges">{''.join(cells)}{easel}{bl}</svg>
<span class="cap">{E(cap)}</span><span class="badge">표지 그림 준비 중 · {key}</span><div class="cast" style="image-rendering:pixelated">{imgs}</div></div></div>
"""

def three(a, b, c, abbr):
    dl = "".join(f"<dt>{E(x)}</dt><dd>{E(y)}</dd>" for x, y in abbr)
    return f"""<div class="three"><h2>처음 오신 분께 — 세 줄 요약</h2><ul>
<li><b>무엇을</b>: {E(a)}</li><li><b>왜 알아야 하나</b>: {E(b)}</li><li><b>어디에 쓰나</b>: {E(c)}</li></ul>
<p>그림 실력·코드·수식을 몰라도 됩니다. 실험을 눌러 보며 따라오세요.</p>
<details class="abbr"><summary>낱말·약어 풀이 (펼치기)</summary><dl>{dl}</dl></details></div>\n"""

ABBR = [("베리에이션", "같은 캐릭터를 그림체·비율·표정·재료·옷을 바꿔 다시 그린 여러 버전"), ("고정값", "어느 버전에서도 바꾸지 않는 캐릭터의 특징(머리 모양·색·장식·나이)"),
        ("군집(클러스터)", "특징이 비슷한 것끼리 묶인 무리. 정답 없이 비슷한 것끼리 묶는 방법을 비지도학습이라 한다"), ("k-평균", "군집 수 k를 정하면 각 점을 가장 가까운 중심에 넣고 중심을 다시 계산하기를 되풀이하는 묶기 방법"), ("주성분(지도 축)", "여섯 특징을 2차원 지도로 펼칠 때, 점들이 가장 넓게 퍼지는 방향을 가로·세로 축으로 삼는 방법"), ("축", "그림을 재는 특징 하나(시대, 선 굵기, 등신 등). 축 하나를 바꾸면 그 방향으로 움직인다"),
        ("셀화", "투명한 셀에 손으로 칠하던 애니메이션. 그림자 경계가 또렷하다"), ("정보량", "그림 한 장의 선·색·세부의 양"),
        ("굵기 비", "한 선에서 가장 굵은 곳 ÷ 가장 가는 곳"), ("클리어 라인", "굵기가 일정한 맑은 선과 평평한 색으로 그리는 유럽 만화 화풍"),
        ("망점(스크린톤)", "작은 점으로 회색을 만드는 흑백 인쇄·만화 기법"), ("해칭", "가는 선을 겹쳐 그림자를 만드는 기법"),
        ("여백", "일부러 비워 둔 곳. 수묵화에서 형태를 읽게 하는 기법"), ("등신", "키 ÷ 머리 높이. 키 안에 머리가 몇 개 쌓이나"),
        ("SD(슈퍼 디포름)", "머리를 크게, 몸을 짧게 줄인 2~3등신 그림체. 나이가 아니라 그림체"), ("잔상", "움직임의 앞 장면을 흐리게 남긴 흔적"),
        ("작화 붕괴(무너짐)", "감정을 위해 일부러 단순하고 우스꽝스럽게 무너뜨린 작화"), ("회색값", "색을 흑백으로 바꾼 밝기(0 검정 ~ 255 흰색)"),
        ("설정 시트", "한 캐릭터의 프로필·각도·표정·부위·옷을 한 장에 모은 기준 그림"), ("부분 수정(인페인팅)", "칠한 영역만 AI가 다시 그리고 나머지는 그대로 두는 기능")]

def talk(lines, pre=""):
    out = []
    for k, e, t in lines:
        side = " r" if k in ("moa", "sia") else ""
        out.append(f'<div class="line{side}">{face(k, e, pre)}<div class="bub"><b style="color:var(--c-{COLOR[k]})">{E(CH[k][0])}</b>{E(t)}</div></div>')
    return '<div class="talk">' + "".join(out) + "</div>"

def quiz(q, opts, ans, ok, no):
    b = "".join(f'<button type="button">{E(o)}</button>' for o in opts)
    return f'<div class="quiz" data-ans="{ans}"><div class="qq">확인 퀴즈 — {E(q)}</div><div class="opts">{b}</div><div class="fb" aria-live="polite"></div><span class="qok" hidden>{E(ok)}</span><span class="qno" hidden>{E(no)}</span></div>'

def panel(no, i, p):
    return (f'<div class="panel"><div class="ph"><b>실험 {no}-{i}</b><small>{E(p["note"])}</small></div>'
            f'<div id="pp-{p["key"]}" data-panel="{p["key"]}"></div><div class="ctrl">{p["ctrl"]}</div><div class="readout" aria-live="polite"></div></div>')

def mathbox(m):
    tries = "".join(f"<div>{E(t)}</div>" for t in m["tries"])
    pcs = "".join(f"<tr><td class='m'>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in m["pieces"])
    return f"""<div class="box mathbox"><h4>수식이 어려운 조수가 대신 묻습니다</h4>
<div class="q">{face('haru','e04')}<div><b>조수</b> {E(m['ask'])}</div></div>
<div class="easy"><b>말로 하면</b> — {E(m['words'])}</div>
<div class="try"><b>숫자로 한 번 해 보기</b>{tries}</div>
<p><b>학교 수학으로 보면</b> — {E(m['school'])}</p>
<div class="fx">{E(m['formula'])}</div>
<table><thead><tr><th>식 조각</th><th>뜻</th></tr></thead><tbody>{pcs}</tbody></table>
<div class="q">{face('haru','e16')}<div><b>조수</b> {E(m['comment'])}</div></div></div>"""

def step(P, i, s):
    no = P["no"]
    labels = ["무엇이 문제인가", "그냥 하면 막히는 곳", "이렇게 푼다"]
    why = "".join(f"<li><b>{labels[k]}</b> — {E(x)}</li>" for k, x in enumerate(s["why"]))
    whybox = f'<div class="box why"><h4>왜 이렇게 하나</h4><ol>{why}</ol><div class="easy"><b>쉽게 말하면</b> — {E(s["easy"])}</div></div>'
    calm = talk([("doctor", "e08", "여기서 한 번 멈춰도 괜찮아요. 식이 낯설면 건너뛰고 아래 실험부터 눌러 보세요. 숫자는 실험이 대신 계산해 줍니다.")])
    duo = f'<div class="duo">{whybox}{mathbox(s["math"])}</div>{calm}' if s.get("math") else f'<div style="margin:16px 0">{whybox}</div>'
    solve = "".join(f"<p>{E(x)}</p>" for x in s["solve"])
    extra = ""
    img = art(s["img"][0], s["img"][1], s["img"][2], s["img"][1], cls="tall" if s["img"][2] == "2/3" else "") if s.get("img") else ""
    q = s["quiz"]
    return f"""<section class="room" id="{s['id']}"><div class="wrap">
<div class="roomno">{no}부 · {i}단계</div>
<h2>{E(s['title'])}</h2><p class="muted">{E(s['sub'])}</p>
<div class="tags"><span class="tag how">{E(s['how'])}</span><span class="tag day">{E(s['day'])}</span></div>
{duo}
<div class="pair"><div class="box"><h4>일상으로 치면</h4><p>{E(s['daily'])}</p></div><div class="box ml"><h4>그림·VFX 현장에서는</h4><p>{E(s['field'])}</p></div></div>
{talk(s['talk'])}
{panel(no, i, s['panel'])}
<div class="solve"><h4>풀이</h4>{solve}</div>
{extra}{img}
<div class="solve"><h4>AI 결과, 그대로 써도 될까?</h4><p>{E(s['ai'][0])}</p><details class="code"><summary>답 보기</summary><p>{E(s['ai'][1])}</p></details></div>
<div class="limit"><b>주의할 점</b> — {E(s['limit'])}</div>
{quiz(q[0], q[1], q[2], q[3], q[4])}
</div></section>
"""

def judge(J):
    rows = ""
    for idx, item in enumerate(J["items"]):
        a, b = J["a"][1][idx], J["b"][1][idx]
        mx = 8 if "8개" in item else 10
        rows += f'<span>{E(item)}</span><span class="bar" title="{J["a"][0]} {a}"><i style="width:{a/mx*100:.0f}%"></i></span><span class="bar" title="{J["b"][0]} {b}"><i style="width:{b/mx*100:.0f}%;background:var(--teal)"></i></span>'
    sa, sb = sum(J["a"][1]), sum(J["b"][1])
    tbl = "".join(f"<tr><td>{E(it)}</td><td>{J['a'][1][k]}</td><td>{J['b'][1][k]}</td></tr>" for k, it in enumerate(J["items"]))
    return f"""<section class="room" id="judge"><div class="wrap"><div class="roomno">평가단 채점</div><h2>{E(J['title'])}</h2>
{talk(J['setup'])}
<div class="judge"><h4>평가단 X1·X2·X3 채점</h4>
<div class="score"><span></span><b>{E(J['a'][0])}</b><b>{E(J['b'][0])}</b>{rows}</div>
<div class="tbl" style="margin-top:10px"><table><thead><tr><th>항목</th><th>{E(J['a'][0])}</th><th>{E(J['b'][0])}</th></tr></thead><tbody>{tbl}<tr><th>합계</th><th>{sa}</th><th>{sb}</th></tr></tbody></table></div>
{talk(J['comments'])}</div>
{talk(J['result'])}
<p class="hint">점수는 이야기 속 예시입니다. 실제 그림을 평가한 값이 아닙니다.</p>
</div></section>
"""

def summary(P):
    rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in P["summary"])
    return f"""<section id="sum"><div class="wrap"><h2>{P['no']}부 정리</h2>
<div class="tbl"><table><thead><tr><th>주제</th><th>한 줄</th><th>작업에서는</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
"""

def outro(P):
    return f"""<section id="outro"><div class="wrap"><h2>다음으로</h2>{talk(P['outro'])}
<div class="next"><a href="{P['prev'][0]}">{E(P['prev'][1])}</a><a href="{P['next'][0]}">{E(P['next'][1])}</a></div></div></section>
"""

def failcard(f):
    note = f'<p class="hint">{E(f["note"])}</p>' if f.get("note") else ""
    return f"""<div class="failcard" id="{f['key'].split('_')[0]}"><h3>{E(f['title'])}</h3><div class="failgrid">
{art(f['key'], f['alt'], f['ar'])}
<div><p><span class="chip">증상</span>{E(f['symptom'])}</p>
{quiz(f['q'], f['opts'], f['ans'], f['ok'], f['no'])}
<p><span class="chip">연결된 원리</span><a href="{f['link'][0]}">{E(f['link'][1])}</a></p>
<div class="promptbox"><b>고치는 프롬프트 조각</b><pre>{E(f['fix'])}</pre></div>{note}</div></div></div>"""

# ---------------- 지식 색인
KG = [
 ("concept/variation-axes", "Concept", "베리에이션 축과 군집", "Variation axes and clusters", "index.html", "#map", "시대·선·사실·과장·재료·색 여섯 특징으로 그림을 재고 비슷한 것끼리 넓게 묶는다"),
 ("method/shadow-steps", "Method", "그림자 단계", "Shadow steps", "01_era.html", "#s1", "색 수 ≈ 부위 수 × (1 + 그림자 단계 + 하이라이트 단계)"),
 ("method/eye-era", "Method", "눈으로 연대 고르기", "Choosing an era through the eyes", "01_era.html", "#s2", "눈 크기는 고정, 하이라이트 개수와 속눈썹 무게로 연대를 고른다"),
 ("concept/information-amount", "Concept", "정보량", "Amount of detail", "01_era.html", "#s3", "1초에 그리는 선 = 1초의 장수 × 장마다 선 개수"),
 ("method/color-grade", "Method", "색보정", "Color grading", "01_era.html", "#s4", "마지막 손잡이. 30도 넘게 돌리면 고정값이 흔들린다"),
 ("concept/line-weight-ratio", "Concept", "굵기 비", "Line weight ratio", "02_line.html", "#s1", "가장 굵은 곳 ÷ 가장 가는 곳. 1 맑은 선, 3 이상 힘 있는 펜선"),
 ("method/tone-methods", "Method", "명암 처리 방법", "Tone rendering methods", "03_mono.html", "#s2", "단색·망점·큰 점·해칭·먹칠. 덮는 비율 = π × 반지름² ÷ 한 변²"),
 ("concept/simplification", "Concept", "단순화 정도", "Degree of simplification", "02_line.html", "#s3", "0 사실 ↔ 1 카툰, 고정값은 남긴다"),
 ("method/brush-space", "Method", "붓선과 여백", "Brush strokes and empty space", "03_mono.html", "#s3", "선을 끊고 비워 둔 곳으로 형태를 읽게 한다"),
 ("concept/head-count", "Concept", "등신", "Head-height proportion", "04_proportion.html", "#s1", "등신 = 키 ÷ 머리 높이"),
 ("method/sd-parts", "Method", "부위 함께 줄이기", "Adapting features to SD", "04_proportion.html", "#s2", "등신이 작아지면 눈은 내리고 손발은 덩어리로"),
 ("method/mascot-symbols", "Method", "마스코트 상징", "Mascot key symbols", "04_proportion.html", "#s3", "둥근 덩어리와 상징 세 개"),
 ("method/motion-trail", "Method", "잔상과 과장", "Afterimages and exaggeration", "04_proportion.html", "#s4", "잔상 간격 = 이동 거리 ÷ (장수 − 1)"),
 ("method/collapse-steps", "Method", "무너짐 단계", "Comic face collapse steps", "05_expression.html", "#s1", "눈 → 입 → 그림자 → 윤곽 순서, 고정값은 끝까지"),
 ("method/one-place", "Method", "한 곳 과장", "Exaggerating one feature", "05_expression.html", "#s2", "길이 1.5배면 넓이 2.25배, 주인공 부위 하나만"),
 ("method/add-lines", "Method", "감정 자리 선 더하기", "Adding lines at emotion spots", "05_expression.html", "#s3", "눈 아래·미간·볼·입, 잔주름은 나이를 바꾼다"),
 ("concept/manga-symbols", "Concept", "만화 기호", "Manga emotion symbols", "05_expression.html", "#s4", "감정 하나에 기호 하나, 글자는 넣지 않는다"),
 ("method/render-swap", "Method", "재료 바꾸기", "Swapping rendering media", "06_media_outfit.html", "#s1", "선·명암·질감은 바뀌고 실루엣·색·장식은 남는다"),
 ("method/gray-value", "Method", "회색값", "Luma (gray value)", "03_mono.html", "#s4", "0.299R + 0.587G + 0.114B, 붙은 색의 차이를 본다"),
 ("method/outfit-theme", "Method", "옷 테마 바꾸기", "Outfit theme variation", "06_media_outfit.html", "#s3", "옷만 바꾸고 머리·장식·얼굴은 고정, 옷은 소재·핏·나이로 적는다"),
 ("method/model-sheet", "Method", "설정 시트", "Character model sheet", "06_media_outfit.html", "#s4", "고정값과 바뀌는 값을 한 장에, 요청마다 첨부"),
 ("method/paint-style", "Method", "칠 방식", "Coloring method", "02_line.html", "#s2", "평면 원색 ↔ 번지는 물감, 채도와 함께 정한다"),
 ("method/background-fx", "Method", "배경 효과선", "Background effect lines", "02_line.html", "#s4", "집중선·속도선은 긴장, 꽃·반짝임은 설렘. 감정 하나에 효과 하나"),
 ("method/line-of-action", "Method", "움직임 선과 러프", "Line of action and rough sketch", "03_mono.html", "#s1", "휜 정도 = 가장 먼 거리 ÷ 양 끝 직선. 러프는 움직임 선부터"),
 ("method/camera-lens", "Method", "카메라 높이와 렌즈", "Camera height and lens", "06_media_outfit.html", "#s2", "올려다보기는 당당, 내려다보기는 귀여움, 넓은 렌즈는 현장감"),
 ("concept/age-cues", "Concept", "나이 신호", "Facial age cues", "07_failure_lab.html", "#drift", "어린이: 낮은 눈 높이·큰 눈·짧은 코. 성인: 가로로 긴 눈·또렷한 코"),
 ("method/variation-diagnosis", "Method", "베리에이션 진단 순서", "Variation diagnosis order", "07_failure_lab.html", "#s1", "고정값 → 축 → 등신·나이 → 과장 → 매체·글자·출처"),
 ("application/variation-failures", "Application", "베리에이션 실패 8종", "Eight variation failures", "07_failure_lab.html", "#fails", "장식 사라짐·두 축·탁함·나이 쏠림·SD 얼굴·과장 여러 곳·조롱·가짜 글씨"),
 ("open/style-by-features", "OpenQuestion", "작품 이름 대신 특징으로", "Describing style by features, not titles", "07_failure_lab.html", "#drift", "남의 캐릭터를 닮지 않게 화풍을 선·명암·색·비율로 적는다"),
 ("application/practice", "Application", "실전 연습장", "Practice simulator", "practice/index.html", "#bench", "베리에이션 작업대·군집 분류판·문장 공방·진단 데스크"),
 ("analogy/crayons", "Analogy", "크레파스 몇 색", "Box of crayons", "01_era.html", "#s1", "12색과 48색 그림은 같은 사람도 분위기가 다르다"),
 ("analogy/subway-map", "Analogy", "노선도와 위성 사진", "Subway map vs satellite photo", "02_line.html", "#s3", "단순화의 양 끝"),
 ("analogy/highlighter", "Analogy", "형광펜", "Highlighter", "05_expression.html", "#s2", "한 줄만 그어야 눈에 띈다"),
 ("analogy/same-song", "Analogy", "같은 노래 다른 악기", "Same song, different instrument", "06_media_outfit.html", "#s1", "멜로디가 고정값"),
]
KG_EDGES = [("concept/variation-axes","motivates","method/shadow-steps"),("method/shadow-steps","motivates","method/eye-era"),("method/eye-era","motivates","concept/information-amount"),("concept/information-amount","motivates","method/color-grade"),
 ("method/color-grade","motivates","concept/line-weight-ratio"),("concept/line-weight-ratio","motivates","method/paint-style"),("method/paint-style","motivates","concept/simplification"),("concept/simplification","motivates","method/background-fx"),("method/background-fx","motivates","method/line-of-action"),("method/line-of-action","motivates","method/tone-methods"),("method/tone-methods","motivates","method/brush-space"),("method/brush-space","motivates","method/gray-value"),
 ("method/gray-value","motivates","concept/head-count"),("concept/head-count","motivates","method/sd-parts"),("method/sd-parts","motivates","method/mascot-symbols"),("method/mascot-symbols","motivates","method/motion-trail"),
 ("method/motion-trail","motivates","method/collapse-steps"),("method/collapse-steps","motivates","method/one-place"),("method/one-place","motivates","method/add-lines"),("method/add-lines","motivates","concept/manga-symbols"),
 ("concept/manga-symbols","motivates","method/render-swap"),("method/render-swap","motivates","method/camera-lens"),("method/camera-lens","motivates","method/outfit-theme"),("method/outfit-theme","motivates","method/model-sheet"),
 ("method/model-sheet","motivates","method/variation-diagnosis"),("method/variation-diagnosis","usedIn","application/variation-failures"),("method/model-sheet","explains","open/style-by-features"),("method/brush-space","explains","open/style-by-features"),
 ("method/tone-methods","explains","method/gray-value"),("concept/head-count","explains","application/variation-failures"),("method/one-place","explains","application/variation-failures"),
 ("concept/age-cues","explains","application/variation-failures"),("method/sd-parts","explains","concept/age-cues"),("analogy/crayons","explains","method/shadow-steps"),("analogy/subway-map","explains","concept/simplification"),("analogy/highlighter","explains","method/one-place"),("analogy/same-song","explains","method/render-swap"),
 ("concept/variation-axes","usedIn","application/practice"),("method/model-sheet","usedIn","application/practice")]
REFS = [
 dict(id="macqueen_1967_kmeans", title="Some methods for classification and analysis of multivariate observations", author="J. MacQueen", year=1967, note="Proc. 5th Berkeley Symposium. k-평균 군집 — 목차 스타일 지도와 연습장의 '비슷한 것끼리 묶기'"),
 dict(id="pearson_1901_pca", title="On lines and planes of closest fit to systems of points in space", author="K. Pearson", year=1901, note="Philosophical Magazine 2(11) — 주성분 분석. 여섯 축을 2차원 지도로 펼치는 방법"),
 dict(id="mccloud_1993", title="Understanding Comics: The Invisible Art", author="Scott McCloud", year=1993, note="Tundra/Kitchen Sink — 사실 ↔ 단순화 축(2부 3단계)과 만화 기호의 읽기. 책의 그림·문장은 옮기지 않음"),
 dict(id="thomas_johnston_1981", title="The Illusion of Life: Disney Animation", author="Frank Thomas, Ollie Johnston", year=1981, note="Abbeville Press — 과장(exaggeration)과 움직임 원리(4부 4단계, 5부)"),
 dict(id="itu_bt601", title="Recommendation ITU-R BT.601: Studio encoding parameters of digital television", author="ITU-R", year=1982, note="밝기(회색값) 무게 0.299·0.587·0.114 (3부 4단계)"),
 dict(id="rombach_2022_ldm", title="High-Resolution Image Synthesis with Latent Diffusion Models", author="Robin Rombach et al.", year=2022, note="CVPR 2022. arXiv:2112.10752 — 글 지시로 그림을 만드는 확산 모델(부분 수정 포함)"),
 dict(id="prev_fun", title="구조 먼저 그리기 연구실 · 웃음 편", author="안상선", year=2026, note="앞 편. 과장·데포르메·타이밍·4컷. https://adminmrobo.github.io/drawing_lab_fun/"),
 dict(id="prev_face", title="구조 먼저 그리기 연구실 03 · 얼굴 편", author="안상선", year=2026, note="얼굴 기준선·남녀 얼굴·AI 얼굴 문장. https://adminmrobo.github.io/drawing_lab_03/"),
]

def kg_block(page, pages):
    nodes = [dict(id="lab:" + i, type=t, label=dict(ko=ko, en=en), page=p, anchor=a, definition=dict(ko=d), source="lab:work/drawing_lab_fun_02")
             for i, t, ko, en, p, a, d in KG if p in pages]
    ids = {n["id"] for n in nodes}
    edges = [dict(s="lab:" + s, p=p, o="lab:" + o) for s, p, o in KG_EDGES if "lab:" + s in ids and "lab:" + o in ids]
    raw = dict(version="1.3", page=page, series=SERIES, nodes=nodes, edges=edges)
    ld = {"@context": {"@vocab": "urn:lab:", "skos": "http://www.w3.org/2004/02/skos/core#", "schema": "https://schema.org/"},
          "@graph": [{"@id": "urn:" + n["id"], "@type": n["type"], "skos:prefLabel": [{"@value": n["label"]["ko"], "@language": "ko"}, {"@value": n["label"]["en"], "@language": "en"}],
                      "skos:definition": n["definition"]["ko"], "schema:url": SITE + n["page"] + n["anchor"]} for n in nodes]}
    meta = dict(title=page, series=SERIES, creator=[dict(name="안상선", role="author", affiliation="(주)M-Robo")], date=DATE, version=VER, license="캐릭터·그림 무단 사용 금지")
    J = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section id="kg"><div class="wrap"><h2>지식 색인 — 이 페이지의 낱말 찾기</h2>
<p class="muted">이 페이지에 나온 개념·방법·비유·쓰임을 모았습니다. 검색하고, "설명 보러 가기"로 본문에 돌아갑니다.</p><div id="kg-mount"></div></div></section>
<section id="export"><div class="wrap"><h2>온톨로지·서지 꾸러미 내려받기</h2>
<p class="muted">지식 색인을 출처와 함께 파일로 내려받습니다. 서지 관리는 BibTeX·RIS, 온톨로지 편집은 Turtle, 그래프 도구는 CSV, 여러 페이지 합치기는 kg.json입니다.</p><div id="export-mount"></div></div></section>
<script type="application/json" id="kg-raw">{J(raw)}</script>
<script type="application/ld+json" id="kg-ld">{J(ld)}</script>
<script type="application/json" id="refs-csl">{J(REFS)}</script>
<script type="application/json" id="page-meta">{J(meta)}</script>
"""

FOOT_LINKS = [("index.html", "목차")] + [(P["file"], f"{P['no']}부") for P in PARTS] + [("practice/index.html", "8부 실전 연습장")]

def footer(pre=""):
    links = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in FOOT_LINKS) + f' · <a href="{REPO}">저장소</a>'
    refs = "".join(f"<tr><td>[{i+1}]</td><td>{E(r['author'])} ({r['year']}). {E(r['title'])}</td><td>{E(r['note'])}</td></tr>" for i, r in enumerate(REFS))
    return f"""<footer><div class="wrap">
<h3>출처·참고</h3>
<div class="tbl"><table><thead><tr><th>#</th><th>자료</th><th>어디에 썼나</th></tr></thead><tbody>{refs}</tbody></table></div>
<h3>예시값·설명용 숫자</h3>
<p>색 수, 1초 장수와 선 개수, 색상 회전 30도, 굵기 비, 망점 비율, 여백 50~70%, 등신, SD 눈 높이, 잔상 간격, 과장 배율, 회색값 차이 40, 일관성 점수, 스타일 지도의 특징값과 평가단 점수는 모두 원리를 보이기 위한 예시값입니다. 실제 작품과 화풍마다 다릅니다.</p>
<p>등장인물은 모두 성인 연구원입니다(하루·시아·모아는 20대, 박사는 30대 성인 남성). SD(2~3등신)는 그림체일 뿐 나이가 아닙니다. 화풍은 작품·작가 이름이 아니라 특징으로 설명하며, 다른 작품의 캐릭터를 닮은 그림은 만들지 않습니다. 사용자가 모아 준 참고 그림(밈·팬아트·화풍 분류표 등)은 페이지에 싣지 않고, 특징을 말로 정리해 군집을 나누는 데만 썼습니다.</p>
<p>캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: <a href="{CHARREPO}">fruitfly-lab-expressions</a>.</p>
<p>글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p>
<p>{links}</p>
</div></footer>
<script src="{pre}assets/panels.js"></script>
</body></html>
"""

REFS_DL = ["haru_anime_base.png", "sia_anime_base.png", "moa_anime_base.png", "haru_sheet.png", "sia_sheet.png", "moa_sheet.png", "doctor_sheet.png", "fruitfly_sprites_6.png", "jupanbot_ref_genspark_v0.png", "pixel_style_ref_prev_cover.png"]
def make_section(P):
    tasks = MAKE.get(P["no"])
    if not tasks:
        return ""
    refs = " · ".join(f'<a href="assets/refs/{f}" download>{f.replace(".png", "")}</a>' for f in REFS_DL)
    out = f"""<section class="room" id="make"><div class="wrap"><div class="roomno">{P['no']}부 · 직접 만들기</div><h2>프롬프트로 직접 만들어 보기</h2>
<div class="box"><p>이 부에서 배운 원리를 그림 생성 AI(Genspark 등)로 직접 확인합니다. <b>A</b>는 이 페이지 그림을 실제로 만든 프롬프트, <b>B</b>는 원리를 하나 빼거나 바꾼 비교용 문장입니다.</p>
<ol style="margin:6px 0 0;padding-left:20px"><li>새 대화를 열고 아래 '첨부'에 적힌 참고 그림을 올립니다.</li><li>A를 붙여 넣어 만들고, 확인표로 결과를 점검합니다.</li><li>같은 대화에 B를 이어 붙여 다시 만들고, A 결과와 나란히 비교합니다. 구도가 흔들리면 'keep the same framing'을 덧붙입니다.</li><li>같은 대화에서 차이가 약하면 새 대화에서 처음부터 만들어 보세요. 결과는 매번 다릅니다.</li></ol>
<p class="hint" style="margin-top:8px">참고 그림 내려받기: {refs}</p></div>"""
    for i, t in enumerate(tasks, 1):
        A = PROMPTS[t["key"]][4]
        att = ATTACH_OF[CONV_OF[t["key"]]]
        ar = "16/9" if "16:9" in A.split("\n")[0] else "2/3"
        alt = PROMPTS[t["img"]][3]
        chk = "".join(f'<li>{E(c)}' + (f' <a href="{l}">원리 보기</a>' if l else "") + "</li>" for c, l in t["check"])
        k = t["b_imgs"][0]
        bbox = f'<div class="promptbox"><b>{E(t["b_title"])}</b><pre>{E(t["b_text"])}</pre><button type="button" class="btn copy">복사하기</button></div>'
        bpart = f'<div class="pair">{bbox}<div>{art(k, "비교 결과 — " + t["b_title"], ar, "B 결과")}</div></div>'
        res = f'<p style="background:#fff7ec;border-left:4px solid var(--orange);padding:8px 12px;border-radius:6px">{E(t["res"])}</p>' if t.get("res") else ""
        tip = f'<p class="hint">{E(t["tip"])}</p>' if t.get("tip") else ""
        out += f"""<div class="failcard" id="make{i}"><h3>실습 {i} · {E(t['title'])}</h3><p>{E(t['goal'])}</p>
<div class="pair"><div class="promptbox"><b>A — 이 페이지 그림을 실제로 만든 프롬프트</b><p class="hint">첨부: {E(att)}</p><pre>{E(A)}</pre><button type="button" class="btn copy">복사하기</button></div>
<div>{art(t['img'], alt, ar, "A 결과 — Genspark로 만든 그림")}</div></div>
{bpart}<h4>결과에서 확인할 것</h4><ol>{chk}</ol>{res}{tip}</div>"""
    return out + "</div></section>"

def res_html(no, did):
    t = DRILL_RES.get(f"{no}-{did}")
    if t and f"{no}-{did}" in RETRY:
        t = t.replace("실제 결과:", "1차 시도 결과:", 1)
    return f'<p style="background:#fff7ec;border-left:4px solid var(--orange);padding:8px 12px;border-radius:6px">{E(t)}</p>' if t else ""

def retry_html(no, did, shown):
    r = RETRY.get(f"{no}-{did}")
    if not r:
        return ""
    out = f'<div class="box" style="border-left:4px solid var(--blue);margin-top:14px"><h4 style="margin-top:0">다시 시도 — 1차 결과는 위에 그대로 두고, 방법을 바꿔 다시 받습니다</h4><p>{E(r["why"])}</p>'
    for lab, how, pr, key, alt, ar, ok in r["items"]:
        pic = "" if key in shown else f"<div>{art(key, alt, ar, alt)}</div>"
        out += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><p class="hint">방법: {E(how)}</p><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div>{pic}</div>
<p><span class="chip">성공 기준</span>{E(ok)}</p>"""
    rr = RETRY_RES.get(f"{no}-{did}")
    if rr:
        col = {"성공": "var(--green)", "부분 성공": "var(--orange)", "실패": "var(--red)"}[rr[0]]
        out += f'<p style="border-left:4px solid {col};background:#f7f9fb;padding:8px 12px;border-radius:6px"><b style="color:{col}">다시 시도 결과 · {rr[0]}</b> — {E(rr[1])}</p>'
    r3 = RETRY3.get(f"{no}-{did}")
    if r3:
        out += f'<h4>3차 시도 — 새 대화에서 크게 과장해 다시 받습니다</h4><p>{E(r3["why"])}</p>'
        for lab, how, pr, key, alt, ar, ok in r3["items"]:
            out += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><p class="hint">방법: {E(how)}</p><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div><div>{art(key, alt, ar, alt)}</div></div>
<p><span class="chip">성공 기준</span>{E(ok)}</p>"""
        r3r = RETRY3_RES.get(f"{no}-{did}")
        if r3r:
            col = {"성공": "var(--green)", "부분 성공": "var(--orange)", "실패": "var(--red)"}[r3r[0]]
            out += f'<p style="border-left:4px solid {col};background:#f7f9fb;padding:8px 12px;border-radius:6px"><b style="color:{col}">3차 시도 결과 · {r3r[0]}</b> — {E(r3r[1])}</p>'
    return out + "</div>"

def drill_section(P):
    ds = DRILL.get(P["no"])
    if not ds:
        return ""
    keys = [p[2] for d in ds for p in d["prompts"]]
    made = "예상 결과 그림은 아래 프롬프트로 실제로 만든 그림입니다. 요청과 다르게 나온 곳은 '실제 결과'에 그대로 적었습니다." if all(has_img(k) for k in keys) else "예상 결과 그림은 아래 프롬프트로 실제로 만든 그림입니다(아직 받지 않은 그림은 '그림 준비 중'). 요청과 다르게 나온 곳은 '실제 결과'에 그대로 적었습니다."
    out = f"""<section class="room" id="drill"><div class="wrap"><div class="roomno">{P['no']}부 · 연습 과제</div><h2>프롬프트 연습 과제</h2>
<div class="box"><p>이 부의 원리를 내 손으로 프롬프트에 옮겨 보는 과제 두 개입니다. 과제마다 <b>목표 → 순서 → 넣을 프롬프트 → 확인할 것 → 예상 결과 → 자주 생기는 문제</b> 순서로 적었습니다. {made} 결과는 매번 조금씩 다르니, 그림이 똑같지 않아도 '확인할 것'이 맞으면 성공입니다.</p></div>"""
    for i, d in enumerate(ds, 1):
        steps = "".join(f"<li>{E(x)}</li>" for x in d["steps"])
        prs = ""
        for lab, pr, key, alt, ar in d["prompts"]:
            prs += f"""<div class="pair"><div class="promptbox"><b>{E(lab)}</b><pre>{E(pr)}</pre><button type="button" class="btn copy">복사하기</button></div><div>{art(key, alt, ar, alt)}</div></div>"""
        chk = "".join(f'<li>{E(c)}' + (f' <a href="{l}">원리 보기</a>' if l else "") + "</li>" for c, l in d["check"])
        tr = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in d["trouble"])
        out += f"""<div class="failcard" id="{d['id']}"><h3>연습 {i} · {E(d['title'])}</h3>
<p><span class="chip">목표</span>{E(d['goal'])}</p><p><span class="chip">왜 이 연습인가</span>{E(d['why'])}</p>
<p class="hint">첨부할 참고 그림: {E(d['attach'])} — 참고 그림은 위 <a href="#make">직접 만들어 보기</a>에서 내려받을 수 있습니다.</p>
<h4>순서</h4><ol>{steps}</ol>
<h4>넣을 프롬프트와 예상 결과</h4>{prs}
<h4>확인할 것</h4><ol>{chk}</ol>
<div class="easy"><b>예상 결과</b> — {E(d['expect'])}</div>{res_html(P['no'], d['id'])}{retry_html(P['no'], d['id'], [p[2] for p in d['prompts']])}
<h4>자주 생기는 문제와 대처</h4><div class="tbl"><table><thead><tr><th>문제</th><th>이렇게 고칩니다</th></tr></thead><tbody>{tr}</tbody></table></div>
<p><span class="chip">더 해 보기</span>{E(d['more'])}</p></div>"""
    return out + "</div></section>"

def build_part(P):
    t = f"{SERIES} {P['no']}부 — {P['title']}"
    s = head(t, P["desc"], P["og"], P["file"])
    navl = [(f"#{x['id']}", f"{k+1}단계") for k, x in enumerate(P["steps"])]
    if P.get("fails"): navl += [("#fails", "실패 8종")]
    navl += [("#make", "직접 만들기"), ("#drill", "연습 과제"), ("#judge", "평가"), ("#sum", "정리"), (P["next"][0], "다음 →")]
    s += nav(navl)
    s += cover(P["cover_key"], P["cover_cap"], P["cover_cast"])
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">{E(P['kicker'])}</span><h1>{E(P['title'])}</h1><p class="lead">{E(P['lead'])}</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three(*P['three'], ABBR)}</div></section>
<section><div class="wrap"><h2>오늘의 과제</h2>{talk(P['intro'])}{flow_strip(P['no'])}</div></section>
"""
    for k, st in enumerate(P["steps"]):
        s += step(P, k + 1, st)
    if P.get("fails"):
        s += '<section class="room" id="fails"><div class="wrap"><div class="roomno">7부 · 2단계</div><h2>베리에이션 실패 8종 진단</h2><p class="muted">그림마다 증상을 보고 처음 걸리는 점검 항목을 고른 뒤, 연결된 원리와 고치는 프롬프트 조각을 확인합니다.</p>'
        s += "".join(failcard(f) for f in P["fails"])
        d = P["drift"]
        s += f'<div class="failcard" id="drift"><h3>{E(d["title"])}</h3>' + "".join(f"<p>{E(x)}</p>" for x in d["body"]) + '<p><span class="chip">연결된 원리</span><a href="03_mono.html#s3">3부 3단계 붓선과 여백</a> · <a href="06_media_outfit.html#s4">6부 4단계 설정 시트</a></p></div></div></section>'
    s += make_section(P)
    s += drill_section(P)
    s += judge(P["judge"]) + summary(P) + outro(P)
    s += kg_block(P["file"].replace(".html", ""), [P["file"]])
    s += footer()
    open(os.path.join(ROOT, P["file"]), "w").write(s)

FLOW = [
 (1, "시대 베리에이션", "'옛날풍'이라고만 하면 색만 바래고 얼굴과 칠은 그대로다", "그림자 단계·눈·정보량·색보정"),
 (2, "선과 지역 베리에이션", "작품 이름으로 화풍을 부르면 남의 캐릭터를 닮는다", "굵기 비·칠 방식·단순화·배경 효과선"),
 (3, "흑백·선화 베리에이션", "컬러를 흑백으로 바꾸기만 하면 경계와 동작이 사라진다", "움직임 선·망점과 해칭·붓선과 여백·회색값"),
 (4, "등신 베리에이션", "통째로 줄이면 SD가 아니라 작은 사람이 된다", "등신 계산·부위 함께 줄이기·마스코트·잔상"),
 (5, "표정·과장 베리에이션", "전부 키우면 아무것도 읽히지 않는다", "무너짐 단계·한 곳 과장·선 더하기·만화 기호"),
 (6, "매체·옷 베리에이션", "재료와 옷이 바뀔 때마다 다른 사람이 되어 간다", "재료·카메라·옷 테마·설정 시트"),
 (7, "베리에이션 실패 실험실", "문장을 써도 베리에이션은 흔들릴 수 있다", "진단 순서와 고치는 조각, 특징으로 적기, 나이 신호"),
 (8, "실전 연습장", "배운 축을 한 화면에서 함께 다뤄 본다", "작업대·분류판·문장 공방·진단 데스크"),
]
def flow_strip(cur=None, pre=""):
    files = {P["no"]: P["file"] for P in PARTS}
    files[8] = "practice/index.html"
    cells = []
    for n, t, _, _ in FLOW:
        mark = ' style="border-color:var(--orange);background:var(--orange-soft)"' if n == cur else ""
        cells.append(f'<a href="{pre}{files[n]}"{mark}><b>{n}부</b>{E(t)}</a>')
    return '<div class="flowgrid" style="grid-template-columns:repeat(auto-fit,minmax(130px,1fr));margin-top:16px">' + "".join(cells) + "</div>"

def style_json():
    from style_points import PTS, AXES, GROUPS
    J = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/json" id="style-pts">{J(dict(axes=AXES, groups=GROUPS, pts=[dict(id=i, d=d, g=g, alt=a, f=f) for i, d, g, a, f in PTS]))}</script>'

MAPMATH = dict(ask="'비슷하다'를 기계는 어떻게 재요?",
  words="그림마다 특징 점수를 매기고, 두 그림의 점수 차이를 축마다 제곱해 더한 뒤 제곱근을 씌웁니다. 지도 위 두 점 사이의 거리와 같습니다.",
  tries=["두 축만 보자: 그림 A (시대 0.2, 사실 0.9), 그림 B (시대 0.8, 사실 0.5)", "차이 0.6과 −0.4 → 0.36 + 0.16 = 0.52", "거리 = √0.52 ≈ 0.72 — 가까울수록 같은 군집에 들어간다"],
  school="피타고라스 정리 — 가로·세로 차이로 빗변(거리)을 구합니다. 축이 여섯 개여도 같은 방법입니다.",
  formula="거리 = √( (시대 차)² + (선 차)² + (사실 차)² + (과장 차)² + (재료 차)² + (색 차)² )",
  pieces=[("특징 점수", "0~1로 매긴 값(예시값)"), ("차의 제곱", "멀리 떨어진 축을 더 크게 센다"), ("√", "제곱한 것을 원래 길이로 되돌린다")],
  comment="지도에서 가까운 점끼리 묶는 거니까, 정답을 안 알려 줘도 비슷한 그림끼리 모이는 거네요!")

def build_index():
    from style_points import PTS, GROUPS
    t = f"{SERIES} — 같은 캐릭터, 다른 그림"
    d = "참고 그림 70여 장을 비슷한 것끼리 넓게 묶은 일곱 군집(시대·선과 지역·흑백·등신·표정·매체와 옷·실패)을 따라, 같은 캐릭터를 다양한 그림체로 즐겁게 바꿔 그리는 법을 실험으로 익힙니다."
    s = head(t, d, "og_index.jpg", "index.html")
    s += nav([("#howto", "읽는 법"), ("#parts", "편 목록"), ("#map", "스타일 지도"), ("#flow", "전체 흐름"), ("#cast", "등장인물"), ("#source", "원리와 출처")])
    s += cover("cover_index", "연구실 갤러리 벽 · 같은 세 사람의 여러 버전을 군집으로 묶는 초파리", [("fruitfly", "e09"), ("haru", "e19"), ("sia", "e13"), ("moa", "e01"), ("doctor", "e16"), ("jupanbot", "e16")])
    cnt = {g: sum(1 for p in PTS if p[2] == g) for g in GROUPS}
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">연구실 특별편 · 웃음 편 2 · 베리에이션</span>
<h1>구조 먼저 그리기 연구실<br>베리에이션 — 같은 캐릭터, 다른 그림</h1>
<p class="lead">80년대 셀화, 맑은 유럽 선, 수묵 붓선, 2.5등신 SD, 무너진 개그 얼굴, 3D 피규어, 잡지 포스터까지. 하루·시아·모아·박사를 <b>여러 그림체로 즐겁게 바꿔 그리며</b>, 무엇을 바꾸고 무엇을 남겨야 같은 캐릭터로 보이는지 실험합니다. 출발점은 참고 그림 70여 장을 <b>정답 없이 비슷한 것끼리 넓게 묶은 스타일 지도</b>입니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section><div class="wrap">{three("같은 캐릭터를 시대·선·흑백·등신·표정·매체와 옷의 여섯 갈래로 바꿔 그리는 법과, 베리에이션이 실패하는 여덟 가지 모습을 실험으로 익힙니다.", "그림체를 바꿀 때마다 무엇을 남길지 모르면, 버전이 늘수록 다른 캐릭터가 되거나 남의 작품을 닮아 갑니다.", "팬아트·굿즈·포스터·스티커·리메이크 비교, 그리고 AI에게 그림체를 작품 이름 없이 특징으로 요청하는 문장에 씁니다.", ABBR)}</div></section>
<section id="howto"><div class="wrap"><h2>읽는 순서와 시간</h2><div class="box"><ul style="margin:0;padding-left:20px">
<li><b>처음부터 차례로</b>(권장): 아래 스타일 지도를 한 번 눌러 본 뒤 1부부터. 부마다 20~30분, 전체 3시간 안팎입니다.</li>
<li><b>앞 편을 안 봤다면</b>: 바로 읽어도 됩니다. 과장·타이밍은 <a href="{PREV_SITE}">웃음 편</a>, 얼굴 기준선은 <a href="{FACE_SITE}">03 얼굴 편</a>, 옷 주름은 <a href="{CLOSET_SITE}">01 옷장 편</a>에 있습니다.</li>
<li><b>궁금한 군집부터</b>: 부마다 따로 읽혀요. 다만 6부 4단계 '설정 시트'와 7부 '진단 순서'는 모든 부에 다시 쓰입니다.</li>
<li>각 부 끝의 <b>평가단 채점</b>은 이야기 속 예시 점수입니다. 확인 퀴즈와 실전 연습장 미션으로 스스로 점검하세요.</li></ul></div></div></section>
<section id="parts"><div class="wrap"><h2>편 목록</h2>
<p class="muted">부마다 주판봇(결과부터 서두름)과 초파리(바꿀 것과 남길 것부터 나눔)가 같은 캐릭터의 베리에이션을 겨루고, 평가단 X1·X2·X3가 점수를 매깁니다.</p>
<div class="cards">
<a class="card" href="01_era.html">{face("moa","e01")}<span class="n">1부 · 모델 모아</span><h3>시대 베리에이션</h3><p>그림자 단계, 눈의 반짝임, 정보량, 색보정으로 80년대부터 지금까지.</p></a>
<a class="card" href="02_line.html">{face("sia","e13")}<span class="n">2부 · 모델 시아</span><h3>선과 지역 베리에이션</h3><p>굵기 비, 칠 방식, 단순화, 집중선과 반짝임.</p></a>
<a class="card" href="03_mono.html">{face("moa","e14")}<span class="n">3부 · 모델 모아·시아·하루</span><h3>흑백·선화 베리에이션</h3><p>움직임 선과 러프, 망점·해칭·먹칠, 붓선과 여백, 컬러와 흑백의 회색값.</p></a>
<a class="card" href="04_proportion.html">{face("haru","e19")}<span class="n">4부 · 모델 하루</span><h3>등신 베리에이션</h3><p>8등신에서 2.5등신 SD, 마스코트 피규어, 등신별 움직임.</p></a>
<a class="card" href="05_expression.html">{face("sia","e14")}<span class="n">5부 · 모델 시아 · 손님 박사</span><h3>표정·과장 베리에이션</h3><p>무너짐 단계, 한 곳 과장, 선 더하기, 만화 기호.</p></a>
<a class="card" href="06_media_outfit.html">{face("moa","e19")}<span class="n">6부 · 모델 셋 모두</span><h3>매체·옷 베리에이션</h3><p>셀·3D·먹·픽셀, 카메라 높이와 렌즈, 옷 테마와 포스터, 설정 시트.</p></a>
<a class="card" href="07_failure_lab.html">{face("jupanbot","e20")}<span class="n">7부 · 의도적 실패 8종</span><h3>베리에이션 실패 실험실</h3><p>증상 → 처음 걸린 곳 → 원리 → 고치는 조각. 작품 이름 대신 특징으로.</p></a>
<a class="card" href="practice/index.html">{face("x2","e16")}<span class="n">8부 · 마지막 장</span><h3>실전 연습장</h3><p>베리에이션 작업대·군집 분류판·문장 공방·진단 데스크.</p></a>
</div></div></section>
<section id="map" class="room"><div class="wrap"><div class="roomno">시작하기 · 스타일 지도</div><h2>참고 그림 70여 장을 비슷한 것끼리 넓게 묶으면</h2>
<p class="muted">모아 둔 참고 그림(밈·팬아트·애니 장면·화풍 분류표·AI 그림)을 여섯 특징(시대·선·사실·과장·재료·색)으로 점수 매겨 60개 점으로 정리했습니다. 비슷한 그림은 한 점으로 합쳤고, 그림과 작품 이름은 싣지 않았습니다. 정답 없이 가까운 점끼리 묶는 방법(k-평균 군집)을 직접 돌려 보세요.</p>
<div class="duo"><div class="box why"><h4>왜 이렇게 하나</h4><ol><li><b>무엇이 문제인가</b> — 그림체는 수없이 많아서 하나씩 배우면 끝이 없습니다.</li><li><b>그냥 하면 막히는 곳</b> — 그림 하나에 정답 하나만 붙여 나누면(하나만 켜지는 표시처럼), 두 군집에 걸친 그림을 설명하지 못하고 묶음이 너무 잘게 나뉩니다.</li><li><b>이렇게 푼다</b> — 특징이 비슷한 것끼리 넓게 묶어 군집 몇 개로 줄이고, 군집마다 '바꾸는 축'을 배웁니다. 경계에 걸친 그림은 걸친 대로 둡니다.</li></ol><div class="easy"><b>쉽게 말하면</b> — 옷장 정리를 옷 하나하나가 아니라 '겉옷·바지·운동복'처럼 큰 묶음으로 하면, 새 옷이 와도 어디에 둘지 바로 압니다.</div></div>{mathbox(MAPMATH)}</div>
{talk([("doctor","e07","군집 수를 2로 하면 어떻게 묶일까? 8로 하면?"),("jupanbot","e16","많을수록 정확합니다! 그림마다 하나씩 60개로 나누겠습니다!"),("fruitfly","e09","그건 묶은 게 아니야. 이걸 눌러 봐 — 군집 수를 2에서 8까지."),("haru","e10","2는 너무 크게 갈리고, 6~7쯤에서 흑백 그림이 따로 한 군집으로 모여요. 이 편이 흑백을 3부로 따로 둔 까닭이에요!")])}
<div class="panel"><div class="ph"><b>실험 0-1</b><small>군집 수와 쓸 특징을 바꿔 보세요 · 점에 손가락이나 마우스를 대면 설명이 보입니다</small></div><div id="pp-p0_map" data-panel="p0_map"></div>
<div class="ctrl"><label>군집 수 k <input type="range" name="k" min="2" max="8" step="1" value="7"></label><label><input type="checkbox" name="human"> 이 편의 부(사람이 붙인 이름)로 색칠</label>
<label><input type="checkbox" name="a0" checked> 시대</label><label><input type="checkbox" name="a1" checked> 선</label><label><input type="checkbox" name="a2" checked> 사실</label><label><input type="checkbox" name="a3" checked> 과장</label><label><input type="checkbox" name="a4" checked> 재료</label><label><input type="checkbox" name="a5" checked> 색</label></div><div class="readout" aria-live="polite"></div></div>
<div class="solve"><h4>풀이</h4><p>군집 수가 작으면 아주 넓게, 크면 잘게 묶입니다. 이 편은 '너무 잘게 나누지 않는다'는 원칙으로 일곱 군집을 골랐습니다. 처음에는 여섯이었는데, 흑백 그림이 기계 군집에서도 따로 모여 흑백을 독립시켰습니다.</p><p>기계가 나눈 군집과 이 편의 부(사람이 붙인 이름)는 대부분 겹치지만 완전히 같지는 않습니다. 이 편은 기계 결과를 참고로 삼고, 가르치기 좋은 축을 기준으로 이름을 붙였습니다.</p><p>두 군집 사이에 걸친 그림(테두리가 두꺼운 점)은 두 부에서 모두 다룹니다. 예: SD 발차기는 4부 등신과 5부 과장 모두에 해당합니다.</p></div>
<div class="tbl" style="margin-top:14px"><table><thead><tr><th>군집(부)</th><th>묶인 점</th><th>주로 바뀌는 축</th><th>배우는 곳</th></tr></thead><tbody>
<tr><td>시대</td><td>{cnt[1]}</td><td>시대 · 색</td><td><a href="01_era.html">1부</a></td></tr>
<tr><td>선과 지역</td><td>{cnt[2]}</td><td>선 · 사실</td><td><a href="02_line.html">2부</a></td></tr>
<tr><td>흑백·선화</td><td>{cnt[3]}</td><td>색(흑백) · 선</td><td><a href="03_mono.html">3부</a></td></tr>
<tr><td>등신</td><td>{cnt[4]}</td><td>사실(SD ↔ 사실) · 재료</td><td><a href="04_proportion.html">4부</a></td></tr>
<tr><td>표정·과장</td><td>{cnt[5]}</td><td>과장</td><td><a href="05_expression.html">5부</a></td></tr>
<tr><td>매체·옷</td><td>{cnt[6]}</td><td>재료 · 색 · 옷</td><td><a href="06_media_outfit.html">6부</a></td></tr>
<tr><td>AI 실수·권리 점검</td><td>{cnt[7]}</td><td>(모든 축에 걸침)</td><td><a href="07_failure_lab.html">7부</a></td></tr></tbody></table></div>
<div class="limit"><b>주의할 점</b> — 특징 점수는 그림을 보고 사람이 매긴 예시값이라, 매기는 사람에 따라 달라집니다. k-평균은 처음 고른 중심에 따라 결과가 조금씩 달라질 수 있어, 이 페이지에서는 같은 결과가 나오도록 시작점을 고정했습니다.</div>
</div></section>
<section id="flow"><div class="wrap"><h2>전체 흐름 — 1부부터 8부까지 이어지는 순서</h2>{flow_strip()}
<div class="tbl" style="margin-top:16px"><table><thead><tr><th>부</th><th>제목</th><th>이 부를 배우는 까닭</th><th>핵심</th></tr></thead><tbody>
{''.join(f"<tr><td>{n}</td><td>{E(t)}</td><td>{E(a)}</td><td>{E(b)}</td></tr>" for n, t, a, b in FLOW)}</tbody></table></div>
<h3 style="margin-top:22px">모든 베리에이션에서 남기는 고정값</h3>
<div class="tbl"><table><thead><tr><th>캐릭터</th><th>고정값(어느 버전에서도 그대로)</th></tr></thead><tbody>
<tr><td>하루</td><td>분홍 긴 머리 + 남색 줄, 정수리 번 2개, 앞머리 가운데 남색 줄, 라벤더 후드, 20대 성인</td></tr>
<tr><td>시아</td><td>검은 긴 생머리, 머리 장식 없음, 은 귀걸이, 회색 눈, 20대 성인</td></tr>
<tr><td>모아</td><td>회갈색 웨이브 머리, 흰 프릴 머리띠, <b>왼쪽</b> 귀 위 흰 리본, 호박색 눈, 20대 성인</td></tr>
<tr><td>박사</td><td>흰 줄이 있는 짙은 뾰족 머리, 굵은 눈썹, 청록 사각 안경, 30대 성인 남성</td></tr></tbody></table></div>
<p class="muted" style="margin-top:12px">같은 시리즈: <a href="{PREV_SITE}">웃음 편(과장·타이밍·4컷)</a> · <a href="{FACE_SITE}">03 얼굴 편</a> · <a href="{CLOSET_SITE}">01 옷장 편</a> · <a href="{FIRST_SITE}">구조 먼저 보는 캐릭터 그리기 연구실</a> · <a href="{RENDER}">AI 렌더링 연구실</a></p></div></section>
<section id="cast"><div class="wrap"><h2>등장인물</h2><div class="cast-grid">{''.join(f'<div class="who">{face(k, "e01" if k in ("haru","sia","moa") else "e13")}<b>{E(CH[k][0])}</b><span>{E(CH[k][1])}</span></div>' for k in ["doctor","haru","sia","moa","jupanbot","fruitfly","x1","x2","x3"])}</div>
<p class="hint" style="margin-top:10px">하루·시아·모아는 20대 성인 연구원, 박사는 30대 성인 남성입니다. 2~3등신 SD로 그려도 나이는 그대로입니다.</p></div></section>
<section id="source"><div class="wrap"><h2>원리와 출처</h2>
<p>이 편의 군집은 사용자가 모아 준 참고 그림 70여 장(애니·만화 장면, 밈, 팬아트, AI 그림, 서양·일본 만화 화풍 분류표 두 장)을 특징으로 정리해 비슷한 것끼리 넓게 묶은 결과입니다. 참고 그림은 저작권이 있는 남의 작품이 대부분이라 <b>페이지에 싣지 않았고</b>, 작품·캐릭터 이름도 적지 않았습니다. 그림마다 '무엇이 바뀌었나'만 특징으로 옮겨 적었습니다. 작가가 'AI 학습 금지'를 밝힌 그림은 그림 요청에 첨부하지 않고 구도만 말로 참고했습니다.</p>
<p>각 부의 원리(그림자 단계, 굵기 비, 망점, 단순화 축, 등신, 과장, 회색값, 설정 시트)는 일반적인 만화·애니메이션 작화 원리이며, 단순화 축은 McCloud(1993), 과장과 움직임은 Thomas·Johnston(1981), 회색값은 ITU-R BT.601, 군집과 지도는 k-평균(MacQueen 1967)과 주성분 분석(Pearson 1901)을 바탕으로 쉽게 풀었습니다. 페이지의 그림은 모두 연구실 캐릭터로 Genspark에 요청해 만들며(요청문 docs/image_requests), 받기 전에는 '그림 준비 중'으로 둡니다. 실험 패널은 모두 페이지 안에서 직접 계산해 그립니다.</p></div></section>
"""
    s += style_json()
    s += kg_block("index", [P["file"] for P in PARTS] + ["practice/index.html", "index.html"])
    s += footer()
    open(os.path.join(ROOT, "index.html"), "w").write(s)

def build_practice():
    pre = "../"
    t = f"{SERIES} 8부 — 실전 연습장"
    d = "베리에이션 작업대(축 맞추기), 군집 분류판(그림 설명을 군집에 넣기), 베리에이션 문장 공방(AI 문장 조립), 진단 데스크(실패 맞히기) 네 곳에서 1~7부를 함께 연습합니다."
    s = head(t, d, "og_08.jpg", "practice/index.html", pre)
    s += nav([("#bench", "작업대"), ("#sort", "분류판"), ("#workshop", "공방"), ("#desk", "진단 데스크"), ("#wrap", "마무리")], pre)
    s += cover("cover_08", "연구실 조종 책상 · 군집 지도 위의 점을 옮기는 하루", [("haru", "e19"), ("doctor", "e16"), ("fruitfly", "e09"), ("jupanbot", "e16")], pre)
    s += f"""<header class="hero"><div class="wrap"><span class="kicker">8부 · 마지막 장</span><h1>실전 연습장</h1>
<p class="lead">네 곳의 작업대를 직접 운영합니다. <span style="color:var(--green)">초록 조작판</span>은 주어진 환경, <span style="color:var(--blue)">파랑 조작판</span>은 내 결정입니다. 미션은 직접 조작해야 판정됩니다.</p>
<p class="byline">글 · 안상선 ((주)M-Robo 대표) · <a href="{AUTHOR_URL}">저자 소개</a> · {DATE} · {VER}</p></div></header>
<section id="practice"><div class="wrap">
<div class="tabs" role="tablist"><button type="button" data-t="bench">베리에이션 작업대</button><button type="button" data-t="sort">군집 분류판</button><button type="button" data-t="workshop">베리에이션 문장 공방</button><button type="button" data-t="desk">진단 데스크</button></div>
"""
    def sc(id_, title, situ, env, me, missions, back, extra_g1=""):
        ms = "".join(f"<li>{E(m)}</li>" for m in missions)
        bk = " · ".join(f'<a href="{pre}{h}">{E(t)}</a>' for h, t in back)
        return f"""<div class="scene" id="{id_}"><h2>{E(title)}</h2><div class="box"><b>상황</b> — {E(situ)}</div>
<div class="panel"><div class="ph"><b>조작판</b><small>초록 = 환경 · 파랑 = 내 결정</small></div>
<div class="ctrl ctl-env">{env}</div><div class="ctrl ctl-me">{me}</div>
<div class="board" aria-live="polite"></div>
<div class="pair"><div class="g1">{extra_g1}</div><div class="g2"></div></div>
<div class="talk"></div>
<h4>미션</h4><ol class="missions">{ms}</ol></div>
<p class="muted">배운 곳 다시 보기: {bk}</p></div>
"""
    rng = lambda n, lab, v: f'<label>{lab} <input type="range" name="{n}" min="0" max="100" step="5" value="{v}"></label>'
    s += sc("bench", "베리에이션 작업대 — 목표 군집으로 옮기기", "캐릭터와 목표 군집이 주어집니다. 여섯 특징 손잡이를 돌려 지금 그림을 목표 군집의 중심 가까이(거리 0.25 이하) 옮깁니다. 고정값은 언제나 그대로입니다.",
            '<label>캐릭터 <select name="who"><option value="haru" selected>하루</option><option value="sia">시아</option><option value="moa">모아</option></select></label><label>목표 <select name="target"><option value="retro" selected>80년대 셀화</option><option value="sd">SD 개그</option><option value="ink">수묵 붓선</option><option value="toy">3D 마스코트</option><option value="graphic">흑백 그래픽 노블</option><option value="sketch">흑백 러프 선화</option><option value="modern">지금의 애니</option></select></label>',
            rng("era", "시대", 80) + rng("line", "선(굵고 강약)", 30) + rng("real", "사실(↔ SD)", 50) + rng("exag", "과장", 20) + rng("media", "재료(2D ↔ 3D)", 10) + rng("color", "색(흑백 ↔ 원색)", 80),
            ["지금 목표 군집에 거리 0.25 이하로 들어가기", "서로 다른 목표 3개를 완성하기", "목표 7개를 모두 완성하기"],
            [("01_era.html", "1부 시대"), ("02_line.html", "2부 선"), ("03_mono.html", "3부 흑백"), ("04_proportion.html", "4부 등신"), ("06_media_outfit.html#s1", "6부 재료")])
    s += sc("sort", "군집 분류판 — 그림 설명을 군집에 넣기", "참고 그림의 설명 카드가 하나씩 들어옵니다. 어느 군집(부)에 넣을지 고르세요. 두 군집에 걸친 카드는 둘 중 어느 쪽도 정답입니다.",
            '<span class="hint">환경: 카드는 무작위로 들어옵니다. 테두리 표시가 있는 카드는 경계 카드입니다.</span>',
            '<div style="width:100%"><p class="sym" style="font-weight:600"></p><div class="opts sortopts"></div></div>',
            ["5장 맞히기", "경계 카드 2장 맞히기", "일곱 군집에 모두 한 장 이상 넣기"],
            [("index.html#map", "목차 스타일 지도")])
    s += sc("workshop", "베리에이션 문장 공방 — 요청서 조립", "요청 상황에 맞춰 베리에이션 문장을 조립합니다. 점검표 6조각(고정값·바꾸는 축 하나·등신·과장·특징 표현·성인과 금지)을 채우고 경고를 없앱니다.",
            '<label>요청 상황 <select name="job"><option value="sticker">SD 스티커(등신·나이 중요)</option><option value="retro">레트로 포스터(축 하나·고정값 중요)</option><option value="ink">수묵 엽서(글자 금지·특징 표현 중요)</option></select></label>',
            '<div class="ow" style="width:100%"></div>',
            ["점검표 6 / 6을 경고 없이 채우기", "SD 등신 + 성인 명시로 SD 스티커 문장 만들기", "수묵 붓선 + 글자 금지 + 특징 표현으로 수묵 엽서 문장 만들기"],
            [("06_media_outfit.html#s4", "6부 4단계 설정 시트"), ("07_failure_lab.html#drift", "7부 특징으로 적기")],
            '<div class="promptbox"><b>조립된 베리에이션 문장</b><pre aria-live="polite"></pre><button type="button" class="btn copy">복사하기</button></div>')
    s += sc("desk", "진단 데스크 — 원인 맞히기", "베리에이션 실패의 증상이 하나씩 들어옵니다. 원인을 고르세요. 순서: 고정값 → 바꾸는 축 → 등신·나이 → 과장 → 매체·글자·출처.",
            '<span class="hint">환경: 증상은 무작위로 들어옵니다.</span>',
            '<div style="width:100%"><p class="sym" style="font-weight:600"></p><div class="opts deskopts"></div></div>',
            ["3개 연속 정답", "8종 원인을 모두 한 번 이상 맞히기", "틀리지 않고 5개 맞히기"],
            [("07_failure_lab.html#s1", "7부 진단 순서"), ("07_failure_lab.html#fails", "7부 실패 8종")])
    s += f"""</div></section>
<section id="wrap"><div class="wrap"><h2>마무리 — 네 작업대를 하나로 묶으면</h2>
<div class="box"><p>작업대에서 돌린 여섯 특징은 공방의 '바꾸는 축' 조각이 되고, 분류판에서 익힌 군집은 '무엇을 바꾸는가'를 한 단어로 부르는 이름이 됩니다. 진단 데스크에서 틀린 원인은 대부분 고정값을 빠뜨렸거나 축을 둘 이상 바꾼 경우입니다. 베리에이션은 결국 <b>고정값은 붙잡고, 축 하나를 돌리는 일</b>입니다.</p>
<p><b>실제 그림으로 이어 가기</b> — 공방에서 조립한 문장을 복사해 그림 생성 AI에 넣어 보세요. 참고 그림은 연구실 캐릭터 기준 그림만 첨부합니다. 결과는 각 부의 '프롬프트로 직접 만들어 보기' 확인표로 점검합니다: <a href="{pre}01_era.html#make">1부</a> · <a href="{pre}02_line.html#make">2부</a> · <a href="{pre}03_mono.html#make">3부</a> · <a href="{pre}04_proportion.html#make">4부</a> · <a href="{pre}05_expression.html#make">5부</a> · <a href="{pre}06_media_outfit.html#make">6부</a> · <a href="{pre}07_failure_lab.html#make">7부</a></p>
<p class="hint">주의할 점: 목표 군집의 중심값과 판정 거리 0.25는 원리를 보이기 위해 정한 예시값입니다. 실제 화풍은 이 여섯 특징보다 훨씬 많은 특징으로 이루어져 있습니다.</p></div>
<div class="next"><a href="{pre}07_failure_lab.html">← 7부 베리에이션 실패 실험실</a><a href="{pre}index.html">목차로</a></div></div></section>
"""
    s += style_json()
    s += kg_block("practice_index", ["practice/index.html"])
    s += footer(pre)
    open(os.path.join(ROOT, "practice", "index.html"), "w").write(s)

if __name__ == "__main__":
    JS = ["js_base.js", "js_practice_util.js", "js_var.js", "js_tail.js"]
    os.makedirs(os.path.join(ROOT, "practice"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "panels.js"), "w").write("".join(open(os.path.join(ROOT, "build", f)).read() for f in JS))
    build_index()
    for P in PARTS:
        build_part(P)
    build_practice()
    print("built", len(PARTS) + 2, "pages")
