import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from app.ml.compositing.shadow import create_contact_shadow, create_projection_shadow, LIGHT_TO_SHADOW_OFFSET
from app.ml.compositing.tone_matching import match_product_tone_to_scene


def _feather_edges(mask: Image.Image, radius: int = 2) -> Image.Image:
    return mask.filter(ImageFilter.GaussianBlur(radius))


def _apply_grain(image: Image.Image, strength: int = 2, protect_mask: Image.Image | None = None) -> Image.Image:
    arr = np.array(image.convert("RGB")).astype(np.int16)
    noise = np.random.randint(-strength, strength + 1, arr.shape, dtype=np.int16)
    if protect_mask is not None:
        protect = np.array(protect_mask.resize(image.size), dtype=np.float32) / 255.0
        noise = (noise * (1.0 - protect)[..., None]).astype(np.int16)
    return Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8), "RGB")


def _bbox_overlap_ratio(deco_bbox_px, protected_bbox_px) -> float:
    dx1, dy1, dx2, dy2 = deco_bbox_px
    px1, py1, px2, py2 = protected_bbox_px
    ix1, iy1 = max(dx1, px1), max(dy1, py1)
    ix2, iy2 = min(dx2, px2), min(dy2, py2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter_area = (ix2 - ix1) * (iy2 - iy1)
    protected_area = max(1, (px2 - px1) * (py2 - py1))
    return inter_area / protected_area


def _surface_mask(canvas_size: tuple[int, int], polygon_ratio: list[list[float]]) -> Image.Image:
    w, h = canvas_size
    mask = Image.new("L", canvas_size, 0)
    draw = ImageDraw.Draw(mask)
    pts = [(x * w, y * h) for x, y in polygon_ratio]
    draw.polygon(pts, fill=255)
    return mask


def composite_full_scene(
    background_path: str,
    product_fg_path: str,
    product_mask_path: str,
    product_box: dict,
    light_direction: str,
    decorations: list[dict],
    decoration_image_paths: dict[str, str],
    output_path: str,
    tone_match_strength: float = 0.35,
    surfaces: list[dict] | None = None,
    protected_regions: list[dict] | None = None,
    excluded_decoration_ids: set[str] | None = None,
    protected_overlap_threshold: float = 0.25,
    needs_contact_shadow: bool = True,
) -> tuple[str, tuple[int, int, int, int]]:

    background = Image.open(background_path).convert("RGBA")
    canvas_w, canvas_h = background.size
    surfaces = surfaces or []
    protected_regions = protected_regions or []
    excluded_decoration_ids = excluded_decoration_ids or set()

    def to_px(box: dict) -> tuple[int, int, int, int]:
        return (
            int(box["x"] * canvas_w), int(box["y"] * canvas_h),
            int(box["width"] * canvas_w), int(box["height"] * canvas_h),
        )

    def to_px_bbox(box: dict) -> tuple[int, int, int, int]:
        x, y, w, h = to_px(box)
        return (x, y, x + w, y + h)

    surface_masks = {s["id"]: _surface_mask(background.size, s["polygon"]) for s in surfaces}
    protected_bboxes_px = [
        (r["name"], (
            int(r["bbox"][0] * canvas_w), int(r["bbox"][1] * canvas_h),
            int(r["bbox"][2] * canvas_w), int(r["bbox"][3] * canvas_h),
        ))
        for r in protected_regions
    ]

    result = background.copy()

    px, py, pw, ph = to_px(product_box)

    original_fg = Image.open(product_fg_path).convert("RGBA")
    orig_w, orig_h = original_fg.size
    scale = min(pw / orig_w, ph / orig_h)
    new_w, new_h = max(1, int(orig_w * scale)), max(1, int(orig_h * scale))

    fg_resized = original_fg.resize((new_w, new_h), Image.LANCZOS)
    mask_resized = Image.open(product_mask_path).convert("L").resize((new_w, new_h), Image.LANCZOS)

    offset_x, offset_y = (pw - new_w) // 2, (ph - new_h) // 2
    product_fg = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    product_mask = Image.new("L", (pw, ph), 0)
    product_fg.paste(fg_resized, (offset_x, offset_y), fg_resized)
    product_mask.paste(mask_resized, (offset_x, offset_y))

    product_fg.putalpha(_feather_edges(product_mask))
    product_bbox = (px + offset_x, py + offset_y, px + offset_x + new_w, py + offset_y + new_h)

    # 톤 매칭: 배경 국소 조명에 맞춰 색상/밝기만 통계적으로 조정
    product_fg = match_product_tone_to_scene(
        product_fg, background, product_bbox, strength=tone_match_strength
    )

    # 소품 필터링: 제외 요청된 id 제거 + 보호영역을 많이 가리는 소품 제거
    active_decorations = []
    for deco in decorations:
        if deco["id"] in excluded_decoration_ids:
            continue
        deco_bbox_px = to_px_bbox(deco)
        blocked = False
        for name, region_bbox_px in protected_bboxes_px:
            if _bbox_overlap_ratio(deco_bbox_px, region_bbox_px) >= protected_overlap_threshold:
                print(f"⚠️ 소품 '{deco['id']}'가 보호 영역 '{name}'을 {protected_overlap_threshold:.0%} "
                      f"이상 가려서 배치에서 제외함")
                blocked = True
                break
        if not blocked:
            active_decorations.append(deco)

    def draw_decoration(result_img, deco):
        dx, dy, dw, dh = to_px(deco)
        deco_img = Image.open(decoration_image_paths[deco["id"]]).convert("RGBA").resize((dw, dh), Image.LANCZOS)
        if deco.get("rotation"):
            deco_img = deco_img.rotate(deco["rotation"], expand=True)

        min_dim_ratio = min(dw / canvas_w, dh / canvas_h)
        is_too_thin_for_shadow = min_dim_ratio < 0.015
        if deco["placement_type"] in ("on_surface", "behind_product") and not is_too_thin_for_shadow:
            deco_shadow = create_contact_shadow(
                background.size, (dx, dy, dx + dw, dy + dh),
                mask=deco_img.getchannel("A"), opacity=60, blur_radius=10,
            )
            surface_id = deco.get("surface_id")
            if surface_id and surface_id in surface_masks:
                # 그림자가 표면(surface) 밖으로 새지 않도록 교집합만 남김
                shadow_alpha = np.array(deco_shadow.getchannel("A")).astype(np.float32)
                mask_alpha = np.array(surface_masks[surface_id]).astype(np.float32) / 255.0
                clipped = (shadow_alpha * mask_alpha).astype(np.uint8)
                deco_shadow.putalpha(Image.fromarray(clipped, "L"))
            result_img = Image.alpha_composite(result_img, deco_shadow)
        result_img.alpha_composite(deco_img, (dx, dy))
        return result_img

    # 상품보다 뒤에 있어야 하는 소품 먼저 그림 (예: 상품 뒤에 살짝 보이는 물건)
    behind_decorations = [d for d in active_decorations if d["placement_type"] == "behind_product"]
    for deco in behind_decorations:
        result = draw_decoration(result, deco)

    # 투영 그림자 (조명 방향 반영)
    offset = LIGHT_TO_SHADOW_OFFSET.get(light_direction, (20, 24))
    projection_shadow, _ = create_projection_shadow(product_mask, offset)
    shadow_canvas = Image.new("RGBA", background.size, (0, 0, 0, 0))
    shadow_canvas.alpha_composite(projection_shadow, (px + offset[0], py + offset[1]))
    result = Image.alpha_composite(result, shadow_canvas)

    # 접지 그림자 (벽걸이 등 바닥에 안 닿는 상품이면 생략)
    if needs_contact_shadow:
        contact_shadow = create_contact_shadow(background.size, product_bbox, mask=product_mask)
        result = Image.alpha_composite(result, contact_shadow)

    # 상품 합성
    result.alpha_composite(product_fg, (px, py))

    # 상품보다 앞에 있어야 하는 소품 (occluding 먼저, on_surface 나중 — 표면 위 소품이 최상단)
    front_decorations = [d for d in active_decorations if d["placement_type"] != "behind_product"]
    ordered = sorted(front_decorations, key=lambda d: 0 if d["placement_type"] == "occluding" else 1)
    for deco in ordered:
        result = draw_decoration(result, deco)

    product_full_mask = Image.new("L", background.size, 0)
    product_full_mask.paste(product_fg.getchannel("A"), (px, py))
    final = _apply_grain(result.convert("RGB"), strength=2, protect_mask=product_full_mask)
    final.save(output_path)
    return output_path, product_bbox
