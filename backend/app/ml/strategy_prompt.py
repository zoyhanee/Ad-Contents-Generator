import json

from pydantic import BaseModel, Field

from app.ml.clients.base import TextModelClient


class StrategyRecommendation(BaseModel):
    strategy_title: str
    strategy_description: str
    slogans: list[str] = Field(
        min_length=3,
        max_length=3,
    )


def generate_strategy_recommendation(
    client: TextModelClient,
    product_name: str,
    product_description: str,
    industry: str,
    price: int | float | None,
    mode: str,
    platform: str,
    goal: str | None,
    style: str | None,
) -> dict:
    prompt = f"""
당신은 소상공인을 위한 전문 광고 전략가이자 카피라이터입니다.

아래 상품 정보와 광고 설정을 분석해 광고 전략과 슬로건을 생성하세요.

[상품 정보]
- 상품명: {product_name}
- 상품 설명: {product_description or "없음"}
- 업종: {industry}
- 가격: {price if price is not None else "정보 없음"}

[광고 설정]
- 설정 방식: {mode}
- 광고 플랫폼: {platform}
- 광고 목표: {goal or "자동 추천"}
- 시각적 스타일: {style or "자동 추천"}

다음 조건을 반드시 지키세요.

1. 상품의 재료, 성능, 효능, 가격, 할인, 수치 등
   사실로 검증되어야 하는 정보는 입력된 상품 정보만 활용하세요.
2. 감정, 분위기, 계절감, 사용 장면은 상품과 자연스럽게 어울리는 범위에서
   창의적으로 표현할 수 있습니다.
3. 실제 사실처럼 오해될 수 있는 고객 반응, 판매 실적, 인증,
   수상 경력 등은 만들지 마세요.
4. 플랫폼 특성과 광고 목표에 맞는 광고 전략을 제안하세요.

5. strategy_title은 30자 이내의 간결하고 매력적인 제목으로 작성하세요.
6. strategy_description은 2~3문장, 200자 이내로 작성하세요.
7. strategy_description에는 다음 내용만 포함하세요.
   - 어떤 상품 특징을 강조할지
   - 어떤 감정과 분위기로 표현할지
   - 플랫폼에 어울리는 시각적 표현과 카피 방향
8. 게시 시간, 해시태그, 광고 타깃, 링크, 쇼핑 기능,
   인플루언서, 고객 후기 등 광고 운영 방법은 포함하지 마세요.

9. 슬로건은 서로 다른 광고 방향으로 정확히 3개 생성하세요.
10. 상품 정보를 단순히 설명하거나 요약하지 말고,
    고객이 한 번 더 읽고 싶어지는 광고 카피로 작성하세요.
11. 첫 번째 슬로건은 상품의 가장 매력적인 특징을 감각적으로 표현하세요.
12. 두 번째 슬로건은 고객이 원하는 순간이나 감정을 떠올리게 하세요.
13. 세 번째 슬로건은 상품을 직접 경험하고 싶게 만드는
    강한 한마디로 작성하세요.
14. "만나보세요", "기다립니다", "특별한", "완벽한"처럼
    흔하고 추상적인 광고 표현은 가능한 한 피하세요.
15. 상품 설명의 핵심 단어를 그대로 나열하지 말고,
    맛, 향, 질감, 분위기, 사용 장면이 자연스럽게 떠오르게 표현하세요.
16. 세 슬로건은 문장 구조, 시작 단어, 핵심 표현이
    서로 겹치지 않아야 합니다.
17. 각 슬로건은 20자에서 35자 사이를 권장하되,
    자연스러운 문장 완결성을 글자 수보다 우선하세요.
18. 글자 수를 맞추기 위해 문장을 어색하게 줄이거나
    생략하지 마세요.
19. 각 슬로건은 조사, 연결어, 쉼표 뒤의 미완성 표현으로
    끝나지 않아야 합니다.

JSON 이외의 설명, 코드 블록, 마크다운은 출력하지 마세요.

반드시 다음 JSON 형식으로만 응답하세요.

{{
    "strategy_title": "30자 이내의 광고 전략 제목",
    "strategy_description": "200자 이내의 핵심 광고 전략 설명",
    "slogans": [
        "20~35자의 서로 다른 슬로건 1",
        "20~35자의 서로 다른 슬로건 2",
        "20~35자의 서로 다른 슬로건 3"
    ]
}}
""".strip()

    response_text = client.generate(prompt)
    response_data = json.loads(response_text)

    recommendation = StrategyRecommendation.model_validate(
        response_data
    )

    return recommendation.model_dump()