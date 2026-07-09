from app.models.product import Product
from app.schemas.strategy_schema import StrategyInfo


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
    "modern": "모던하고 미니멀한",
    "vivid": "생동감 있는",
    "premium": "프리미엄한",
}


def recommend_strategy(
    product: Product,
    strategy: StrategyInfo,
):

    product_name = product.name
    description = product.description or ""

    category = _normalize_category(product.industry)
    category_label = CATEGORY_LABELS.get(category, "상품")

    main_platform = strategy.platform or "instagram"
    platform_label = PLATFORM_LABELS.get(main_platform, main_platform)

    goal_label = GOAL_LABELS.get(strategy.goal, "광고 효과 향상")
    style_label = STYLE_LABELS.get(strategy.style, "트렌디한")

    if strategy.mode == "faster":
        return _recommend_fast(
            product_name=product_name,
            description=description,
            category=category,
            category_label=category_label,
            platform=main_platform,
            platform_label=platform_label,
        )

    return _recommend_manual(
        product_name=product_name,
        category=category,
        category_label=category_label,
        platform=main_platform,
        platform_label=platform_label,
        goal_label=goal_label,
        style_label=style_label,
    )


def _normalize_category(category: str | None):
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


def _recommend_fast(
    product_name: str,
    description: str,
    category: str,
    category_label: str,
    platform: str,
    platform_label: str,
):
    slogans = _platform_category_slogans(
        product_name=product_name,
        category=category,
        platform=platform,
    )

    strategy_title = f"{platform_label} {category_label} 맞춤 광고 전략"

    strategy_description = _strategy_description(
        product_name=product_name,
        category_label=category_label,
        platform=platform,
        platform_label=platform_label,
        style_label=None,
        goal_label=None,
    )

    return {
        "strategy_title": strategy_title,
        "strategy_description": strategy_description,
        "slogans": slogans,
    }


def _recommend_manual(
    product_name: str,
    category: str,
    category_label: str,
    platform: str,
    platform_label: str,
    goal_label: str,
    style_label: str,
):
    slogans = _platform_category_slogans(
        product_name=product_name,
        category=category,
        platform=platform,
        style_label=style_label,
        goal_label=goal_label,
    )

    strategy_title = f"{platform_label} {category_label} {goal_label} 광고 전략"

    strategy_description = _strategy_description(
        product_name=product_name,
        category_label=category_label,
        platform=platform,
        platform_label=platform_label,
        style_label=style_label,
        goal_label=goal_label,
    )

    return {
        "strategy_title": strategy_title,
        "strategy_description": strategy_description,
        "slogans": slogans,
    }


def _strategy_description(
    product_name: str,
    category_label: str,
    platform: str,
    platform_label: str,
    style_label: str | None = None,
    goal_label: str | None = None,
):
    style_text = f"{style_label} 분위기로 " if style_label else ""
    goal_text = f"{goal_label}을 높일 수 있도록 " if goal_label else ""

    if platform == "instagram":
        return (
            f"{category_label} 업종에 맞춰 {product_name}의 매력을 "
            f"{style_text}짧고 감각적인 문구로 전달하는 방향을 추천했습니다."
        )

    if platform == "baemin":
        return (
            f"{category_label} 고객이 공감할 수 있도록 {product_name}의 장점과 "
            f"이용 상황을 구체적으로 전달하는 방향을 추천했습니다."
        )

    if platform == "naver":
        return (
            f"검색 사용자가 빠르게 이해할 수 있도록 {product_name}의 특징과 "
            f"{category_label} 업종의 핵심 정보를 명확하게 전달하는 방향을 추천했습니다."
        )

    if platform == "offline":
        return (
            f"매장 앞이나 오프라인 홍보물에서 한눈에 기억될 수 있도록 "
            f"{product_name}을 짧고 강하게 강조하는 방향을 추천했습니다."
        )

    return (
        f"{platform_label} 플랫폼에서 {goal_text}{product_name}의 매력을 "
        f"효과적으로 전달하는 방향을 추천했습니다."
    )


