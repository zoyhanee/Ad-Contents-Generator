from app.schemas.strategy_schema import StrategyRecommendRequest


def recommend_strategy(request: StrategyRecommendRequest):
    product = request.product
    strategy = request.strategy

    product_name = product.name
    category = product.category or "상품"
    description = product.description or ""

    platform_text = ", ".join(strategy.platforms)

    if strategy.mode == "faster":
        return {
            "strategy_title": "트렌드 기반 맞춤 광고 전략",
            "strategy_description": (
                f"{product_name}의 상품 정보와 {platform_text} 플랫폼 특성을 바탕으로 "
                f"빠르게 활용할 수 있는 광고 방향을 추천했습니다."
            ),
            "slogans": [
                f"오늘의 선택, {product_name}",
                f"{description} 감성을 담은 {product_name}",
                f"{category} 고객을 위한 특별한 {product_name}",
            ],
        }

    goal_label = {
        "awareness": "브랜드 인지도",
        "sales": "판매 전환",
        "traffic": "방문 유도",
        "promotion": "프로모션 홍보",
    }.get(strategy.goal, "광고 효과 향상")

    style_label = {
        "warm": "따뜻한 감성",
        "modern": "모던하고 미니멀한",
        "vivid": "생동감 있는",
        "premium": "프리미엄한",
    }.get(strategy.style, "트렌디한")

    return {
        "strategy_title": f"{goal_label} 중심 광고 전략",
        "strategy_description": (
            f"{product_name}을 {style_label} 분위기로 표현하여 "
            f"{platform_text}에서 {goal_label}을 높이는 광고 방향을 추천했습니다."
        ),
        "slogans": [
            f"{style_label} 분위기로 전하는 {product_name}",
            f"{goal_label}을 위한 {product_name} 맞춤 메시지",
            f"고객의 시선을 사로잡는 {product_name}",
        ],
    }