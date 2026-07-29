from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BACKEND_DIR = Path(__file__).resolve().parents[3]
FONT_DIR = BACKEND_DIR / "assets" / "fonts"

FONT_CANDIDATES = [
    str(FONT_DIR / "NotoSansKR-Bold.ttf"),
]
REGULAR_FONT_CANDIDATES = [
    str(FONT_DIR / "NotoSansKR-Regular.ttf"),
]


def _find_font(bold: bool = False) -> str | None:
    candidates = FONT_CANDIDATES if bold else REGULAR_FONT_CANDIDATES
    for path in candidates:
        if Path(path).exists():
            return path
    other = REGULAR_FONT_CANDIDATES if bold else FONT_CANDIDATES
    for path in other:
        if Path(path).exists():
            return path
    return None


def _text_width(draw, text, font, space_width_ratio=0.28, stroke_width=0):
    words = text.split(" ")
    space_w = int(font.size * space_width_ratio)
    total = 0
    for i, word in enumerate(words):
        if word:
            bbox = draw.textbbox((0, 0), word, font=font, stroke_width=stroke_width)
            total += bbox[2] - bbox[0]
        if i < len(words) - 1:
            total += space_w
    return total


def _draw_text_no_space_glyph(
    draw, xy, text, font, fill, align="left", space_width_ratio=0.28,
    stroke_width=0, stroke_fill=None,
):
    words = text.split(" ")
    space_width = int(font.size * space_width_ratio)
    total_w = _text_width(draw, text, font, space_width_ratio, stroke_width=stroke_width)

    x, y = xy
    if align == "center":
        x -= total_w // 2
    elif align == "right":
        x -= total_w

    for i, word in enumerate(words):
        if word:
            draw.text(
                (x, y), word, font=font, fill=fill,
                stroke_width=stroke_width, stroke_fill=stroke_fill,
            )
            bbox = draw.textbbox((x, y), word, font=font, stroke_width=stroke_width)
            x = bbox[2]
        if i < len(words) - 1:
            x += space_width
    return x


def _fit_text_to_width(draw, text, font_path, initial_size, max_width_px, min_size=20):
    if not font_path:
        return ImageFont.load_default()
    size = initial_size
    while size > min_size:
        font = ImageFont.truetype(font_path, size)
        if _text_width(draw, text, font) <= max_width_px:
            return font
        size -= 2
    return ImageFont.truetype(font_path, min_size)


