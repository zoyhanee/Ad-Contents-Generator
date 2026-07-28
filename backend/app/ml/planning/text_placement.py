from app.ml.compositing.quiet_region_finder import find_quiet_region
from app.ml.planning.layout_vision_planner import plan_text_placement_from_image


def apply_quiet_region_placement(ad_state: dict) -> None:

    hl = ad_state.get("headline") or {}
    sl = ad_state.get("subheadline")
    badge = ad_state.get("badge")

    if not hl.get("text"):
        return

    hl_lines = max(1, str(hl.get("text", "")).count("\n") + 1)
    block_h_ratio = hl.get("font_size_ratio", 0.08) * hl_lines * 1.5
    if sl and sl.get("text"):
        block_h_ratio += sl.get("font_size_ratio", 0.03) * 3
    if badge and badge.get("text"):
        block_h_ratio += 0.05
    block_h_ratio = min(max(block_h_ratio, 0.12), 0.4)
    block_w_ratio = 0.42

    product_box = ad_state.get("product_box") or {}
    avoid_bbox = None
    if product_box:
        avoid_bbox = (
            product_box.get("x", 0), product_box.get("y", 0),
            product_box.get("x", 0) + product_box.get("width", 0),
            product_box.get("y", 0) + product_box.get("height", 0),
        )

    zone = find_quiet_region(
        ad_state["background_path"], block_w_ratio, block_h_ratio,
        avoid_bbox_ratio=avoid_bbox,
    )

    cursor_y = zone["y"]
    if badge and badge.get("text"):
        badge["x"], badge["y"] = zone["x"], cursor_y
        cursor_y += 0.05
    hl["x"], hl["y"] = zone["x"], cursor_y
    cursor_y += hl.get("font_size_ratio", 0.08) * hl_lines * 1.4
    if sl and sl.get("text"):
        sl["x"], sl["y"] = zone["x"], cursor_y


def apply_text_placement(ad_state: dict) -> None:

    hl = ad_state.get("headline") or {}
    sl = ad_state.get("subheadline")
    badge = ad_state.get("badge")

    if not hl.get("text"):
        return

    try:
        plan = plan_text_placement_from_image(
            ad_state["background_path"],
            ad_state.get("product_box") or {},
            has_subheadline=bool(sl and sl.get("text")),
            has_badge=bool(badge and badge.get("text")),
        )
    except Exception as e:
        print(f"⚠️ vision 기반 텍스트 배치 실패({e}) - 픽셀 분산 기반으로 폴백")
        apply_quiet_region_placement(ad_state)
        return

    hl["x"], hl["y"], hl["align"] = plan.headline.x, plan.headline.y, plan.headline.align
    if sl and sl.get("text") and plan.subheadline:
        sl["x"], sl["y"], sl["align"] = plan.subheadline.x, plan.subheadline.y, plan.subheadline.align
    if badge and badge.get("text") and plan.badge:
        badge["x"], badge["y"], badge["align"] = plan.badge.x, plan.badge.y, plan.badge.align
