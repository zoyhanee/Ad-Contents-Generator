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


class TextPropertyChange(BaseModel):
    target: Literal["headline", "subheadline", "badge", "feature"]
    feature_index: Optional[int] = Field(
        default=None, description="target이 feature일 때, 몇 번째 feature인지 (0부터). 아니면 null."
    )
    remove: bool = Field(
        default=False,
        description="이 요소 **전체**(헤드라인/서브헤드라인/배지/feature 한 항목 통째로)를 "
                    "완전히 없애 달라는 요청일 때만 true. 예: '서브헤드라인 빼줘', '배지 없애줘', "
                    "'이 feature 항목 삭제해줘'.\n"
                    "중요: 텍스트 **일부(문구, 한 줄, 한 단어)만** 지워 달라는 요청은 remove가 "
                    "아닙니다! 예를 들어 헤드라인이 '도심을 걷고\\n오프로드로 이어지는\\n실버 "
                    "트레일' 3줄인데 사용자가 \"'도심을 걷고' 문구 제거해줘\"라고 하면, 이건 "
                    "헤드라인 전체를 지우라는 게 아니라 그 부분만 빼고 나머지는 그대로 두라는 "
                    "뜻입니다 - 이때는 remove=false로 두고, new_text에 그 부분을 뺀 나머지 "
                    "텍스트('오프로드로 이어지는\\n실버 트레일')를 직접 계산해서 넣으세요. "
                    "target이 headline이면 이 구분이 특히 중요합니다 - 헤드라인은 통째로는 "
                    "지울 수 없지만(remove=false 고정), 일부 문구만 빼고 나머지를 유지하는 "
                    "건 new_text로 항상 가능합니다.\n"
                    "remove=true일 때는 new_text/size_operation/new_x/new_y를 전부 null로 두세요.",
    )
    new_text: Optional[str] = Field(default=None, description="문구 자체를 바꾸는 요청이면 새 문구, 아니면 null")
    size_operation: Optional[Literal["multiply", "add", "set"]] = Field(
        default=None,
        description="글자 크기 변경 요청이면 방식을 지정하세요. 'X% 키워줘/줄여줘'처럼 "
                    "비율로 말한 요청은 반드시 'multiply'로 (예: '20% 키워줘' -> "
                    "size_operation='multiply', size_value=1.2 / '30% 줄여줘' -> "
                    "size_value=0.7). '조금/살짝/약간 크게' 같은 애매한 정도 표현은 "
                    "'add'로 작은 절대값을 더하세요 (예: size_value=0.01). 특정 크기값을 "
                    "정확히 지정한 요청(드묾)은 'set'. 크기 변경 요청이 아니면 null.",
    )
    size_value: Optional[float] = Field(
        default=None,
        description="size_operation에 맞는 값. multiply=배율(1.2, 0.7 등, 1.0=변화없음), "
                    "add=현재값에 더할 절대량(예: +0.01, -0.008), set=최종 font_size_ratio 값 자체.",
    )
    new_x: Optional[float] = Field(default=None, description="위치 이동 요청이면 새 x, 아니면 null")
    new_y: Optional[float] = Field(default=None, description="위치 이동 요청이면 새 y, 아니면 null")
    new_align: Optional[Literal["left", "center", "right"]] = Field(
        default=None,
        description="정렬 자체를 바꾸는 요청이면 (예: '가운데 정렬로', '중앙으로 옮겨줘') 새 정렬값. "
                    "'중앙/가운데로 이동'은 위치(new_x)만으로는 실제로 중앙에 오지 않습니다 - "
                    "정렬이 'left'인 채로 x만 0.5로 옮기면 텍스트가 0.5 지점에서 오른쪽으로 뻗어나갑니다. "
                    "진짜 가운데 정렬을 원하는 요청이면 new_align='center'와 new_x=0.5를 함께 설정하세요. "
                    "target이 feature면 정렬 개념이 없으니 항상 null로 두세요.",
    )
    new_color: Optional[list[int]] = Field(
        default=None,
        description="텍스트 글자 색 자체를 바꾸는 요청이면 [R, G, B] 3개 정수 (0~255). "
                    "예: '빨간색으로 바꿔줘' -> [220, 30, 30] 같은 구체적인 값. 색 변경 요청이 "
                    "아니면 null. target이 feature면 이 필드 대신 title_color/desc_color를 "
                    "구분해야 하므로(어느 쪽인지 애매하면) 둘 다인 것으로 보고 new_color를 채우세요.",
    )
    new_outline_color: Optional[list[int]] = Field(
        default=None,
        description="헤드라인 **외곽선/테두리** 색을 바꾸는 요청일 때만 [R, G, B]. 예: '테두리를 "
                    "빨간색으로', '외곽선 색 바꿔줘'. 사용자가 '글자색'과 '테두리색' 중 어느 걸 "
                    "말하는지 애매하면, 화면에 두꺼운 테두리가 있는 대담한 포스터 스타일일 경우 "
                    "보통 눈에 띄는 색은 테두리 쪽이므로 new_outline_color를 우선 채우세요. "
                    "target이 headline이 아니면 항상 null (다른 요소는 외곽선 개념이 없음).",
    )


