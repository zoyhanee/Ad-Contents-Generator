import base64
import random
from typing import Literal, Optional

from openai import OpenAI
from pydantic import BaseModel, Field

from app.core.config import settings

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client

CREATIVE_ANGLES = [
    "타이포그래피 중심 — 큰 글씨가 레이아웃의 주인공, 제품은 상대적으로 작게 배치",
    "제품 히어로형 — 제품을 최대한 크게 보여주고, 텍스트는 최소한으로 절제",
    "그리드/구조형 — 격자와 구분선을 적극 활용한 정보 중심 레이아웃",
    "여백 극대화형 — 요소 수를 줄이고 네거티브 스페이스로 고급스러움을 표현",
    "비대칭 다이나믹형 — 정중앙/균등 그리드를 피하고 의도적으로 비대칭 배치",
    "매거진 히어로형 — 상업 잡지 광고처럼 강렬한 첫인상을 주는 접근. 제품을 당당하게 "
    "선보이되, 정보는 시각적으로 정돈된 리듬감 있게 배치",
    "그래픽 임팩트형 — 스트리트/드롭 컬처 포스터처럼 대담한 타이포와 강렬한 그래픽"
    "요소(붓터치, 잉크 스플래시, 기하학적 도형 등)로 시선을 압도하는 접근. 설명적인 "
    "문구 없이 짧고 굵은 슬로건 + 상품이 화면을 지배하는 구도.",
]

CREATIVE_ANGLE_MOOD_KEYWORDS = {
    CREATIVE_ANGLES[0]: "bold graphic minimalism, flat high-contrast color field in deep charcoal or ink-black, editorial poster energy, crisp confident tone",
    CREATIVE_ANGLES[1]: "cinematic product stage, dramatic single-source spotlight, deep navy or espresso-brown backdrop, glossy premium sheen",
    CREATIVE_ANGLES[2]: "architectural structured composition, cool slate-gray museum-gallery lighting, precise geometric surface texture",
    CREATIVE_ANGLES[3]: "vast quiet negative space, soft diffused ambient daylight, pale warm cream or soft blush tone, understated tonal minimalism",
    CREATIVE_ANGLES[4]: "dynamic off-center energy, dramatic raking light with long soft shadow over a deep teal or graphite backdrop, unexpected subtle color accent",
    CREATIVE_ANGLES[5]: "warm terracotta or amber gradient, gentle diagonal light streak across the surface, magazine-cover glamour, tactile depth",
    CREATIVE_ANGLES[6]: "explosive graphic paint-splash background art, bold saturated neon or acid colors (magenta, cyan, electric yellow) against a deep dark base, energetic street-culture poster energy, hand-drawn ink-splatter and geometric shard accents, high-contrast graphic illustration style rather than photorealistic",
}

CREATIVE_ANGLE_TEXT_BUDGET = {
    CREATIVE_ANGLES[0]: "subheadline은 있어도 되지만 짧게, features는 0~2개",
    CREATIVE_ANGLES[1]: "subheadline은 생략을 우선 고려, features는 0~1개만 (제품이 스스로 말하게 두세요)",
    CREATIVE_ANGLES[2]: "subheadline 포함, features는 3~5개 (정보 구조가 핵심이므로 충분히)",
    CREATIVE_ANGLES[3]: "subheadline은 생략 또는 1줄, features는 0개 (여백이 핵심이므로 텍스트를 적극적으로 줄이세요)",
    CREATIVE_ANGLES[4]: "subheadline은 짧게, features는 0~2개",
    CREATIVE_ANGLES[5]: "subheadline 포함, features는 2~4개, 배치 방식(가로/세로)은 상품에 맞게 자유 결정",
    CREATIVE_ANGLES[6]: "subheadline은 아주 짧은 한 줄이거나 생략, features는 0개 (설명 문구 없이 "
                        "임팩트만으로 승부 - headline에 outline_color로 대비되는 굵은 외곽선을 "
                        "적극 활용하세요)",
}

# 장면 유형 다양성 - 상품과 안 어울리면 GPT가 무시해도 됨.
SCENE_TYPES = [
    "studio", "outdoor_natural_light", "kitchen_or_cafe_lifestyle",
    "workspace_or_office", "home_interior", "architectural_minimal",
]

# 배경 색 계열은 무작위로 하나를 뽑아 강제 주입한다 (매번 다른 팔레트로 결과 다양성 확보).
BACKGROUND_COLOR_PALETTES = [
    "deep charcoal black with subtle graphite texture",
    "warm terracotta and burnt orange gradient",
    "cool slate blue with a hint of steel gray",
    "deep forest green with muted olive undertones",
    "dusty rose pink with soft mauve shadows",
    "rich espresso brown with warm amber highlights",
    "navy blue with a faint midnight indigo gradient",
    "muted mustard yellow with soft ochre texture",
    "warm cream and pale sand tone",  # 이것만 베이지 계열 - 무작위로 뽑힐 때만 허용
]

