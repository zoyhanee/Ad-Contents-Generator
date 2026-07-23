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


INDUSTRY_GUIDES = {
    "restaurant": (
        "상품 설명에 직접 포함된 메뉴 특징만 사용하세요. "
        "상품 설명에 없는 육즙, 불향, 그릴, 바삭함, 매운맛, "
        "치즈, 소스, 재료와 조리법을 추측하지 마세요. "
        "메뉴를 알아볼 수 없는 추상적인 감성 표현만 작성하지 마세요."
    ),
    "cafe": (
        "상품 설명에 직접 포함된 메뉴 종류, 재료, 향, 맛과 식감만 사용하세요. "
        "상품 설명에 없는 원두, 산미, 당도, 향과 토핑을 추측하지 마세요. "
        "오후, 휴식과 퇴근길 같은 상황 표현만으로 문장을 완성하지 마세요."
    ),
    "beauty": (
        "제품 유형과 상품 설명에 직접 포함된 성분, 제형, 사용감, "
        "사용 대상과 색상 등의 특징만 사용하세요. "
        "상품 설명에 없는 미백, 주름 개선, 진정, 재생과 치료 효과를 "
        "추측하거나 만들어내지 마세요. "
        "어떤 화장품에도 적용할 수 있는 추상적인 문구만 작성하지 마세요."
    ),
    "retail": (
        "상품 설명에 직접 포함된 제품 유형, 기능, 재질, 구성, "
        "사용 방법과 사용 상황만 사용하세요. "
        "상품 설명에 없는 성능, 내구성, 인증, 기능과 재질을 추측하지 마세요. "
        "어떤 상품에도 적용할 수 있는 추상적인 문구만 작성하지 마세요."
    ),
}


PLATFORM_GUIDES = {
    "instagram": (
        "이미지와 함께 보았을 때 상품의 특징이나 분위기가 떠오르는 "
        "짧고 감각적인 문장으로 작성하세요. "
        "긴 설명문과 과도한 해시태그는 사용하지 마세요. "
        "세 문장이 모두 같은 감성 표현으로 시작하지 않도록 작성하세요."
    ),
    "baemin": (
        "메뉴 특징을 빠르게 이해할 수 있고 주문이나 선택으로 이어질 수 있는 "
        "직접적인 문장으로 작성하세요. "
        "음식점이나 카페가 아닌 상품에는 음식과 배달 표현을 사용하지 마세요. "
        "모든 문장을 주문 유도 표현으로 끝내지 마세요."
    ),
    "naver": (
        "상품 설명에 포함된 실제 특징과 선택 이유를 명확하게 전달하세요. "
        "감성적인 표현만으로 문장을 완성하지 마세요. "
        "광고 문구처럼 자연스럽게 작성하되 설명문처럼 길게 작성하지 마세요."
    ),
    "offline": (
        "멀리서도 한눈에 읽을 수 있도록 짧고 명확하게 작성하세요. "
        "한 문장에는 상품명 또는 핵심 특징 하나를 중심적으로 전달하세요. "
        "해시태그는 사용하지 마세요."
    ),
}


GOAL_GUIDES = {
    "awareness": (
        "상품의 대표 특징과 인상이 소비자에게 기억될 수 있도록 작성하세요. "
        "구매를 직접 재촉하기보다 상품에 관심을 갖거나 새롭게 인식하게 하는 "
        "방향으로 표현하세요. "
        "세 문장이 동일한 인지도 표현을 반복할 필요는 없습니다."
    ),
    "sales": (
        "상품의 실제 특징과 소비자가 선택할 이유가 자연스럽게 연결되도록 "
        "작성하세요. 필요한 문장에서는 구매나 선택을 유도할 수 있지만, "
        "모든 문장에 같은 행동 유도 표현을 반복하지 마세요."
    ),
    "traffic": (
        "상품이나 서비스에 관심을 가진 소비자가 실제로 가능한 다음 접점으로 "
        "이어질 수 있도록 작성하세요. "
        "오프라인 매장이나 예약 정보가 확인되지 않았다면 방문, 예약과 상담을 "
        "임의로 만들어내지 마세요."
    ),
    "promotion": (
        "상품 정보에 실제 프로모션이 포함된 경우에만 할인, 이벤트, 증정, "
        "쿠폰과 한정 혜택을 강조하세요. "
        "프로모션 정보가 없다면 존재하지 않는 혜택을 만들지 말고 "
        "상품의 현재 특징과 관심 요소를 중심으로 작성하세요."
    ),
}