class BackgroundObjectChange(BaseModel):
    target_object_id: Optional[str] = Field(
        default=None,
        description="아래 '배경 실측 객체 목록'의 id 중에서 고르세요. 목록에 없는 걸 "
                    "요청하면 null로 두고 edit_type을 unclear로 바꾸세요.",
    )
    action: Literal["remove", "reduce", "increase", "modify"] = Field(
        description="remove=완전히 제거, reduce=줄이거나 덜 두드러지게, increase=늘리거나 "
                    "더 두드러지게, modify=형태/색 등을 다르게"
    )
    modification_instruction: str = Field(
        description="이 물체에 대해 실제로 어떻게 다시 그려야 하는지, 영어로 구체적인 지시문 "
                    "(예: 'remove the high-heel shoe and fill the area naturally with the "
                    "surrounding rocky terrain')"
    )


class DecorationAddition(BaseModel):
    prompt: str = Field(
        description="새 소품 이미지 생성에 쓸 영어 프롬프트. 실물처럼 사실적으로 묘사하세요 "
                    "(예: 'thick melted cheese dripping down in glossy strands'). 상품 자체를 "
                    "다시 그리라는 지시는 절대 포함하지 마세요 - 이 소품은 상품과 별개로 생성되어 "
                    "나중에 겹쳐서 합성될 뿐, 상품 원본 픽셀은 전혀 건드리지 않습니다."
    )
    placement_type: Literal["occluding", "behind_product", "on_surface"] = Field(
        description="occluding=상품 위에 겹쳐 보이게(상품 표면에서 일어나는 것처럼 묘사되는 "
                    "요청은 대부분 이것), behind_product=상품 뒤에, on_surface=상품 옆 바닥/"
                    "표면 위에"
    )
    x: float = Field(description="0~1 비율, 새 소품의 왼쪽 위 x")
    y: float = Field(description="0~1 비율, 새 소품의 왼쪽 위 y")
    width: float = Field(description="0~1 비율, 새 소품의 너비")
    height: float = Field(description="0~1 비율, 새 소품의 높이")


class EditClassification(BaseModel):
    edit_type: Literal[
        "decoration_toggle", "text_property", "background_brightness",
        "background_regenerate", "background_object_edit", "decoration_add",
        "product_change", "unclear",
    ]
    reasoning: str = Field(description="왜 이렇게 분류했는지 한 문장 (디버깅용)")
    target_decoration_id: Optional[str] = Field(
        default=None, description="edit_type이 decoration_toggle일 때, 대상 소품의 id"
    )
    decoration_visible: Optional[bool] = Field(
        default=None, description="edit_type이 decoration_toggle일 때, false=제거 요청, true=다시 넣기 요청"
    )
    text_property_change: Optional[TextPropertyChange] = Field(
        default=None, description="edit_type이 text_property일 때만 채움"
    )
    brightness_delta: Optional[float] = Field(
        default=None, description="edit_type이 background_brightness일 때, -1.0(많이 어둡게)~1.0(많이 밝게)"
    )
    background_regenerate_instruction: Optional[str] = Field(
        default=None, description="edit_type이 background_regenerate일 때, 새 배경에 반영할 영어 지시문"
    )
    background_object_change: Optional[BackgroundObjectChange] = Field(
        default=None, description="edit_type이 background_object_edit일 때만 채움"
    )
    decoration_addition: Optional[DecorationAddition] = Field(
        default=None, description="edit_type이 decoration_add일 때만 채움"
    )
    clarifying_question: Optional[str] = Field(
        default=None, description="edit_type이 unclear일 때, 사용자에게 되물을 질문"
    )


