import streamlit as st


def render_product_input():
    # 1. 상품 입력 상태 초기화
    if "product_name" not in st.session_state:
        st.session_state.product_name = ""

    if "product_price" not in st.session_state:
        st.session_state.product_price = ""

    if "product_description" not in st.session_state:
        st.session_state.product_description = ""

    if "product_industry" not in st.session_state:
        st.session_state.product_industry = "restaurant"

    # 2. 공통 헤더
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
                <a class="nav-btn" href="?page=login" target="_self">
                    로그인
                </a>
                <a class="nav-btn primary" href="?page=signup" target="_self">
                    회원가입
                </a>
            </div>
        </div>
        """
    )

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
                    JPG, PNG, WebP 파일 지원 (최대 10MB)
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
            type=["jpg", "jpeg", "png", "webp"],
            key="product_image",
            label_visibility="collapsed",
        )

        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption="업로드된 상품 이미지",
                use_container_width=True,
            )

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
            value=st.session_state.product_name,
            placeholder="예: 프리미엄 수제 함박스테이크",
            max_chars=50,
            key="product_name_input",
        )

        product_price = st.text_input(
            "상품 가격 *",
            value=st.session_state.product_price,
            placeholder="예: 12,900",
            max_chars=20,
            key="product_price_input",
        )

        product_description = st.text_area(
            "상품 설명 *",
            value=st.session_state.product_description,
            placeholder=(
                "예: 신선한 재료로 정성껏 만든 수제 함박스테이크입니다.\n"
                "상품의 특징과 장점을 자세히 입력해주세요."
            ),
            max_chars=300,
            height=150,
            key="product_description_input",
        )
            
        st.session_state.product_name = product_name
        st.session_state.product_price = product_price
        st.session_state.product_description = product_description
        
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
    can_continue = (
        uploaded_image is not None
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
        st.session_state.product_data = {
            "name": product_name.strip(),
            "price": product_price.strip(),
            "description": product_description.strip(),
            "industry": st.session_state.product_industry,
            "image_name": uploaded_image.name,
            "image_type": uploaded_image.type,
            "image_bytes": uploaded_image.getvalue(),
        }

        st.query_params["page"] = "strategy_selection"
        st.rerun()