# -*- coding: utf-8 -*-
"""부마다 '프롬프트로 직접 만들어 보기' 실습. A 프롬프트는 make_requests.py(이 페이지 그림을 만드는 프롬프트)에서 가져온다.
res: 실제 결과 기록. 그림을 만들기 전에는 '아직 만들지 않음'을 그대로 적고, 그림이 들어오면 A·B를 나란히 보고 실제로 달라진 점을 적는다."""

PENDING = "실제 결과: 아직 그림을 만들지 않았습니다. A·B 그림이 들어오면 나란히 놓고 실제로 무엇이 달라졌는지(또는 달라지지 않았는지) 이 자리에 적습니다."

def T(key, title, goal, b_title, b_text, check, tip=None, b_key=None, res=PENDING):
    return dict(key=key, title=title, goal=goal, b_title=b_title, b_text=b_text, check=check, tip=tip, img=key, b_imgs=[b_key or key + "_b"], res=res)

TIP_SAME = "같은 대화에서 차이가 약하면 새 대화에서 처음부터 만들어 보세요. 작은 변화는 도구가 원래 모양을 지키려 해 약하게 나오는 일이 많습니다."

MAKE = {
1: [
 T("p1_moa_era_grid", "같은 모아를 네 연대로", "그림자 단계·눈·선·색감을 연대마다 다르게 적어, 같은 사람이 연대를 건너가는지 확인합니다.",
   "B — 원리 빼기: 색감만 바꾸기", "Same image, keep the same framing. Change only: make all four panels use the same present-day anime shading and eyes; only change the color grading from warm faded (left) to bright crisp (right). Still no text.",
   [("네 장 모두 머리띠와 왼쪽 리본이 그대로인가", "06_media_outfit.html#s4"), ("왼쪽 장은 그림자 1단계·하이라이트 1개인가", "#s1"), ("B 결과에서 색만 바뀌면 연대가 덜 느껴지는지 비교", "#s4")], tip=TIP_SAME),
 T("p1_moa_detail_pair", "정보량만 다른 두 장", "같은 모아를 가닥 선이 적은 그림과 많은 그림으로 만들어 정보량의 차이를 봅니다.",
   "B — 원리 빼기: 정보량을 같게", "Same image, keep the same framing. Change only: give both panels the same medium amount of hair strand lines and the same line thickness. Still no text.",
   [("왼쪽은 선이 굵고 가닥 선이 적은가", "#s3"), ("오른쪽은 가닥·주름 선이 많고 가는가", "#s3"), ("B 결과에서 두 장의 인상 차이가 줄었는지 비교", None)], tip=TIP_SAME),
],
2: [
 T("p2_sia_line_styles", "같은 시아를 네 가지 선으로", "선 굵기·명암 처리·단순화·여백을 패널마다 다르게 적어, 작품 이름 없이 화풍이 바뀌는지 확인합니다.",
   "B — 원리 빼기: 명암 방법을 같게", "Same image, keep the same framing. Change only: use the same flat two-tone cel shading in all four panels; keep each panel's line style. Still no text.",
   [("네 장 모두 검은 긴 머리·은 귀걸이의 시아인가", "#s3"), ("첫 장은 굵기가 일정하고, 둘째 장은 굵은 윤곽인가", "#s1"), ("B 결과에서 명암이 같아지면 전통의 차이가 얼마나 줄어드는지 비교", "03_mono.html#s2")], tip=TIP_SAME),
 T("p2_sia_paint", "칠 방식 세 가지", "같은 시아를 평면 색·원색 망점·번지는 수채로 칠해, 칠 방식만으로 지역 인상이 바뀌는지 봅니다.",
   "B — 원리 빼기: 선과 칠 규칙 섞기", "Same image, keep the same framing. Change only: in the watercolor panel use very thick bold comic outlines instead of thin light lines. Still no text.",
   [("세 장 모두 검은 긴 머리·은 귀걸이인가", "#s3"), ("수채 장은 선이 가늘고 채도가 낮은가", "#s2"), ("B 결과에서 수채 장이 탁해 보이는지 비교", "#s2")]),
],
3: [
 T("p3_moa_gesture", "흑백 러프 동작 시트", "움직임 선부터 잡은 흑백 러프 동작 다섯 개를 받고, 동작마다 몸이 휘었는지 확인합니다.",
   "B — 원리 빼기: 곧게 선 자세", "Same image, keep the same framing. Change only: make every pose stand straight and stiff with no curve through the body. Still no text.",
   [("동작마다 머리에서 발끝까지 휜 선이 보이는가", "#s1"), ("러프 선이지만 머리띠와 왼쪽 리본이 남았는가", "#s1"), ("B 결과에서 같은 동작인데 힘이 빠져 보이는지 비교", "#s1")]),
 T("p3_sia_brush", "수묵풍 시아, 글씨 없이", "끊긴 선과 여백으로 수묵 느낌을 내고, 글씨·도장이 들어가지 않는지 확인합니다.",
   "B — 원리 빼기: 선을 다 잇고 여백을 채우기", "Same image, keep the same framing. Change only: draw every outline as a continuous unbroken line and fill the background with a flat light gray wash, no empty white space. Still no text.",
   [("머리카락은 굵은 먹, 얼굴은 끊긴 가는 선인가", "#s3"), ("글씨·도장이 하나도 없는가", "07_failure_lab.html#f8"), ("B 결과에서 붓을 썼는데도 수묵 느낌이 줄었는지 비교", "#s3")]),
],
4: [
 T("p4_haru_heads", "키를 맞춘 다섯 등신", "같은 하루를 키를 맞춰 7.5등신부터 2.5등신까지 세우고, SD도 성인으로 보이는지 확인합니다.",
   "B — 원리 빼기: 통째로 축소", "Same image, keep the same framing. Change only: make the four smaller figures simple scaled-down copies of the 7.5-head-tall figure (same proportions, just smaller). Still no text.",
   [("다섯 장의 키(머리 꼭대기~발)가 같은가", "#s1"), ("SD로 갈수록 눈이 내려가고 손이 둥글어지는가", "#s2"), ("B 결과가 'SD'가 아니라 '작은 사람'으로 보이는지 비교", "#s1")], tip=TIP_SAME),
 T("p4_haru_mascot", "마스코트 피규어와 그림 카드", "입체 마스코트에서 상징 세 개만 남겨도 하루로 보이는지 확인합니다.",
   "B — 원리 빼기: 세부를 모두 남기기", "Same image, keep the same framing. Change only: give the mascot figure every small detail (coat buttons, pocket seams, hoodie drawstring tips, small hair strands). Still no text.",
   [("분홍 머리·번 2개·라벤더 후드가 굵게 보이는가", "#s3"), ("피규어에 테두리 선 대신 둥근 명암이 있는가", "#s3"), ("B 결과를 휴대전화 화면에서 아주 작게 줄여 보고 무엇이 뭉개지는지 비교", "#s3")]),
],
5: [
 T("p5_sia_collapse", "무너짐 다섯 단계", "같은 시아를 예쁜 놀람에서 개그 작화까지 단계별로 무너뜨리고, 고정값이 끝까지 남는지 확인합니다.",
   "B — 원리 빼기: 고정값까지 무너뜨리기", "Same image, keep the same framing. Change only: in the two rightmost panels also change her hair to short and messy and remove the earrings. Still no text.",
   [("다섯 장 모두 검은 긴 머리와 은 귀걸이인가", "#s1"), ("눈 → 입 → 그림자 선 순서로 무너지는가", "#s1"), ("B 결과에서 오른쪽 두 장이 누구인지 헷갈리는지 비교", "#s1")], tip=TIP_SAME),
 T("p5_sia_one_place", "한 곳만 과장한 세 장", "눈만·입만·땀만 과장한 세 장을 만들어, 한 곳 과장이 감정을 또렷하게 하는지 봅니다.",
   "B — 원리 빼기: 세 곳 다 과장", "Same image, keep the same framing. Change only: in all three panels exaggerate the eyes, the mouth and the sweat drop at the same time. Still no text.",
   [("각 장에서 커진 곳이 하나뿐인가", "#s2"), ("나머지 부위는 평소 크기인가", "#s2"), ("B 결과에서 세 장의 감정 차이가 사라지는지 비교", "07_failure_lab.html#f6")]),
],
6: [
 T("p6_haru_media", "같은 하루, 네 가지 재료", "셀·3D·먹·픽셀로 재료만 바꾸고 실루엣·색·장식이 남는지 확인합니다.",
   "B — 원리 빼기: 재료마다 새 디자인", "Same image, keep the same framing. Change only: in the 3D and pixel panels redesign her hair (one bun instead of two, lighter purple color). Still no text.",
   [("네 장 모두 번 2개·분홍 머리·남색 줄인가", "#s1"), ("픽셀 장에서 가는 선이 사라지고 큰 덩어리만 남는가", "#s1"), ("B 결과에서 3D·픽셀 하루가 다른 사람처럼 보이는지 비교", "#s4")]),
 T("p6_moa_outfits", "모아의 포스터 세 장", "옷 테마만 바꾼 포스터 세 장에서 머리띠·왼쪽 리본이 남는지, 글자 자리가 비어 있는지 확인합니다.",
   "B — 원리 빼기: 테마에 맞춰 머리까지 바꾸기", "Same image, keep the same framing. Change only: in each poster also change her hairstyle and remove the headband to match the theme (spiky hair for punk, a bun for preppy). Still no text.",
   [("세 장 모두 흰 프릴 머리띠와 왼쪽 귀 위 리본인가", "#s3"), ("옷이 교복처럼 보이지 않고 20대 성인 코디인가", "#s3"), ("B 결과가 '모아의 베리에이션'이 아니라 다른 사람으로 보이는지 비교", "#s3")], tip=TIP_SAME),
],
7: [
 T("f1_identity", "f1 실패를 고치기", "f1(장식이 사라진 수묵풍 모아)을 고정값 조각으로 고쳐 봅니다.",
   "B — 고치기: 고정값 조각 넣기", "Same image, keep the same framing and the ink brush style. Change only: add her white frilled maid headband with the white ribbon over her LEFT ear, and make her hair ash-beige and wavy. Still no text, no calligraphy, no seals.",
   [("고친 그림에 머리띠와 왼쪽 리본이 있는가", "#s1"), ("수묵풍(끊긴 선·여백)은 그대로인가", "03_mono.html#s3"), ("고치는 조각이 '처음 걸린 항목' 하나만 다뤘는가", "#s1")], b_key="f1_fixed"),
 T("f8_fake_text", "f8 실패를 고치기", "f8(가짜 글씨·도장이 들어간 수묵풍 시아)에서 글씨를 없애고 특징으로만 화풍을 적어 봅니다.",
   "B — 고치기: 글씨·도장 없애기", "Same image, keep the same framing and the ink brush style. Change only: remove all calligraphy columns and the red seal stamp, leave that area as empty white paper. No text, no seals.",
   [("글씨·도장이 모두 사라졌는가", "#f8"), ("여백이 그대로 남아 수묵 느낌이 유지되는가", "03_mono.html#s3"), ("요청문에 작품·작가 이름이 하나도 없는가", "#drift")], b_key="f8_fixed"),
],
}