# 구도(레이아웃) 패턴도 색과 마찬가지로 코드 레벨에서 무작위 강제 주입한다.
LAYOUT_FAMILIES = {
    "hero_left_copy_right": (
        "상품을 화면 왼쪽 40~55% 영역에 최대한 크게 배치(product_box.x는 0.0~0.05 근처, "
        "width는 0.45~0.55). 헤드라인/서브헤드/features는 전부 오른쪽 절반에 세로로 배치."
    ),
    "copy_top_product_bottom": (
        "상단 25~35%는 텍스트(헤드라인+서브헤드) 전용 영역으로 비워두고, 상품은 화면 "
        "하단 중앙에 크게 배치(product_box.y는 0.4 이상). features가 있다면 상품 좌우 "
        "여백에 나눠 배치."
    ),
    "full_bleed_center_hero": (
        "상품을 화면 정중앙에 가능한 가장 크게 배치(product_box: x/y 대략 0.15~0.25, "
        "width/height 0.5~0.7). 텍스트는 상품을 절대 침범하지 않는 가장자리(상단 또는 "
        "하단 좁은 띠)에만 배치, 양은 최소한으로."
    ),
    "dynamic_diagonal": (
        "상품을 화면 대각선 방향으로 기울여 배치하는 느낌을 배경 구도 자체로 표현 "
        "(예: 소실점이나 사선 지형선을 배경에 넣고, product_box를 그 대각선을 따라 "
        "치우친 위치에 배치). 헤드라인도 그 대각선 흐름을 따라가는 방향으로 배치하고, "
        "요소들을 격자에 딱 맞추지 말고 의도적으로 비대칭으로 배치."
    ),
    "editorial_split": (
        "화면을 좌우 정확히 절반으로 나눈다는 느낌으로: 한쪽 절반은 상품 전용 공간, "
        "반대쪽 절반은 텍스트+여백 전용 공간으로 명확히 분리. 두 영역의 색이나 톤을 "
        "미묘하게 다르게 서술해도 좋음."
    ),
    "corner_badge_asymmetric": (
        "상품을 화면의 한쪽 모서리(예: 우측 하단)에 비대칭으로 치우쳐 배치하고, 반대쪽 "
        "모서리에 badge를 크게 배치. 헤드라인은 화면 상단을 가로지르듯 넓게 배치해서 "
        "전체적으로 좌우/상하 균형이 아니라 대각선 긴장감을 주는 구도."
    ),
}


# ============================================================
# Structured Outputs 스키마 (Pydantic)
# ============================================================

class ClaimAudit(BaseModel):
    """상품에 대해 뭘 근거로 광고 문구를 쓰는지 감사(audit) 기록.
    factual_claims는 사실 주장(기능/성능/재료 등)에, allowed_emotional_themes는
    슬로건 같은 감성적 표현에 쓰인다."""
    user_claims: list[str] = Field(
        description="사용자가 입력한 상품 설명에 직접 적힌 사실들 (예: '노이즈캔슬링 지원')"
    )
    visual_facts: list[str] = Field(
        description="사용자 설명엔 없지만, 상품 사진에서 명확히 눈으로 확인되는 사실 "
                    "(예: '케이블 정리용 구멍이 상판에 있음'). 추측이 아니라 사진에서 확실히 보이는 것만."
    )
    factual_claims: list[str] = Field(
        description="기능·성능·재료·수치처럼 '사실 주장'으로 읽히는 문구는 반드시 이 범위 "
                    "안에서만 작성하세요. 기본적으로 user_claims 전체 + visual_facts 전체를 "
                    "포함시키세요 — 판매자가 직접 말한 내용은 사진과 명백히 모순되지 않는 한 "
                    "신뢰하고 포함합니다 (사진으로 검증 불가 = 제외 사유 아님)."
    )
    forbidden_claims: list[str] = Field(
        description="사용자 설명에도 없고 사진에서도 확인 안 되는데, 광고를 그럴듯하게 만들려고 "
                    "스스로 지어내고 싶어지는 구체적 스펙 (예: 사용자가 언급 안 한 '10시간 배터리', "
                    "'IPX4 방수'). user_claims에 이미 있는 항목을 여기 중복으로 넣지 마세요."
    )
    allowed_emotional_themes: list[str] = Field(
        description="headline/subheadline 같은 슬로건에 쓸 수 있는 감성적·은유적 주제어 "
                    "(예: '고요함', '아침의 여유', '집중'). 이건 사실 주장이 아니므로 factual_claims "
                    "안에 문자 그대로 있을 필요 없습니다. 다만 forbidden_claims와 모순되면 안 되고, "
                    "구체적 성능을 보장하는 것처럼 읽히지 않게 하세요 (예: '완벽한 방음'은 성능 "
                    "보장처럼 읽히므로 factual_claims 근거 없이 쓰면 안 됨)."
    )


