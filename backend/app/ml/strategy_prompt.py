import json
import logging

from pydantic import BaseModel, Field, ValidationError

from app.ml.clients.base import TextModelClient


logger = logging.getLogger("uvicorn.error")


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
    clean_product_name = str(product_name or "").strip()
    clean_product_description = str(
        product_description or ""
    ).strip()

    prompt = f"""
당신은 소상공인을 위한 전문 광고 전략가이자 카피라이터입니다.

아래 상품 정보와 광고 설정을 바탕으로 광고 전략과 슬로건을 생성하세요.

[상품 정보]
- 상품명: {clean_product_name}
- 상품 설명: {clean_product_description or "없음"}
- 업종: {industry}
- 가격: {price if price is not None else "정보 없음"}

[광고 설정]
- 설정 방식: {mode}
- 광고 플랫폼: {platform}
- 광고 목표: {goal or "자동 추천"}
- 광고 스타일: {style or "자동 추천"}

[사실성 규칙]
1. 상품 설명에 직접 포함된 정보만 사실로 사용하세요.
2. 상품 설명에 없는 재료, 맛, 향, 식감, 조리법, 성능,
   효능, 인증, 수치, 할인과 혜택을 추가하지 마세요.
3. 일반적인 상품 지식으로 입력되지 않은 특징을 추측하지 마세요.
4. 고객 반응, 판매 실적, 수상 경력과 인증을 만들어내지 마세요.

[광고 전략 작성 규칙]
1. strategy_title은 30자 이내로 작성하세요.
2. strategy_description은 2~3문장, 200자 이내로 작성하세요.
3. strategy_description에는 다음 내용만 포함하세요.
   - 강조할 실제 상품 특징
   - 광고에서 사용할 분위기와 표현 방향
   - 플랫폼에 적합한 시각적 표현과 카피 방향
4. 게시 시간, 해시태그, 링크, 인플루언서,
   고객 후기와 같은 광고 운영 방법은 포함하지 마세요.

[슬로건 필수 규칙]
1. 슬로건은 정확히 3개 작성하세요.
2. 첫 번째 슬로건은 반드시 정확한 상품명
   "{clean_product_name}"으로 시작하세요.
3. 세 슬로건 모두 상품 설명에 실제로 포함된 특징이나 단어를
   최소 한 가지 이상 사용하세요.
4. 세 슬로건 모두 상품의 종류를 알아볼 수 있게 작성하세요.
5. 세 슬로건 모두 광고 목표에 맞는 행동 또는 인식 유도 표현을
   최소 한 가지 포함하세요.
6. 세 슬로건 모두 선택한 광고 스타일이 문장에 드러나야 합니다.
7. 각 슬로건은 50자 이내의 자연스러운 한 문장으로 작성하세요.
8. 세 슬로건은 시작 단어, 문장 구조와 핵심 표현이 서로 달라야 합니다.
9. 슬로건은 조사, 연결어 또는 미완성 표현으로 끝나면 안 됩니다.
10. 상품 설명을 단순하게 나열하거나 요약하지 말고,
    실제 광고 문구처럼 자연스럽게 작성하세요.

[후보별 역할]
1번 슬로건:
- 정확한 상품명 "{clean_product_name}"으로 시작
- 대표 상품 특징을 중심으로 작성

2번 슬로건:
- 상품 설명에 포함된 특징
- 소비자가 얻는 경험이나 사용 장면을 중심으로 작성

3번 슬로건:
- 상품 특징
- 광고 목표에 맞는 행동 유도를 가장 명확하게 작성

[출력 전 자체 확인]
- 1번 슬로건이 정확한 상품명으로 시작하는지 확인하세요.
- 슬로건이 정확히 3개인지 확인하세요.
- 세 문장 모두 상품 설명의 실제 특징을 포함했는지 확인하세요.
- 세 문장 모두 광고 목표를 반영했는지 확인하세요.
- 세 문장 모두 광고 스타일을 반영했는지 확인하세요.
- 상품 설명에 없는 정보를 추가하지 않았는지 확인하세요.

JSON 이외의 설명, 코드 블록과 마크다운은 출력하지 마세요.

반드시 다음 JSON 형식으로만 응답하세요.

{{
    "strategy_title": "30자 이내의 광고 전략 제목",
    "strategy_description": "200자 이내의 핵심 광고 전략 설명",
    "slogans": [
        "{clean_product_name}으로 시작하는 슬로건",
        "서로 다른 두 번째 슬로건",
        "행동 유도가 포함된 세 번째 슬로건"
    ]
}}
""".strip()

    logger.info(
        "\n"
        "========== 실제 광고 전략 생성 프롬프트 ==========\n"
        "%s\n"
        "===================================================",
        prompt,
    )

    try:
        response_text = client.generate(prompt)

        logger.info(
            "\n"
            "========== 광고 전략 생성 원본 응답 ==========\n"
            "%s\n"
            "===============================================",
            response_text,
        )

        response_data = json.loads(response_text)

        logger.info(
            "\n"
            "========== 광고 전략 JSON 파싱 결과 ==========\n"
            "%s\n"
            "================================================",
            response_data,
        )

        recommendation = StrategyRecommendation.model_validate(
            response_data
        )

        result = recommendation.model_dump()

        logger.info(
            "\n"
            "========== 최종 광고 전략 생성 결과 ==========\n"
            "전략 제목: %s\n"
            "전략 설명: %s\n"
            "슬로건: %s\n"
            "================================================",
            result["strategy_title"],
            result["strategy_description"],
            result["slogans"],
        )

        return result

    except json.JSONDecodeError as exc:
        logger.exception(
            "광고 전략 응답을 JSON으로 변환하지 못했습니다. "
            "원본 응답: %s",
            response_text,
        )
        raise ValueError(
            "텍스트 모델이 올바른 JSON 형식으로 응답하지 않았습니다."
        ) from exc

    except ValidationError as exc:
        logger.exception(
            "광고 전략 응답이 스키마 검증에 실패했습니다. "
            "파싱 결과: %s",
            response_data,
        )
        raise ValueError(
            "생성된 광고 전략의 응답 형식이 올바르지 않습니다."
        ) from exc

    except Exception:
        logger.exception(
            "광고 전략과 슬로건 생성 중 오류가 발생했습니다."
        )
        raise