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
    style: Optional[str],
):
    # 1. 업종 + 목표 + 스타일 기준으로 자연스러운 문장 생성
    slogans = _get_natural_slogans(
        product_name=product_name,
        category=category,
        goal=goal,
        style=style,
    )

    # 2. 플랫폼 특성은 마지막에 살짝만 반영
    slogans = _adapt_to_platform(
        slogans=slogans,
        platform=platform,
    )

    return slogans


def _get_natural_slogans(
    product_name: str,
    category: str,
    goal: str,
    style: Optional[str],
):
    if style is None:
        return _get_fast_recommend_slogans(
            product_name=product_name,
            category=category,
        )

    if category == "restaurant":
        return _restaurant_slogans(
            product_name=product_name,
            goal=goal,
            style=style,
        )

    if category == "cafe":
        return _cafe_slogans(
            product_name=product_name,
            goal=goal,
            style=style,
        )

    if category == "beauty":
        return _beauty_slogans(
            product_name=product_name,
            goal=goal,
            style=style,
        )

    if category == "retail":
        return _retail_slogans(
            product_name=product_name,
            goal=goal,
            style=style,
        )

    return [
        f"오늘 만나보는 {product_name}",
        f"{product_name}로 완성하는 특별한 순간",
        f"지금 선택하기 좋은 {product_name}",
    ]


def _get_fast_recommend_slogans(
    product_name: str,
    category: str,
):
    if category == "restaurant":
        return [
            f"오늘 한 끼는 {product_name}",
            "맛있게 채우는 든든한 식사",
            "한 번 보면 떠오르는 인기 메뉴",
        ]

    if category == "cafe":
        return [
            f"오늘의 여유를 더하는 {product_name}",
            "커피와 함께 즐기기 좋은 순간",
            "가볍게 들러도 기분 좋아지는 메뉴",
        ]

    if category == "beauty":
        return [
            f"나를 위한 관리, {product_name}",
            "오늘 더 빛나는 변화를 시작하세요",
            "가볍게 시작하는 뷰티 케어",
        ]

    if category == "retail":
        return [
            f"일상에 더하는 {product_name}",
            "취향을 보여주는 감각적인 선택",
            "오늘 발견하기 좋은 추천 아이템",
        ]

    return [
        f"오늘의 선택, {product_name}",
        f"지금 만나보는 {product_name}",
        "한눈에 기억되는 특별한 상품",
    ]


def _restaurant_slogans(
    product_name: str,
    goal: str,
    style: str,
):
    templates = {
        "awareness": {
            "warm": [
                f"오늘 저녁, 따뜻한 한 끼가 필요할 때",
                f"{product_name}로 채우는 든든한 식사",
                "마음까지 편안해지는 맛있는 순간",
            ],
            "modern": [
                "깔끔하게 완성한 한 접시",
                f"{product_name}의 깊은 맛을 담다",
                "불필요함 없이 맛에 집중한 메뉴",
            ],
            "vivid": [
                "한 입에 퍼지는 진한 풍미",
                f"오늘은 {product_name}로 든든하게",
                "눈길을 사로잡는 맛있는 한 접시",
            ],
            "premium": [
                "정성스럽게 완성한 프리미엄 한 접시",
                f"{product_name}의 깊은 맛을 경험하세요",
                "특별한 식사를 위한 품격 있는 선택",
            ],
        },
        "sales": {
            "warm": [
                f"오늘 식사는 {product_name}로 따뜻하게",
                "고민 없이 주문하기 좋은 든든한 메뉴",
                "맛있는 한 끼가 필요한 순간에",
            ],
            "modern": [
                f"오늘의 메뉴 선택, {product_name}",
                "간결하게 즐기는 든든한 한 끼",
                "맛과 만족을 모두 담은 선택",
            ],
            "vivid": [
                f"지금 먹고 싶은 맛, {product_name}",
                "한 입부터 기분 좋아지는 메뉴",
                "오늘의 식욕을 깨우는 한 접시",
            ],
            "premium": [
                f"제대로 즐기는 {product_name}",
                "한 끼의 만족을 높이는 프리미엄 메뉴",
                "특별한 식사를 위한 오늘의 선택",
            ],
        },
        "traffic": {
            "warm": [
                "가까운 곳에서 만나는 따뜻한 한 끼",
                f"매장에서 더 맛있게 즐기는 {product_name}",
                "편안하게 들러 든든하게 채우세요",
            ],
            "modern": [
                "오늘 들르기 좋은 깔끔한 식사 공간",
                f"매장에서 직접 만나는 {product_name}",
                "가볍게 방문해 만족스럽게 즐기세요",
            ],
            "vivid": [
                "지금 바로 맛보고 싶은 한 접시",
                f"매장에서 생생하게 즐기는 {product_name}",
                "오늘의 방문을 맛있게 만드는 메뉴",
            ],
            "premium": [
                "공간에서 더 깊게 느껴지는 맛",
                f"매장에서 완성되는 {product_name}의 매력",
                "특별한 식사를 위해 방문해보세요",
            ],
        },
        "promotion": {
            "warm": [
                f"{product_name}를 더 기분 좋게 만나는 혜택",
                "따뜻한 한 끼에 특별함을 더하세요",
                "오늘의 식사를 더 알차게 즐기는 방법",
            ],
            "modern": [
                f"{product_name}를 합리적으로 즐기는 기회",
                "깔끔하게 준비한 오늘의 혜택",
                "필요한 순간에 딱 맞는 프로모션",
            ],
            "vivid": [
                f"놓치기 아쉬운 {product_name} 혜택",
                "맛있는 순간을 더 활기차게",
                "오늘 더 즐겁게 만나는 특별 이벤트",
            ],
            "premium": [
                f"{product_name}를 특별하게 즐기는 혜택",
                "프리미엄 한 끼에 더해진 가치",
                "오늘만 더 특별한 식사 경험",
            ],
        },
    }

    return _select_templates(templates, goal, style)


