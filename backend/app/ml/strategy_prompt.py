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
    improvement_rules: list[str] | None = None,
) -> dict:
    clean_product_name = str(product_name or "").strip()
    clean_product_description = str(
        product_description or ""
    ).strip()
    
    improvement_rules = improvement_rules or []

    improvement_guide = ""

    if improvement_rules:
        formatted_rules = "\n".join(
            f"- {rule}"
            for rule in improvement_rules
        )

        improvement_guide = f"""
[누적 광고 평가 기반 개선 지침]
아래 지침은 이전 광고 생성 결과에서 반복적으로 발견된 약점을
일반화하여 만든 개선 기준입니다.
현재 상품 정보와 광고 설정을 우선하며,
관련되는 범위에서만 적용하세요.

{formatted_rules}
""".strip()

    prompt = f"""
    당신은 소상공인을 위한 전문 광고 전략가이자 카피라이터입니다.

    아래 상품 정보와 광고 설정을 바탕으로
    광고 전략과 서로 다른 아이디어의 슬로건 3개를 생성하세요.

    [상품 정보]
    - 상품명: {clean_product_name}
    - 상품 설명: {clean_product_description or "없음"}
    - 업종: {industry}
    - 가격: {price if price is not None else "정보 없음"}

    [광고 설정]
    - 설정 방식: {mode}
    - 광고 플랫폼: {platform}
    - 광고 목표: {goal or "미지정"}
    - 광고 스타일: {style or "미지정"}
    
    {improvement_guide}

    [중요한 해석 규칙]
    - 설정 방식, 자동추천, AI 추천, faster 등의 표현은
    시스템 내부에서 광고 전략을 선택하는 방식일 뿐
    소비자에게 전달할 광고 메시지가 아닙니다.
    - 광고 목표나 스타일이 지정되지 않은 경우에는
    상품 정보와 플랫폼에 자연스럽게 어울리는 방향을 스스로 선택하세요.
    - "자동추천", "AI 추천", "추천 전략", "faster" 등의 표현을
    strategy_title, strategy_description 또는 slogans에 사용하지 마세요.

    [사실성 규칙]
    1. 상품 설명에 직접 포함된 정보만 사실로 사용하세요.
    2. 상품 설명에 없는 재료, 맛, 향, 식감, 조리법, 성능,
    효능, 인증, 수치, 할인과 혜택을 추가하지 마세요.
    3. 일반적인 상품 지식으로 입력되지 않은 특징을 추측하지 마세요.
    4. 고객 반응, 판매 실적, 수상 경력과 인증을 만들어내지 마세요.
    5. 상품 설명에 근거가 없는 감각, 감정, 사용 경험이나
    소비 상황을 새롭게 만들어 사실처럼 표현하지 마세요.

    [광고 전략 작성 규칙]
    1. strategy_title은 30자 이내로 작성하세요.
    2. strategy_description은 2~3문장, 200자 이내로 작성하세요.
    3. strategy_description에는 다음 내용을 중심으로 작성하세요.
    - 가장 강조할 실제 상품 특징
    - 소비자에게 전달할 핵심 가치
    - 플랫폼에 어울리는 광고 분위기와 표현 방향
    4. 시스템의 설정 방식이나 자동추천 여부를 전략 내용에 포함하지 마세요.
    5. 게시 시간, 해시태그, 링크, 인플루언서,
    고객 후기 같은 광고 운영 방법은 포함하지 마세요.

    [슬로건 작성 원칙]
    1. 슬로건은 정확히 3개 작성하세요.
    2. 상품 설명을 요약하는 문장이 아니라
    실제 광고 이미지의 메인 카피로 사용할 수 있는 문구를 작성하세요.
    3. 한 문장에 여러 상품 특징과 광고 목표를 모두 넣으려 하지 마세요.
    4. 하나의 슬로건에는 하나의 핵심 아이디어만 담으세요.
    5. 짧고 읽기 쉬우며 기억에 남는 표현을 우선하세요.
    6. 상품 설명의 문장을 그대로 복사하거나 단어만 재배열하지 마세요.
    7. 상품 설명에 없는 사실은 추가하지 마세요.
    8. 세 슬로건은 단어만 바꾼 유사 문장이 아니라
    서로 다른 카피 아이디어를 사용해야 합니다.
    9. 같은 핵심 동사, 문장 구조와 끝맺음을 반복하지 마세요.
    10. 행동 유도 표현은 필요한 후보에만 자연스럽게 사용하고
        세 문장 모두에 억지로 넣지 마세요.
    11. 각 슬로건은 공백 포함 30자 이내를 권장하며,
        최대 40자를 넘지 마세요.

    [후보별 역할]

    1번 - 핵심 가치형
    - 상품의 가장 중요한 특징이나 가치를 한 가지 선택하세요.
    - 상품명을 반드시 넣을 필요는 없습니다.
    - 브랜드를 대표할 수 있는 메인 카피처럼 작성하세요.

    2번 - 감성·경험형
    - 상품 설명에 실제로 포함된 특징을 바탕으로
    소비자에게 전달할 분위기나 인상을 표현하세요.
    - 상품 설명만으로 확인할 수 없는 맛, 식감, 사용 경험,
    감정적 효과나 상황을 새롭게 만들어내지 마세요.
    - 구체적인 사실을 추가하기보다 표현 방식과 문장 리듬을 통해
    1번과 다른 인상을 만드세요.
    - 1번의 문장 구조와 핵심 표현을 반복하지 마세요.

    3번 - 임팩트·행동형
    - 소비자의 관심이나 다음 행동을 자연스럽게 유도하세요.
    - "지금 구매하세요", "경험해보세요", "만나보세요",
    "느껴보세요", "신어보세요" 같은 전형적인 광고 명령형은
    특별히 필요한 경우가 아니면 피하세요.
    - 직접 명령하지 않아도 소비자의 관심을 끌 수 있는
    짧은 선언형, 질문형 또는 리듬감 있는 표현을 우선하세요.

    [다양성 기준]
    다음과 같은 결과는 피하세요.

    나쁜 예:
    - 가벼운 운동화를 경험해보세요
    - 편안한 운동화를 만나보세요
    - 가벼운 운동화를 지금 느껴보세요

    위 문장들은 끝맺음만 다르고 같은 아이디어이므로
    서로 다른 슬로건으로 간주하지 않습니다.

    세 후보는 각각
    "무엇을 말하는가"와 "어떻게 말하는가"가 모두 달라야 합니다.

    [출력 전 자체 확인]
    - 슬로건이 정확히 3개인가?
    - 세 후보의 핵심 아이디어가 서로 다른가?
    - 상품 설명을 단순 요약한 문장이 아닌가?
    - 불필요하게 길거나 설명문처럼 작성되지 않았는가?
    - 모든 후보가 같은 행동 유도형 문장으로 끝나지 않는가?
    - 입력되지 않은 사실을 추가하지 않았는가?
    - 자동추천이나 시스템 내부 용어가 결과에 포함되지 않았는가?

    JSON 이외의 설명, 코드 블록과 마크다운은 출력하지 마세요.

    반드시 다음 JSON 형식으로만 응답하세요.

    {{
        "strategy_title": "30자 이내의 광고 전략 제목",
        "strategy_description": "200자 이내의 핵심 광고 전략 설명",
        "slogans": [
            "핵심 가치 중심의 첫 번째 카피",
            "감성 또는 경험 중심의 두 번째 카피",
            "임팩트 또는 행동 중심의 세 번째 카피"
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