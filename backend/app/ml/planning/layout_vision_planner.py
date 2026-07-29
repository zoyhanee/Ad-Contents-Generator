"""
실제로 생성된 배경 이미지를 GPT-vision에게 보여주고, 헤드라인/서브헤드라인/배지를
어디에 놓으면 좋을지 물어본다. quiet_region_finder.py(픽셀 분산 계산)보다 구도
균형·시선 흐름 같은 판단까지 반영할 수 있다. API 실패 시 quiet_region_finder로
폴백하는 걸 권장한다 (app.ml.planning.text_placement.apply_text_placement 참고).
"""
import base64
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


class TextPlacement(BaseModel):
    x: float = Field(description="0~1 비율, 텍스트 블록의 왼쪽 시작 x좌표")
    y: float = Field(description="0~1 비율, 텍스트 블록의 위쪽 시작 y좌표")
    align: Literal["left", "center", "right"] = Field(default="left")


class VisionLayoutPlan(BaseModel):
    reasoning: str = Field(
        description="이 배치를 선택한 이유 (구도/균형/시선흐름 관점에서 한 문장, 디버깅용)"
    )
    headline: TextPlacement
    subheadline: Optional[TextPlacement] = None
    badge: Optional[TextPlacement] = None


def plan_text_placement_from_image(
    background_path: str,
    product_box: dict,
    has_subheadline: bool,
    has_badge: bool,
) -> VisionLayoutPlan:
    """실제로 생성된 배경 이미지를 보고, 헤드라인/서브헤드라인/배지를 어디에
    놓을지 다시 기획한다. product_box와 겹치지 않는 선에서, 여백뿐 아니라
    시각적 균형까지 고려하도록 지시한다."""
    client = _get_client()
    with open(background_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    elements = "headline" + (", subheadline" if has_subheadline else "") + (", badge" if has_badge else "")
    px1 = product_box.get("x", 0)
    py1 = product_box.get("y", 0)
    px2 = px1 + product_box.get("width", 0)
    py2 = py1 + product_box.get("height", 0)

    prompt = f"""당신은 광고 레이아웃을 기획하는 아트 디렉터입니다.

이 배경 이미지를 실제로 보고, 다음 텍스트 요소({elements})를 어디에 배치하면
가장 자연스럽고 균형 잡힌 구도가 될지 판단하세요.

=== 절대 규칙 ===
- 상품이 배치될 영역(x: {px1:.2f}~{px2:.2f}, y: {py1:.2f}~{py2:.2f}, 비율 좌표)과
  절대 겹치지 마세요. 이 영역은 지금 비어있지만 나중에 상품이 합성될 자리입니다.
- 이미지를 실제로 보고, 디테일이 적고 여백이 있는 영역을 우선하세요 (배경이
  복잡한 곳에 텍스트를 놓으면 안 읽힙니다).
- 시각적 균형과 시선 흐름을 고려하세요 (예: 상품 영역이 오른쪽이면 텍스트는
  왼쪽 여백에 두는 게 자연스러운지, 배경 자체가 특정 방향의 흐름/대각선을
  암시한다면 그 흐름을 따라가는 게 나은지 등을 실제 이미지를 보고 판단하세요).
- x, y는 텍스트 블록의 왼쪽 위 시작점 기준 0~1 비율입니다.
- subheadline/badge는 요청된 요소({elements})에 포함된 경우에만 채우고,
  포함 안 됐으면 null로 두세요.

JSON만 출력하세요."""

    response = client.chat.completions.parse(
        model=settings.TEXT_MODEL_NAME,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
            ],
        }],
        response_format=VisionLayoutPlan,
    )
    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise RuntimeError(f"텍스트 배치 기획 실패 (모델 거부): {response.choices[0].message.refusal}")
    return parsed
