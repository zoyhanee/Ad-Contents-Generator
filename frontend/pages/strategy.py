import base64
import html
import streamlit as st

from components.header import render_header
from api.product import get_product, get_product_image
from api.project import create_project
from api.strategy import recommend_strategy
from api.client import APIError
from utils.state import clear_recommendation_state


def handle_custom_size_change():
    clear_recommendation_state()


def get_generation_image_size(
    width: int,
    height: int,
) -> tuple[int, int]:
    aspect_ratio = width / height

    if aspect_ratio < 0.8:
        return 1024, 1536

    if aspect_ratio > 1.25:
        return 1536, 1024

    return 1024, 1024

def render_strategy_selection():
    if "strategy_mode" not in st.session_state:
        st.session_state.strategy_mode = "faster"

    # 1. 공통 헤더
    render_header()

    # 2. 페이지 제목 + Stepper
    st.html(
        """
        <div class="product-page-head">
            <div class="page-title-wrap">
                <div class="step-badge">2</div>

                <div>
                    <h1>광고 전략 선택</h1>
                    <p>
                        광고 목적과 스타일을 선택하면
                        AI가 최적의 광고 전략을 추천해드려요.
                    </p>
                </div>
            </div>

            <div class="stepper">
                <div class="step-item done">
                    <div class="step-dot">✓</div>
                    <span>상품 정보</span>
                </div>

                <div class="step-line active"></div>

                <div class="step-item active">
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
    
    product_id = st.session_state.get("product_id")

    if product_id is None:
        st.error("상품 정보를 찾을 수 없습니다.")
        st.stop()
        
    product_cache_key = f"strategy_product_{product_id}"
    image_cache_key = f"strategy_product_image_src_{product_id}"

    try:
        if product_cache_key not in st.session_state:
            st.session_state[product_cache_key] = get_product(product_id)

        product = st.session_state[product_cache_key]

        if image_cache_key not in st.session_state:
            image_bytes, image_type = get_product_image(product_id)

            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            st.session_state[image_cache_key] = (
                f"data:{image_type};"
                f"base64,{image_base64}"
            )

        image_src = st.session_state[image_cache_key]

    except APIError as e:
        st.error(str(e))
        return
    
    industry_labels = {
        "restaurant": "음식점",
        "cafe": "카페",
        "beauty": "뷰티",
        "retail": "소매점",
    }

    industry_label = industry_labels.get(
        product["industry"],
        product["industry"],
    )
    product_name = html.escape(product["name"])
    product_price = html.escape(str(product["price"]))

    # 3. 상품 요약 카드
    st.html(
        f"""
        <div class="strategy-content">
            <div class="strategy-container">
                <section class="strategy-summary-card">
                    <div class="strategy-product-info">
                        <div class="strategy-product-image">
                            <img
                                src="{image_src}"
                                alt="상품 이미지"
                            >
                        </div>

                        <div class="strategy-product-text">
                            <h3>{product_name}</h3>
                            <p>
                                {product_price}
                                ·
                                {industry_label}
                            </p>
                        </div>
                    </div>
                </section>
            </div>
        </div>
        """
    )
    st.html(
        """
        <style>
        .st-key-edit_product {
            margin-top: 10px;
            margin-bottom: 24px;
        }

        .st-key-edit_product button {
            height: 42px;
            border: 1.5px solid #d9e1dc;
            border-radius: 10px;
            background: #ffffff;
            color: #0f8a5f;
            font-size: 14px;
            font-weight: 700;
            transition:
                border-color 0.2s ease,
                background 0.2s ease;
        }

        .st-key-edit_product button:hover {
            border-color: #0f8a5f;
            background: #f4fbf7;
            color: #0f8a5f;
        }
        </style>
        """
    )
    left, right = st.columns([5, 1])
    with left:
        st.empty()
    with right:
        if st.button(
            "정보 수정",
            key="edit_product",
            use_container_width=True,
        ):
            st.session_state.editing_product = True
            
            st.session_state.product_name_input = product["name"]
            st.session_state.product_price_input = (
                f"{product['price']:,}"
                if product["price"] is not None
                else ""
            )
            st.session_state.product_description_input = (
                product["description"] or ""
            )
            st.session_state.product_industry = product["industry"]
            
            st.query_params["page"] = "product_input"
            st.rerun()
    

    # 4. 전략 모드 선택
    selected_mode = st.session_state.strategy_mode

    st.html(
        f"""
        <style>
        .st-key-strategy_faster button,
        .st-key-strategy_manual button {{
            position: relative;
            height: 176px;
            padding: 68px 30px 28px;
            border-radius: 16px;
            background: #ffffff;
            border: 1.5px solid #d9e1dc;
            color: #17211c;
            text-align: left;
            justify-content: flex-start;
            overflow: hidden;
            transition:
                border-color 0.2s ease,
                background 0.2s ease,
                box-shadow 0.2s ease,
                transform 0.2s ease;
        }}

        .st-key-strategy_faster button p,
        .st-key-strategy_manual button p {{
            width: 100%;
            margin: 0;
            font-size: 22px;
            font-weight: 800;
            text-align: left;
        }}

        .st-key-strategy_faster button:hover,
        .st-key-strategy_manual button:hover {{
            border-color: #79b79c;
            background: #ffffff;
            color: #17211c;
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(15, 92, 60, 0.08);
        }}

        .st-key-strategy_faster button::before,
        .st-key-strategy_manual button::before {{
            position: absolute;
            top: 26px;
            left: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: #edf3ef;
            font-size: 20px;
        }}

        .st-key-strategy_faster button::before {{
            content: "⚡";
        }}

        .st-key-strategy_manual button::before {{
            content: "⚙";
        }}

        .st-key-strategy_faster button::after,
        .st-key-strategy_manual button::after {{
            position: absolute;
            left: 30px;
            bottom: 24px;
            color: #66736c;
            font-size: 15px;
            font-weight: 500;
            line-height: 1.6;
        }}

        .st-key-strategy_faster button::after {{
            content: "AI가 현재 트렌드에 맞춰 가장 적합한 스타일을 제안합니다.";
        }}

        .st-key-strategy_manual button::after {{
            content: "광고 목표와 시각적 스타일을 직접 세밀하게 설정합니다.";
        }}

        .st-key-strategy_{selected_mode} button {{
            border-color: #0f8a5f;
            background: #f4fbf7;
            color: #17211c;
            box-shadow: 0 0 0 3px rgba(15, 138, 95, 0.1);
        }}

        .st-key-strategy_{selected_mode} button:hover {{
            background: #f4fbf7;
        }}

        .st-key-strategy_{selected_mode} button::before {{
            background: #dff4e9;
        }}

        /* 선택된 카드 오른쪽 위 체크 표시 */
        .st-key-strategy_{selected_mode} {{
            position: relative;
        }}

        .st-key-strategy_{selected_mode}::after {{
            content: "✓";
            position: absolute;
            top: 24px;
            right: 28px;
            z-index: 10;

            width: 28px;
            height: 28px;
            border-radius: 50%;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #0f8a5f;
            color: #ffffff;
            font-size: 15px;
            font-weight: 900;

            pointer-events: none;
        }}
        
        </style>
        """
    )
    
    st.subheader("전략 모드 선택")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "빠른 추천",
            key="strategy_faster",
            use_container_width=True,
        ):
            if st.session_state.strategy_mode != "faster":
                st.session_state.strategy_mode = "faster"
                clear_recommendation_state()
            
            st.rerun()

    with col2:
        if st.button(
            "직접 설정",
            key="strategy_manual",
            use_container_width=True,
        ):
            if st.session_state.strategy_mode != "manual":
                st.session_state.strategy_mode = "manual"
                clear_recommendation_state()
            st.rerun()

    # 5. 광고 플랫폼 선택
    st.subheader("광고 플랫폼 선택")

    platform_options = {
        "instagram": "📷 Instagram",
        "baemin": "🚚 배달의민족",
        "naver": "🟢 네이버",
        "offline": "🖼 오프라인 포스터",
    }

    if "selected_platform" not in st.session_state:
        st.session_state.selected_platform = None

    selected_platform = st.session_state.selected_platform

    platform_css = """
    <style>
    .st-key-platform_instagram button,
    .st-key-platform_baemin button,
    .st-key-platform_naver button,
    .st-key-platform_offline button {
        height: 72px;
        border-radius: 12px;
        background: #ffffff;
        border: 1.5px solid #d9e1dc;
        color: #17211c;
        font-size: 16px;
        font-weight: 700;
    }

    .st-key-platform_instagram button:hover,
    .st-key-platform_baemin button:hover,
    .st-key-platform_naver button:hover,
    .st-key-platform_offline button:hover {
        border-color: #79b79c;
        background: #ffffff;
        color: #17211c;
    }

    .st-key-platform_instagram button:focus,
    .st-key-platform_baemin button:focus,
    .st-key-platform_naver button:focus,
    .st-key-platform_offline button:focus {
        outline: none !important;
    }
    """

    if selected_platform:
        platform_css += f"""
        .st-key-platform_{selected_platform} button {{
            border-color: #0f8a5f;
            background: #f4fbf7;
            color: #0f8a5f;
            box-shadow: 0 0 0 2px rgba(15,138,95,.1);
        }}

        .st-key-platform_{selected_platform} button:hover {{
            background:#f4fbf7;
            color:#0f8a5f;
        }}
        """

    platform_css += "</style>"

    st.html(platform_css)

    platform_cols = st.columns(4)

    for col, (platform_id, platform_label) in zip(
        platform_cols,
        platform_options.items(),
    ):
        with col:
            if st.button(
                platform_label,
                key=f"platform_{platform_id}",
                use_container_width=True,
            ):
                if st.session_state.selected_platform != platform_id:
                    st.session_state.selected_platform = platform_id
                    clear_recommendation_state()
                
                st.rerun()

    # 6. 오프라인 포스터 규격 선택
    if st.session_state.selected_platform == "offline":
        st.subheader("포스터 규격 선택")

        poster_size_options = {
            "a4": "A4",
            "a3": "A3",
            "a2": "A2",
            "custom": "직접 입력",
        }

        if "poster_size" not in st.session_state:
            st.session_state.poster_size = "a4"

        selected_poster_size = st.session_state.poster_size

        st.html(
            f"""
            <style>
            .st-key-poster_size_a4 button,
            .st-key-poster_size_a3 button,
            .st-key-poster_size_a2 button,
            .st-key-poster_size_custom button {{
                height: 58px;
                border-radius: 10px;
                background: #ffffff;
                border: 1.5px solid #d9e1dc;
                color: #17211c;
                font-size: 15px;
                font-weight: 700;
            }}

            .st-key-poster_size_a4 button:hover,
            .st-key-poster_size_a3 button:hover,
            .st-key-poster_size_a2 button:hover,
            .st-key-poster_size_custom button:hover {{
                border-color: #79b79c;
                background: #ffffff;
                color: #17211c;
            }}

            .st-key-poster_size_{selected_poster_size} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
            }}

            .st-key-poster_size_{selected_poster_size} button:hover {{
                background: #f4fbf7;
                color: #0f8a5f;
            }}
            </style>
            """
        )
        poster_cols = st.columns(4)

        for col, (size_id, size_label) in zip(
            poster_cols,
            poster_size_options.items(),
        ):
            with col:
                if st.button(
                    size_label,
                    key=f"poster_size_{size_id}",
                    use_container_width=True,
                ):
                    if st.session_state.poster_size != size_id:
                        st.session_state.poster_size = size_id
                        clear_recommendation_state()
                    st.rerun()

        if st.session_state.poster_size == "custom":
            st.html(
                """
                <style>
                .custom-size-section {
                    margin-top: 18px;
                    margin-bottom: 8px;
                    padding: 20px 22px;
                    border: 1.5px solid #d9e1dc;
                    border-radius: 14px;
                    background: #f8fbf9;
                }

                .custom-size-title {
                    margin: 0 0 4px;
                    color: #17211c;
                    font-size: 16px;
                    font-weight: 800;
                }

                .custom-size-description {
                    margin: 0 0 16px;
                    color: #66736c;
                    font-size: 13px;
                    line-height: 1.6;
                }

                .st-key-custom_image_width label,
                .st-key-custom_image_height label {
                    color: #36423c;
                    font-size: 14px;
                    font-weight: 700;
                }

                .st-key-custom_image_width input,
                .st-key-custom_image_height input {
                    min-height: 48px;
                    border: 1.5px solid #d9e1dc;
                    border-radius: 10px;
                    background: #ffffff;
                    color: #17211c;
                    font-size: 15px;
                    font-weight: 600;
                }

                .st-key-custom_image_width input:focus,
                .st-key-custom_image_height input:focus {
                    border-color: #0f8a5f;
                    box-shadow:
                        0 0 0 2px rgba(15, 138, 95, 0.1);
                }

                .st-key-custom_image_width button,
                .st-key-custom_image_height button {
                    border-color: #d9e1dc;
                    background: #ffffff;
                    color: #0f8a5f;
                }

                .st-key-custom_image_width button:hover,
                .st-key-custom_image_height button:hover {
                    border-color: #79b79c;
                    background: #f4fbf7;
                    color: #0f8a5f;
                }
                </style>

                <div class="custom-size-section">
                    <div class="custom-size-title">
                        사용자 지정 크기
                    </div>
                    <p class="custom-size-description">
                        원하는 출력 이미지의 가로와 세로 크기를 입력해주세요.
                    </p>
                </div>
                """
            )

            custom_size_col1, custom_size_col2 = st.columns(2)

            with custom_size_col1:
                custom_width = st.number_input(
                    "가로 (px)",
                    min_value=256,
                    max_value=4096,
                    value=1024,
                    step=64,
                    key="custom_image_width",
                    on_change=handle_custom_size_change,
                )

            with custom_size_col2:
                custom_height = st.number_input(
                    "세로 (px)",
                    min_value=256,
                    max_value=4096,
                    value=1536,
                    step=64,
                    key="custom_image_height",
                    on_change=handle_custom_size_change,
                )
    # 7. 직접 설정: 광고 목표 선택
    if st.session_state.strategy_mode == "manual":
        st.subheader("광고 목표 선택")

        goal_options = {
            "awareness": "📢 브랜드 인지도",
            "sales": "🛒 판매 전환",
            "traffic": "🔗 방문 유도",
            "promotion": "🎁 프로모션 홍보",
        }

        if "selected_goal" not in st.session_state:
            st.session_state.selected_goal = "awareness"

        selected_goal = st.session_state.selected_goal

        st.html(
            f"""
            <style>
            .st-key-goal_awareness button,
            .st-key-goal_sales button,
            .st-key-goal_traffic button,
            .st-key-goal_promotion button {{
                height: 76px;
                border-radius: 12px;
                background: #ffffff;
                border: 1.5px solid #d9e1dc;
                color: #17211c;
                font-size: 16px;
                font-weight: 700;
            }}

            .st-key-goal_awareness button:hover,
            .st-key-goal_sales button:hover,
            .st-key-goal_traffic button:hover,
            .st-key-goal_promotion button:hover {{
                border-color: #79b79c;
                background: #ffffff;
                color: #17211c;
            }}

            .st-key-goal_{selected_goal} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
            }}

            .st-key-goal_{selected_goal} button:hover {{
                background: #f4fbf7;
                color: #0f8a5f;
            }}
            </style>
            """
        )

        goal_cols = st.columns(4)

        for col, (goal_id, goal_label) in zip(
            goal_cols,
            goal_options.items(),
        ):
            with col:
                if st.button(
                    goal_label,
                    key=f"goal_{goal_id}",
                    use_container_width=True,
                ):
                    if st.session_state.selected_goal != goal_id:
                        st.session_state.selected_goal = goal_id
                        clear_recommendation_state()
                    st.rerun()
                    
        # 8. 직접 설정: 시각적 스타일 선택
        st.subheader("시각적 스타일 선택")

        style_options = {
            "warm": "☀️ 따뜻한 감성",
            "modern": "◼️ 모던 & 미니멀",
            "vivid": "🎨 생동감 있는",
            "premium": "✨ 프리미엄",
        }

        if "selected_style" not in st.session_state:
            st.session_state.selected_style = "warm"

        selected_style = st.session_state.selected_style

        st.html(
            f"""
            <style>
            .st-key-style_warm button,
            .st-key-style_modern button,
            .st-key-style_vivid button,
            .st-key-style_premium button {{
                height: 76px;
                border-radius: 12px;
                background: #ffffff;
                border: 1.5px solid #d9e1dc;
                color: #17211c;
                font-size: 16px;
                font-weight: 700;
            }}

            .st-key-style_warm button:hover,
            .st-key-style_modern button:hover,
            .st-key-style_vivid button:hover,
            .st-key-style_premium button:hover {{
                border-color: #79b79c;
                background: #ffffff;
                color: #17211c;
            }}

            .st-key-style_{selected_style} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
            }}

            .st-key-style_{selected_style} button:hover {{
                background: #f4fbf7;
                color: #0f8a5f;
            }}
            </style>
            """
        )

        style_cols = st.columns(4)

        for col, (style_id, style_label) in zip(
            style_cols,
            style_options.items(),
        ):
            with col:
                if st.button(
                    style_label,
                    key=f"style_{style_id}",
                    use_container_width=True,
                ):
                    if st.session_state.selected_style != style_id:
                        st.session_state.selected_style = style_id
                        clear_recommendation_state()
                    st.rerun()

    # 9. 현재 전략 데이터 구성
    platform_image_sizes = {
        "instagram": (1024, 1024),
        "baemin": (1024, 1536),
        "naver": (1536, 1024),
        "offline": (1024, 1536),
    }

    selected_platform = st.session_state.get(
        "selected_platform"
    )

    image_width, image_height = platform_image_sizes.get(
        selected_platform,
        (1024, 1024),
    )
    
    output_width = image_width
    output_height = image_height
    
    if (
        selected_platform == "offline"
        and st.session_state.get("poster_size") == "custom"
    ):
        output_width = st.session_state.get(
            "custom_image_width",
            1024,
        )
        output_height = st.session_state.get(
            "custom_image_height",
            1536,
        )

        image_width, image_height = get_generation_image_size(
            output_width,
            output_height,
        )
        
    strategy_data = {
        "mode": st.session_state.strategy_mode,
        "platform": st.session_state.get(
            "selected_platform"
        ),
        "poster_size": (
            st.session_state.get("poster_size")
            if st.session_state.get("selected_platform")
            == "offline"
            else None
        ),
        "image_width": image_width,
        "image_height": image_height,
        "output_width": output_width,
        "output_height": output_height,
        "goal": (
            st.session_state.get("selected_goal")
            if st.session_state.strategy_mode == "manual"
            else None
        ),
        "style": (
            st.session_state.get("selected_style")
            if st.session_state.strategy_mode == "manual"
            else None
        ),
    }

    # 10. AI 추천받기
    can_recommend = (
        strategy_data["platform"] is not None
    )

    st.html(
        """
        <style>
        .st-key-recommend_strategy button {
            height: 56px;
            border: none;
            border-radius: 12px;
            background: #0f8a5f;
            color: #ffffff;
            font-size: 17px;
            font-weight: 800;
            box-shadow: 0 6px 16px rgba(15, 138, 95, 0.18);
            transition:
                background 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .st-key-recommend_strategy button:hover {
            border: none;
            background: #0b7651;
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(15, 138, 95, 0.24);
        }

        .st-key-recommend_strategy button:focus,
        .st-key-recommend_strategy button:focus-visible {
            outline: none !important;
            border: none;
            color: #ffffff;
        }

        .st-key-recommend_strategy button:disabled {
            border: 1px solid #e1e6e3;
            background: #f1f3f2;
            color: #a5ada9;
            box-shadow: none;
            cursor: not-allowed;
            transform: none;
        }

        .st-key-recommend_strategy button:disabled:hover {
            border: 1px solid #e1e6e3;
            background: #f1f3f2;
            color: #a5ada9;
            box-shadow: none;
            transform: none;
        }
        </style>
        """
    )

    if st.button(
        "✨ AI 추천받기",
        key="recommend_strategy",
        use_container_width=True,
        disabled=not can_recommend,
    ):
        st.session_state.pop("recommendation", None)
        st.session_state.pop("selected_slogan", None)
        
        loading_placeholder = st.empty()

        loading_placeholder.html(
            """
            <div class="strategy-loading">
                <div class="strategy-loading-icon">✨</div>

                <div class="strategy-loading-text">
                    <h3>AI가 상품을 분석하고 있어요</h3>
                    <p>
                        상품의 매력과 광고 설정을 바탕으로
                        가장 어울리는 전략과 슬로건을 만들고 있습니다.
                    </p>
                </div>

                <div class="strategy-loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>

            <style>
            .strategy-loading {
                display: flex;
                align-items: center;
                gap: 18px;
                margin-top: 16px;
                padding: 22px 24px;
                border: 1.5px solid #cfe7da;
                border-radius: 14px;
                background: #f4fbf7;
            }

            .strategy-loading-icon {
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                width: 46px;
                height: 46px;
                border-radius: 12px;
                background: #dff4e9;
                font-size: 22px;
                animation: strategy-pulse 1.6s ease-in-out infinite;
            }

            .strategy-loading-text {
                flex: 1;
            }

            .strategy-loading-text h3 {
                margin: 0 0 5px;
                color: #17211c;
                font-size: 17px;
                font-weight: 800;
            }

            .strategy-loading-text p {
                margin: 0;
                color: #66736c;
                font-size: 14px;
                line-height: 1.6;
            }

            .strategy-loading-dots {
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .strategy-loading-dots span {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #0f8a5f;
                animation: strategy-bounce 1.2s infinite ease-in-out;
            }

            .strategy-loading-dots span:nth-child(2) {
                animation-delay: 0.15s;
            }

            .strategy-loading-dots span:nth-child(3) {
                animation-delay: 0.3s;
            }

            @keyframes strategy-pulse {
                0%, 100% {
                    transform: scale(1);
                }

                50% {
                    transform: scale(1.08);
                }
            }

            @keyframes strategy-bounce {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }

                30% {
                    transform: translateY(-5px);
                    opacity: 1;
                }
            }
            </style>
            """
        )

        try:
            project = create_project(product_id)

            project_id = project["id"]

            recommendation = recommend_strategy(
                project_id=project_id,
                mode=strategy_data["mode"],
                platform=strategy_data["platform"],
                poster_size=strategy_data["poster_size"],
                goal=strategy_data["goal"],
                style=strategy_data["style"],
            )
            
            st.session_state.project_id = project_id
            st.session_state.strategy_data = strategy_data.copy()
            st.session_state.recommendation = recommendation
            st.session_state.selected_slogan = None

            st.rerun()

        except APIError as e:
            loading_placeholder.empty()
            st.error(str(e))

    recommendation = st.session_state.get("recommendation")

    if recommendation:
        strategy_title = html.escape(
            recommendation.get("strategy_title")
            or "AI 추천 전략"
        )
        strategy_description = html.escape(
            recommendation.get("strategy_description")
            or "상품과 광고 설정을 바탕으로 추천된 전략입니다."
        )

        st.html(
            f"""
            <div class="recommendation-section">
                <div class="recommendation-label">
                    <span class="recommendation-label-icon">✨</span>
                    AI 추천 전략
                </div>

                <div class="recommendation-card">
                    <div class="recommendation-card-icon">💡</div>

                    <div class="recommendation-card-content">
                        <h3>{strategy_title}</h3>
                        <p>{strategy_description}</p>
                    </div>
                </div>
            </div>

            <style>
            .recommendation-section {{
                margin-top: 32px;
            }}

            .recommendation-label {{
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 12px;
                color: #17211c;
                font-size: 20px;
                font-weight: 800;
            }}

            .recommendation-label-icon {{
                display: flex;
                align-items: center;
                justify-content: center;
                width: 30px;
                height: 30px;
                border-radius: 9px;
                background: #dff4e9;
                font-size: 15px;
            }}

            .recommendation-card {{
                display: flex;
                align-items: flex-start;
                gap: 18px;
                padding: 24px;
                border: 1.5px solid #cfe7da;
                border-radius: 16px;
                background:
                    linear-gradient(
                        135deg,
                        #f4fbf7 0%,
                        #ffffff 100%
                    );
                box-shadow: 0 8px 24px rgba(15, 92, 60, 0.06);
            }}

            .recommendation-card-icon {{
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                width: 48px;
                height: 48px;
                border-radius: 13px;
                background: #dff4e9;
                font-size: 22px;
            }}

            .recommendation-card-content {{
                flex: 1;
                min-width: 0;
            }}

            .recommendation-card-content h3 {{
                margin: 1px 0 8px;
                color: #17211c;
                font-size: 19px;
                font-weight: 800;
                line-height: 1.45;
            }}

            .recommendation-card-content p {{
                margin: 0;
                color: #59665f;
                font-size: 15px;
                font-weight: 500;
                line-height: 1.75;
                word-break: keep-all;
            }}
            </style>
            """
        )

        # 11. 추천 슬로건 선택
        st.subheader("추천 슬로건 선택")

        slogans = recommendation.get("slogans", [])
        
        if not slogans:
            st.warning(
                "추천 슬로건을 불러올 수 없습니다. "
                "AI 추천을 다시 받아주세요."
            )
            return

        selected_slogan = st.session_state.get("selected_slogan")

        slogan_selectors = [
            f".st-key-slogan_{index} button"
            for index in range(len(slogans))
        ]

        slogan_selector = ",\n".join(slogan_selectors)

        slogan_css = f"""
        <style>
        {slogan_selector} {{
            position: relative;
            min-height: 132px;
            padding: 46px 22px 22px;
            border: 1.5px solid #d9e1dc;
            border-radius: 14px;
            background: #ffffff;
            color: #17211c;
            font-size: 16px;
            font-weight: 700;
            line-height: 1.6;
            white-space: normal;
            word-break: keep-all;
            text-align: left;
            justify-content: flex-start;
            align-items: flex-start;
            transition:
                border-color 0.2s ease,
                background 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }}

        {slogan_selector} p {{
            width: 100%;
            margin: 0;
            text-align: left;
        }}

        {slogan_selector}:hover {{
            border-color: #79b79c;
            background: #ffffff;
            color: #17211c;
            transform: translateY(-2px);
            box-shadow: 0 8px 22px rgba(15, 92, 60, 0.08);
        }}
        """

        for index in range(len(slogans)):
            slogan_css += f"""
            .st-key-slogan_{index} {{
                position: relative;
            }}

            .st-key-slogan_{index}::before {{
                content: "0{index + 1}";
                position: absolute;
                top: 17px;
                left: 22px;
                z-index: 10;
                color: #0f8a5f;
                font-size: 12px;
                font-weight: 900;
                letter-spacing: 0.08em;
                pointer-events: none;
            }}
            """

        if selected_slogan is not None:
            slogan_css += f"""
            .st-key-slogan_{selected_slogan} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #17211c;
                box-shadow: 0 0 0 3px rgba(15, 138, 95, 0.1);
            }}

            .st-key-slogan_{selected_slogan} button:hover {{
                background: #f4fbf7;
                color: #17211c;
            }}

            .st-key-slogan_{selected_slogan}::after {{
                content: "✓";
                position: absolute;
                top: 14px;
                right: 18px;
                z-index: 10;

                display: flex;
                align-items: center;
                justify-content: center;

                width: 24px;
                height: 24px;
                border-radius: 50%;

                background: #0f8a5f;
                color: #ffffff;
                font-size: 13px;
                font-weight: 900;

                pointer-events: none;
            }}
            """

        slogan_css += "</style>"

        st.html(slogan_css)

        slogan_cols = st.columns(len(slogans))

        for index, (col, slogan) in enumerate(
            zip(slogan_cols, slogans)
        ):
            with col:
                if st.button(
                    slogan,
                    key=f"slogan_{index}",
                    use_container_width=True,
                ):
                    st.session_state.selected_slogan = index
                    st.rerun()

        # 12. 광고 시안 생성
        selected_slogan = st.session_state.get("selected_slogan")
        project_id = st.session_state.get("project_id")

        st.html(
            """
            <style>
            .st-key-generate_ad {
                margin-top: 32px;
                margin-bottom: 48px;
            }

            .st-key-generate_ad button {
                height: 58px;
                border: none;
                border-radius: 12px;
                background: #0f8a5f;
                color: #ffffff;
                font-size: 16px;
                font-weight: 800;
                box-shadow: 0 8px 20px rgba(15, 138, 95, 0.16);
                transition:
                    background 0.2s ease,
                    transform 0.2s ease,
                    box-shadow 0.2s ease;
            }

            .st-key-generate_ad button:hover {
                border: none;
                background: #0b7651;
                color: #ffffff;
                transform: translateY(-1px);
                box-shadow: 0 10px 24px rgba(15, 138, 95, 0.22);
            }

            .st-key-generate_ad button:active {
                transform: translateY(0);
            }

            .st-key-generate_ad button:focus,
            .st-key-generate_ad button:focus-visible {
                border: none;
                outline: none;
                box-shadow:
                    0 0 0 3px rgba(15, 138, 95, 0.16),
                    0 8px 20px rgba(15, 138, 95, 0.16);
            }

            .st-key-generate_ad button:disabled {
                border: none;
                background: #dce3df;
                color: #98a39d;
                box-shadow: none;
                opacity: 1;
                cursor: not-allowed;
                transform: none;
            }
            </style>
            """
        )
        can_generate = (
            selected_slogan is not None
            and project_id is not None
        )
        
        if project_id is None:
            st.warning(
                "프로젝트 정보를 찾을 수 없습니다. "
                "AI 추천을 다시 받아주세요."
            )

        if st.button(
            "광고 시안 생성하기 →",
            key="generate_ad",
            use_container_width=True,
            disabled=not can_generate,
        ):
            st.query_params["page"] = "ad_generation"
            st.rerun()