def classify_edit_request(ad_state: dict, user_feedback: str) -> EditClassification:
    client = _get_client()

    decoration_summary = [
        {"id": d["id"], "item": d["item"], "purpose": d.get("purpose", ""), "removable": d.get("removable", True)}
        for d in ad_state.get("decorations", [])
    ]
    features_summary = [
        {"index": i, "title": f.get("title")} for i, f in enumerate(ad_state.get("features", []))
    ]
    background_objects_summary = [
        {"id": o["id"], "label": o["label"], "description": o.get("description", "")}
        for o in ad_state.get("background_objects", [])
    ]

    prompt = f"""당신은 광고 수정 요청을 가장 안전하고 좁은 범위의 연산으로 분류하는 라우터입니다.
이미지 전체 재생성(background_regenerate)은 정말 필요할 때만 고르고, 그 전에 더 좁은 범위
(decoration_toggle, text_property, background_brightness)로 처리할 수 있는지 먼저 확인하세요.

=== 현재 광고 상태 ===
상품: {ad_state.get("product_visual_analysis", {}).get("category", "(알 수 없음)")}
헤드라인: {ad_state.get("headline", {}).get("text")}
서브헤드라인: {(ad_state.get("subheadline") or {}).get("text")}
배지: {ad_state.get("badge")}
features: {features_summary}
소품(decorations, Planner가 계획해서 생성한 것): {decoration_summary}
배경 실측 객체 목록(Object Inventory - 배경이 실제로 생성된 후 Vision으로 확인한 것.
    Planner가 계획하지 않았는데 gpt-image가 실수로 그렸을 수도 있는 것들 포함):
    {background_objects_summary}

=== 사용자 수정 요청 ===
"{user_feedback}"

=== 공통 원칙 ===
사용자가 명시적으로 언급하지 않은 속성은 절대 같이 바꾸지 마세요. 예를 들어 "맨
왼쪽으로 옮겨줘"는 위치(new_x/new_y)만 바꾸라는 뜻이고, 크기(size_operation/size_value)나
정렬(new_align)은 요청에 없었으면 반드시 null로 둬야 합니다. 요청 하나당 실제로
언급된 속성만 정확히 하나씩 바꾸세요 - "더 눈에 띄게" 같은 애매한 강조 표현이 아닌 한,
위치 이동 요청이 크기 변경을 겸한다고 임의로 추측하지 마세요.

=== 분류 기준 ===
- decoration_toggle: "OO 빼줘/제거해줘/없애줘"처럼, 위 **소품(decorations) 목록**에 있는
  특정 소품을 켜고 끄는 요청. target_decoration_id는 반드시 위 소품 목록의 id 중에서
  고르세요. 사용자가 말한 물체가 소품 목록엔 없지만 **배경 실측 객체 목록**에 있다면
  이건 decoration_toggle이 아니라 background_object_edit입니다 (아래 참고).
  주의 1: 위 상품("{ad_state.get("product_visual_analysis", {}).get("category", "")}")
  자체의 일부(부품, 구성품 등)를 없애거나 바꿔달라는 요청은 소품이 아닙니다 - 상품은
  누끼 딴 사진 하나가 통째로 알파합성되는 것이라, 그 안의 일부만 지우거나 바꾸는 기능은
  없습니다. 이런 요청(예: 이어폰 세트 중 한쪽만 없애기, 상품 구성품 중 하나만 빼기)은
  decoration_toggle이나 unclear가 아니라 product_change로 분류하세요.
  주의 2: 각 feature 항목 옆에는 원래부터 작은 동그라미 아이콘이 자동으로 그려집니다
  (image-generation으로 만든 소품이 아니라, 텍스트 렌더러가 벡터로 그리는 장식임).
  "텍스트 옆에 동그라미/아이콘 추가해줘"처럼 들리는 요청은 실제로는 (a) 이미 있는
  feature의 아이콘을 말하는 것이거나 (b) 새로운 feature 항목 자체를 추가해 달라는
  뜻일 가능성이 높습니다. 이 파이프라인은 아직 자연어로 새 feature를 추가하는 기능이
  없으므로, 이런 요청은 decoration_toggle로 분류하지 말고 unclear로 분류한 뒤
  clarifying_question에 "현재는 기존 요소 수정/삭제만 가능하고 새 feature 추가는
  아직 지원하지 않는다"고 안내하세요.
  소품 목록에도, 배경 실측 객체 목록에도 없고 상품 자체도 아닌, 정말 뭘 말하는지 모를
  요청만 unclear로 두세요.
- background_object_edit: 사용자가 말한 물체가 **배경 실측 객체 목록**에 있는 경우
  (예: Planner가 계획하지 않았는데 gpt-image가 배경에 실수로 그려 넣은 물체). "OO 제거해줘",
  "OO만 줄여줘", "OO 더 크게" 같은 요청이 여기 해당합니다. target_object_id는 반드시
  배경 실측 객체 목록의 id 중에서 고르고, action과 modification_instruction을 채우세요.
  목록에 있는 이름과 사용자가 말한 표현이 다소 달라도(예: 목록엔 "은색 하이힐", 사용자는
  "구두") 같은 물체를 가리키면 매칭하세요.
- text_property: 텍스트의 크기/색/위치/정렬/문구 자체를 바꾸는 요청. "더 크게/작게"는
  size_operation/size_value로, 위치 이동은 new_x/new_y로, 정렬 자체를 바꾸는 요청은
  new_align으로 표현하세요. "가운데/정중앙으로 옮겨줘"는 위치 이동이 아니라 정렬
  변경이 핵심이므로 new_align="center"를 반드시 같이 설정하세요 (new_x만 0.5로
  주면 정렬이 그대로라 실제로 가운데에 오지 않습니다).
  색을 바꾸는 요청("빨간색으로", "노란색 말고 파란색으로")은 반드시 new_color(또는
  헤드라인 외곽선을 가리키면 new_outline_color)에 실제 RGB 값을 채우세요 - 색 이름만
  알아듣고 필드를 안 채우면 아무 변화도 안 일어납니다. "노란색이 아니라"처럼 현재 색을
  같이 언급했다면, 사용자가 말한 그 색이 실제로 headline.color인지 headline.outline_color
  인지 헷갈릴 수 있습니다 - 헤드라인에 굵은 테두리가 있는 포스터 스타일이면 눈에 잘
  띄는 색은 보통 outline_color 쪽이니 그쪽을 우선 의심하세요.
  요청이 "문구를 바꿔라/키워라/옮겨라"가 아니라 "이 요소 자체를 없애라/지워라/빼라"는
  뜻이면 (예: "노이즈캔슬링 문구 제거해줘", "서브헤드라인 빼줘", "배지 없애줘"),
  text_property_change.remove를 true로 설정하고 나머지 필드는 비워두세요.
  target이 feature면 feature_index로 어느 항목인지 반드시 특정하세요.
- background_brightness: "배경 더 밝게/어둡게/화사하게/차분하게"처럼 단순 밝기·톤 조정.
  큰 변화가 아니면 brightness_delta는 -0.3~0.3 정도의 작은 값으로 잡으세요.
- background_regenerate: 배경의 장면/분위기 자체를 바꾸고 싶은 요청 (밝기 조정보다 큰 변화).
  상품과 텍스트는 그대로 유지된다는 전제입니다.
- decoration_add: 지금 소품 목록에 없는 새로운 시각 요소를 추가해 달라는 요청.
  중요: "치즈가 흘러내리는", "물이 튀는", "연기가 나는", "꽃잎이 떨어지는", "불꽃이 튀는"처럼
  **상품 표면/주변에서 일어나는 현상을 묘사하는 요청도 대부분 여기 해당합니다** - 상품
  원본 픽셀을 바꾸지 않고도, 그 현상을 표현하는 새 이미지를 만들어서 상품 위에 겹쳐
  합성(placement_type="occluding")하면 시각적으로 동일한 결과를 만들 수 있기 때문입니다.
  이런 요청을 "상품 자체를 바꿔야만 가능하다"고 단정하지 말고, 먼저 겹쳐지는 소품으로
  표현 가능한지 검토하세요. decoration_addition.prompt는 상품이 아니라 그 현상/물체
  자체만 묘사하세요 (예: "melted cheese dripping in glossy strands" - 신발이나 원래
  상품을 다시 언급하지 않음).
- product_change: 소품을 겹쳐서는 표현할 수 없고, 상품 자체의 실제 색/형태/재질/구조를
  바꿔야만 가능한 요청 (예: "신발 색을 파란색으로 바꿔줘", "밑창 패턴을 다르게 해줘").
  이런 요청은 원본 상품과 달라질 위험이 있으므로 자동 실행하지 않고 사용자에게 경고만
  표시합니다. decoration_add로 해결 가능한 요청을 여기로 잘못 분류하지 않도록 항상
  먼저 검토하세요.
- unclear: 위 어디에도 명확히 안 맞거나, 요청이 모호함. clarifying_question에 되물을 질문을 쓰세요.

JSON만 출력하세요."""

    response = client.chat.completions.parse(
        model=settings.TEXT_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format=EditClassification,
    )
    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise RuntimeError(f"수정 요청 분류 실패 (모델 거부): {response.choices[0].message.refusal}")
    return parsed