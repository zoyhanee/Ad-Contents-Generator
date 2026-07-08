from typing import List, Optional

from app.schemas.strategy_schema import StrategyRecommendRequest


PLATFORM_LABELS = {
    "instagram": "Instagram",
    "baemin": "배달의민족",
    "naver": "네이버",
    "offline": "오프라인 포스터",
}

CATEGORY_LABELS = {
    "restaurant": "음식점",
    "cafe": "카페",
    "beauty": "뷰티",
    "retail": "소매점",
    "음식점": "음식점",
    "카페": "카페",
    "뷰티": "뷰티",
    "소매점": "소매점",
}

GOAL_LABELS = {
    "awareness": "브랜드 인지도",
    "sales": "판매 전환",
    "traffic": "방문 유도",
    "promotion": "프로모션 홍보",
}

STYLE_LABELS = {
    "warm": "따뜻한 감성",
    "modern": "모던 & 미니멀",
    "vivid": "생동감 있는",
    "premium": "프리미엄",
}


def recommend_strategy(request: StrategyRecommendRequest):
    product = request.product
    strategy = request.strategy

    product_name = product.name
    category = _normalize_category(product.category)
    category_label = CATEGORY_LABELS.get(category, "상품")

    platforms = strategy.platforms or ["instagram"]
    platform = platforms[0]
    platform_label = PLATFORM_LABELS.get(platform, platform)

    goal = strategy.goal or "awareness"
    style = strategy.style

    goal_label = GOAL_LABELS.get(goal, "브랜드 인지도")
    style_label = STYLE_LABELS.get(style, "기본")

    print("mode:", strategy.mode)
    print("platforms:", strategy.platforms)
    print("platform:", platform)
    print("goal:", goal)
    print("style:", style)
    print("category:", category)

    # 직접 설정
    if strategy.mode == "manual":
        slogans = _build_slogans(
            product_name=product_name,
            category=category,
            platform=platform,
            goal=goal,
            style=style,
        )

        return {
            "strategy_title": (
                f"{platform_label} {category_label} "
                f"{goal_label} 전략"
            ),
            "strategy_description": (
                f"{product_name}을 {style_label} 스타일로 표현하여 "
                f"{platform_label}에서 {goal_label}을 높일 수 있는 "
                "광고 방향을 추천했습니다."
            ),
            "slogans": slogans,
        }

    # 빠른 추천
    # 빠른 추천에서는 사용자가 스타일을 직접 고르지 않으므로 style=None 사용
    # 단, _apply_style_tone()에서 빠른 추천 전용 톤을 적용함
    slogans = _build_slogans(
        product_name=product_name,
        category=category,
        platform=platform,
        goal="awareness",
        style=None,
    )

    return {
        "strategy_title": f"{platform_label} {category_label} 빠른 추천 전략",
        "strategy_description": (
            f"{category_label} 업종과 {platform_label} 플랫폼에 맞춰 "
            f"{product_name}의 핵심 매력을 빠르게 전달하는 "
            "광고 방향을 추천했습니다."
        ),
        "slogans": slogans,
    }


def _normalize_category(category: Optional[str]):
    if category is None:
        return "product"

    mapping = {
        "restaurant": "restaurant",
        "음식점": "restaurant",
        "식당": "restaurant",
        "cafe": "cafe",
        "카페": "cafe",
        "beauty": "beauty",
        "뷰티": "beauty",
        "미용": "beauty",
        "retail": "retail",
        "소매점": "retail",
        "소매": "retail",
    }

    return mapping.get(category, category)


def _build_slogans(
    product_name: str,
    category: str,
    platform: str,
    goal: str,
    style: Optional[str] = None,
):
    base_slogans = _get_goal_slogans(
        product_name=product_name,
        category=category,
        goal=goal,
    )

    platform_slogans = _apply_platform_tone(
        slogans=base_slogans,
        platform=platform,
    )

    styled_slogans = _apply_style_tone(
        slogans=platform_slogans,
        style=style,
    )

    return styled_slogans