class ProductVisualAnalysis(BaseModel):
    """상품 사진 자체의 시각 정보 - 합성/톤매칭/그림자 등 렌더링 단계가 참고할 근거.
    claim_audit이 '광고에 뭐라고 써도 되는지'라면, 이건 '상품이 실제로 어떻게 생겼는지'.

    상품은 픽셀 그대로 알파 합성되므로 카메라 각도 자체를 재해석하지 않는다. 아래
    필드들은 배경이 이 고정된 누끼와 자연스럽게 어울리도록(지지면, 원근, 조명 방향
    일치) 계획하기 위한 것이다."""
    category: str = Field(description="상품 카테고리 (예: 'wireless earbuds', 'wooden desk')")
    dominant_colors: list[str] = Field(description="상품의 주요 색상 (자연어, 예: 'matte white', 'natural oak wood')")
    material: list[str] = Field(description="주요 재질 (예: ['plastic', 'silicone'])")
    orientation: str = Field(description="사진 속 상품이 놓인 방향/각도 (예: 'three-quarter front view')")
    has_existing_shadow: bool = Field(description="원본 사진 자체에 이미 뚜렷한 그림자가 있는지")
    color_fidelity_importance: Literal["critical", "high", "normal"] = Field(
        description="이 상품의 색이 광고 신뢰성에 얼마나 중요한지. 흰색/파스텔처럼 색 자체가 "
                    "정체성인 경우나 음식(실제 색과 다르면 클레임 위험)은 critical, 그 외 일반 "
                    "제품은 high, 색이 크게 중요하지 않은 상품은 normal."
    )
    viewpoint_class: Literal["top_down", "high_angle", "eye_level", "low_angle", "front_flat"] = Field(
        description="원본 사진이 상품을 어떤 시점에서 찍었는지. 배경의 원근/지지면을 이 "
                    "시점과 맞추기 위한 것이지, 상품 자체를 다른 각도로 재해석하라는 게 아님."
    )
    support_type: Literal["horizontal_surface", "vertical_surface", "free_floating", "held_by_person", "unknown"] = Field(
        description="상품이 실제로 어디에 놓이는 상품인지 (바닥/테이블 위, 벽걸이, 공중부양 연출, 손에 든 것 등)"
    )
    perspective_strength: Literal["flat", "weak", "moderate", "strong"] = Field(
        description="원본 사진에서 느껴지는 원근감의 강도. 배경도 이 정도의 원근감으로 설계해야 자연스럽다."
    )
    needs_contact_shadow: bool = Field(description="상품이 바닥/표면에 실제로 닿아있어서 접지 그림자가 필요한지")
    contact_edge: Literal["bottom", "bottom_left", "bottom_right", "full_base", "none"] = Field(
        description="접지 그림자가 필요하다면, 상품의 어느 쪽 가장자리가 접촉면인지"
    )
    observed_light_direction: Literal["upper_left", "upper_right", "left", "right", "front", "diffuse", "unclear"] = Field(
        description="원본 상품 사진 자체에서 실제로 관찰되는 광원 방향 (상품의 밝은 면/그림자 "
                    "위치로 판단). 명확하지 않으면 'unclear'. 이후 배경의 light_direction은 "
                    "이 값과 맞추는 게 원칙이다 (상품은 왼쪽에서 빛을 받았는데 배경은 반대 "
                    "방향으로 설계하면 합성 티가 남)."
    )


class ProductBox(BaseModel):
    x: float
    y: float
    width: float
    height: float


class Decoration(BaseModel):
    id: str = Field(description="이 소품의 고유 식별자 (예: 'prop_laptop'). 수정 요청 시 "
                    "이 id로 특정 소품만 켜고 끌 수 있어야 하므로, 같은 브리프 안에서 중복되면 안 됨")
    item: str
    purpose: str = Field(description="이 소품을 넣는 이유 (예: '카페에서 사용하는 맥락을 보여줌'). "
                    "단순히 화면을 채우기 위한 장식이면 애초에 넣지 마세요.")
    removable: bool = Field(default=True, description="사용자가 나중에 '이거 빼줘'라고 요청할 "
                    "가능성이 높은 소품이면 True (거의 항상 True). 배경에 녹아든 고정 구조물이면 "
                    "애초에 decoration이 아니라 background_prompt로 표현하세요.")
    prompt: str = Field(description="영어로 작성된 이 소품의 image-generation 프롬프트")
    placement_type: Literal["occluding", "on_surface", "behind_product"] = Field(
        description="occluding=상품 일부를 가리는 소품(상품 핵심 부위는 절대 가리면 안 됨, "
                    "신중하게 사용), on_surface=상품 옆 표면 위, behind_product=상품보다 뒤쪽"
    )
    surface_id: Optional[str] = Field(
        default=None,
        description="이 소품이 놓이는 surfaces 중 하나의 id. 특정 표면 위에 놓이는 게 아니면 null."
    )
    x: float
    y: float
    width: float
    height: float
    rotation: float = 0


