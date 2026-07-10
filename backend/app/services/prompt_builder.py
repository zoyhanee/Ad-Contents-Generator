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
- 광고 목표: {goal}
- 광고 스타일: {style}{custom_theme}

[작성 조건]
- 소상공인이 바로 사용할 수 있는 자연스러운 문장으로 작성해주세요.
- 플랫폼 특성에 맞는 표현을 사용해주세요.
- 각 후보는 짧고 명확하게 작성해주세요.
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