STYLE_GUIDES = {
    "warm": (
        "친근하고 편안한 어조와 부드러운 문장 흐름을 사용하세요. "
        "따뜻함, 포근함과 부드러움 같은 같은 계열의 단어를 "
        "세 문장에 반복하지 마세요. "
        "특정 스타일 단어를 직접 쓰지 않아도 문장 전체의 분위기로 표현할 수 있습니다."
    ),
    "modern": (
        "짧고 명확한 문장과 절제된 표현을 사용하세요. "
        "불필요한 수식어를 줄이고 정돈된 인상을 주세요. "
        "모던, 미니멀과 세련 같은 단어를 직접 반복하지 마세요."
    ),
    "vivid": (
        "생동감 있는 리듬과 선명한 인상을 주되 과장된 표현은 피하세요. "
        "같은 감탄 표현, 형용사와 강한 어조를 반복하지 마세요. "
        "과도한 느낌표는 사용하지 마세요."
    ),
    "premium": (
        "절제되고 차분한 어휘와 문장 흐름으로 고급스러운 인상을 주세요. "
        "프리미엄, 고급과 품격 같은 단어를 모든 문장에 직접 넣지 마세요. "
        "근거 없는 최고, 완벽과 업계 1위 등의 표현은 사용하지 마세요."
    ),
}


SLOGAN_LENGTH_GUIDES = {
    "instagram": {
        "first": 38,
        "others": 24,
        "guide": (
            "1번은 상품명을 포함해 공백 포함 38자 이내로 작성하세요. "
            "2번과 3번은 공백 포함 24자 이내로 작성하세요. "
            "이미지에 한두 줄로 배치할 수 있도록 핵심만 남기세요."
        ),
    },
    "baemin": {
        "first": 40,
        "others": 26,
        "guide": (
            "1번은 상품명을 포함해 공백 포함 40자 이내로 작성하세요. "
            "2번과 3번은 공백 포함 26자 이내로 작성하세요. "
            "메뉴 특징과 행동 유도를 짧고 빠르게 전달하세요."
        ),
    },
    "naver": {
        "first": 42,
        "others": 28,
        "guide": (
            "1번은 상품명을 포함해 공백 포함 42자 이내로 작성하세요. "
            "2번과 3번은 공백 포함 28자 이내로 작성하세요. "
            "핵심 특징은 유지하되 설명문처럼 길어지지 않게 작성하세요."
        ),
    },
    "offline": {
        "first": 34,
        "others": 18,
        "guide": (
            "1번은 상품명을 포함해 공백 포함 34자 이내로 작성하세요. "
            "2번과 3번은 공백 포함 18자 이내로 작성하세요. "
            "멀리서도 한눈에 읽히도록 가장 짧게 압축하세요."
        ),
    },
}


IMAGE_STYLE_GUIDES = {
    "warm": (
        "부드러운 조명, 편안한 배경, 자연스러운 소품과 따뜻한 분위기"
    ),
    "modern": (
        "정돈된 배경, 간결한 소품, 충분한 여백과 미니멀한 구도"
    ),
    "vivid": (
        "선명한 대비, 생동감 있는 구도와 활기찬 분위기"
    ),
    "premium": (
        "절제된 소품, 섬세한 조명, 고급스러운 재질감과 정돈된 구도"
    ),
}


def _label(
    mapping: dict[str, str],
    key: str | None,
) -> str:
    if not key:
        return "미지정"

    return mapping.get(key, key)


def _guide(
    mapping: dict[str, str],
    key: str | None,
    default: str,
) -> str:
    if not key:
        return default

    return mapping.get(key, default)


def _format_price(price) -> str:
    if price is None or price == "":
        return "미입력"

    if isinstance(price, int):
        return f"{price:,}원"

    return str(price)


