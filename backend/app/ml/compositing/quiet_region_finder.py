import numpy as np
from PIL import Image


def find_quiet_region(
    background_path: str,
    region_w_ratio: float,
    region_h_ratio: float,
    avoid_bbox_ratio: tuple[float, float, float, float] | None = None,
    margin_ratio: float = 0.04,
) -> dict:
    """region_w_ratio x region_h_ratio 크기의 사각형을 캔버스 위에서 슬라이딩하며,
    디테일(밝기 표준편차)이 가장 적은 위치를 찾는다.

    avoid_bbox_ratio: (x1, y1, x2, y2) 비율 좌표 - 이 영역(보통 product_box)과
    겹치는 후보는 제외한다.
    margin_ratio: 캔버스 가장자리에서 이 비율만큼은 후보에서 제외한다 (텍스트가
    가장자리에 너무 붙지 않도록).

    반환: {"x", "y", "width", "height", "variance"} (전부 0~1 비율 좌표).
    적당한 후보를 못 찾으면 variance=None과 함께 안전한 기본 위치를 반환한다.
    """
    img = Image.open(background_path).convert("L")
    w, h = img.size
    gray = np.array(img, dtype=np.float32)

    region_w_px = max(int(region_w_ratio * w), 1)
    region_h_px = max(int(region_h_ratio * h), 1)
    margin_px = int(margin_ratio * min(w, h))

    step_x = max(region_w_px // 3, 8)
    step_y = max(region_h_px // 3, 8)

    avoid_px = None
    if avoid_bbox_ratio:
        ax1, ay1, ax2, ay2 = avoid_bbox_ratio
        avoid_px = (int(ax1 * w), int(ay1 * h), int(ax2 * w), int(ay2 * h))

    best_xy = None
    best_variance = None

    y = margin_px
    while y + region_h_px <= h - margin_px:
        x = margin_px
        while x + region_w_px <= w - margin_px:
            if avoid_px is not None:
                ox1, oy1, ox2, oy2 = avoid_px
                ix1, iy1 = max(x, ox1), max(y, oy1)
                ix2, iy2 = min(x + region_w_px, ox2), min(y + region_h_px, oy2)
                if ix2 > ix1 and iy2 > iy1:
                    x += step_x
                    continue  # product_box와 겹치는 후보는 건너뜀

            patch = gray[y:y + region_h_px, x:x + region_w_px]
            variance = float(patch.std())

            if best_variance is None or variance < best_variance:
                best_variance = variance
                best_xy = (x, y)

            x += step_x
        y += step_y

    if best_xy is None:
        # 캔버스가 너무 작거나 avoid_bbox가 너무 커서 후보가 하나도 없었던 경우 -
        # 안전한 기본 위치(좌상단)로 폴백함.
        return {
            "x": margin_ratio, "y": margin_ratio,
            "width": region_w_ratio, "height": region_h_ratio,
            "variance": None,
        }

    bx, by = best_xy
    return {
        "x": bx / w, "y": by / h,
        "width": region_w_ratio, "height": region_h_ratio,
        "variance": best_variance,
    }
