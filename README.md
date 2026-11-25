# 구조 먼저 그리기 연구실 · 웃음 편 2 · 베리에이션 — 같은 캐릭터, 다른 그림

80년대 셀화, 맑은 유럽 선, 흑백 러프와 수묵 붓선, 2.5등신 SD, 무너진 개그 얼굴, 3D 피규어, 잡지 포스터까지. 하루·시아·모아·박사를 여러 그림체로 즐겁게 바꿔 그리며, 무엇을 바꾸고 무엇을 남겨야 같은 캐릭터로 보이는지 실험으로 익힙니다. 출발점은 참고 그림 70여 장을 정답 없이 비슷한 것끼리 넓게 묶은 **스타일 지도**(k-평균 군집)입니다.

- 사이트: https://adminmrobo.github.io/drawing_lab_fun_02/
- 글 · 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)

## 구성
| 부 | 페이지 | 내용 |
|---|---|---|
| 목차 | `index.html` | 세 줄 요약, 스타일 지도(군집 실험), 전체 흐름, 고정값 표, 등장인물, 원리와 출처 |
| 1부 | `01_era.html` | 시대 — 그림자 단계, 눈, 정보량, 색보정 (모델 모아) |
| 2부 | `02_line.html` | 선과 지역 — 굵기 비, 칠 방식, 단순화, 배경 효과선 (모델 시아) |
| 3부 | `03_mono.html` | 흑백·선화 — 움직임 선과 러프, 망점·해칭·먹칠, 붓선과 여백, 회색값 (모아·시아·하루) |
| 4부 | `04_proportion.html` | 등신 — 등신 계산, 부위 함께 줄이기, 마스코트, 잔상 (모델 하루) |
| 5부 | `05_expression.html` | 표정·과장 — 무너짐 단계, 한 곳 과장, 선 더하기, 만화 기호 (시아·박사) |
| 6부 | `06_media_outfit.html` | 매체·옷 — 재료, 카메라, 옷 테마와 포스터, 설정 시트 (셋 모두) |
| 7부 | `07_failure_lab.html` | 베리에이션 실패 8종, 특징으로 적기, 나이 신호 |
| 8부 | `practice/index.html` | 실전 연습장 — 베리에이션 작업대, 군집 분류판, 문장 공방, 진단 데스크 |

## 원리와 출처
참고 그림은 저작권이 있는 남의 작품이 대부분이라 페이지에 싣지 않았고, 작품·캐릭터 이름도 적지 않았습니다. 그림마다 바뀐 특징만 여섯 축(시대·선·사실·과장·재료·색)으로 정리했습니다(`build/style_points.py`). 원리 출처: MacQueen(1967) k-평균, Pearson(1901) 주성분, McCloud(1993), Thomas·Johnston(1981), ITU-R BT.601, Rombach 외(2022). 모든 숫자는 설명용 예시값입니다.

## 빌드와 점검
```
python3 build/build.py && python3 build/check_numbers.py && python3 build/make_og.py
python3 -m http.server 8765 &   # 아래 두 점검용
python3 build/check_pages.py && python3 build/check_missions.py
```
작성 방침: `docs/WRITING_POLICY.md` · 그림 요청(Genspark): `docs/image_requests/`(표지 9 + 본문 12 + 실패 8), `docs/image_requests_make/`(비교 14), `docs/image_requests_drill/`(연습 7) · 페르소나 검사: `docs/persona_review.md`

캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다. 캐릭터 그림: [fruitfly-lab-expressions](https://github.com/adminmrobo/fruitfly-lab-expressions).