def _cafe_slogans(
    product_name: str,
    goal: str,
    style: str,
):
    templates = {
        "awareness": {
            "warm": [
                f"따뜻한 하루를 채우는 {product_name}",
                "커피와 함께 머물고 싶은 순간",
                "편안한 여유가 필요한 날에",
            ],
            "modern": [
                f"감각적으로 즐기는 {product_name}",
                "깔끔한 공간에 어울리는 카페 메뉴",
                "오늘의 여유를 단정하게 채우다",
            ],
            "vivid": [
                f"기분 좋은 하루를 여는 {product_name}",
                "달콤하게 살아나는 카페의 순간",
                "한 입으로 분위기가 달라지는 메뉴",
            ],
            "premium": [
                f"프리미엄한 여유를 담은 {product_name}",
                "커피와 함께 완성되는 특별한 시간",
                "작은 순간까지 고급스럽게 채우다",
            ],
        },
        "sales": {
            "warm": [
                f"오늘 카페 메뉴는 {product_name}",
                "커피와 함께 즐기기 좋은 따뜻한 선택",
                "잠깐의 여유를 맛있게 채우세요",
            ],
            "modern": [
                f"깔끔하게 즐기는 {product_name}",
                "커피 한 잔과 잘 어울리는 메뉴",
                "간결하지만 만족스러운 카페 선택",
            ],
            "vivid": [
                f"지금 먹기 좋은 {product_name}",
                "달콤한 기분을 더하는 오늘의 메뉴",
                "한 입에 살아나는 카페의 즐거움",
            ],
            "premium": [
                f"특별하게 즐기는 {product_name}",
                "커피와 함께 완성되는 프리미엄 메뉴",
                "오늘의 여유를 더 고급스럽게",
            ],
        },
        "traffic": {
            "warm": [
                "잠깐 쉬어가고 싶은 날",
                f"매장에서 더 맛있게 즐기는 {product_name}",
                "따뜻한 공간에서 만나는 카페 메뉴",
            ],
            "modern": [
                "오늘 들르기 좋은 감각적인 카페",
                f"공간과 함께 즐기는 {product_name}",
                "깔끔한 여유가 필요한 순간에",
            ],
            "vivid": [
                "기분 전환이 필요한 순간",
                f"매장에서 생생하게 즐기는 {product_name}",
                "오늘의 카페 코스로 추천해요",
            ],
            "premium": [
                "조금 더 특별한 카페 시간을 위해",
                f"매장에서 완성되는 {product_name}의 매력",
                "여유로운 공간에서 즐기는 프리미엄 메뉴",
            ],
        },
        "promotion": {
            "warm": [
                f"{product_name}와 함께하는 따뜻한 혜택",
                "오늘의 카페 시간을 더 알차게",
                "기분 좋은 여유에 특별함을 더하세요",
            ],
            "modern": [
                f"{product_name}를 합리적으로 즐기는 방법",
                "깔끔하게 준비한 카페 프로모션",
                "오늘의 선택을 더 가볍게",
            ],
            "vivid": [
                f"놓치기 아쉬운 {product_name} 혜택",
                "달콤한 시간을 더 즐겁게",
                "오늘 더 기분 좋아지는 카페 이벤트",
            ],
            "premium": [
                f"{product_name}를 특별하게 즐기는 혜택",
                "프리미엄 카페 타임을 위한 이벤트",
                "오늘의 여유를 더 가치 있게",
            ],
        },
    }

    return _select_templates(templates, goal, style)