def _platform_category_slogans(
    product_name: str,
    category: str,
    platform: str,
    style_label: str | None = None,
    goal_label: str | None = None,
):
    style_prefix = f"{style_label} 무드로 " if style_label else ""

    # Instagram
    if platform == "instagram":
        if category == "restaurant":
            return [
                f"보기만 해도 배고픈 한 접시, {product_name}",
                f"오늘 피드에 남기고 싶은 든든한 한 끼",
                f"한 입에 담긴 풍미, {product_name}",
            ]

        if category == "cafe":
            return [
                f"커피와 함께 완성되는 오늘의 여유, {product_name}",
                f"감성 카페 타임에 어울리는 {product_name}",
                f"피드에 남기고 싶은 달콤한 순간",
            ]

        if category == "beauty":
            return [
                f"오늘의 나를 더 빛나게 하는 {product_name}",
                f"거울 앞에서 먼저 느껴지는 변화",
                f"{style_prefix}완성하는 나만의 뷰티 루틴",
            ]

        if category == "retail":
            return [
                f"일상에 감각을 더하는 {product_name}",
                f"작지만 확실한 취향의 발견",
                f"오늘의 공간을 바꾸는 특별한 아이템",
            ]

    # Baemin
    if platform == "baemin":
        if category == "restaurant":
            return [
                f"가족, 친구와 함께 즐기기 좋은 {product_name}",
                f"든든한 식사가 필요할 때 추천하는 한 끼",
                f"오늘 메뉴 고민된다면 {product_name}",
            ]

        if category == "cafe":
            return [
                f"잠깐의 휴식이 필요할 때, {product_name}",
                f"함께 나누기 좋은 카페 메뉴",
                f"오늘의 여유를 채워주는 {product_name}",
            ]

        if category == "beauty":
            return [
                f"나를 위한 관리가 필요할 때, {product_name}",
                f"일상 속 자신감을 더하는 뷰티 케어",
                f"편안하게 시작하는 오늘의 관리 루틴",
            ]

        if category == "retail":
            return [
                f"생활에 꼭 필요한 실용적인 선택",
                f"가까운 곳에서 만나는 추천 상품, {product_name}",
                f"오늘의 일상을 더 편하게 만드는 아이템",
            ]

    # Naver
    if platform == "naver":
        if category == "restaurant":
            return [
                f"{product_name} 맛집 찾는다면 지금 확인하세요",
                f"든든한 한 끼가 필요할 때 추천하는 메뉴",
                f"음식점 인기 메뉴, {product_name}",
            ]

        if category == "cafe":
            return [
                f"카페 추천 메뉴, {product_name}",
                f"커피와 잘 어울리는 인기 메뉴",
                f"분위기 좋은 카페에서 즐기는 {product_name}",
            ]

        if category == "beauty":
            return [
                f"뷰티 관리가 필요할 때 추천하는 {product_name}",
                f"나에게 맞는 뷰티 케어를 찾고 있다면",
                f"관리 전후가 기대되는 뷰티 서비스",
            ]

        if category == "retail":
            return [
                f"소매점 추천 상품, {product_name}",
                f"실용적인 상품을 찾는다면 지금 확인하세요",
                f"일상에 필요한 아이템, {product_name}",
            ]

    # Offline Poster
    if platform == "offline":
        if category == "restaurant":
            return [
                f"오늘의 추천 메뉴! {product_name}",
                f"든든한 한 끼, 지금 바로 만나보세요",
                f"맛있는 시간이 시작되는 곳",
            ]

        if category == "cafe":
            return [
                f"오늘의 카페 메뉴, {product_name}",
                f"잠깐의 여유가 필요할 때",
                f"커피와 함께 즐겨보세요",
            ]

        if category == "beauty":
            return [
                f"오늘, 더 빛나는 나를 만나보세요",
                f"나를 위한 뷰티 케어 시작",
                f"지금 관리가 필요한 순간",
            ]

        if category == "retail":
            return [
                f"오늘의 추천 상품! {product_name}",
                f"지금 매장에서 만나보세요",
                f"일상을 바꾸는 작은 선택",
            ]

    return [
        f"오늘의 선택, {product_name}",
        f"지금 만나보는 특별한 {product_name}",
        f"고객의 시선을 사로잡는 {product_name}",
    ]