class SurfacePlane(BaseModel):
    """상품 위에 소품을 얹을 수 있는 평면 (예: 책상 상판). 소품 그림자를 이 영역
    안으로만 제한하는 데 쓰인다 (원근 왜곡 배치는 아직 지원 안 함 - 추후 확장)."""
    id: str
    polygon: list[list[float]] = Field(
        description="이 평면의 꼭짓점들 (x,y 비율 좌표, 시계방향). 최소 3개 이상."
    )
    surface_type: str = Field(description="예: 'horizontal tabletop', 'shelf'")


class ProtectedRegion(BaseModel):
    """상품에서 가려지면 안 되는 핵심 부위 (케이블 홀, 로고, 조작부 등).
    소품 배치 시 이 영역과 많이 겹치는 소품은 자동으로 제외된다."""
    name: str
    bbox: list[float] = Field(description="[x1, y1, x2, y2] 비율 좌표")


class Badge(BaseModel):
    text: str
    x: float
    y: float
    align: Literal["left", "center", "right"]


class Headline(BaseModel):
    text: str
    x: float
    y: float
    align: Literal["left", "center", "right"]
    font_size_ratio: float
    color: list[int] = Field(description="정확히 [R, G, B] 3개 정수, 0~255")
    outline_color: Optional[list[int]] = Field(
        default=None,
        description="헤드라인에 대비되는 외곽선을 두르고 싶을 때 [R, G, B] 3개 정수. "
                    "그래픽 임팩트형처럼 대담한 포스터 타이포에 어울리며, 그 외엔 보통 "
                    "null(외곽선 없음)로 두는 게 자연스럽습니다.",
    )
    outline_width: Optional[int] = Field(
        default=None,
        description="외곽선 두께(px, 대략 3~10 범위). outline_color가 null이면 이 값도 "
                    "무시되니 null로 두세요.",
    )


class Subheadline(BaseModel):
    text: str
    x: float
    y: float
    align: Literal["left", "center", "right"]
    font_size_ratio: float
    color: list[int]


class Feature(BaseModel):
    title: str
    description: str
    x: float
    y: float
    title_color: list[int]
    desc_color: list[int]
    divider_after: bool
    divider_color: Optional[list[int]] = None


class CreativeBrief(BaseModel):
    claim_audit: ClaimAudit = Field(
        description="다른 모든 필드보다 먼저 이것부터 채우세요."
    )
    product_visual_analysis: ProductVisualAnalysis
    background_prompt: str
    design_rationale: str
    typography_style: Literal["bold_modern", "soft_editorial"]
    product_box: ProductBox
    light_direction: Literal["upper_left", "upper_right", "left", "right", "front"]
    ambient_color_temperature: Literal["warm", "neutral", "cool"]
    surfaces: list[SurfacePlane] = Field(default_factory=list)
    protected_regions: list[ProtectedRegion] = Field(default_factory=list)
    decorations: list[Decoration]
    badge: Optional[Badge] = None
    headline: Headline
    subheadline: Optional[Subheadline] = None
    features: list[Feature]