def _get_goal_slogans(
    product_name: str,
    category: str,
    goal: str,
):
    if category == "restaurant":
        if goal == "awareness":
            return [
                f"{product_name}의 맛을 기억하게 만드는 한 끼",
                "오늘의 식사 시간을 특별하게 만드는 메뉴",
                f"한 번 보면 먹고 싶어지는 {product_name}",
            ]

        if goal == "sales":
            return [
                f"지금 주문하고 싶은 메뉴, {product_name}",
                f"오늘 한 끼 고민 끝, {product_name}",
                "든든하게 즐기는 프리미엄 한 접시",
            ]

        if goal == "traffic":
            return [
                f"오늘 방문하고 싶은 맛, {product_name}",
                "가까운 곳에서 만나는 든든한 한 끼",
                f"매장에서 직접 즐기기 좋은 {product_name}",
            ]

        if goal == "promotion":
            return [
                f"지금 놓치기 아쉬운 {product_name} 혜택",
                "맛있는 순간을 더 특별하게 만드는 이벤트",
                "오늘만 더 특별한 추천 메뉴",
            ]

    if category == "cafe":
        if goal == "awareness":
            return [
                f"{product_name}로 기억되는 카페의 순간",
                "커피와 함께 떠오르는 시그니처 메뉴",
                f"감성적인 하루를 완성하는 {product_name}",
            ]

        if goal == "sales":
            return [
                f"오늘 카페 메뉴는 {product_name}",
                "커피와 함께 주문하기 좋은 메뉴",
                "지금 먹기 좋은 달콤한 선택",
            ]

        if goal == "traffic":
            return [
                "잠깐의 여유가 필요할 때 들러보세요",
                f"오늘의 카페 코스, {product_name}",
                "머물고 싶은 공간에서 즐기는 메뉴",
            ]

        if goal == "promotion":
            return [
                f"오늘의 카페 혜택, {product_name}",
                "달콤한 시간을 더 특별하게",
                "지금 즐기기 좋은 카페 프로모션",
            ]

    if category == "beauty":
        if goal == "awareness":
            return [
                f"{product_name}로 완성하는 나만의 관리 루틴",
                "오늘의 나를 더 빛나게 하는 선택",
                "변화를 기대하게 만드는 뷰티 케어",
            ]

        if goal == "sales":
            return [
                f"지금 시작하는 나를 위한 관리, {product_name}",
                "오늘 예약하고 싶은 뷰티 케어",
                "나에게 투자하는 가장 쉬운 방법",
            ]

        if goal == "traffic":
            return [
                "오늘, 나를 위한 관리 시간을 예약하세요",
                "가까운 곳에서 시작하는 뷰티 케어",
                f"관리받고 싶은 날 찾게 되는 {product_name}",
            ]

        if goal == "promotion":
            return [
                "놓치기 아쉬운 뷰티 케어 혜택",
                "오늘 더 빛나는 나를 위한 이벤트",
                "지금 만나보는 특별 관리 프로모션",
            ]

    if category == "retail":
        if goal == "awareness":
            return [
                f"{product_name}로 완성하는 감각적인 일상",
                "취향을 보여주는 특별한 아이템",
                "일상에 새로운 분위기를 더하는 선택",
            ]

        if goal == "sales":
            return [
                f"지금 장바구니에 담고 싶은 {product_name}",
                "오늘 구매하기 좋은 추천 아이템",
                "실용성과 감각을 모두 담은 선택",
            ]

        if goal == "traffic":
            return [
                f"매장에서 직접 만나보는 {product_name}",
                "가까운 곳에서 발견하는 취향 아이템",
                "오늘 들러서 확인해보세요",
            ]

        if goal == "promotion":
            return [
                "지금 놓치면 아쉬운 추천 상품 혜택",
                f"오늘의 특별 프로모션, {product_name}",
                "합리적인 선택을 위한 이벤트",
            ]

    return [
        f"오늘의 선택, {product_name}",
        f"지금 만나보는 특별한 {product_name}",
        f"고객의 시선을 사로잡는 {product_name}",
    ]


def _apply_platform_tone(
    slogans: List[str],
    platform: str,
):
    if platform == "instagram":
        return [
            f"피드에 남기고 싶은 순간, {slogans[0]}",
            f"오늘 공유하고 싶은 선택, {slogans[1]}",
            f"감각적인 하루를 위한 {slogans[2]}",
        ]

    if platform == "baemin":
        return [
            f"지금 주문하기 좋은 {slogans[0]}",
            f"오늘 메뉴 고민 끝! {slogans[1]}",
            f"배달로 편하게 즐기는 {slogans[2]}",
        ]

    if platform == "naver":
        return [
            f"찾고 있다면 확인하세요, {slogans[0]}",
            f"검색으로 만나는 추천 정보, {slogans[1]}",
            f"선택 전에 꼭 봐야 할 {slogans[2]}",
        ]

    if platform == "offline":
        return [
            f"오늘의 추천! {slogans[0]}",
            f"지금 매장에서 만나보세요, {slogans[1]}",
            f"한눈에 기억되는 {slogans[2]}",
        ]

    return slogans


def _apply_style_tone(
    slogans: List[str],
    style: Optional[str],
):
    # 빠른 추천 전용 톤
    # style=None이면 사용자가 직접 선택한 스타일이 없는 상태
    if style is None:
        return [
            f"오늘 바로 떠오르는 {slogans[0]}",
            f"쉽게 기억되는 {slogans[1]}",
            f"한눈에 끌리는 {slogans[2]}",
        ]

    # 따뜻한 감성
    if style == "warm":
        return [
            f"마음까지 따뜻해지는 {slogans[0]}",
            f"오늘의 분위기를 부드럽게 채우는 {slogans[1]}",
            f"편안한 하루에 어울리는 {slogans[2]}",
        ]

    # 모던 & 미니멀
    if style == "modern":
        return [
            f"군더더기 없이 선명한 {slogans[0]}",
            f"깔끔한 감각으로 완성한 {slogans[1]}",
            f"모던한 분위기로 전달하는 {slogans[2]}",
        ]

    # 생동감 있는
    if style == "vivid":
        return [
            f"생생한 매력이 느껴지는 {slogans[0]}",
            f"눈길을 사로잡는 활기찬 {slogans[1]}",
            f"기분 좋게 살아나는 {slogans[2]}",
        ]

    # 프리미엄
    if style == "premium":
        return [
            f"한층 더 고급스럽게 전하는 {slogans[0]}",
            f"특별한 가치를 담아낸 {slogans[1]}",
            f"프리미엄 감성으로 완성한 {slogans[2]}",
        ]

    return slogans