def _beauty_slogans(
    product_name: str,
    goal: str,
    style: str,
):
    templates = {
        "awareness": {
            "warm": [
                f"나를 아끼는 시간, {product_name}",
                "오늘의 나를 부드럽게 가꾸는 케어",
                "편안하게 시작하는 아름다운 변화",
            ],
            "modern": [
                f"깔끔하게 완성하는 {product_name}",
                "불필요함 없이 나에게 집중하는 관리",
                "오늘의 변화를 단정하게 시작하세요",
            ],
            "vivid": [
                f"오늘 더 빛나는 나를 위한 {product_name}",
                "생기 있는 변화를 만드는 뷰티 케어",
                "기분까지 달라지는 관리의 순간",
            ],
            "premium": [
                f"나를 위한 프리미엄 케어, {product_name}",
                "아름다움을 더 섬세하게 완성하는 시간",
                "특별한 변화를 위한 고급스러운 선택",
            ],
        },
        "sales": {
            "warm": [
                f"지금 시작하는 나를 위한 {product_name}",
                "부담 없이 예약하기 좋은 뷰티 케어",
                "오늘의 나에게 선물하는 관리",
            ],
            "modern": [
                f"필요한 관리만 깔끔하게, {product_name}",
                "간결하게 시작하는 뷰티 루틴",
                "나에게 맞는 변화를 지금 선택하세요",
            ],
            "vivid": [
                f"변화가 기대되는 {product_name}",
                "오늘 예약하고 싶은 생기 있는 케어",
                "나를 더 빛나게 하는 선택",
            ],
            "premium": [
                f"프리미엄 관리로 만나는 {product_name}",
                "나에게 투자하는 특별한 시간",
                "아름다움을 높이는 가치 있는 선택",
            ],
        },
        "traffic": {
            "warm": [
                "오늘, 나를 위한 관리 시간을 가져보세요",
                f"가까운 곳에서 만나는 {product_name}",
                "편안하게 방문해 시작하는 뷰티 케어",
            ],
            "modern": [
                "가볍게 방문해 깔끔하게 관리하세요",
                f"매장에서 직접 경험하는 {product_name}",
                "오늘의 루틴을 단정하게 바꾸는 시간",
            ],
            "vivid": [
                "지금 방문하고 싶은 뷰티 케어",
                f"현장에서 더 생생하게 느끼는 {product_name}",
                "관리받고 싶은 날, 바로 시작하세요",
            ],
            "premium": [
                "공간에서 완성되는 프리미엄 케어",
                f"직접 경험하는 {product_name}의 차이",
                "특별한 관리를 위해 방문해보세요",
            ],
        },
        "promotion": {
            "warm": [
                f"{product_name}를 더 기분 좋게 만나는 혜택",
                "나를 위한 관리에 특별함을 더하세요",
                "오늘의 아름다움을 더 알차게 시작하세요",
            ],
            "modern": [
                f"{product_name}를 합리적으로 시작하는 기회",
                "깔끔하게 준비한 뷰티 프로모션",
                "필요한 관리에 혜택을 더하세요",
            ],
            "vivid": [
                f"놓치기 아쉬운 {product_name} 혜택",
                "오늘 더 빛나는 나를 위한 이벤트",
                "생기 있는 변화를 위한 특별 프로모션",
            ],
            "premium": [
                f"{product_name}를 특별하게 만나는 혜택",
                "프리미엄 관리에 더해진 가치",
                "나를 위한 고급스러운 이벤트",
            ],
        },
    }

    return _select_templates(templates, goal, style)


