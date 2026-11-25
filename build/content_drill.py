# -*- coding: utf-8 -*-
"""부마다 '프롬프트 연습 과제' 1개씩(모두 7개). 과제의 프롬프트는 예상 결과 그림을 실제로 만드는 프롬프트와 같다(이 파일이 원본).
python3 build/content_drill.py → docs/image_requests_drill/ 요청 꾸러미 생성.
RETRY·RETRY3: 1차 결과가 실패했을 때 붙이는 '다시 시도' 자리(그림을 받은 뒤 채운다)."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
from make_requests import who, KEEP, END, CH, ANIME

def P(ratio, scene, style):
    return ("Illustration, " + ("vertical 2:3." if ratio == "2:3" else "wide 16:9.") + f"\nArt style: {style}\n{KEEP}\n{scene}\nPlain white background.\n" + END)

DRILL = {
1: [dict(id="d1", title="'80년대풍'을 특징 네 줄로 적기", goal="연대 이름 대신 그림자 단계·눈·선·색감 네 줄로 80년대 셀화 느낌을 적어, 모아를 한 장 만들고 네 손잡이가 모두 반영됐는지 검사합니다.",
      why="'80s anime style' 한 마디로 요청하면 색만 바래고 칠하는 방식은 지금 그대로인 그림이 자주 나옵니다(1부 4단계). 특징을 한 줄씩 적으면 어느 손잡이가 빠졌는지 바로 보입니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png",
      steps=["새 대화를 열고 참고 그림 두 장을 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "그림자 경계가 또렷한 1단계인지, 눈 하이라이트가 하나인지, 윤곽선이 굵은지, 색이 따뜻하게 바랬는지 네 가지를 하나씩 확인합니다.",
             "빠진 손잡이가 있으면 그 한 줄만 같은 대화에 'Same image. Change only: …'로 다시 넣습니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Chest-up portrait of " + who("moa") + ", gentle smile, looking at the viewer.",
               "retro cel animation look described by features only: one hard-edged shadow tone, one small round eye highlight, heavy upper lashes, thick even outlines, warm slightly faded colors"), "d1_moa_retro", "예상 결과 — 특징 네 줄로 만든 80년대 셀화풍 모아. 그림자 1단계, 하이라이트 1개, 굵은 윤곽, 따뜻하게 바랜 색", "2/3")],
      check=[("그림자가 한 단계이고 경계가 또렷한가", "#s1"), ("눈 하이라이트가 하나이고 속눈썹이 무거운가", "#s2"), ("머리띠와 왼쪽 리본, 20대 성인 얼굴이 그대로인가", "#s2")],
      expect="지금 애니풍보다 선이 굵고 그림자 경계가 또렷한 모아가 나옵니다. 눈 크기는 기준 그림과 비슷하고, 하이라이트만 하나로 줄어 '옛날 그림' 인상이 납니다.",
      trouble=[("색만 바래고 그림자는 부드럽다", "'Same image. Change only: one hard-edged shadow tone, no soft gradients.'"), ("눈이 커지고 어려 보인다", "'same eye size as the reference, adult woman in her twenties'를 덧붙입니다."), ("머리띠가 사라졌다", "고정값부터 다시 적습니다(7부 f1).")],
      more="같은 네 줄의 값을 바꿔 '90년대풍'(그림자 2단계, 날카로운 턱, 머리 광택)으로도 만들어 비교해 보세요.")],
2: [dict(id="d2", title="작품 이름 없이 '맑은 선' 화풍 요청하기", goal="굵기가 일정한 선과 평평한 색만으로 시아를 그려 달라고 적고, 받은 그림에서 굵기 비가 1에 가까운지 확인합니다.",
      why="화풍을 작품 이름으로 요청하면 그 작품 캐릭터의 옷과 얼굴이 섞여 나옵니다(7부 f8). 선 규칙만 적으면 시아는 그대로이고 화풍만 바뀝니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "윤곽선의 가장 굵은 곳과 가장 가는 곳을 눈으로 비교해 굵기 비가 1~1.5인지 봅니다.", "명암이 단색(또는 없음)인지, 배경이 깔끔한지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Upper-body portrait of " + who("sia") + ", walking with a calm expression.",
               "clean line style described by features only: uniform line weight everywhere (no thick-thin variation), flat colors, no shading or one flat shadow tone, simple clean background shapes"), "d2_sia_clear", "예상 결과 — 굵기가 일정한 선과 평평한 색으로 그린 시아. 검은 긴 머리·은 귀걸이는 그대로", "2/3")],
      check=[("윤곽선 굵기가 처음부터 끝까지 비슷한가(굵기 비 1~1.5)", "#s1"), ("칠이 평평한가(번짐 없음)", "#s2"), ("시아의 고정값(검은 긴 머리·장식 없음·은 귀걸이)이 그대로인가", "#s3")],
      expect="굵기가 고른 맑은 선의 시아가 나옵니다. 지금 애니풍보다 평평하고 깔끔해 보이며, 옷의 주름 선도 같은 굵기입니다.",
      trouble=[("윤곽만 굵고 안쪽 선은 가늘다", "'Same image. Change only: inner lines the same thickness as the outline.'"), ("그림자가 부드러운 그라데이션이다", "'flat colors only, no gradients'를 덧붙입니다."), ("다른 작품 캐릭터 옷이 섞였다", "작품 이름을 빼고 특징만 남겼는지 확인합니다.")],
      more="같은 프롬프트의 선 규칙만 'bold outlines with strong thick-thin variation'으로 바꿔 굵기 비가 큰 그림과 비교해 보세요.")],
3: [dict(id="d5", title="흑백 굿즈용 하루 — 머리와 옷을 구별하기", goal="하루를 흑백 만화풍으로 만들되, 회색값이 비슷한 분홍 머리와 라벤더 옷을 망점 밝기로 구별하게 적습니다.",
      why="분홍 머리(회색값 약 170)와 라벤더 옷(약 182)은 흑백에서 거의 같은 회색이 됩니다(3부 4단계). 부위마다 다른 밝기를 적지 않으면 둘이 붙어 버립니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "받은 그림에서 머리와 옷의 경계가 또렷한지 봅니다.", "흐리면 같은 대화에 'Change only: make the hoodie a darker screentone' 한 줄만 넣습니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Chest-up portrait of " + who("haru") + ", cheerful smile.",
               "black and white manga style for a printed postcard: clean black ink outlines; hair in light dotted screentone, hoodie in clearly darker dotted screentone, lab coat left white, so that hair and hoodie are easy to tell apart; no gray gradients"), "d5_haru_mono", "예상 결과 — 흑백 만화풍 하루. 머리는 옅은 망점, 후드는 진한 망점, 랩코트는 흰색으로 구별됨", "2/3")],
      check=[("머리와 후드의 회색 밝기가 분명히 다른가", "#s4"), ("번 2개와 앞머리 가운데 줄(진한 선)이 보이는가", "06_media_outfit.html#s1"), ("회색 그라데이션 없이 망점만 썼는가", "03_mono.html#s2")],
      expect="세 부위(머리·후드·랩코트)가 옅은 망점·진한 망점·흰색으로 나뉘어, 색이 없어도 하루의 옷차림이 또렷하게 읽힙니다.",
      trouble=[("머리와 후드가 같은 회색이다", "'Change only: hoodie in much darker screentone'."), ("앞머리 가운데 줄이 사라졌다", "'a dark stripe down the center of the bangs'를 덧붙입니다."), ("회색 그라데이션이 섞였다", "'screentone dots only, no gradients'.")],
      more="같은 그림을 컬러로 다시 받아 두 장을 나란히 놓고, 흑백판의 밝기가 컬러판의 어느 색에 해당하는지 짝지어 보세요.")],
4: [dict(id="d3", title="성인 SD 하루를 한 장에", goal="2.5등신 SD 하루를 만들되, 성인임을 적고 눈 위치·손을 SD 규칙으로 함께 바꿨는지 확인합니다.",
      why="SD만 적으면 얼굴이 아이처럼 어려지거나(7부 f4), 8등신 얼굴이 큰 머리에 얹혀 이마가 넓어집니다(7부 f5). 나이와 부위 규칙을 함께 적어 두 실패를 한 번에 막습니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "머리 높이로 키를 재어 2~3등신인지 봅니다(키 ÷ 머리 높이).", "눈이 머리의 아래쪽에 있는지, 손이 둥근 덩어리인지, 성인으로 보이는지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Full-body standing figure of " + who("haru") + ", waving happily.",
               "comedy SD style: an adult woman in her twenties drawn 2.5 heads tall, not a child; eyes placed low in the large head, small simple rounded mitten-like hands, small feet, clean anime lineart"), "d3_haru_sd", "예상 결과 — 2.5등신 SD로 그린 20대 하루. 눈이 머리 아래쪽, 둥근 손, 성인 옷차림", "2/3")],
      check=[("키 ÷ 머리 높이가 2~3인가", "#s1"), ("눈이 머리의 아래쪽에 있고 손이 단순한가", "#s2"), ("아이가 아니라 성인 연구원으로 보이는가", "07_failure_lab.html#f4")],
      expect="머리가 크고 몸이 짧은 하루가 나오지만, 랩코트와 후드 차림과 얼굴 인상 덕분에 아이가 아니라 SD로 그린 성인으로 보입니다.",
      trouble=[("아이처럼 어려 보인다", "'not a child, adult proportions in the face shape'를 덧붙이고, 볼을 덜 둥글게 요청합니다."), ("손가락이 다섯 개 다 그려져 답답하다", "부분 수정으로 손만 칠해 'simple mitten-like hands'."), ("4~5등신으로 나온다", "'very large head, the head is 40 percent of the total height'처럼 크게 과장해 적습니다.")],
      more="같은 프롬프트에서 등신만 '6 heads tall'로 바꿔 두 장을 나란히 놓고, 눈 위치와 손이 어떻게 다른지 보세요.")],
5: [dict(id="d4", title="눈 하나만 과장한 반응 스티커", goal="시아의 놀람 스티커를 '눈만 과장'으로 만들고, 다른 부위와 고정값이 평소 그대로인지 확인합니다.",
      why="'과장된 놀람'만 적으면 눈·입·땀·기호가 한꺼번에 커지는 일이 많습니다(7부 f6). 주인공 부위 하나를 적고, 나머지는 평소대로라고 함께 적습니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "눈 말고 커진 곳이 있는지 셉니다.", "검은 긴 머리·은 귀걸이가 그대로인지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Face and shoulders of " + who("sia") + ", reacting with surprise, as a sticker illustration with a thin white outline around her.",
               ANIME + "; only the eyes are comically exaggerated (about 1.5 times larger, round), the mouth, eyebrows and everything else stay at normal size; one small sweat drop symbol only, no other symbols"), "d4_sia_sticker", "예상 결과 — 눈만 크게 과장한 시아 놀람 스티커. 입과 나머지는 평소 크기, 작은 땀 한 방울", "2/3")],
      check=[("커진 곳이 눈 하나뿐인가", "#s2"), ("기호가 땀방울 하나뿐인가", "#s4"), ("머리와 귀걸이가 그대로인가", "#s1")],
      expect="동그랗게 커진 눈 때문에 '놀람'이 한눈에 읽히고, 입과 눈썹은 평소 크기라 시아의 얼굴 인상이 그대로 남습니다.",
      trouble=[("입도 크게 벌렸다", "'Same image. Change only: mouth small and closed, normal size.'"), ("땀·하트·눈물이 잔뜩 붙었다", "'one small sweat drop only, no hearts, no tears'."), ("글자나 '!' 표시가 들어갔다", "'no text, no exclamation marks'를 덧붙입니다.")],
      more="같은 장면을 '입만 과장'으로 바꿔 만들고, 두 스티커의 감정이 어떻게 다르게 읽히는지 비교해 보세요.")],
6: [dict(id="d6c", title="같은 옷, 다른 카메라 — 광고 포스터 한 장", goal="하루의 실험실 차림은 그대로 두고 카메라 높이와 렌즈만 적어, 당당한 광고 포스터 구도가 나오는지 확인합니다.",
      why="카메라를 적지 않으면 같은 시리즈 그림도 각도가 매번 달라집니다(6부 2단계). 옷은 고정하고 카메라 두 손잡이만 문장으로 적습니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png",
      steps=["새 대화를 열고 참고 그림을 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "카메라가 아래에서 올려다보는지, 내민 손이 크게 다가오는지 봅니다.", "옷·머리·번 2개가 그대로인지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Full-body poster illustration of " + who("haru") + ", running toward the viewer and reaching one hand forward, energetic smile.",
               ANIME + "; low camera angle looking up, wide-angle lens so the reaching hand looks large and close, sky in the background, empty blank area at the top for a title"), "d6_haru_camera", "예상 결과 — 아래에서 넓은 렌즈로 잡은 하루. 내민 손이 크게 보이고, 옷과 고정값은 그대로", "2/3")],
      check=[("아래에서 올려다본 구도인가", "#s2"), ("내민 손이 몸보다 크게 다가와 보이는가", "#s2"), ("라벤더 후드·흰 랩코트·번 2개가 그대로인가", "#s4")],
      expect="하늘을 배경으로 하루가 화면 밖으로 뛰어나오는 듯한 포스터가 나옵니다. 손이 크게 보이고, 위쪽에 제목 자리가 비어 있습니다.",
      trouble=[("눈높이 정면 구도로 나온다", "'Same image. Change only: camera placed near the ground looking up.'"), ("손이 이상하게 길어졌다", "'wide-angle but natural hand size, slightly closer to the camera'로 낮춥니다."), ("제목 글자가 들어갔다", "'no text, leave the area blank'를 덧붙입니다.")],
      more="같은 프롬프트의 카메라만 'high camera angle looking down'으로 바꿔, 귀여운 인상과 비교해 보세요.")],
7: [dict(id="d6", title="실패 그림 하나를 조각 하나로 고치기", goal="7부 실패 그림 중 하나를 골라 진단 순서로 처음 걸린 항목을 찾고, 그 항목의 조각 하나만 넣어 고칩니다. 여기서는 f6(과장 여러 곳)을 예로 듭니다.",
      why="실패 그림을 '더 잘 그려 줘'로 다시 요청하면 같은 실패가 반복됩니다. 처음 걸린 항목의 조각 하나만 넣어야 무엇이 효과가 있었는지 알 수 있습니다.",
      attach="f6_overexag.png (실패 그림) + refs/sia_anime_base.png",
      steps=["실패 그림을 다섯 항목 순서로 진단합니다(① 고정값 → ② 축 → ③ 등신·나이 → ④ 과장 → ⑤ 매체·글자·출처).", "처음 걸린 항목을 적습니다(f6은 ④).", "아래 프롬프트처럼 그 항목의 조각 하나만 넣어 다시 만듭니다.", "고친 그림을 다시 다섯 항목으로 진단해 모두 통과하는지 봅니다."],
      prompts=[("넣을 프롬프트", "Same character and pose as the attached image. Change only: exaggerate the eyes only; mouth, sweat and everything else at normal size; remove all extra symbols except one small sweat drop. Keep her long black hair and small silver earrings. No text.",
                "d6_sia_fixed", "예상 결과 — f6을 고친 시아. 눈만 크게, 나머지는 평소 크기, 땀 한 방울", "2/3")],
      check=[("처음 걸린 항목을 ④로 골랐는가", "#s1"), ("고친 그림에서 커진 곳이 하나인가", "05_expression.html#s2"), ("다섯 항목을 다시 보면 모두 통과하는가", "#s1")],
      expect="눈만 커진 놀람 얼굴로 돌아오고, 기호가 줄어 감정이 한 가지로 읽힙니다. 다른 항목(고정값·나이)은 처음부터 통과였으니 그대로입니다.",
      trouble=[("기호가 그대로 남았다", "부분 수정으로 기호 부분만 칠해 지웁니다."), ("얼굴이 통째로 바뀌었다", "실패 그림을 첨부했는지, 'Same character and pose'를 넣었는지 확인합니다."), ("고친 뒤 다른 항목에서 걸린다", "그 항목의 조각을 하나만 더합니다.")],
      more="f1·f4·f8도 같은 방법으로 고쳐 보고, 어느 항목의 조각이 가장 효과가 컸는지 적어 두세요.")]
}
# ---------------- 2차 연습 과제(2026-11-25): 부마다 2개씩 더해 부당 3개. 1차 그림에서 배운 점을 반영 ----------------
NEWCONV = "새 대화를 열고 참고 그림을 첨부합니다."
DRILL2 = {
1: [dict(id="d1b", title="두 연대를 서로 다른 새 대화에서 — 90년대와 지금", goal="같은 모아를 90년대풍과 지금 애니풍으로 각각 새 대화에서 만들어 나란히 놓고, 그림자 단계·눈·턱선 차이가 분명한지 봅니다.",
      why="1차 그림에서 같은 대화에 'Change only'로 연대를 바꾸면 차이가 거의 나지 않았습니다(1부 직접 만들기 B). 비교할 두 장은 서로 다른 새 대화에서 처음부터 만들어야 차이가 살아납니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png",
      steps=["새 대화 ①을 열고 참고 그림을 첨부해 프롬프트 ①을 넣습니다.", "새 대화 ②를 따로 열고 같은 참고 그림을 첨부해 프롬프트 ②를 넣습니다.", "두 장을 나란히 놓고 그림자 단계, 눈 하이라이트 수, 턱선을 비교합니다."],
      prompts=[("① 새 대화에서 — 90년대풍", P("2:3", "Chest-up portrait of " + who("moa") + ", gentle smile.", "1990s-like cel animation look described by features: two hard-edged shadow tones, sharper narrow chin, glossy band-shaped hair highlights, slightly smaller nose and mouth, saturated colors"), "d1b_moa_90s", "예상 결과 ① — 90년대풍 모아. 또렷한 그림자 두 단계, 날렵한 턱, 머리의 띠 모양 광택", "2/3"),
               ("② 다른 새 대화에서 — 지금의 애니풍", P("2:3", "Chest-up portrait of " + who("moa") + ", gentle smile.", "present-day anime look described by features: soft gradient shading, large eyes with three sparkling highlights, thin light lashes, bright airy colors"), "d1b_moa_now", "예상 결과 ② — 지금의 애니풍 모아. 부드러운 명암, 여러 하이라이트, 밝은 색", "2/3")],
      check=[("①은 그림자 경계가 또렷하고 ②는 부드러운가", "#s1"), ("①은 하이라이트가 적고 ②는 많은가", "#s2"), ("두 장 모두 머리띠와 왼쪽 리본, 같은 20대 얼굴인가", "06_media_outfit.html#s4")],
      expect="같은 모아인데 ①은 힘 있고 선명한 90년대 셀화, ②는 밝고 부드러운 지금의 그림으로 나뉩니다. 같은 대화에서 만들 때보다 차이가 훨씬 큽니다.",
      trouble=[("두 장이 비슷하다", "② 대화에 ①의 그림을 첨부하지 않았는지 확인합니다. 비교용 그림은 서로 첨부하지 않습니다."), ("①의 얼굴이 다른 사람이 됐다", "'keep her face shape from the reference'를 덧붙입니다."), ("①의 피부가 너무 누렇다", "'natural skin tone, only the shading style is retro'.")],
      more="같은 방법으로 2000년대 초 디지털풍(얇은 선, 에어브러시 명암)까지 세 번째 새 대화에서 만들어 세 장을 비교해 보세요."),
     dict(id="d1c", title="색보정만 바꾸고 머리색은 지키기", goal="오래된 인쇄물 느낌의 색보정을 요청하되, 머리·눈 색(고정값)은 그대로인지 확인합니다.",
      why="1부 4단계 실험처럼 색을 크게 돌리면 머리색이 바뀌어 다른 사람처럼 보입니다. 1차 그림 f1에서도 화풍을 바꾸자 머리색이 회색빛 금발로 바뀌었습니다. 고정값을 먼저 적고 색감은 '전체 보정'으로만 요청합니다.",
      attach="refs/moa_anime_base.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "참고 그림과 나란히 놓고 머리가 회갈색, 눈이 호박색인지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Chest-up portrait of " + who("moa") + ", looking slightly to the side.", ANIME + "; keep her ash-beige hair and amber eyes exactly as in the reference; apply only an overall warm faded old-print color grading (yellowish tint, lower saturation) over the whole picture"), "d1c_moa_faded", "예상 결과 — 바랜 인쇄물 느낌의 모아. 전체가 누렇게 바랬지만 머리는 회갈색 그대로", "2/3")],
      check=[("그림 전체가 따뜻하게 바랬는가", "#s4"), ("머리가 회갈색, 눈이 호박색 그대로인가", "#s4"), ("머리띠와 왼쪽 리본이 그대로인가", "06_media_outfit.html#s4")],
      expect="오래된 화집에서 꺼낸 듯한 모아가 나옵니다. 색이 전체적으로 누렇지만 머리와 눈의 색 차이는 그대로라 같은 사람으로 보입니다.",
      trouble=[("머리가 금발이나 갈색으로 바뀌었다", "'hair color must match the reference exactly'를 맨 앞에 둡니다."), ("색만 바래고 흐릿하다", "'keep crisp lines, only colors fade'."), ("배경에 종이 질감 글자가 생겼다", "'no text, plain paper texture only'.")],
      more="같은 그림을 '차갑고 진한 지금 화면 느낌'으로도 만들어, 두 장의 머리색이 같은지 비교해 보세요.")],
2: [dict(id="d2b", title="배경 효과선 하나로 장르 바꾸기", goal="같은 시아를 집중선 배경과 꽃·반짝임 배경으로 각각 만들어, 배경만으로 장면이 어떻게 달라지는지 봅니다.",
      why="효과선을 섞으면 장면이 흐려집니다(2부 4단계). 두 장을 새 대화 두 개에서 따로 만들고, 각 문장에 효과 하나만 적습니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png",
      steps=["새 대화 ①에서 프롬프트 ①로 만듭니다.", "새 대화 ②에서 프롬프트 ②로 만듭니다.", "두 장의 표정·구도는 비슷하고 배경만 다른지 봅니다."],
      prompts=[("① 긴장 — 집중선", P("2:3", "Upper-body portrait of " + who("sia") + ", determined expression, looking at the viewer.", ANIME + "; background: black radial focus lines converging on her only, nothing else"), "d2b_sia_focus", "예상 결과 ① — 검은 집중선 배경의 시아. 액션 장면처럼 긴장감", "2/3"),
               ("② 설렘 — 꽃과 반짝임", P("2:3", "Upper-body portrait of " + who("sia") + ", gentle smile, looking at the viewer.", ANIME + "; background: soft flowers and small sparkles around her only, nothing else"), "d2b_sia_sparkle", "예상 결과 ② — 꽃과 반짝임 배경의 시아. 순정 만화 장면처럼 설렘", "2/3")],
      check=[("①에는 집중선만, ②에는 꽃·반짝임만 있는가", "#s4"), ("두 장 모두 검은 긴 머리·은 귀걸이인가", "#s3"), ("그림 안에 글자나 효과음 글씨가 없는가", "07_failure_lab.html#f8")],
      expect="같은 시아가 ①에서는 결의에 찬 액션 장면, ②에서는 부드러운 설렘 장면으로 읽힙니다.",
      trouble=[("①에 꽃잎이 섞였다", "'no flowers, no hearts, no sparkles'."), ("효과선이 얼굴을 가린다", "'focus lines only in the background, face clear'."), ("효과음 글씨가 들어갔다", "'no text, no sound-effect lettering'.")],
      more="같은 두 배경을 하루에게도 적용해 보고, 캐릭터가 바뀌어도 장르 인상이 같은지 보세요."),
     dict(id="d2c", title="카툰으로 줄여도 시아로 보이게", goal="시아를 기본 도형으로 아주 단순하게 줄이되, 고정값(검은 긴 생머리·장식 없음·은 귀걸이)이 남아 같은 사람으로 보이는지 확인합니다.",
      why="단순화를 크게 하면 고정값부터 사라지기 쉽습니다. 1차 그림에서도 고정값을 적지 않은 비교 그림은 머리 모양이 바로 바뀌었습니다(5부·6부 직접 만들기 B). 남길 것을 먼저 적습니다.",
      attach="refs/sia_anime_base.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "기준 그림과 나란히 놓고 고정값 세 가지가 남았는지 셉니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Full-body figure of " + who("sia") + ", standing and waving.", "very simple cartoon style made of basic shapes: round head, dot eyes, simple lines, flat colors; keep exactly: long straight black hair, no headdress, small silver earrings, the black dress with white apron"), "d2c_sia_cartoon", "예상 결과 — 기본 도형으로 줄인 카툰 시아. 점 눈이지만 검은 긴 머리와 은 귀걸이로 시아임을 알 수 있음", "2/3")],
      check=[("얼굴과 몸이 기본 도형으로 단순해졌는가", "#s3"), ("검은 긴 생머리·은 귀걸이·흰 앞치마가 남았는가", "#s3"), ("아이처럼 보이지 않는가", "07_failure_lab.html#drift")],
      expect="점 눈과 단순한 선의 카툰이지만, 검은 긴 머리와 흰 앞치마 실루엣만으로 시아로 읽힙니다.",
      trouble=[("머리가 짧아졌다", "'long straight black hair reaching her waist' 처럼 길이를 숫자 없이 크게 적습니다."), ("귀걸이가 사라졌다", "작은 장식은 단순화에서 먼저 사라집니다. 'clearly visible silver earrings'."), ("아이처럼 보인다", "'adult woman, cartoon style, not a child'를 덧붙입니다.")],
      more="같은 문장의 단순화 정도를 '반실사'로 바꾼 그림과 나란히 놓아 보세요.")],
3: [dict(id="d3b", title="러프에서 정리 선으로 — 움직임 선은 그대로", goal="흑백 러프처럼 크게 휜 찌르기 동작을 깔끔한 펜 선화로 받아, 정리해도 움직임 선이 살아 있는지 봅니다.",
      why="선을 깔끔하게 정리하면 동작까지 뻣뻣해지기 쉽습니다. 1차 그림에서 곧게 선 자세(3부 직접 만들기 B)는 막대를 들어도 동작이 읽히지 않았습니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "머리에서 발끝까지 휜 선을 손가락으로 따라가 봅니다. 곧으면 'strongly curved line of action'을 다시 넣습니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Full-body action pose of " + CH["moa"] + " in a simple long-sleeved blouse and long skirt, lunging forward with a plain wooden stick.", "clean black ink line art, no shading, white background; a strongly curved line of action runs from her head through her back leg; dynamic but clear"), "d3b_moa_lineart", "예상 결과 — 깔끔한 펜 선의 모아 찌르기 동작. 몸 전체가 활처럼 휘어 있음", "2/3")],
      check=[("머리~발끝을 잇는 휜 선이 보이는가", "#s1"), ("선이 깔끔한 한 줄(정리 선)인가", "#s1"), ("머리띠와 왼쪽 리본이 선으로 남았는가", "06_media_outfit.html#s4")],
      expect="러프의 기세는 그대로이고 선만 깨끗해진 동작 그림이 나옵니다. 막대 끝과 뒷발이 대각선으로 이어집니다.",
      trouble=[("곧게 선 자세다", "'deep lunge, body leaning far forward, back leg fully stretched'."), ("회색 명암이 들어갔다", "'line art only, no gray, no shading'."), ("막대가 무기처럼 보인다", "'plain wooden practice stick, not a weapon'.")],
      more="같은 동작을 연필 러프(겹친 선)로도 받아 두 장의 기세를 비교해 보세요."),
     dict(id="d3c", title="해칭만으로 그림자 넣기", goal="회색과 망점 없이 가는 펜 선을 겹친 해칭만으로 시아의 그림자를 넣고, 방법이 하나로 지켜졌는지 확인합니다.",
      why="흑백 요청은 망점·회색·해칭이 한 얼굴에 섞이기 쉽습니다(3부 2단계). 쓸 방법 하나와 쓰지 않을 방법을 함께 적습니다.",
      attach="refs/sia_anime_base.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "그림자를 확대해 점이나 회색 칠이 섞였는지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Chest-up portrait of " + who("sia") + ", calm expression.", "black and white pen-and-ink drawing; shadows made only with fine cross-hatching lines; no gray tones, no screentone dots, no solid black areas except her hair"), "d3c_sia_hatch", "예상 결과 — 해칭만으로 그림자를 넣은 흑백 시아. 머리만 검게, 나머지 그림자는 가는 선의 겹침", "2/3")],
      check=[("그림자가 모두 선의 겹침인가", "#s2"), ("회색 칠·망점이 없는가", "#s2"), ("은 귀걸이와 리본이 선으로 보이는가", "02_line.html#s3")],
      expect="진지한 그래픽 노블 느낌의 시아가 나옵니다. 얼굴 그림자는 옅은 해칭, 옷 그림자는 촘촘한 해칭입니다.",
      trouble=[("망점이 섞였다", "'no screentone, hatching only'를 다시 넣습니다."), ("얼굴이 너무 어둡다", "'very light hatching on the face'."), ("선이 지저분하다", "'evenly spaced parallel lines'.")],
      more="같은 그림을 '망점만'으로 받아 두 장의 분위기를 비교해 보세요.")],
4: [dict(id="d4b", title="성인 SD 스티커 네 장 한 번에", goal="하루를 2등신 SD 스티커 네 장(손 흔들기·생각·놀람·졸음)으로 받고, 네 장 모두 같은 성인 캐릭터로 보이는지 봅니다.",
      why="1차 연습에서 SD 하루는 성인 문장을 넣어도 어려 보였습니다(4부 연습 결과). 이번에는 성인 신호(가로로 조금 긴 눈, 작은 코 선, 랩코트)를 함께 적습니다.",
      attach="refs/haru_anime_base.png, refs/haru_sheet.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "네 스티커의 머리 모양·번·후드가 모두 같은지, 어려 보이지 않는지 봅니다."],
      prompts=[("넣을 프롬프트", "Illustration, wide 16:9.\nArt style: cute 2-head-tall SD sticker style with thick white outlines.\n" + KEEP + "\nA sheet of four separate stickers of the adult woman " + CH["haru"] + ", wearing a lavender hoodie and white lab coat: (1) waving, (2) thinking with a hand on her chin, (3) surprised, (4) sleepy. Adult cues: slightly longer eye shape, a small visible nose line, adult lab coat; an adult drawn in SD style, not a child.\nPlain white background.\n" + END, "d4b_haru_stickers", "예상 결과 — 2등신 하루 스티커 네 장. 표정은 다르지만 번 2개·남색 줄·라벤더 후드는 모두 같음", "16/9")],
      check=[("네 장의 고정값(번 2개·남색 줄·후드)이 같은가", "#s3"), ("눈이 머리 아래쪽, 손이 둥근가", "#s2"), ("아이가 아니라 SD로 그린 성인으로 보이는가", "07_failure_lab.html#drift")],
      expect="스티커로 쓰기 좋은 작은 하루 네 명이 나옵니다. 표정은 넷이지만 같은 사람이고, 랩코트와 코 선 덕분에 어린아이로 보이지 않습니다.",
      trouble=[("어려 보인다", "'no round baby cheeks, adult face cues'를 덧붙입니다."), ("네 장의 머리가 다르다", "참고 그림을 다시 첨부하고 'all four identical hairstyle'."), ("말풍선 글씨가 생겼다", "'no text, no speech bubbles'.")],
      more="같은 네 표정을 시아·모아로도 만들어 세 사람 스티커 세트를 꾸려 보세요."),
     dict(id="d4c", title="SD 하루의 공차기 — 과장과 잔상", goal="짧은 다리의 SD 하루가 공을 차는 동작을 과장과 잔상으로 또렷하게 보이게 합니다.",
      why="SD는 팔다리가 짧아 그대로 움직이면 동작이 작게 보입니다(4부 4단계). 다리를 크게 늘이고 잔상을 넣으라고 적습니다.",
      attach="refs/haru_anime_base.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "차는 다리가 몸 밖으로 크게 나왔는지, 잔상이 3장 안팎인지 봅니다."],
      prompts=[("넣을 프롬프트", "Illustration, wide 16:9.\nArt style: " + ANIME + "\n" + KEEP + "\nA 2.5-head-tall comedy SD figure of the adult woman " + CH["haru"] + ", lavender hoodie and white lab coat, kicking a soccer ball with a big happy smile. The kicking leg is exaggerated and stretched far out, three faint afterimages show the path of the leg, speed lines trail behind the ball. An adult drawn in SD style, not a child.\nPlain white background.\n" + END, "d4c_haru_kick", "예상 결과 — 공을 차는 2.5등신 하루. 다리가 크게 늘어나고 잔상 세 개와 속도선이 동작을 보여 줌", "16/9")],
      check=[("다리가 몸 밖으로 크게 뻗었는가", "#s4"), ("잔상이 서너 개, 간격이 고른가", "#s4"), ("성인 SD로 보이는가", "07_failure_lab.html#drift")],
      expect="짧은 SD 몸이지만 늘어난 다리와 잔상 덕분에 공을 힘차게 찼다는 것이 한눈에 읽힙니다.",
      trouble=[("다리가 몸 가까이에 있다", "'leg stretched to almost the length of her whole body'."), ("잔상이 너무 많아 어지럽다", "'only three afterimages'."), ("공이 사람에게 맞는다", "'kicking the ball across an empty floor'.")],
      more="같은 동작을 6등신으로도 만들어, 과장이 얼마나 덜 필요해지는지 비교해 보세요.")],
5: [dict(id="d5b", title="박사의 첫날과 1년 차 — 새 대화 두 개", goal="같은 박사를 밝은 첫날 얼굴과 지친 1년 차 얼굴로 따로 만들어, 감정 자리 선만으로 나이는 그대로 두고 지쳐 보이게 합니다.",
      why="'지친 얼굴'만 적으면 나이가 들어 보이기 쉽습니다(5부 3단계). 감정 자리(눈 아래·미간·입)와 '같은 나이'를 함께 적고, 두 장은 새 대화에서 따로 만듭니다.",
      attach="refs/doctor_sheet.png", steps=["새 대화 ①에서 프롬프트 ①로 만듭니다.", "새 대화 ②에서 프롬프트 ②로 만듭니다.", "두 장의 머리색·안경·얼굴형이 같고 선만 다른지 봅니다."],
      prompts=[("① 첫날", P("2:3", "Face and shoulders of " + who("doctor") + ", bright cheerful smile, energetic.", ANIME), "d5b_doctor_day1", "예상 결과 ① — 밝은 첫날의 박사", "2/3"),
               ("② 1년 차", P("2:3", "Face and shoulders of " + who("doctor") + ", exhausted.", ANIME + "; only add dark lines under the eyes, a furrowed brow and clenched teeth; same man in his thirties, no gray hair, no extra wrinkles, not older"), "d5b_doctor_tired", "예상 결과 ② — 지친 1년 차 박사. 눈 아래 선, 미간 주름, 이를 악문 입, 나이는 그대로", "2/3")],
      check=[("②에 더해진 선이 감정 자리 서너 곳뿐인가", "#s3"), ("머리가 세거나 주름이 늘지 않았는가", "#s3"), ("청록 사각 안경·흰 줄 머리가 그대로인가", "06_media_outfit.html#s4")],
      expect="같은 박사가 ①에서는 의욕 넘치는 신입, ②에서는 마감에 지친 베테랑으로 보입니다. 나이 차이는 느껴지지 않습니다.",
      trouble=[("②가 늙어 보인다", "'no aging, same age as image one'을 다시 넣습니다."), ("②의 얼굴형이 바뀌었다", "참고 그림을 다시 첨부합니다."), ("괴로워 보이기만 한다", "'tired but still funny, comedic exhaustion'.")],
      more="같은 두 장을 시아로도 만들어, 여성 캐릭터에서도 같은 자리의 선이 통하는지 보세요."),
     dict(id="d5c", title="무표정에 기호 하나 — 음표", goal="모아의 무표정 얼굴에 음표 기호 하나만 붙여, 표정을 바꾸지 않고도 기분 좋은 느낌이 나는지 봅니다.",
      why="기호를 여러 개 붙이면 감정이 흐려집니다(5부 4단계, 1차 그림 f6). 기호 하나와 '다른 기호 없음'을 함께 적습니다.",
      attach="refs/moa_anime_base.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "기호가 음표 하나뿐인지, 표정이 무표정 그대로인지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Face and shoulders of " + who("moa") + ", calm neutral expression, eyes half closed.", ANIME + "; add exactly one small music note symbol floating beside her head; no other symbols, no text"), "d5c_moa_note", "예상 결과 — 무표정 모아 옆에 음표 하나. 콧노래를 흥얼거리는 듯한 기분 좋은 느낌", "2/3")],
      check=[("기호가 음표 하나뿐인가", "#s4"), ("표정은 무표정 그대로인가", "#s4"), ("머리띠와 왼쪽 리본이 그대로인가", "06_media_outfit.html#s4")],
      expect="표정은 조용한데 음표 하나 덕분에 콧노래를 부르는 듯한 기분 좋은 장면으로 읽힙니다.",
      trouble=[("음표가 여러 개다", "'exactly one note'를 맨 앞에 둡니다."), ("웃는 얼굴이 됐다", "'keep the neutral mouth'."), ("악보 글씨가 생겼다", "'no sheet music, no text'.")],
      more="같은 그림의 음표를 땀방울로 바꿔 새 대화에서 만들고, 감정이 어떻게 뒤집히는지 비교해 보세요.")],
6: [dict(id="d6b", title="시아를 3D 피규어로 — 고정값 먼저", goal="시아를 매끈한 3D 피규어로 받되, 고정값 문장을 재료 문장보다 앞에 적어 머리·장식이 바뀌지 않게 합니다.",
      why="1차 그림에서 재료를 바꾸는 비교 요청은 번 개수 같은 고정값까지 바꿨습니다(6부 직접 만들기 B). 남길 것을 먼저, 바꿀 것을 나중에 적습니다.",
      attach="refs/sia_anime_base.png, refs/sia_sheet.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "검은 긴 생머리·장식 없음·은 귀걸이·흰 앞치마가 남았는지 셉니다."],
      prompts=[("넣을 프롬프트", "Illustration, vertical 2:3.\nKeep exactly first: Sia's long straight jet-black hair, no headdress, small silver earrings, gray eyes, charcoal-black maid dress with a large gray bow and a long white frilled apron.\nThen change only the rendering: a smooth vinyl collectible figure of this adult woman, standing on a small round base, soft studio lighting, no outlines.\nPlain white background.\n" + END, "d6b_sia_figure", "예상 결과 — 매끈한 3D 피규어 시아. 받침대 위에 서 있고 검은 생머리·은 귀걸이·흰 앞치마 그대로", "2/3")],
      check=[("선 대신 둥근 명암으로 형태가 보이는가", "#s1"), ("고정값 다섯 가지가 그대로인가", "#s4"), ("SD가 아니라 원래 비율의 성인인가", "04_proportion.html#s1")],
      expect="장난감 가게 진열장에 있을 법한 시아 피규어가 나옵니다. 재료는 바뀌었지만 머리·장식·옷은 그대로입니다.",
      trouble=[("SD 비율이 됐다", "'normal adult proportions, not chibi'."), ("머리가 짧아졌다", "고정값 문장을 다시 맨 앞에 둡니다."), ("상자에 상표 글씨가 생겼다", "'no box, no text, no logo'.")],
      more="같은 문장의 재료 부분만 '16-bit pixel art'로 바꿔 새 대화에서 만들고, 두 장의 고정값을 비교해 보세요."),
     dict(id="d6d", title="모아 설정 시트 한 장", goal="모아의 설정 시트(정면·옆·뒤 전신, 표정 다섯, 머리띠·리본 확대)를 받아, 앞으로 베리에이션을 요청할 때 첨부할 기준으로 삼습니다.",
      why="설정 시트가 있으면 어떤 베리에이션을 해도 같은 캐릭터로 돌아옵니다(6부 4단계). 다만 시트 안 이름표 글씨는 깨지기 쉬우니 비워 두고 직접 적습니다.",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "뒤에서 본 모습에서도 리본이 왼쪽 귀 위에 있는지 봅니다(뒤에서 보면 화면 왼쪽).", "이름표 자리는 비어 있어야 합니다. 이름·키는 나중에 직접 넣으세요."],
      prompts=[("넣을 프롬프트", "Illustration, wide 16:9.\nArt style: " + ANIME + "\n" + KEEP + "\nA clean character model sheet of " + who("moa") + ": front, side and back full-body views on the left; five small face expressions (neutral, smile, surprised, troubled, angry) on the upper right; close-ups of the frilled headband and the white ribbon over her LEFT ear on the lower right; small blank label boxes with no text.\nPlain white background.\n" + END, "d6d_moa_sheet", "예상 결과 — 모아 설정 시트. 세 방향 전신, 표정 다섯, 머리띠·리본 확대, 빈 이름표 자리", "16/9")],
      check=[("세 방향 전신의 머리띠·리본 위치가 서로 맞는가", "#s4"), ("이름표 자리에 글씨가 없는가", "#s4"), ("표정 다섯이 같은 얼굴인가", "05_expression.html#s1")],
      expect="한 장으로 모아의 모든 고정값을 확인할 수 있는 기준 그림이 나옵니다. 이후 베리에이션 요청에 이 그림을 첨부합니다.",
      trouble=[("뒷모습에서 리본이 반대쪽이다", "'from behind, the ribbon appears on the left side of the picture'를 덧붙입니다."), ("이름표에 글씨가 생겼다", "'blank boxes, no letters'."), ("표정마다 얼굴이 다르다", "'same face in all five expressions'.")],
      more="같은 양식으로 하루·시아 시트도 만들어 세 사람 시트를 나란히 두세요.")],
7: [dict(id="d7b", title="f4 다시 시도 — 나이 신호를 함께 적기", goal="1차에서 엉뚱하게 나온 f4(SD 나이 쏠림)를, 이번에는 '고친 쪽' 프롬프트로 만들어 SD지만 성인으로 보이는지 확인합니다.",
      why="1차 f4 그림은 요청과 전혀 다른 3컷 만화가 나왔고, 4부 연습의 SD 하루는 성인 문장에도 어려 보였습니다. 나이 문장만이 아니라 성인 신호를 함께 적습니다(7부 나이 신호).",
      attach="refs/haru_anime_base.png", steps=[NEWCONV, "아래 프롬프트로 한 장을 만듭니다.", "4부 연습 결과(d3)와 나란히 놓고, 어느 쪽이 더 성인으로 보이는지 봅니다."],
      prompts=[("넣을 프롬프트", P("2:3", "Full-body figure of the adult woman " + CH["haru"] + " drawn 2.5 heads tall in comedy SD style, standing confidently with a clipboard.", ANIME + "; adult face cues: eyes slightly longer horizontally and a bit narrower, a small visible nose line, calm confident smile; adult outfit: white knee-length lab coat over a lavender hoodie, slim dark trousers, low heels; she is an adult in her twenties, not a child"), "d7b_haru_sd_adult", "예상 결과 — 성인 신호를 적은 2.5등신 하루. 가로로 긴 눈, 코 선, 클립보드와 랩코트로 SD지만 성인 연구원", "2/3")],
      check=[("눈이 가로로 조금 길고 코 선이 보이는가", "#drift"), ("옷차림이 어른 옷인가", "#drift"), ("4부 연습 결과보다 성인으로 보이는가", "04_proportion.html#drill")],
      expect="머리는 크지만 차분한 눈매와 코 선, 클립보드 덕분에 '작게 그린 어른 연구원'으로 읽힙니다.",
      trouble=[("여전히 어려 보인다", "'no round baby cheeks, mature expression'을 더합니다."), ("SD가 아니라 보통 비율이 됐다", "'head is 40 percent of total height'처럼 크게 과장해 적습니다."), ("클립보드에 글씨가 생겼다", "'blank clipboard, no text'.")],
      more="같은 프롬프트에서 성인 신호 문장만 빼고 새 대화에서 만들어, 신호의 효과를 비교해 보세요."),
     dict(id="d7c", title="f1 고치기 — 고정값을 맨 앞에, 새 대화에서", goal="1차 f1(수묵풍에서 머리색이 바뀐 모아)을 부분 수정이 아니라 새 대화에서, 고정값을 맨 앞에 적어 다시 만듭니다.",
      why="1차에서 f1을 부분 수정으로 고쳤더니 리본 색만 바뀌고 머리색은 그대로였습니다. 작은 수정이 잘 반영되지 않을 때는 새 대화에서 고정값을 먼저 적고 처음부터 만듭니다(7부 1단계).",
      attach="refs/moa_anime_base.png, refs/moa_sheet.png", steps=["f1 그림은 첨부하지 않습니다. 새 대화를 열고 참고 그림만 첨부합니다.", "아래 프롬프트로 한 장을 만듭니다.", "머리띠·왼쪽 리본·웨이브 머리를 확인하고, 수묵풍(끊긴 선·여백)도 지켜졌는지 봅니다."],
      prompts=[("넣을 프롬프트", "Illustration, vertical 2:3.\nKeep exactly first: Moa's wavy hair (in ink it is a mid gray wash, not white or blond), the white frilled maid headband and the white ribbon over her LEFT ear, her gentle face from the reference.\nThen change only the drawing style: black ink brush painting with broken brush lines and large empty white space, bold strokes for the hair.\nPlain white paper.\n" + END, "d7c_moa_ink_fixed", "예상 결과 — 고정값을 먼저 적은 수묵풍 모아. 웨이브 머리·프릴 머리띠·왼쪽 리본이 남고 끊긴 붓선과 여백", "2/3")],
      check=[("머리띠와 왼쪽 귀 위 리본이 있는가", "#s1"), ("웨이브 머리가 회색 먹으로 칠해졌는가(금발처럼 희지 않은가)", "#s1"), ("글씨·도장이 없는가", "#f8")],
      expect="1차 f1과 같은 수묵풍이지만 장식과 머리가 모아 그대로라 한눈에 모아로 알아봅니다.",
      trouble=[("머리가 또 하얗다", "'hair painted in mid-gray ink wash'를 맨 앞에 둡니다."), ("리본이 오른쪽이다", "'ribbon on her left side, which is the right side of the picture when she faces the viewer'."), ("가짜 글씨가 생겼다", "'no calligraphy, no seals'를 다시 넣습니다.")],
      more="1차 f1, 부분 수정한 f1, 이번 결과 세 장을 나란히 놓고 어떤 방법이 가장 효과가 있었는지 적어 두세요.")],
}
NEW_IDS = {d["id"] for v in DRILL2.values() for d in v}
for _k, _v in DRILL2.items():
    DRILL[_k] = DRILL[_k] + _v

RETRY = {}
RETRY3 = {}
BASE_OF = {}

def write_bundle(D, ids, title, note):
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for no, ds in DRILL.items():
        md = f"# D0{no} · {no}부 연습 과제 예상 결과 그림\n"; got = False
        for d in ds:
            if d["id"] not in ids: continue
            got = True
            md += f"\n## {d['id']} — {d['title']}\n첨부: {d['attach']}\n순서: " + " / ".join(d["steps"]) + "\n"
            for lab, pr, key, alt, ar in d["prompts"]:
                n += 1; rows.append([n, f"D0{no}", key, ar.replace('/', ':'), ""])
                md += f"\n### {key} ({lab})\nalt: {alt}\n```\n{pr}\n```\n"
        if got: open(os.path.join(D, "prompts", f"D0{no}_part{no}.md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "ratio", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(f"# {title} ({n}장)\n\n{note}\n")
    return n

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    old = {d["id"] for v in DRILL.values() for d in v} - NEW_IDS
    n1 = write_bundle(os.path.join(ROOT, "docs", "image_requests_drill"), old, "그림 요청 꾸러미 3 — 연습 과제 예상 결과", "부마다 연습 과제의 프롬프트를 그대로 넣어 만든 결과 그림입니다. 파일 하나 = 새 대화 하나. d6은 7부 실패 그림 f6을 받은 뒤 요청합니다.")
    n2 = write_bundle(os.path.join(ROOT, "docs", "image_requests_drill2"), NEW_IDS, "그림 요청 꾸러미 5 — 2차 연습 과제 예상 결과", "부마다 2개씩 더한 연습 과제(부당 3개)의 예상 결과 그림입니다. **프롬프트 하나 = 새 대화 하나**로 만들어 주세요(①·② 두 장짜리 과제도 서로 다른 새 대화에서). 비교할 그림끼리는 서로 첨부하지 않습니다. 첨부는 각 과제의 '첨부'에 적힌 연구실 기준 그림만.")
    print("drill images", n1, "+", n2)
