import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

LIGHT_TO_SHADOW_OFFSET = {
    "upper_left": (20, 24),
    "upper_right": (-20, 24),
    "left": (24, 6),
    "right": (-24, 6),
    "front": (0, 16),
}


def create_projection_shadow(
    mask: Image.Image,
    offset: tuple[int, int],
    blur_radius: int = 24,
    opacity: int = 70,
) -> tuple[Image.Image, tuple[int, int]]:
    shadow_alpha = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    shadow_alpha = ImageEnhance.Brightness(shadow_alpha).enhance(opacity / 255)

    shadow = Image.new("RGBA", mask.size, (20, 15, 10, 0))
    shadow.putalpha(shadow_alpha)
    return shadow, offset


def _find_contact_line(mask: Image.Image, threshold: int = 30) -> tuple[int, int, int]:
    """마스크에서 실제로 상품이 존재하는 가장 아래쪽 행(y)과, 그 행 근처의 x범위를 찾는다.
    product_box와 원본 상품의 종횡비가 달라 letterbox 여백(투명 영역)이 위아래에 생기더라도,
    '박스의 맨 밑바닥'이 아니라 '실제 상품 픽셀이 끝나는 지점'을 정확히 찾는다."""
    arr = np.array(mask)
    h, w = arr.shape

    rows_with_product = np.where(arr.max(axis=1) > threshold)[0]
    if len(rows_with_product) == 0:
        # 상품이 전혀 없으면(마스크가 완전히 비었으면) 폴백으로 박스 맨 밑바닥 사용
        return 0, w, h - 1

    contact_y = int(rows_with_product.max())  # 실제 상품이 존재하는 가장 아래 행

    # 그 행 바로 위 얇은 밴드(전체 높이의 3%)에서 x범위를 측정
    band_top = max(0, contact_y - int(h * 0.03))
    band = arr[band_top:contact_y + 1, :]
    cols_with_product = np.where(band.max(axis=0) > threshold)[0]
    if len(cols_with_product) == 0:
        return 0, w, contact_y

    x_min, x_max = int(cols_with_product.min()), int(cols_with_product.max())
    return x_min, x_max, contact_y


def create_contact_shadow(
    canvas_size: tuple[int, int],
    bbox: tuple[int, int, int, int],
    mask: Image.Image,
    opacity: int = 100,
    blur_radius: int = 14,
) -> Image.Image:
    """상품이 실제로 바닥에 닿는 부분(마스크 최하단부)만 기준으로 좁고 진한 그림자를 그린다."""
    dest_x, dest_y, dest_x2, dest_y2 = bbox

    x_min, x_max, contact_y_local = _find_contact_line(mask)
    contact_width = x_max - x_min
    contact_x_center = dest_x + (x_min + x_max) // 2
    contact_y = dest_y + contact_y_local

    shadow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)

    half_w = max(int(contact_width * 0.55), 10)
    ellipse_box = (
        contact_x_center - half_w,
        contact_y - int(contact_width * 0.05),
        contact_x_center + half_w,
        contact_y + int(contact_width * 0.10),
    )
    draw.ellipse(ellipse_box, fill=(15, 10, 8, opacity))
    return shadow.filter(ImageFilter.GaussianBlur(blur_radius))
