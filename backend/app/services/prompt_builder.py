from app.schemas.prompt import ImagePromptInput, SloganPromptInput


INDUSTRY_LABELS = {
    "restaurant": "음식점",
    "cafe": "카페",
    "beauty": "뷰티",
    "retail": "소매점",
}

PLATFORM_LABELS = {
    "instagram": "인스타그램",
    "baemin": "배달의민족",
    "naver": "네이버",
    "offline": "오프라인 포스터",
}

GOAL_LABELS = {
    "awareness": "브랜드 인지도 향상",
    "sales": "판매 전환",
    "traffic": "방문 유도",
    "promotion": "프로모션 홍보",
}

STYLE_LABELS = {
    "warm": "따뜻한 감성",
    "modern": "모던하고 미니멀한 분위기",
    "vivid": "생동감 있고 선명한 분위기",
    "premium": "프리미엄하고 고급스러운 분위기",
}

PLATFORM_GUIDES = {
    "인스타그램": (
        "이미지와 함께 보았을 때 감정이나 장면이 떠오르고, "
        "첫눈에 관심을 끄는 짧고 감각적인 표현"
    ),
    "배달의민족": (
        "메뉴의 맛과 특징을 빠르게 이해할 수 있고, "
        "지금 이 메뉴를 선택하고 싶어지게 하는 직접적인 표현"
    ),
    "네이버": (
        "감성적인 분위기보다 상품의 특징과 선택 이유가 "
        "구체적으로 전달되는 신뢰감 있는 표현"
    ),
    "오프라인 포스터": (
        "짧은 시간 안에 핵심을 파악할 수 있도록 "
        "간결하고 강하게 전달하는 표현"
    ),
}



def _label(mapping: dict[str, str], key: str | None) -> str:
    if not key:
        return "미지정"
    return mapping.get(key, key)


def build_slogan_prompt(prompt_input: SloganPromptInput) -> str:
    product = prompt_input.product
    strategy = prompt_input.strategy

    industry = _label(INDUSTRY_LABELS, product.industry)
    platform = _label(PLATFORM_LABELS, strategy.platform)
    goal = _label(GOAL_LABELS, strategy.goal)
    style = _label(STYLE_LABELS, strategy.style)
    platform_guide = PLATFORM_GUIDES.get(
        platform,
        "해당 플랫폼의 사용 환경에 자연스럽게 어울리는 표현",
    )

    custom_theme = ""
    if strategy.custom_theme:
        custom_theme = f"\n- 추가 테마: {strategy.custom_theme}"

    return f"""
다음 상품을 위한 광고 슬로건 후보 3개를 작성해주세요.

[상품 정보]
- 상품명: {product.name}
- 가격: {product.price or "미입력"}
- 업종: {industry}
- 상품 설명: {product.description}

[광고 설정]
- 플랫폼: {platform}
- 플랫폼 작성 방향: {platform_guide}
- 광고 목표: {goal}
- 광고 스타일: {style}
- 이전 작업물 톤 유지: {"예" if strategy.reuse_tone else "아니오"}{custom_theme}

[작성 방향]
광고 설정을 단순히 문구에 넣지 말고, 각 조건이 문장의 목적과 표현 방식에 반영되도록 작성해주세요.

- 플랫폼에 실제로 게시했을 때 자연스러운 문구여야 합니다.
- 광고 목표에 따라 소비자가 기억하거나, 구매하거나, 방문하거나, 프로모션에 관심을 갖도록 핵심 메시지를 구성해주세요.
- 광고 스타일은 특정 단어를 반복하는 방식이 아니라 문장의 길이, 리듬, 표현 방식과 분위기로 보여주세요.
- 상품 설명에서 가장 광고 가치가 높은 특징을 찾아 활용해주세요.
- 같은 시간대, 상황, 감정 표현을 반복하지 말고 다양한 일상 장면을 활용해주세요.
- 광고 스타일을 특정한 단어나 상황 하나로만 표현하지 마세요.

[후보 작성 원칙]
세 후보는 서로 다른 핵심 아이디어를 사용하고,
이전 후보에서 사용한 소재와 상황을 다음 후보에서 반복하지 마세요.

후보 번호별 역할이나 순서를 미리 정하지 말고,
상품 정보와 광고 설정에 적합한 관점을 자유롭게 선택해주세요.

세 후보에서 같은 핵심 소재, 소비 상황, 문장 구조를 반복하지 마세요.
한 후보의 단어만 바꾸어 다른 후보를 만들지 마세요.

일반적인 음식 광고 표현보다 상품 설명에서 확인되는 고유한 특징을 우선해주세요.
상품 정보에 없는 특징은 만들어내지 마세요.

각 후보는 앞선 후보에서 사용한 핵심 소재, 상황, 행동을 다시 사용하지 말고 완전히 다른 광고 아이디어로 작성해주세요.

[작성 조건]
- 소상공인이 바로 사용할 수 있는 자연스러운 한국어로 작성해주세요.
- 각 후보는 짧고 명확한 한 문장으로 작성해주세요.
- 설명이나 작성 이유는 출력하지 마세요.
- 최종 출력 전 세 후보의 의미와 문장 구조가 겹치지 않는지 확인해주세요.
""".strip()


def build_image_prompt(prompt_input: ImagePromptInput) -> str:
    product = prompt_input.product
    strategy = prompt_input.strategy

    industry = _label(INDUSTRY_LABELS, product.industry)
    platform = _label(PLATFORM_LABELS, strategy.platform)
    style = _label(STYLE_LABELS, strategy.style)

    poster_size = ""
    if strategy.platform == "offline" and strategy.poster_size:
        poster_size = f"\n- 포스터 규격: {strategy.poster_size.upper()}"

    custom_theme = ""
    if strategy.custom_theme:
        custom_theme = f"\n- 추가 테마: {strategy.custom_theme}"

    return f"""
다음 정보를 바탕으로 광고 이미지 생성을 위한 프롬프트를 작성해주세요.

[상품 정보]
- 상품명: {product.name}
- 가격: {product.price or "미입력"}
- 업종: {industry}
- 상품 설명: {product.description}

[광고 설정]
- 플랫폼: {platform}
- 시각적 스타일: {style}
- 선택 슬로건: {prompt_input.selected_slogan}{poster_size}{custom_theme}

[이미지 방향]
- 상품이 명확하게 보이도록 구성해주세요.
- 광고 문구가 들어갈 여백을 고려해주세요.
- 소상공인이 실제 홍보물로 사용할 수 있는 완성도 높은 이미지로 구성해주세요.
""".strip()