def build_slogan_prompt(
    prompt_input: SloganPromptInput,
) -> str:
    product = prompt_input.product
    strategy = prompt_input.strategy

    product_name = str(product.name or "").strip()
    product_description = str(product.description or "").strip()

    industry_key = product.industry
    platform_key = strategy.platform
    goal_key = strategy.goal
    style_key = strategy.style

    industry = _label(
        INDUSTRY_LABELS,
        industry_key,
    )
    platform = _label(
        PLATFORM_LABELS,
        platform_key,
    )
    goal = _label(
        GOAL_LABELS,
        goal_key,
    )
    style = _label(
        STYLE_LABELS,
        style_key,
    )

    industry_guide = _guide(
        INDUSTRY_GUIDES,
        industry_key,
        (
            "상품 설명에 직접 포함된 제품 유형과 핵심 특징만 사용하세요. "
            "입력되지 않은 특징이나 효과를 추측하지 마세요."
        ),
    )

    platform_guide = _guide(
        PLATFORM_GUIDES,
        platform_key,
        (
            "해당 플랫폼에서 실제 광고로 사용할 수 있는 자연스러운 길이와 "
            "표현으로 작성하세요."
        ),
    )

    goal_guide = _guide(
        GOAL_GUIDES,
        goal_key,
        (
            "상품의 특징과 광고 목표가 문장 전체의 의미에서 자연스럽게 "
            "드러나도록 작성하세요."
        ),
    )

    style_guide = _guide(
        STYLE_GUIDES,
        style_key,
        (
            "선택한 분위기가 특정 단어의 반복이 아니라 문장의 어조, "
            "길이와 표현 방식에서 드러나도록 작성하세요."
        ),
    )

    length_rule = SLOGAN_LENGTH_GUIDES.get(
        platform_key,
        {
            "first": 40,
            "others": 26,
            "guide": (
                "1번은 상품명을 포함해 공백 포함 40자 이내로 작성하세요. "
                "2번과 3번은 공백 포함 26자 이내로 작성하세요. "
                "이미지에 한두 줄로 배치할 수 있도록 간결하게 작성하세요."
            ),
        },
    )
    length_guide = length_rule["guide"]

    custom_theme = ""
    if strategy.custom_theme:
        custom_theme = (
            f"\n추가 테마: "
            f"{str(strategy.custom_theme).strip()}"
        )

    return f"""
한국어 광고 슬로건을 정확히 3개 작성하세요.

[입력 정보]
상품명: {product_name}
상품 설명: {product_description or "상세 설명 없음"}
가격: {_format_price(product.price)}
업종: {industry}
플랫폼: {platform}
광고 목표: {goal}
광고 스타일: {style}{custom_theme}

[업종 작성 기준]
{industry_guide}

[플랫폼 작성 기준]
{platform_guide}

[광고 목표 작성 기준]
{goal_guide}

[광고 스타일 작성 기준]
{style_guide}

[이미지 배치용 길이 기준]
{length_guide}

[필수 규칙]
1. 1번 슬로건은 반드시 정확한 상품명 "{product_name}"으로 시작하세요.
2. 2번과 3번 슬로건에는 상품명 전체를 반복하지 않아도 됩니다.
3. 세 슬로건 모두 상품 설명에 실제로 포함된 특징이나 단어를
   최소 한 가지 이상 사용하세요.
4. 세 슬로건 모두 상품의 종류를 알아볼 수 있게 작성하세요.
5. 세 슬로건 전체에서 광고 목표가 분명하게 드러나야 합니다.
6. 각 슬로건은 광고 목표를 서로 다른 관점과 방식으로 표현하세요.
7. 선택한 광고 스타일은 특정 단어의 반복이 아니라
   문장의 어조, 리듬과 표현 방식에서 자연스럽게 드러나야 합니다.
8. 같은 형용사, 핵심 동사, 행동 유도 표현과 문장 끝맺음을
   두 문장 이상 반복하지 마세요.
9. 상품 설명에 없는 맛, 식감, 재료, 조리법, 성분, 기능,
   효능, 인증, 할인과 혜택을 새로 만들지 마세요.
10. 상품 설명에 없는 내용을 일반적인 상품 지식으로 추측하지 마세요.
11. 위의 플랫폼별 길이 기준을 반드시 지키세요.
12. 쉼표 뒤에 긴 설명을 이어 붙이지 말고, 한 문장에는 핵심 특징 하나만 강조하세요.
13. 세 슬로건은 시작 방식, 문장 구조와 핵심 아이디어가
    서로 분명하게 달라야 합니다.
14. 조사, 연결어와 미완성 표현으로 문장을 끝내지 마세요.
15. 상품 설명을 단순히 나열하거나 요약하지 말고
    실제 광고 문구처럼 자연스럽게 작성하세요.

[후보별 역할]
1번:
- 정확한 상품명 "{product_name}"으로 시작하세요.
- 대표 상품 특징을 가장 명확하게 전달하세요.
- 브랜드를 대표하는 문구처럼 작성하세요.

2번:
- 상품 설명에 포함된 특징을 사용하세요.
- 상품에서 느낄 수 있는 분위기, 인상 또는 경험을 중심으로 작성하세요.
- 1번과 다른 문장 구조와 어조를 사용하세요.
- 직접적인 행동 유도 표현은 필수가 아닙니다.

3번:
- 상품 설명에 포함된 특징을 사용하세요.
- 소비자의 관심이나 다음 행동을 자연스럽게 유도하세요.
- 1번과 2번에서 사용한 핵심 동사와 종결 표현을 반복하지 마세요.

[다양성 규칙]
- 세 문장을 같은 형용사로 시작하지 마세요.
- 같은 행동 유도 표현을 두 번 이상 사용하지 마세요.
- 같은 종결 표현을 두 번 이상 사용하지 마세요.
- 상품 특징은 유지하되 서로 다른 특징의 조합이나 관점으로 표현하세요.
- 문장마다 상품명, 상품 특징, 경험, 관심 유도의 비중을 다르게 구성하세요.

[출력 전 자체 확인]
- 1번 문장이 정확한 상품명 "{product_name}"으로 시작하는가?
- 세 문장 모두 실제 상품 특징에 근거하는가?
- 1번과 2·3번이 플랫폼별 글자 수 제한을 지켰는가?
- 세 문장이 서로 다른 관점과 문장 구조를 사용하는가?
- 같은 형용사, 동사, 행동 유도와 끝맺음이 반복되지 않는가?
- 세 문장 전체에서 광고 목표와 스타일이 자연스럽게 드러나는가?
- 입력되지 않은 사실을 추가하지 않았는가?

[출력 형식]
아래 형식을 정확히 지키고 번호와 슬로건 외에는 출력하지 마세요.

1. {product_name} ...
2. ...
3. ...
""".strip()