def _draw_wrapped_text(draw, xy, text, font, fill, max_width_px, align="left", line_gap=1.4):
    manual_lines = text.split("\n")
    lines = []
    for manual_line in manual_lines:
        words = manual_line.split(" ")
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if _text_width(draw, test_line, font) > max_width_px and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

    x, y = xy
    line_height = int(font.size * line_gap)
    for i, line in enumerate(lines):
        _draw_text_no_space_glyph(draw, (x, y + i * line_height), line, font, fill, align=align)
    return len(lines)


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast_ratio(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> float:
    l1, l2 = _relative_luminance(rgb1), _relative_luminance(rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def _pick_text_colors(canvas: Image.Image, x_ratio: float, y_ratio: float,
                       w_ratio: float = 0.35, h_ratio: float = 0.35) -> dict:
    width, height = canvas.size
    x1, y1 = int(x_ratio * width), int(y_ratio * height)
    x2 = min(width, x1 + int(w_ratio * width))
    y2 = min(height, y1 + int(h_ratio * height))
    if x2 <= x1 or y2 <= y1:
        avg_brightness = 200
    else:
        region = np.array(canvas.crop((x1, y1, x2, y2)).convert("L"))
        avg_brightness = region.mean()

    if avg_brightness > 140:
        return {"headline": (15, 15, 15), "subheadline": (55, 55, 55), "feature_title": (25, 25, 25), "feature_desc": (95, 90, 85)}
    else:
        return {"headline": (245, 245, 245), "subheadline": (215, 215, 215), "feature_title": (235, 235, 235), "feature_desc": (185, 180, 175)}


def _fit_text_block_to_width(draw, text, font_path, initial_size, max_width_px, min_size=20, line_gap=1.25, stroke_width=0):

    size = initial_size
    while size > min_size:
        font = ImageFont.truetype(font_path, size)
        lines = text.split("\n")
        if all(_text_width(draw, line, font, stroke_width=stroke_width) <= max_width_px for line in lines):
            return font, lines
        size -= 2
    font = ImageFont.truetype(font_path, min_size)
    return font, text.split("\n")


def render_text_layer(background_image_path, brief, output_path, canvas_size=(2480, 3508), right_margin_ratio=0.05):
    width, height = canvas_size
    canvas = Image.open(background_image_path).convert("RGB").resize((width, height))
    draw = ImageDraw.Draw(canvas)
    bold_path, regular_path = _find_font(bold=True), _find_font(bold=False)

    def get_font(size, bold=False):
        path = bold_path if bold else regular_path
        return ImageFont.truetype(path, max(size, 12)) if path else ImageFont.load_default()

    def ensure_readable_color(x_ratio, y_ratio, w_ratio, h_ratio, gpt_color, role, min_contrast=3.0):

        width_, height_ = canvas.size
        x1, y1 = int(x_ratio * width_), int(y_ratio * height_)
        x2 = min(width_, x1 + max(int(w_ratio * width_), 1))
        y2 = min(height_, y1 + max(int(h_ratio * height_), 1))
        if x2 <= x1 or y2 <= y1:
            return gpt_color
        region = np.array(canvas.crop((x1, y1, x2, y2)).convert("RGB")).reshape(-1, 3)
        avg_bg = tuple(int(v) for v in region.mean(axis=0))
        if _contrast_ratio(gpt_color, avg_bg) >= min_contrast:
            return gpt_color
        # 대비 부족 -> 배경 밝기 기준 안전한 색으로 교체
        return _pick_text_colors(canvas, x_ratio, y_ratio, w_ratio, h_ratio)[role]

    hl = brief.get("headline", {})
    text_x_ratio = hl.get("x", 0.6)

    # typography_style 반영: soft_editorial이면 헤드라인에 bold 대신 regular
    # 폰트를 쓰고 줄간격을 넉넉하게, bold_modern이면 두껍고 타이트하게.
    typography_style = brief.get("typography_style", "bold_modern")
    is_editorial = typography_style == "soft_editorial"
    headline_font_path_choice = regular_path if is_editorial else bold_path
    headline_line_gap = 1.45 if is_editorial else 1.25
    subheadline_line_gap = 1.65 if is_editorial else 1.4
    feature_title_bold = not is_editorial
    icon_outline_width = 2 if is_editorial else 3

    # 이 광고에 실제로 등장하는 모든 텍스트 컬럼의 x좌표를 미리 모아둠
    column_x_positions = set()
    if hl.get("text"):
        column_x_positions.add(hl.get("x", text_x_ratio))
    sl = brief.get("subheadline")
    if sl and sl.get("text"):
        column_x_positions.add(sl.get("x", text_x_ratio))
    for feat in brief.get("features", []):
        column_x_positions.add(feat.get("x", text_x_ratio))
    sorted_column_x = sorted(column_x_positions)

    def remaining_width(x_ratio):
        start_px = int(x_ratio * width)
        # 이 x보다 오른쪽에 있는 가장 가까운 다른 컬럼이 있으면, 그 컬럼을 침범하지 않도록 거기까지만 폭을 허용
        # 겹침 방지. 오차 범위(0.01) 안의 값은 같은 컬럼으로 취급.
        next_columns = [c for c in sorted_column_x if c > x_ratio + 0.01]
        if next_columns:
            boundary_px = int(min(next_columns) * width)
            gutter_px = int(width * 0.03)
            return max(boundary_px - start_px - gutter_px, 100)
        return max(width - start_px - int(width * right_margin_ratio), 100)

    column_cursors = {}
    def get_cursor(x_ratio, default_y):
        key = round(x_ratio, 2)
        if key not in column_cursors:
            column_cursors[key] = int(default_y * height)
        return column_cursors[key]
    def advance_cursor(x_ratio, delta_px):
        key = round(x_ratio, 2)
        column_cursors[key] = column_cursors.get(key, 0) + delta_px

    ## 배지 ##
    badge = brief.get("badge")
    if badge and badge.get("text"):
        badge_font = get_font(36, bold=True)
        bx, by = int(badge["x"] * width), int(badge["y"] * height)
        text_bbox = draw.textbbox((0, 0), badge["text"], font=badge_font)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        pad_x, pad_y = 20, 14
        if badge.get("align") == "center":
            bx -= (text_w + pad_x * 2) // 2
        draw.rounded_rectangle([bx, by, bx + text_w + pad_x*2, by + text_h + pad_y*2], radius=28, fill=(26,26,26))
        draw.text((bx+pad_x, by+pad_y-text_bbox[1]), badge["text"], font=badge_font, fill=(255,255,255))

    ## 헤드라인 ##
    cursor_y = int(hl.get("y", 0.1) * height)
    if hl.get("text"):
        x_r = hl.get("x", text_x_ratio)
        cursor_y = get_cursor(x_r, hl.get("y", 0.1))
        avail_w = remaining_width(x_r)

        outline_color = hl.get("outline_color")
        stroke_width = int(hl.get("outline_width") or 0) if outline_color else 0
        stroke_fill = tuple(outline_color) if outline_color else None

        headline_font, hl_lines = _fit_text_block_to_width(
            draw, hl["text"], headline_font_path_choice,
            initial_size=int(width * hl.get("font_size_ratio", 0.06)), max_width_px=avail_w,
            stroke_width=stroke_width,
        )
        line_h = int(headline_font.size * headline_line_gap)
        headline_color = ensure_readable_color(
            x_r, hl.get("y", 0.1),
            w_ratio=avail_w / width, h_ratio=(len(hl_lines) * line_h) / height,
            gpt_color=tuple(hl.get("color", [15, 15, 15])), role="headline", min_contrast=3.0,
        )
        for i, line in enumerate(hl_lines):
            _draw_text_no_space_glyph(draw, (int(x_r*width), cursor_y + i*line_h),
                line, headline_font, headline_color, align=hl.get("align", "left"),
                stroke_width=stroke_width, stroke_fill=stroke_fill)
        advance_cursor(x_r, len(hl_lines) * line_h + int(height * 0.025))

    ##서브헤드라인 ##
    sl = brief.get("subheadline")
    if sl and sl.get("text"):
        x_r = sl.get("x", text_x_ratio)
        cursor_y = get_cursor(x_r, sl.get("y", 0.2))
        sub_font = get_font(int(width * sl.get("font_size_ratio", 0.03)), bold=False)
        avail_w = remaining_width(x_r)
        approx_lines = max(1, len(sl["text"]) * sub_font.size // max(avail_w, 1) + 1)
        sub_color = ensure_readable_color(
            x_r, sl.get("y", 0.2),
            w_ratio=avail_w / width, h_ratio=(approx_lines * sub_font.size * 1.4) / height,
            gpt_color=tuple(sl.get("color", [55, 55, 55])), role="subheadline", min_contrast=4.5,
        )
        n_lines = _draw_wrapped_text(draw, (int(x_r*width), cursor_y), sl["text"], sub_font,
            sub_color, max_width_px=avail_w, align=sl.get("align", "left"), line_gap=subheadline_line_gap)
        advance_cursor(x_r, n_lines * int(sub_font.size * subheadline_line_gap) + int(height * 0.035))

    ## Feature ##
    features = brief.get("features", [])
    title_font = get_font(int(width * 0.024), bold=feature_title_bold)
    desc_font = get_font(int(width * 0.017), bold=False)
    icon_size, text_offset_x = 44, 58
    title_h = int(title_font.size * 1.2)

    for idx, feat in enumerate(features):
        x_r = feat.get("x", text_x_ratio)
        fx = int(x_r * width)
        fy = get_cursor(x_r, feat.get("y", 0.5))
        title = feat.get("title", "")
        desc = feat.get("description", "")

        avail_w = remaining_width(x_r) - text_offset_x

        title_color = ensure_readable_color(
            x_r, feat.get("y", 0.5), w_ratio=avail_w / width, h_ratio=title_h / height,
            gpt_color=tuple(feat.get("title_color", [25, 25, 25])), role="feature_title", min_contrast=3.0,
        )
        desc_color = ensure_readable_color(
            x_r, feat.get("y", 0.5) + (title_h / height), w_ratio=avail_w / width, h_ratio=(desc_font.size * 2.8) / height,
            gpt_color=tuple(feat.get("desc_color", [95, 90, 85])), role="feature_desc", min_contrast=4.5,
        )

        draw.ellipse([fx, fy, fx+icon_size, fy+icon_size], outline=(60,60,60), width=icon_outline_width)
        _draw_text_no_space_glyph(draw, (fx+text_offset_x, fy), title, title_font, title_color)
        desc_lines = 0
        if desc:
            desc_lines = _draw_wrapped_text(draw, (fx+text_offset_x, fy+title_h), desc, desc_font,
                desc_color, max_width_px=max(avail_w, 100))
        block_height = max(icon_size, title_h + desc_lines * int(desc_font.size * 1.4))

        if feat.get("divider_after"):
            divider_color = tuple(feat.get("divider_color", [200, 195, 188]))
            line_y = fy + block_height + int(height * 0.012)
            draw.line([(fx, line_y), (fx + int(width * 0.22), line_y)], fill=divider_color, width=2)

        advance_cursor(x_r, block_height + int(height * 0.028))

    canvas.save(output_path)
