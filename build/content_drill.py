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
RETRY = {}
RETRY3 = {}
BASE_OF = {}

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    D = os.path.join(ROOT, "docs", "image_requests_drill")
    os.makedirs(os.path.join(D, "prompts"), exist_ok=True)
    rows = []; n = 0
    for no, ds in DRILL.items():
        md = f"# D0{no} · {no}부 연습 과제 예상 결과 그림\n"
        for d in ds:
            md += f"\n## {d['id']} — {d['title']}\n첨부: {d['attach']}\n"
            for lab, pr, key, alt, ar in d["prompts"]:
                n += 1; rows.append([n, f"D0{no}", key, ar.replace('/', ':'), ""])
                md += f"\n### {key} ({lab})\nalt: {alt}\n```\n{pr}\n```\n"
        open(os.path.join(D, "prompts", f"D0{no}_part{no}.md"), "w").write(md)
    with open(os.path.join(D, "checklist.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["order", "conversation", "file", "ratio", "status"]); w.writerows(rows)
    open(os.path.join(D, "README.md"), "w").write(f"# 그림 요청 꾸러미 3 — 연습 과제 예상 결과 ({n}장)\n\n부마다 연습 과제의 프롬프트를 그대로 넣어 만든 결과 그림입니다. 파일 하나 = 새 대화 하나. d6은 7부 실패 그림 f6을 받은 뒤 요청합니다.\n")
    print("drill images", n)