def build_image_prompt(
    prompt_input: ImagePromptInput,
) -> str:
    product = prompt_input.product
    strategy = prompt_input.strategy

    product_name = str(product.name or "").strip()
    product_description = str(product.description or "").strip()
    selected_slogan = str(
        prompt_input.selected_slogan or ""
    ).strip()

    industry_key = product.industry
    platform_key = strategy.platform
    goal_key = strategy.goal
    style_key = strategy.style

    industry = _label(
        INDUSTRY_LABELS,
        industry_key,
    )
    platform = _label(
        PLATFORM_LABELS,
        platform_key,
    )
    goal = _label(
        GOAL_LABELS,
        goal_key,
    )
    style = _label(
        STYLE_LABELS,
        style_key,
    )

    image_style_guide = _guide(
        IMAGE_STYLE_GUIDES,
        style_key,
        (
            "상품이 분명하게 보이고 선택한 광고 분위기가 "
            "배경과 조명에 자연스럽게 드러나는 구성"
        ),
    )

    poster_size = ""
    if (
        platform_key == "offline"
        and strategy.poster_size
    ):
        poster_size = (
            f"\n포스터 규격: "
            f"{str(strategy.poster_size).upper()}"
        )

    custom_theme = ""
    if strategy.custom_theme:
        custom_theme = (
            f"\n추가 테마: "
            f"{str(strategy.custom_theme).strip()}"
        )

    return f"""
이미지 생성 모델에 전달할 광고 이미지 프롬프트를 하나 작성하세요.

[상품 정보]
상품명: {product_name}
상품 설명: {product_description or "상세 설명 없음"}
가격: {_format_price(product.price)}
업종: {industry}

[광고 설정]
플랫폼: {platform}
광고 목표: {goal}
시각적 스타일: {style}
선택 슬로건: {selected_slogan}{poster_size}{custom_theme}

[시각적 스타일 방향]
{image_style_guide}

[필수 조건]
1. 원본 상품 이미지가 제공되었다면 상품의 형태, 색상,
   패키지와 주요 외형을 유지하세요.
2. 상품이 이미지의 중심에 분명하게 보이도록 구성하세요.
3. 상품 설명에 실제로 포함된 특징만 배경, 소품,
   조명 또는 사용 장면에 반영하세요.
4. 상품 설명에 없는 재료, 성분, 기능, 효능,
   구성품과 사용 방식을 추가하지 마세요.
5. 음식 상품에는 상품 설명에 없는 조리법, 소스,
   재료와 식감을 새로 만들지 마세요.
6. 뷰티 상품은 음식처럼 표현하지 말고 제품 유형,
   제형과 실제 사용 방식에 맞게 구성하세요.
7. 소매 상품은 실제 크기와 사용 방식을 왜곡하지 마세요.
8. 선택 슬로건의 의미와 이미지의 장면이 자연스럽게 연결되어야 합니다.
9. 광고 문구를 배치할 수 있도록 충분하고 깨끗한 여백을 확보하세요.
10. 상품 위에 글자, 장식 또는 다른 물체가 겹치지 않도록 구성하세요.
11. 이미지 안에 상품명이나 슬로건 글자를 직접 생성하지 마세요.
12. 플랫폼에 적합한 화면 비율과 정보 밀도를 고려하세요.
13. 소상공인이 실제 광고물로 사용할 수 있는 완성도 높은 이미지로 구성하세요.

[출력 조건]
- 이미지 생성 모델에 바로 전달할 하나의 구체적인 프롬프트만 출력하세요.
- 제목, 번호, 설명, 분석과 작성 이유는 출력하지 마세요.
""".strip()