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

    industry = _label(INDUSTRY_LABELS, industry_key)
    platform = _label(PLATFORM_LABELS, platform_key)
    goal = _label(GOAL_LABELS, goal_key)
    style = _label(STYLE_LABELS, style_key)

    image_style_guide = _guide(
        IMAGE_STYLE_GUIDES,
        style_key,
        (
            "상품이 분명하게 보이고 선택한 광고 분위기가 "
            "배경과 조명에 자연스럽게 드러나는 구성"
        ),
    )

    poster_size = "해당 없음"
    if platform_key == "offline" and strategy.poster_size:
        poster_size = str(strategy.poster_size).upper()

    custom_theme = (
        str(strategy.custom_theme).strip()
        if strategy.custom_theme
        else ""
    )

    platform_composition_guides = {
        "instagram": (
            "세로형 또는 정사각형 소셜 광고 구도. 상품을 중심보다 약간 아래에 두고, "
            "상단이나 측면에 슬로건 배치를 위한 깨끗한 여백을 확보하세요."
        ),
        "baemin": (
            "모바일 화면에서 상품이 즉시 보이도록 중앙 중심의 밀도 높은 구도. "
            "상품 크기를 충분히 크게 유지하고 핵심 장면을 단순하게 구성하세요."
        ),
        "naver": (
            "상품 정보 전달에 적합한 정돈된 상업 광고 구도. "
            "상품과 배경을 명확히 분리하고 텍스트 영역을 안정적으로 확보하세요."
        ),
        "offline": (
            f"멀리서도 상품이 한눈에 보이는 강한 중심 구도. "
            f"포스터 규격은 {poster_size}이며, 큰 문구 배치를 위한 넓은 여백을 확보하세요."
        ),
    }
    platform_composition = platform_composition_guides.get(
        platform_key,
        (
            "상품이 명확하게 보이는 상업 광고 구도와 "
            "슬로건 배치를 위한 충분한 여백을 확보하세요."
        ),
    )

    industry_environment_guides = {
        "restaurant": (
            "상품 설명에 직접 언급된 메뉴 특징만 활용한 자연스러운 음식 광고 배경. "
            "설명에 없는 재료, 소스, 조리 도구와 곁들임 메뉴는 추가하지 마세요."
        ),
        "cafe": (
            "상품 설명에 직접 언급된 음료 또는 디저트 특성에 맞는 카페 광고 환경. "
            "설명에 없는 원두, 토핑, 재료와 장식은 추가하지 마세요."
        ),
        "beauty": (
            "제품 유형과 실제 사용 방식에 맞는 깨끗하고 정돈된 뷰티 광고 환경. "
            "음식처럼 표현하거나 설명에 없는 성분, 꽃, 과일과 효능 상징물을 추가하지 마세요."
        ),
        "retail": (
            "제품의 실제 크기, 기능과 사용 방식에 맞는 현실적인 상업 광고 환경. "
            "설명에 없는 구성품, 기능과 사용 장면을 만들어내지 마세요."
        ),
    }
    environment_guide = industry_environment_guides.get(
        industry_key,
        (
            "상품 설명에 직접 포함된 특징과 사용 방식만 반영한 현실적인 광고 환경. "
            "입력되지 않은 소품, 기능과 사용 장면을 임의로 추가하지 마세요."
        ),
    )

    text_instruction = (
        f'선택 슬로건 "{selected_slogan}"의 의미가 장면과 연결되도록 구성하되, '
        "이미지 모델이 글자를 직접 생성하지 않도록 하세요. "
        "슬로건은 후편집으로 삽입할 수 있게 깨끗하고 대비가 충분한 여백만 확보하세요."
        if selected_slogan
        else (
            "이미지 안에 문구를 직접 생성하지 말고, "
            "후편집용 텍스트 영역으로 사용할 깨끗한 여백을 확보하세요."
        )
    )

    custom_theme_line = (
        f"\n추가 테마: {custom_theme}"
        if custom_theme
        else ""
    )

    return f"""
원본 상품 이미지를 활용한 완성도 높은 광고 이미지를 생성하세요.

[PRODUCT INFORMATION]
상품명: {product_name}
상품 설명: {product_description or "상세 설명 없음"}
가격: {_format_price(product.price)}
업종: {industry}

[PRODUCT PRESERVATION]
- 원본 상품의 형태, 색상, 로고, 패키지, 라벨, 재질감과 비율을 변경하지 마세요.
- 원본 상품의 주요 외형과 식별 가능한 특징을 정확히 유지하세요.
- 상품을 다시 디자인하거나 다른 상품처럼 재해석하지 마세요.
- 로고와 패키지 문구를 임의로 수정, 대체 또는 새로 생성하지 마세요.

[CREATIVE OBJECTIVE]
이번 시안의 광고 목적: {goal}
- 선택한 광고 목적이 배경, 구도, 조명과 전체 분위기에서 자연스럽게 드러나야 합니다.
- 상품 설명에 없는 혜택, 할인, 효능과 성능을 광고 목적으로 새로 만들지 마세요.
- 선택 슬로건의 핵심 의미와 시각적 장면이 서로 어긋나지 않게 구성하세요.

[COMPOSITION]
- 제품 위치: 광고의 주인공으로 분명하게 보이는 중심 영역에 배치하세요.
- 제품 크기: 모바일 또는 포스터에서 상품을 즉시 알아볼 수 있을 만큼 충분히 크게 표현하세요.
- 카메라 앵글: 원본 상품의 형태와 비율이 왜곡되지 않는 자연스러운 광고 촬영 각도를 사용하세요.
- 여백: 상품을 가리지 않는 위치에 슬로건 후편집용 여백을 확보하세요.
- 플랫폼별 구성: {platform_composition}
- 상품 위에 글자, 장식, 손, 소품 또는 다른 물체가 겹치지 않도록 하세요.

[ENVIRONMENT]
- 배경: 상품과 명확히 구분되면서 선택한 스타일을 보조하는 현실적인 광고 배경을 사용하세요.
- 소품: 상품 설명과 업종에 직접 관련된 최소한의 소품만 사용하세요.
- 사용 장면: 실제 상품 유형과 사용 방식에 맞는 경우에만 표현하세요.
- 업종별 환경 기준: {environment_guide}{custom_theme_line}

[LIGHTING]
- 광원: 상품의 실제 색상, 로고와 재질이 정확하게 보이는 상업 광고용 조명을 사용하세요.
- 명암: 상품 윤곽이 배경과 분명하게 분리되도록 자연스러운 대비를 적용하세요.
- 분위기: {image_style_guide}
- 과도한 반사, 색 번짐, 강한 그림자로 상품 정보가 가려지지 않게 하세요.

[STYLE]
선택한 광고 스타일: {style}
- 스타일은 상품 자체를 변형하지 말고 배경, 조명, 소품과 구도에만 반영하세요.
- 선택 스타일을 상징하는 요소를 과도하게 반복하거나 장면을 비현실적으로 만들지 마세요.

[PLATFORM]
광고 플랫폼: {platform}
포스터 규격: {poster_size}
- 해당 플랫폼의 일반적인 화면 비율, 가독성과 정보 밀도를 고려하세요.
- 상품이 작은 썸네일에서도 식별될 수 있도록 핵심 시각 요소를 단순하고 명확하게 유지하세요.

[TEXT]
선택 슬로건: {selected_slogan or "미선택"}
- {text_instruction}
- 읽을 수 없는 글자, 임의의 문구, 워터마크와 가짜 브랜드명을 생성하지 마세요.

[NEGATIVE CONSTRAINTS]
- 상품 형태, 색상, 로고, 패키지, 라벨과 비율 변형 금지
- 가짜 로고, 가짜 브랜드명, 임의의 패키지 문구 생성 금지
- 동일 상품 또는 다른 추가 제품 생성 금지
- 상품 설명에 없는 재료, 성분, 기능, 효능, 구성품과 사용 방식 추가 금지
- 상품 일부 잘림, 찌그러짐, 녹아내림, 중복, 비대칭과 비현실적 크기 금지
- 손가락 오류, 부자연스러운 손, 상품을 가리는 인물과 소품 금지
- 읽을 수 없는 텍스트, 깨진 글자, 임의의 숫자, 워터마크 생성 금지
- 과도한 장식, 복잡한 배경과 상품보다 눈에 띄는 소품 금지

[OUTPUT CONDITION]
- 이미지 생성 모델에 바로 전달할 하나의 구체적인 광고 이미지 프롬프트만 출력하세요.
- 제목, 번호, 분석, 설명과 작성 이유를 추가로 출력하지 마세요.
""".strip()