CREATIVE_BRIEF_INSTRUCTION_TEMPLATE = """당신은 20년 경력의 광고 아트 디렉터입니다.

=== 절대 규칙 (다른 모든 지시보다 우선) ===
1. 상품의 재료, 구조, 색상, 기능, 수치를 임의로 만들지 마세요.
2. 원본 상품 이미지는 상품 외형의 유일한 시각적 기준입니다. 상품 자체를
   background_prompt에서 다시 생성하도록 요청하지 마세요 (별도 시스템이 원본을 그대로 합성함).
3. 이미지 생성 모델(background_prompt)에 실제 글자를 그리게 하지 마세요 — 텍스트는
   별도 렌더러가 좌표에 맞춰 그립니다.
4. 사용자가 명시하지 않은 가격, 할인, 인증, 후기, 통계를 만들지 마세요.
5. factual_claims에 없는 사실 주장을 headline/subheadline/feature에 쓰지 마세요
   (감성적 슬로건은 allowed_emotional_themes 범위에서 자유롭게 써도 됩니다).

이 상품 사진과 아래 정보를 보고, 오프라인 인쇄 광고(A4, 세로 210:297 비율)를
처음부터 끝까지 직접 기획하세요. 좌표, 요소 유무, 개수를 전부 당신이 결정합니다.

상품명: {product_name}
상품 설명: {product_description}
가격: {price}
플랫폼: {platform}
광고 목표: {ad_goal}
스타일: {style}
사용자가 선택한 슬로건(있다면): {selected_slogan}

이번 광고는 특히 다음 접근으로 풀어보세요: {creative_angle}
(단, 상품 설명이나 광고 목표와 상충되면 이 방향을 무리하게 따르지 말고 상품에 맞게 조정하세요.)
이 접근의 텍스트 분량 가이드: {text_budget}
(이 가이드를 무시하고 항상 서브헤드+features를 풀로 채우면 접근이 다른 의미가 없어집니다.)

=== 1. product_visual_analysis부터 채우세요 ===
상품 사진을 보고 카테고리, 주요 색상, 재질, 방향, 원본에 이미 그림자가 있는지, 색
보존이 얼마나 중요한지를 정리하세요. 이건 이후 합성/톤매칭 코드가 참고합니다.

중요: 원본 상품은 알파 합성으로 픽셀을 그대로 사용하므로, 상품의 시점·형태·회전·
원근을 변경하거나 재해석하지 마세요. 대신 상품이 자연스럽게 합성될 수 있도록,
원본 사진에서 관찰되는 시점(viewpoint_class)·원근 강도(perspective_strength)·
접촉면(contact_edge)·광원 방향(observed_light_direction)을 있는 그대로 읽어서
기록하세요. 이건 배경을 상품과 충돌 없이 계획하기 위한 것이지, 정확한 렌즈 수치나
새로운 촬영 각도를 지시하는 게 아닙니다.

배경의 light_direction은 원칙적으로 observed_light_direction과 같은 방향으로
설정하세요 (상품은 왼쪽에서 빛을 받았는데 배경을 오른쪽 조명으로 기획하면, 픽셀은
그대로여도 합성 티가 납니다). observed_light_direction이 'unclear'나 'diffuse'면
배경도 부드러운 확산광으로 가는 게 안전합니다. 상품 광원과 정반대 방향의 강한
광원은 쓰지 마세요.

=== 2. claim_audit ===
상품 설명에 적힌 것(user_claims)과 사진에서 실제로 눈으로 확인되는 것(visual_facts)을
구분해서 정리하세요.

factual_claims에는 기본적으로 user_claims 전체 + visual_facts 전체를 포함시키세요.
판매자가 직접 설명한 내용은, 사진과 명백히 모순되지 않는 한 "사진으로 검증이 안 된다"는
이유만으로 제외하지 마세요.

forbidden_claims는 오직 "사용자도 말 안 했고 사진에서도 안 보이는데, 당신이 스스로
지어내고 싶어지는 구체적 스펙"만 위한 자리입니다.

allowed_emotional_themes에는 슬로건에 쓸 수 있는 감성 주제어를 자유롭게 적으세요
(사실 주장이 아니라 무드/감정 표현이므로 factual_claims처럼 엄격할 필요 없음).

가격을 받았다면, 광고 목표·플랫폼에 실제로 도움이 될 때만 headline/badge 등에 표시하세요
(표시한다면 정확히 사용자가 준 값만 사용). 억지로 넣지 마세요.

{slogan_usage_rule}

=== Feature 스타일 규칙 ===
- divider_after는 이 항목 뒤에 구분선을 넣을지 여부입니다. 자유롭게 결정하세요.

=== 타이포그래피 기획 규칙 ===
- headline.text에는 의미 단위로 줄바꿈(\\n)을 직접 넣어 임팩트를 만드세요.
- font_size_ratio: 헤드라인 0.06~0.11, 서브헤드 0.025~0.04. 대담한 그래픽 포스터
  스타일이면 0.11에 가깝게, 정보 중심 레이아웃이면 0.06에 가깝게.
- color는 배경 밝기를 고려해 가독성 확보되는 RGB로, 배경 톤과 어울리는 미묘한 색조로.
- headline.outline_color/outline_width: 스트리트/드롭 포스터처럼 대담하고 그래픽적인
  타이포가 어울리는 컨셉일 때만 채우세요 (예: 밝은 배경색 위에 어두운 글씨 + 대비되는
  밝은 색 외곽선, 혹은 그 반대). 절제되고 편집숍 감성의 디자인이면 null로 비워두세요 -
  모든 헤드라인에 외곽선을 넣으면 오히려 특별함이 사라집니다.
- 헤드라인 줄바꿈을 쓸 경우 세로 공간이 늘어난다는 걸 감안해 이후 요소 배치에 여유를 두세요.

=== 디자인 기획 원칙 ===
- 모든 요소(badge, subheadline, features)는 필요 없으면 생략하세요.
- product_box: 아래 "이번 광고에 배정된 구도(layout_family)"를 반드시 따르세요.
  {layout_instruction}
  이 구도 지시가 이번 product_box/텍스트 배치 좌표를 결정하는 최우선 기준입니다 -
  "hero처럼 크게/정보 위주로 작게" 같은 일반론이 아니라 위 구체적 배치를 실제로 따르세요.
  단, 어떤 구도를 고르든 product_box.width * product_box.height(캔버스 면적 대비 상품이
  차지하는 비율)는 최소 0.15(15%) 이상이어야 합니다 - 상품이 광고의 주인공이라는 원칙은
  구도와 무관하게 항상 지켜야 합니다. 구도 지시가 크기를 명시하지 않았다면 이 하한선을
  기준으로 스스로 정하세요.
- 모든 요소의 x,y,width,height는 서로 겹치지 않게 배치하세요 (product_box 포함).
- 여백을 적극 활용하고, 시선 흐름이 자연스럽게 이어지도록 배치하세요.

=== background_prompt 작성 규칙 ===
- 상품 자체나 상품과 동일한 오브젝트를 다시 그리라고 하지 마세요.
- 이번 광고가 촬영된 것으로 보일 장면 유형 힌트: {scene_type}
  (이 유형이 상품과 안 어울리면 무시하고 스튜디오로 가도 됩니다.)
- 배경 요소는 두 종류로 엄격하게 나눠 생각하세요:
  · 환경 구성 요소 — 오직 벽, 바닥, 천장, 창문, 벽에 붙박이로 고정된 선반/구조물,
    자연광/조명 분위기처럼 "그 자체로는 독립된 물건이 아닌" 배경 그 자체만
    background_prompt에 포함하세요.
  · 그 외 독립적으로 서 있거나 놓인 모든 물건(의자, 스탠드 조명, 노트북, 컵, 책, 접시,
    화분, 반찬, 도구, 다른 가구 등)은 예외 없이 decorations로 분리하세요. "환경 분위기를
    살리기 위해서"라는 이유로 이런 독립 물체를 background_prompt에 슬쩍 넣지 마세요 —
    사용자가 나중에 "이거 빼줘"라고 요청할 수 있는 모든 물체는 반드시 decoration이어야
    수정이 가능합니다.
  · 절대 규칙: 상품과 같은 카테고리이거나 헷갈릴 수 있는 사물은 배경에도, 소품에도
    절대 그리지 마세요. 예를 들어 상품이 책상/테이블이면 배경에 다른 책상·테이블·선반·
    캐비닛 같은 가구를 그리지 마세요. 상품이 그릇에 담긴 음식이면 배경에 다른 그릇·
    접시에 담긴 음식을 그리지 마세요. 상품이 의자면 배경에 다른 의자를 그리지 마세요.
    이 규칙은 "환경 요소 허용" 규칙보다 우선합니다.
- 구체적 스타일 키워드를 쓰세요. 참고할 무드 키워드: {mood_keywords}
  (그대로 베끼지 말고 이 상품에 맞게 구체적으로 풀어서, 매번 다르게 서술하세요.)
- 색 계열 강제 규칙 (반드시 지키세요 - 이번 광고에 배정된 색 팔레트):
  {palette}
  · background_prompt의 첫 문장에 반드시 이 색 팔레트를 구체적으로 반영하세요.
    "neutral tone", "soft beige" 같은 애매한 대체 표현으로 바꾸지 말고, 위에 주어진
    색 이름을 실제로 장면에 녹여내세요 (예: 배정된 팔레트가 "deep forest green"이면
    벽/바닥/조명 색조가 실제로 초록 계열이어야 합니다).
  · 상품이 이 팔레트와 색이 겹쳐서 안 보이면(예: 흰색 상품 + 아주 밝은 팔레트),
    product_box 주변만 팔레트보다 살짝 밝거나 어두운 톤으로 대비를 주고, 나머지
    영역은 팔레트를 유지하세요.
- 스타일({style})에 맞는 무드 키워드 추가. 흰색 상품에 흰색 배경 금지.
- 실존 브랜드명·로고·워터마크·타사 상표를 절대 포함하지 마세요.
- 돌(stone), 받침대, 좌대 같은 소품성 사물도 배경에 직접 넣지 말고 필요하면 decorations로
  분리하세요.
- 나중에 별도 시스템이 headline/subheadline/badge/features 좌표에 텍스트를 렌더링합니다.
  그 영역들은 "텍스트를 얹기 좋게" 낮은 디테일·낮은 대비가 되도록 구체적으로 서술하세요
  (product_box 영역은 반대로 상품이 돋보이도록 서술).

=== copy 작성 규칙 ===
- headline은 슬로건 (7~14자, 기능과 은유적으로 연결 가능, allowed_emotional_themes 활용 가능)
- subheadline은 필요할 때만, 40~60자 이내
- features는 title(짧은 명사구) + description(효과 한 줄)
- 사실 주장(기능/성능/수치)은 factual_claims 범위 안에서만. 감성 표현은 allowed_emotional_themes 참고.
- '브랜드 이름', '가격' 같은 자리표시자(placeholder) 문구를 그대로 쓰지 마세요.

=== decorations 규칙 ===
- 소품은 상품의 사용 맥락이나 광고 아이디어를 명확히 강화할 때만 추가하세요.
  단순히 화면을 채우기 위한 장식은 넣지 마세요.
- 상품의 핵심 특징, 로고, 구조, 재료를 가리지 마세요 (필요하면 protected_regions로 보호).
- 기본 0~2개, 특별한 이유가 있을 때만 3개까지.
- background_prompt와 소품을 중복 표현하지 마세요.
- 각 decoration의 id는 고유해야 합니다.
- 주의: decoration의 prompt는 항상 "사실적인 실물 사진"으로 렌더링됩니다. 물감
  튀김(paint splash), 잉크 스플래터, 기하학적 도형 같은 그래픽/일러스트 요소는
  decoration이 아니라 background_prompt 안에 장면의 일부로 직접 묘사하세요 -
  decoration으로 넣으면 사실적인 물체로 어색하게 렌더링됩니다.

=== surfaces / protected_regions 규칙 ===
- 상품이 책상/선반/테이블처럼 소품을 올릴 평평한 면이 있으면 surfaces에 등록하고
  decoration.surface_id로 연결하세요. 없으면 빈 배열.
- 사진에서 명확히 보이는 상품의 핵심 특징이 소품에 가려질 위험이 있으면
  protected_regions에 등록하세요. 확신 없으면 빈 배열."""