def _retail_slogans(
    product_name: str,
    goal: str,
    style: str,
):
    templates = {
        "awareness": {
            "warm": [
                f"일상에 따뜻함을 더하는 {product_name}",
                "매일 쓰고 싶은 편안한 선택",
                "취향을 부드럽게 보여주는 아이템",
            ],
            "modern": [
                f"깔끔한 일상을 위한 {product_name}",
                "불필요함 없이 감각을 담은 아이템",
                "오늘의 공간과 잘 어울리는 선택",
            ],
            "vivid": [
                f"일상에 활기를 더하는 {product_name}",
                "눈길을 사로잡는 감각적인 아이템",
                "기분 좋은 변화를 만드는 선택",
            ],
            "premium": [
                f"가치를 더하는 프리미엄 아이템, {product_name}",
                "취향을 고급스럽게 완성하는 선택",
                "일상 속 특별함을 만드는 상품",
            ],
        },
        "sales": {
            "warm": [
                f"오늘 장바구니에 담고 싶은 {product_name}",
                "일상에 편안하게 스며드는 추천 아이템",
                "부담 없이 선택하기 좋은 상품",
            ],
            "modern": [
                f"필요한 순간에 딱 맞는 {product_name}",
                "깔끔하게 고르는 오늘의 아이템",
                "실용성과 감각을 모두 담은 선택",
            ],
            "vivid": [
                f"지금 눈길이 가는 {product_name}",
                "일상에 기분 좋은 포인트를 더하세요",
                "오늘 바로 만나보고 싶은 아이템",
            ],
            "premium": [
                f"특별하게 고르는 {product_name}",
                "가치를 아는 사람을 위한 추천 상품",
                "일상에 품격을 더하는 선택",
            ],
        },
        "traffic": {
            "warm": [
                "매장에서 직접 만나보는 편안한 선택",
                f"가까운 곳에서 확인하는 {product_name}",
                "오늘 들러 천천히 살펴보세요",
            ],
            "modern": [
                "직접 보고 고르는 깔끔한 아이템",
                f"매장에서 확인하는 {product_name}",
                "오늘의 취향을 단정하게 완성하세요",
            ],
            "vivid": [
                "매장에서 더 생생하게 만나는 상품",
                f"직접 보면 더 끌리는 {product_name}",
                "오늘 들러 새로운 취향을 발견하세요",
            ],
            "premium": [
                "직접 확인할수록 느껴지는 가치",
                f"매장에서 경험하는 {product_name}",
                "특별한 선택을 위해 방문해보세요",
            ],
        },
        "promotion": {
            "warm": [
                f"{product_name}를 더 기분 좋게 만나는 혜택",
                "일상에 필요한 상품을 더 알차게",
                "오늘의 선택에 특별함을 더하세요",
            ],
            "modern": [
                f"{product_name}를 합리적으로 만나는 기회",
                "깔끔하게 준비한 오늘의 프로모션",
                "필요한 아이템에 혜택을 더하세요",
            ],
            "vivid": [
                f"놓치기 아쉬운 {product_name} 혜택",
                "기분 좋은 쇼핑을 위한 특별 이벤트",
                "오늘 더 즐겁게 만나는 추천 상품",
            ],
            "premium": [
                f"{product_name}를 특별하게 만나는 혜택",
                "프리미엄한 선택에 더해진 가치",
                "오늘의 쇼핑을 더 고급스럽게",
            ],
        },
    }

    return _select_templates(templates, goal, style)


def _select_templates(
    templates: dict,
    goal: str,
    style: str,
):
    goal_templates = templates.get(goal)

    if goal_templates is None:
        goal_templates = templates.get("awareness", {})

    style_templates = goal_templates.get(style)

    if style_templates is None:
        style_templates = goal_templates.get("warm")

    if style_templates is None:
        return [
            "오늘 만나보는 특별한 선택",
            "지금 확인하기 좋은 추천 상품",
            "한눈에 기억되는 매력적인 순간",
        ]

    return style_templates


def _adapt_to_platform(
    slogans: List[str],
    platform: str,
):
    if platform == "instagram":
        return [
            f"피드에 남기고 싶은 {slogans[0]}",
            slogans[1],
            f"오늘 공유하고 싶은 {slogans[2]}",
        ]

    if platform == "baemin":
        return [
            f"지금 주문하기 좋은 {slogans[0]}",
            slogans[1],
            f"배달로 편하게 즐기는 {slogans[2]}",
        ]

    if platform == "naver":
        return [
            f"찾고 있다면 확인해볼 {slogans[0]}",
            slogans[1],
            f"선택 전에 살펴보기 좋은 {slogans[2]}",
        ]

    if platform == "offline":
        return [
            f"오늘의 추천, {slogans[0]}",
            slogans[1],
            f"매장에서 직접 만나는 {slogans[2]}",
        ]

    return slogans