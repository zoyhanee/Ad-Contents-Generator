"""
OpenAI images.edit용 마스크 생성 헬퍼.

마스크 규약: 이미지와 같은 크기의 PNG에서, 투명인 영역이 다시 그릴 곳,
불투명한 영역이 "그대로 보존할 곳"이다. Object Inventory(analyze_background_objects)가
찾아낸 bbox를 이 규약에 맞는 마스크로 변환하는 역할만 한다.
"""
from PIL import Image, ImageDraw


def build_edit_mask(
    canvas_size: tuple[int, int],
    bbox_ratio: list[float],
    padding_ratio: float = 0.03,
) -> Image.Image:
    """bbox_ratio([x1,y1,x2,y2], 0~1 비율) 영역을 투명하게(=편집 대상) 뚫은 마스크를 만든다.

    padding_ratio: bbox 경계에 딱 맞춰 자르면 물체의 그림자/경계 일부가 남아 어색하게
    잘릴 수 있어서, 캔버스 짧은 변 기준 이 비율만큼 여유를 더 넓혀서 뚫는다.
    """
    w, h = canvas_size
    x1, y1, x2, y2 = bbox_ratio
    pad_px = int(padding_ratio * min(w, h))

    px1 = max(0, int(x1 * w) - pad_px)
    py1 = max(0, int(y1 * h) - pad_px)
    px2 = min(w, int(x2 * w) + pad_px)
    py2 = min(h, int(y2 * h) + pad_px)

    # 불투명(alpha=255)한 캔버스에서 시작해서, 편집할 영역만 투명(alpha=0)하게 뚫음.
    mask = Image.new("RGBA", canvas_size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(mask)
    draw.rectangle([px1, py1, px2, py2], fill=(255, 255, 255, 0))
    return mask