class BackgroundObject(BaseModel):
    id: str = Field(description="obj_1, obj_2 처럼 이 배경 안에서 고유한 식별자")
    label: str = Field(description="이 물체를 가리키는 짧은 한국어 이름 (예: '은색 하이힐', '바위 무더기', '구름')")
    description: str = Field(description="한 문장 설명")
    bbox: list[float] = Field(
        description="이 물체가 차지하는 대략적인 사각형 영역 [x1, y1, x2, y2], 0~1 비율 좌표"
    )
    same_domain_as_product: bool = Field(
        description="상품과 상위 카테고리가 같은 물체인지 (스타일이 완전히 달라도 같은 상위 "
                    "카테고리면 true - 예: 상품이 운동화면 하이힐/부츠/샌들도 전부 '신발'이라는 "
                    "상위 카테고리가 같으므로 true. 스타일 유사성이 아니라 카테고리 자체를 기준으로 "
                    "판단하세요)"
    )


class BackgroundAnalysis(BaseModel):
    objects: list[BackgroundObject] = Field(
        default_factory=list,
        description="배경에 실제로 그려진, 언급할 만한 모든 물체 (환경 자체인 벽/바닥/하늘/조명은 "
                    "제외하고, 독립적으로 식별 가능한 사물만)",
    )
    contains_forbidden_object: bool = Field(
        description="objects 중 same_domain_as_product=true인 항목이 하나라도 있으면 true"
    )
    detected_object_description: str = Field(
        default="", description="금지 물체가 있다면 무엇인지 한 문장 요약, 없으면 빈 문자열"
    )


