import base64
import html
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"


def clear_recommendation_state():
    st.session_state.pop("recommendation", None)
    st.session_state.pop("selected_slogan", None)


def render_strategy_selection():
    if "strategy_mode" not in st.session_state:
        st.session_state.strategy_mode = "faster"

    # 1. 공통 헤더
    st.html(
        """
        <div class="header">
            <a class="logo" href="?page=landing" target="_self">
                AdMaker <span>AI</span>
            </a>

            <div class="nav">
                <div>서비스 소개</div>
                <div>기능 안내</div>
                <div>이용방법</div>
                <div>요금 안내</div>
                <div>고객 센터</div>
            </div>

            <div class="auth">
                <a class="nav-btn" href="?page=login" target="_self">로그인</a>
                <a class="nav-btn primary" href="?page=signup" target="_self">
                    회원가입
                </a>
            </div>
        </div>
        """
    )

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

    product_data = st.session_state.get("product_data")

    if not product_data:
        st.warning("상품 정보가 없습니다. 먼저 상품 정보를 입력해주세요.")

        if st.button("상품 정보 입력으로 이동"):
            st.query_params["page"] = "product_input"
            st.rerun()

        return

    image_base64 = base64.b64encode(
        product_data["image_bytes"]
    ).decode("utf-8")

    image_src = (
        f"data:{product_data['image_type']};"
        f"base64,{image_base64}"
    )

    industry_labels = {
        "restaurant": "음식점",
        "cafe": "카페",
        "beauty": "뷰티",
        "retail": "소매점",
    }

    industry_label = industry_labels.get(
        product_data["industry"],
        product_data["industry"],
    )

    product_name = html.escape(str(product_data.get("name", "")))
    product_price = html.escape(str(product_data.get("price", "")))

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
            clear_recommendation_state()
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
            st.session_state.strategy_mode = "faster"
            clear_recommendation_state()
            st.rerun()

    with col2:
        if st.button(
            "직접 설정",
            key="strategy_manual",
            use_container_width=True,
        ):
            st.session_state.strategy_mode = "manual"
            clear_recommendation_state()
            st.rerun()

    # 5. 이전 작업물 톤 유지
    st.checkbox(
        "이전 작업물과 비슷한 톤으로",
        key="reuse_previous_tone",
    )

    # 6. 광고 플랫폼 선택
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
                st.session_state.selected_platform = platform_id
                clear_recommendation_state()
                st.rerun()

    # 7. 오프라인 포스터 규격 선택
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
                    st.session_state.poster_size = size_id
                    clear_recommendation_state()
                    st.rerun()

    # 8. 직접 설정: 광고 목표 선택
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
                    st.session_state.selected_goal = goal_id
                    clear_recommendation_state()
                    st.rerun()

        # 9. 직접 설정: 시각적 스타일 선택
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
                    st.session_state.selected_style = style_id
                    clear_recommendation_state()
                    st.rerun()

    # 10. 현재 전략 데이터 구성
    selected_platform = st.session_state.get(
        "selected_platform",
        None,
    )

    strategy_data = {
        "mode": st.session_state.strategy_mode,
        "reuse_tone": st.session_state.get(
            "reuse_previous_tone",
            False,
        ),
        "platforms": (
            [selected_platform]
            if selected_platform is not None
            else []
        ),
        "poster_size": (
            st.session_state.get("poster_size")
            if selected_platform == "offline"
            else None
        ),
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

    # 11. AI 추천받기
    can_recommend = len(strategy_data["platforms"]) > 0

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
        st.session_state.strategy_data = strategy_data.copy()

        try:
            # 이미 업로드한 이미지 경로가 있으면 재사용
            image_path = st.session_state.get("product_image_path")

            # 아직 업로드하지 않은 경우에만 백엔드로 전송
            if image_path is None:
                image_response = requests.post(
                    f"{BACKEND_URL}/products/image",
                    files={
                        "image": (
                            product_data["image_name"],
                            product_data["image_bytes"],
                            product_data["image_type"],
                        )
                    },
                    timeout=30,
                )
                image_response.raise_for_status()

                image_path = image_response.json()["image_path"]
                st.session_state.product_image_path = image_path

            api_product_data = {
                "name": product_data["name"],
                "price": product_data["price"],
                "description": product_data["description"],
                "category": product_data["industry"],
                "image_path": image_path,
            }

            payload = {
                "product": api_product_data,
                "strategy": strategy_data,
            }

            response = requests.post(
                f"{BACKEND_URL}/strategy/recommend",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()

            st.session_state.recommendation = response.json()
            st.session_state.selected_slogan = None
            st.rerun()

        except requests.exceptions.ConnectionError:
            st.error(
                "백엔드 서버에 연결할 수 없습니다. "
                "FastAPI 서버가 실행 중인지 확인해주세요."
            )

        except requests.exceptions.RequestException as e:
            st.error(f"AI 추천 요청 중 오류가 발생했습니다: {e}")

    recommendation = st.session_state.get("recommendation")

    if recommendation:
        st.subheader("AI 추천 결과")

        st.write(recommendation["strategy_title"])
        st.caption(recommendation["strategy_description"])

        # 13. 추천 슬로건 선택
        st.subheader("추천 슬로건 선택")

        slogans = recommendation["slogans"]

        selected_slogan = st.session_state.get("selected_slogan")

        slogan_selector_list = [
            f".st-key-slogan_{index} button"
            for index in range(len(slogans))
        ]

        slogan_selector = ",\n".join(slogan_selector_list)

        slogan_css = f"""
        <style>
        {slogan_selector} {{
            min-height: 92px;
            padding: 20px;
            border-radius: 12px;
            background: #ffffff;
            border: 1.5px solid #d9e1dc;
            color: #17211c;
            font-size: 16px;
            font-weight: 700;
            white-space: normal;
        }}

        {slogan_selector}:hover {{
            border-color: #79b79c;
            background: #ffffff;
            color: #17211c;
        }}
        """

        if selected_slogan is not None:
            slogan_css += f"""
            .st-key-slogan_{selected_slogan} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
            }}

            .st-key-slogan_{selected_slogan} button:hover {{
                background: #f4fbf7;
                color: #0f8a5f;
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

        # 14. 광고 시안 생성
        selected_slogan = st.session_state.get("selected_slogan")
        project_id = recommendation.get("project_id")

        final_strategy_data = {
            "project_id": project_id,
            "product": {
                "name": product_data["name"],
                "price": product_data["price"],
                "description": product_data["description"],
                "industry": product_data["industry"],
                "image_name": product_data["image_name"],
                "image_type": product_data["image_type"],
                "image_bytes": product_data["image_bytes"],
                "image_path": st.session_state.get("product_image_path"),
            },
            **st.session_state.strategy_data,
            "recommendation": {
                "strategy_title": recommendation["strategy_title"],
                "strategy_description": recommendation[
                    "strategy_description"
                ],
            },
            "selected_slogan": (
                recommendation["slogans"][selected_slogan]
                if selected_slogan is not None
                else None
            ),
        }

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

        if st.button(
            "광고 시안 생성하기 →",
            key="generate_ad",
            use_container_width=True,
            disabled=selected_slogan is None,
        ):
            st.session_state.final_strategy_data = final_strategy_data
            st.query_params["page"] = "ad_generation"
            st.rerun()