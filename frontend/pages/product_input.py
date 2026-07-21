from io import BytesIO

import requests
import streamlit as st
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
from streamlit.runtime.uploaded_file_manager import UploadedFile

from api.client import APIError
from api.product import (
    create_product,
    get_product_image,
    update_product,
    upload_product_image,
)
from components.header import render_header
from utils.state import clear_after_product


register_heif_opener()


def normalize_uploaded_image(
    uploaded_file: UploadedFile,
) -> BytesIO:
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)

    if image.mode != "RGB":
        image = image.convert("RGB")

    buffer = BytesIO()
    image.save(
        buffer,
        format="JPEG",
        quality=95,
    )

    buffer.seek(0)

    buffer.name = (
        uploaded_file.name.rsplit(".", 1)[0]
        + ".jpg"
    )
    buffer.type = "image/jpeg"

    return buffer


def format_product_price():
    value = st.session_state.get(
        "product_price_input",
        "",
    )

    digits = value.replace(",", "").strip()

    if digits.isdigit():
        st.session_state.product_price_input = (
            f"{int(digits):,}"
        )
    
    
def render_product_input():
    # 1. 상품 입력 상태 초기화
    if "product_industry" not in st.session_state:
        st.session_state.product_industry = "restaurant"
    
    is_editing = st.session_state.get(
        "editing_product",
        False,
    )

    # 수정 모드 진입 시 최신 상품 정보를 입력 위젯에 한 번만 반영
    if is_editing:
        current_product = st.session_state.get("product")
        current_product_id = st.session_state.get("product_id")
        edit_init_key = f"product_edit_initialized_{current_product_id}"

        if (
            current_product is not None
            and edit_init_key not in st.session_state
        ):
            st.session_state.product_name_input = (
                current_product.get("name", "")
            )
            st.session_state.product_price_input = (
                f"{int(current_product.get('price', 0)):,}"
            )
            st.session_state.product_description_input = (
                current_product.get("description", "")
            )
            st.session_state.product_industry = (
                current_product.get("industry", "restaurant")
            )

            # 수정 화면 진입 시 이전 업로드 파일 상태 제거
            st.session_state.pop("product_image", None)
            st.session_state[edit_init_key] = True

    # 2. 공통 헤더
    render_header()

    # 3. 페이지 제목 + Stepper
    st.html(
        """
        <div class="product-page-head">
            <div class="page-title-wrap">
                <div class="step-badge">1</div>

                <div>
                    <h1>상품 정보 입력</h1>
                    <p>
                        상품 정보를 입력하면 최적의 광고 전략과
                        콘텐츠를 추천해드려요.
                    </p>
                </div>
            </div>

            <div class="stepper">
                <div class="step-item active">
                    <div class="step-dot">1</div>
                    <span>상품 정보</span>
                </div>

                <div class="step-line"></div>

                <div class="step-item">
                    <div class="step-dot">2</div>
                    <span>광고 전략</span>
                </div>

                <div class="step-line"></div>

                <div class="step-item">
                    <div class="step-dot">3</div>
                    <span>A/B 생성</span>
                </div>

                <div class="step-line"></div>

                <div class="step-item">
                    <div class="step-dot">4</div>
                    <span>결과 선택</span>
                </div>
            </div>
        </div>
        """
    )

    # 4. 상품 입력 레이아웃
    upload_col, form_col = st.columns(
        [0.9, 1.1],
        gap="large",
    )
    
    # 5. 상품 이미지 업로드
    with upload_col:
        st.html(
            """
            <div class="upload-card-head">
                <div class="upload-icon">☁</div>
                <h2>상품 이미지 업로드</h2>
                <p class="upload-main">
                    대표 상품 사진을 올려주세요
                </p>
                <p class="upload-sub">
                    JPG, PNG, WebP, HEIC 파일 지원 (최대 10MB)
                </p>
            </div>
            """
        )

        st.html(
            """
            <style>
            .st-key-product_image {
                margin-top: 22px;
            }

            .st-key-product_image [data-testid="stFileUploaderDropzone"] {
                min-height: 150px;
                padding: 24px;
                border: 1.5px dashed #b9c8c0;
                border-radius: 14px;
                background: #f8fbf9;
            }

            .st-key-product_image [data-testid="stFileUploaderDropzone"]:hover {
                border-color: #0f8a5f;
                background: #f4fbf7;
            }

            .st-key-product_image button {
                border: none;
                border-radius: 10px;
                background: #0f8a5f;
                color: #ffffff;
                font-weight: 700;
            }

            .st-key-product_image button:hover {
                border: none;
                background: #0b7651;
                color: #ffffff;
            }
            </style>
            """
        )

        uploaded_image = st.file_uploader(
            "상품 이미지 선택",
            type=["jpg", "jpeg", "png", "webp", "heic", "heif"],
            key="product_image",
            label_visibility="collapsed",
        )
        
        normalized_image = None

        if uploaded_image is not None:
            try:
                normalized_image = normalize_uploaded_image(
                    uploaded_image
                )

                st.image(
                    normalized_image,
                    caption="업로드된 상품 이미지",
                    use_container_width=True,
                )

            except Exception:
                st.error(
                    "이미지를 처리할 수 없습니다. "
                    "지원되는 이미지 파일인지 확인해주세요."
                )
        
        elif is_editing:
            try:
                product_id = st.session_state.product_id
                cache_key = f"editing_product_image_{product_id}"

                if cache_key not in st.session_state:
                    image_bytes, image_type = get_product_image(
                        product_id
                    )

                    st.session_state[cache_key] = {
                        "bytes": image_bytes,
                        "content_type": image_type,
                    }

                cached_image = st.session_state[cache_key]

                st.image(
                    cached_image["bytes"],
                    caption="현재 상품 이미지",
                    use_container_width=True,
                )

            except APIError as e:
                st.error(str(e))

        st.html(
            """
            <div class="upload-tip">
                <strong>TIP</strong>
                <span>
                    상품이 잘 보이도록 밝고 선명한 사진을
                    업로드해 주세요.
                </span>
            </div>
            """
        )
        
    # 6. 상품 기본 정보 입력
    with form_col:
        st.html(
            """
            <style>
            .st-key-product_name_input,
            .st-key-product_price_input,
            .st-key-product_description_input {
                margin-bottom: 18px;
            }

            .st-key-product_name_input label,
            .st-key-product_price_input label,
            .st-key-product_description_input label {
                color: #17211c;
                font-size: 14px;
                font-weight: 700;
            }

            .st-key-product_name_input input,
            .st-key-product_price_input input,
            .st-key-product_description_input textarea {
                border: 1.5px solid #d9e1dc;
                border-radius: 10px;
                background: #ffffff;
                color: #17211c;
            }

            .st-key-product_name_input input:focus,
            .st-key-product_price_input input:focus,
            .st-key-product_description_input textarea:focus {
                border-color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
            }

            .st-key-product_name_input input::placeholder,
            .st-key-product_price_input input::placeholder,
            .st-key-product_description_input textarea::placeholder {
                color: #a0aaa5;
            }
            </style>
            """
        )
        
        st.html(
            """
            <div class="form-title">
                <span>▤</span>
                <h2>상품 기본 정보</h2>
            </div>
            """
        )

        product_name = st.text_input(
            "상품명 *",
            placeholder="예: 프리미엄 수제 함박스테이크",
            max_chars=50,
            key="product_name_input",
        )

        product_price = st.text_input(
            "상품 가격 *",
            placeholder="예: 12,900",
            max_chars=20,
            key="product_price_input",
            on_change=format_product_price,
        )

        product_description = st.text_area(
            "상품 설명 *",
            placeholder=(
                "예: 신선한 재료로 정성껏 만든 수제 함박스테이크입니다.\n"
                "상품의 특징과 장점을 자세히 입력해주세요."
            ),
            max_chars=300,
            height=150,
            key="product_description_input",
        )
        
        st.html(
            """
            <div class="industry-section-title">
                <h3>업종 선택 *</h3>
                <p>상품과 가장 가까운 업종을 선택해주세요.</p>
            </div>
            """
        )

        industry_options = {
            "restaurant": "🍽️ 음식점",
            "cafe": "☕ 카페",
            "beauty": "✨ 뷰티",
            "retail": "🛍️ 소매점",
        }
        
        selected_industry = st.session_state.product_industry

        st.html(
            f"""
            <style>
            .st-key-industry_restaurant button,
            .st-key-industry_cafe button,
            .st-key-industry_beauty button,
            .st-key-industry_retail button {{
                height: 58px;
                border: 1.5px solid #d9e1dc;
                border-radius: 12px;
                background: #ffffff;
                color: #4f5d56;
                font-size: 14px;
                font-weight: 700;
                transition:
                    border-color 0.2s ease,
                    background 0.2s ease,
                    transform 0.2s ease;
            }}

            .st-key-industry_restaurant button:hover,
            .st-key-industry_cafe button:hover,
            .st-key-industry_beauty button:hover,
            .st-key-industry_retail button:hover {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                transform: translateY(-1px);
            }}

            .st-key-industry_{selected_industry} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.08);
            }}
            </style>
            """
        )

        industry_cols = st.columns(4)

        for col, (industry_key, industry_label) in zip(
            industry_cols,
            industry_options.items(),
        ):
            with col:
                if st.button(
                    industry_label,
                    key=f"industry_{industry_key}",
                    use_container_width=True,
                ):
                    st.session_state.product_industry = industry_key
                    st.rerun()
                    
    # 7. 필수 입력 검증
    has_image = (
        normalized_image is not None
        or (
            is_editing
            and st.session_state.get("product") is not None
        )
    )
    
    can_continue = (
        has_image
        and product_name.strip()
        and product_price.strip()
        and product_description.strip()
        and st.session_state.product_industry
    )
    
    if not can_continue:
        st.caption(
            "상품 이미지와 필수 정보를 모두 입력하면 다음 단계로 이동할 수 있어요."
        )

    st.html(
        """
        <style>
        .st-key-product_next {
            margin-top: 32px;
            margin-bottom: 48px;
        }

        .st-key-product_next button {
            height: 56px;
            border: none;
            border-radius: 12px;
            background: #0f8a5f;
            color: #ffffff;
            font-size: 16px;
            font-weight: 800;
        }

        .st-key-product_next button:hover {
            border: none;
            background: #0b7651;
            color: #ffffff;
        }

        .st-key-product_next button:disabled {
            border: none;
            background: #dce3df;
            color: #98a39d;
            opacity: 1;
            cursor: not-allowed;
        }
        </style>
        """
    )

    # 8. 다음 단계
    if st.button(
        "다음 단계 →",
        key="product_next",
        use_container_width=True,
        disabled=not can_continue,
    ):
        try:
            current_product_id = st.session_state.get("product_id")

            # 가격 문자열 → 숫자 변환
            price = int(product_price.replace(",", "").strip())
            
            # 1. 이미지 경로 결정
            if normalized_image is not None:
                image_result = upload_product_image(normalized_image)
                image_path = image_result["image_path"]
            else:
                image_path = st.session_state.product["image_path"]

            # 2. 신규 생성 / 기존 상품 수정
            if is_editing:
                product = update_product(
                    product_id=current_product_id,
                    name=product_name.strip(),
                    price=price,
                    description=product_description.strip(),
                    industry=st.session_state.product_industry,
                    image_path=image_path,
                )
            else:
                product = create_product(
                    name=product_name.strip(),
                    price=price,
                    description=product_description.strip(),
                    industry=st.session_state.product_industry,
                    image_path=image_path,
                )
            
            if current_product_id is not None:
                st.session_state.pop(
                    f"editing_product_image_{current_product_id}",
                    None,
                )
                st.session_state.pop(
                    f"product_edit_initialized_{current_product_id}",
                    None,
                )

                # 상품 정보/이미지 수정 후 페이지별 기존 상품 캐시 제거
                st.session_state.pop(
                    f"strategy_product_{current_product_id}",
                    None,
                )
                st.session_state.pop(
                    f"ad_generation_product_{current_product_id}",
                    None,
                )

                # image_path가 포함된 전략 이미지 캐시까지 모두 제거
                strategy_image_prefix = (
                    f"strategy_product_image_src_{current_product_id}"
                )
                for state_key in list(st.session_state.keys()):
                    if state_key.startswith(strategy_image_prefix):
                        st.session_state.pop(state_key, None)

                # get_product_image가 st.cache_data 함수인 경우 API 이미지 캐시 제거
                if normalized_image is not None and hasattr(
                    get_product_image,
                    "clear",
                ):
                    get_product_image.clear()
            
            # 3. 이전 상품 기준의 이후 단계 상태 초기화
            clear_after_product()

            # 4. 현재 상품 정보만 최신값으로 저장
            # 위젯 key는 이미 생성된 상태이므로 여기서 직접 수정하지 않음
            st.session_state.product_id = product["id"]
            st.session_state.product = product
            
            # 5. 수정 모드 종료
            st.session_state.pop("editing_product", None)
            
            st.query_params["page"] = "strategy_selection"
            st.rerun()

        except ValueError:
            st.error("상품 가격은 숫자로 입력해주세요.")

        except APIError as e:
            st.error(str(e))

        except requests.exceptions.ConnectionError:
            st.error("백엔드 서버에 연결할 수 없습니다.")

        except Exception as e:
            st.exception(e)