def analyze_background_objects(background_path: str, product_category: str) -> BackgroundAnalysis:
    """생성된 배경 이미지를 GPT-vision으로 분석해서:
    1) 상품과 같은 상위 카테고리의 물체가 실수로 그려졌는지 확인하고
    2) 배경에 실제로 존재하는 모든 물체를 목록화한다 (Object Inventory).

    이 목록은 edit_router가 "배경에 있는 OO 제거해줘" 같은 요청을 처리할 때 참조한다.
    판정 기준은 "스타일이 유사한지"가 아니라 "상위 카테고리가 같은지"다 - 트레일화
    광고에 하이힐이 나오면 스타일은 다르지만 둘 다 "신발"이므로 금지 대상이다.
    """
    client = _get_client()
    with open(background_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.parse(
        model=settings.TEXT_MODEL_NAME,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": (
                    f"이 배경 이미지를 보세요. 이 배경은 광고 상품('{product_category}')을 "
                    f"나중에 별도로 합성하기 위해 생성된 장면입니다.\n\n"
                    f"1. 이 배경에 실제로 그려진, 독립적으로 식별 가능한 모든 물체를 목록화하세요 "
                    f"(벽/바닥/하늘 같은 환경 자체는 제외).\n"
                    f"2. 그중 상품('{product_category}')과 **상위 카테고리가 같은** 물체가 있는지 "
                    f"확인하세요. 스타일이 완전히 달라도 상위 카테고리가 같으면(예: 상품이 운동화면 "
                    f"하이힐/부츠/슬리퍼도 전부 '신발') same_domain_as_product를 true로 표시하세요. "
                    f"'스타일이 비슷한지'가 아니라 '같은 종류의 물건인지'로 판단하세요."
                )},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
            ],
        }],
        response_format=BackgroundAnalysis,
    )
    parsed = response.choices[0].message.parsed
    if parsed is None:
        return BackgroundAnalysis(objects=[], contains_forbidden_object=False, detected_object_description="")
    return parsed


def verify_background_clean(background_path: str, product_category: str) -> tuple[bool, str]:
    """하위호환용 wrapper. 신규 코드는 analyze_background_objects를 직접 쓰는 걸 권장한다
    (객체 목록까지 같이 받을 수 있어서 vision 호출을 중복으로 안 해도 됨)."""
    analysis = analyze_background_objects(background_path, product_category)
    return not analysis.contains_forbidden_object, analysis.detected_object_description


def create_creative_brief(
    image_path: str,
    product_name: str,
    product_description: str,
    ad_goal: str,
    style: str,
    price: str | None = None,
    platform: str | None = None,
    selected_slogan: str | None = None,
    creative_angle: str | None = None,
    scene_type: str | None = None,
    layout_family: str | None = None,
    force_decoration: bool = False,
) -> dict:
    """creative_angle/scene_type을 직접 지정하면 그 방향으로 강제 생성한다 (테스트/비교용).
    None이면 각각 무작위로 뽑는다 (기본 동작).
    price/platform은 선택적 - 없으면 GPT가 알아서 생략한다.
    selected_slogan이 있으면 문장부호까지 정확히 그대로 headline/subheadline에 반영한다.
    force_decoration=True면 decorations를 최소 1개 이상 넣도록 강제한다 (소품 합성
    파이프라인 검증용)."""
    client = _get_client()
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    chosen_angle = creative_angle or random.choice(CREATIVE_ANGLES)
    chosen_scene = scene_type or random.choice(SCENE_TYPES)
    mood_keywords = CREATIVE_ANGLE_MOOD_KEYWORDS.get(chosen_angle, "premium editorial minimal art direction")
    text_budget = CREATIVE_ANGLE_TEXT_BUDGET.get(chosen_angle, "상황에 맞게 자유롭게 결정")
    palette = random.choice(BACKGROUND_COLOR_PALETTES)
    chosen_layout_family = layout_family or random.choice(list(LAYOUT_FAMILIES.keys()))
    layout_instruction = LAYOUT_FAMILIES[chosen_layout_family]

    if not selected_slogan:
        slogan_usage_rule = (
            "사용자가 선택한 슬로건이 없습니다. 슬로건은 당신이 새로 기획하세요."
        )
    else:
        slogan_usage_rule = (
            f"사용자가 선택한 슬로건 \"{selected_slogan}\"은 문장부호(쉼표, 마침표 등)까지 "
            "포함해서 정확히 그대로 headline 또는 subheadline에 사용해야 합니다. "
            "절대 다듬거나, 줄이거나, 문장부호를 생략하거나, 다른 표현으로 바꾸지 마세요. "
            "다만 headline.text에 의미 단위로 줄바꿈(\\n)을 넣는 것은 허용됩니다 - "
            "단, 줄바꿈으로 인해 문장부호가 삭제되거나 단어가 잘리면 안 됩니다."
        )

    instruction = (
        CREATIVE_BRIEF_INSTRUCTION_TEMPLATE
        .replace("{creative_angle}", chosen_angle)
        .replace("{text_budget}", text_budget)
        .replace("{mood_keywords}", mood_keywords)
        .replace("{palette}", palette)
        .replace("{layout_instruction}", layout_instruction)
        .replace("{scene_type}", chosen_scene)
        .replace("{product_name}", product_name)
        .replace("{product_description}", product_description)
        .replace("{price}", price or "(입력 안 됨 - 광고에 가격 표시하지 마세요)")
        .replace("{platform}", platform or "(입력 안 됨)")
        .replace("{selected_slogan}", selected_slogan or "(선택 안 됨 - 슬로건은 당신이 새로 기획하세요)")
        .replace("{slogan_usage_rule}", slogan_usage_rule)
        .replace("{ad_goal}", ad_goal)
        .replace("{style}", style)
    )

    if force_decoration:
        instruction += (
            "\n\n=== 테스트 모드 ===\n"
            "이번엔 decorations를 반드시 1개 이상 포함하세요 (소품 합성 파이프라인 검증 목적)."
        )

    response = client.chat.completions.parse(
        model=settings.TEXT_MODEL_NAME,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": instruction},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
            ],
        }],
        response_format=CreativeBrief,
    )

    parsed = response.choices[0].message.parsed
    if parsed is None:
        refusal = response.choices[0].message.refusal
        raise RuntimeError(f"Creative Brief 생성 실패 (모델 거부): {refusal}")

    result = parsed.model_dump()
    result["_creative_angle"] = chosen_angle  # 디버깅용 (렌더링엔 안 씀)
    result["_scene_type"] = chosen_scene
    result["_palette"] = palette
    result["_layout_family"] = chosen_layout_family

    forbidden_claims = result.get("claim_audit", {}).get("forbidden_claims", [])
    if forbidden_claims:
        print(f"ℹ️ 참고: 이번 생성에서 배제된 불확실한 주장들: {forbidden_claims}")

    user_claims = result.get("claim_audit", {}).get("user_claims", [])
    factual_claims = result.get("claim_audit", {}).get("factual_claims", [])
    dropped = [c for c in user_claims if c not in factual_claims]
    if dropped:
        print(f"⚠️ 경고: 사용자가 직접 말한 내용인데 factual_claims에서 빠진 것으로 보임: {dropped}")

    return result