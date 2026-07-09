import streamlit as st

from components.header import render_header
from api.client import APIError
from api.generate import download_generated_image
from utils.state import clear_after_draft


BACKEND_URL = "http://127.0.0.1:8000"


def render_result():
    # 최종 결과 데이터 확인
    final_ad_result = st.session_state.get("final_ad_result")

    if final_ad_result is None:
        st.warning(
            "선택된 최종 광고 시안이 없습니다. "
            "광고 시안을 먼저 선택해주세요."
        )
        
        st.html(
            """
            <style>
            .st-key-back_to_ad_generation button {
                height: 48px;
                border: 1.5px solid #0f8a5f;
                border-radius: 10px;
                background: #ffffff;
                color: #0f8a5f;
                font-weight: 800;
            }

            .st-key-back_to_ad_generation button:hover {
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
            }
            </style>
            """
        )

        if st.button(
            "광고 시안 선택으로 돌아가기",
            key="back_to_ad_generation",
        ):
            st.query_params["page"] = "ad_generation"
            st.rerun()

        return

    # 공통 헤더
    render_header()

    # 선택된 최종 시안
    selected_draft = final_ad_result["selected_draft"]

    image_path = selected_draft.get("image_path")
    image_url = (
        f"{BACKEND_URL}/{image_path}"
        if image_path
        else None
    )
    
    # 1. 페이지 제목 + Stepper
    st.html(
        """
        <div class="product-page-head">
            <div class="page-title-wrap">
                <div class="step-badge">4</div>

                <div>
                    <h1>최종 광고 결과</h1>
                    <p>
                        선택한 광고 시안을 확인하고
                        최종 결과물을 저장해보세요.
                    </p>
                </div>
            </div>

            <div class="stepper">
                <div class="step-item done">
                    <div class="step-dot">✓</div>
                    <span>상품 정보</span>
                </div>

                <div class="step-line active"></div>

                <div class="step-item done">
                    <div class="step-dot">✓</div>
                    <span>광고 전략</span>
                </div>

                <div class="step-line active"></div>

                <div class="step-item done">
                    <div class="step-dot">✓</div>
                    <span>A/B 생성</span>
                </div>

                <div class="step-line active"></div>

                <div class="step-item active">
                    <div class="step-dot">4</div>
                    <span>결과 선택</span>
                </div>
            </div>
        </div>
        """
    )
    
    # 2. 최종 시안 미리보기
    draft_id = selected_draft["id"]
    draft_version = selected_draft.get("version", 1)

    image_path = selected_draft.get("image_path")
    image_url = (
        f"{BACKEND_URL}/{image_path}"
        if image_path
        else None
    )
    
    st.html(
        """
        <style>
        .final-result-preview-image {
            overflow: hidden;
            background: #f4f6f5;
        }

        .final-result-preview-image img {
            display: block;
            width: 100%;
            height: auto;
            object-fit: contain;
        }
        </style>
        """
    )

    if image_url:
        preview_html = f"""
            <div class="final-result-preview-image">
                <img
                    src="{image_url}"
                    alt="최종 광고 시안 {draft_id}"
                >
            </div>
        """
    else:
        preview_html = f"""
            <div class="final-result-preview">
                <span>시안 {draft_id}</span>
                <p>이미지를 불러올 수 없습니다.</p>
                <small>Version {draft_version}</small>
            </div>
        """

    st.html(
        f"""
        <div class="result-content">
            <div class="result-container">
                <section class="final-result-card">
                    <div class="final-result-badge">
                        ✓ 최종 선택
                    </div>

                    {preview_html}

                    <div class="final-result-info">
                        <div>
                            <span class="final-result-label">
                                최종 광고 시안
                            </span>
                            <h2>
                                시안 {draft_id} · Version {draft_version}
                            </h2>
                        </div>
                    </div>
                </section>
            </div>
        </div>
        """
    )
    
    left, right = st.columns([5, 1])

    with left:
        st.empty()

    st.html(
        """
        <style>
        .st-key-back_to_generation button {
            height: 48px;
            border: 1.5px solid #0f8a5f;
            border-radius: 10px;
            background: #ffffff;
            color: #0f8a5f;
            font-size: 14px;
            font-weight: 700;
            transition:
                background 0.2s ease,
                color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .st-key-back_to_generation button:hover {
            border-color: #0f8a5f;
            background: #f4fbf7;
            color: #0f8a5f;
            transform: translateY(-1px);
            box-shadow: 0 5px 14px rgba(15, 138, 95, 0.12);
        }

        .st-key-back_to_generation button:active {
            transform: translateY(0);
        }

        .st-key-back_to_generation button:focus,
        .st-key-back_to_generation button:focus-visible {
            border-color: #0f8a5f;
            outline: none !important;
            color: #0f8a5f;
            box-shadow: 0 0 0 3px rgba(15, 138, 95, 0.12);
        }
        </style>
        """
    )
    with right:
        if st.button(
            "다른 시안 선택",
            key="back_to_generation",
            use_container_width=True,
        ):
            clear_after_draft()

            st.query_params["page"] = "ad_generation"
            st.rerun()

    # 3. 최종 광고 전략 요약
    strategy = final_ad_result["strategy"]

    mode_labels = {
        "faster": "빠른 추천",
        "manual": "직접 설정",
    }

    platform_labels = {
        "instagram": "Instagram",
        "facebook": "Facebook",
        "naver": "네이버",
        "offline": "오프라인 포스터",
    }

    goal_labels = {
        "awareness": "브랜드 인지도",
        "sales": "판매 전환",
        "traffic": "방문 유도",
        "promotion": "프로모션 홍보",
    }

    style_labels = {
        "warm": "따뜻한 감성",
        "modern": "모던 & 미니멀",
        "vivid": "생동감 있는",
        "premium": "프리미엄",
    }

    mode = strategy.get("mode")
    platform = strategy.get("platform")
    goal = strategy.get("goal")
    style = strategy.get("style")
    poster_size = strategy.get("poster_size")
    selected_slogan = strategy.get("selected_slogan")
    
    summary_items = []

    if mode:
        summary_items.append(
            f"""
            <div class="result-summary-item">
                <span>전략 모드</span>
                <strong>{mode_labels.get(mode, mode)}</strong>
            </div>
            """
        )

    if platform:
        platform_text = platform_labels.get(
            platform,
            platform,
        )

        summary_items.append(
            f"""
            <div class="result-summary-item">
                <span>광고 플랫폼</span>
                <strong>{platform_text}</strong>
            </div>
            """
        )

    if goal:
        summary_items.append(
            f"""
            <div class="result-summary-item">
                <span>광고 목표</span>
                <strong>{goal_labels.get(goal, goal)}</strong>
            </div>
            """
        )

    if style:
        summary_items.append(
            f"""
            <div class="result-summary-item">
                <span>시각적 스타일</span>
                <strong>{style_labels.get(style, style)}</strong>
            </div>
            """
        )

    if poster_size:
        summary_items.append(
            f"""
            <div class="result-summary-item">
                <span>포스터 규격</span>
                <strong>{poster_size.upper()}</strong>
            </div>
            """
        )

    summary_html = "".join(summary_items)

    st.html(
        f"""
        <div class="result-content">
            <div class="result-container">
                <section class="result-strategy-card">
                    <div class="result-strategy-head">
                        <span>최종 광고 전략</span>
                        <h3>
                            {selected_slogan or "선택한 전략으로 생성된 광고"}
                        </h3>
                    </div>

                    <div class="result-summary-grid">
                        {summary_html}
                    </div>
                </section>
            </div>
        </div>
        """
    )
    
    # 4. 최종 액션 버튼
    image_path = selected_draft.get("image_path")

    st.html(
        """
        <style>
        /* 결과물 다운로드 */
        .st-key-download_final_ad button {
            height: 56px;
            border: none;
            border-radius: 12px;
            background: #0f8a5f;
            color: #ffffff;
            font-size: 15px;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(15, 138, 95, 0.16);
            transition:
                background 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .st-key-download_final_ad button:hover {
            border: none;
            background: #0b7651;
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(15, 138, 95, 0.22);
        }

        /* 다운로드 비활성화 */
        .st-key-download_final_ad_disabled button {
            height: 56px;
            border: none;
            border-radius: 12px;
            background: #dce3df;
            color: #98a39d;
            font-size: 15px;
            font-weight: 800;
            opacity: 1;
            cursor: not-allowed;
        }

        /* 새 광고 만들기 */
        .st-key-create_new_ad button {
            height: 56px;
            border: 1.5px solid #d9e1dc;
            border-radius: 12px;
            background: #ffffff;
            color: #17211c;
            font-size: 15px;
            font-weight: 800;
            transition:
                border-color 0.2s ease,
                background 0.2s ease,
                transform 0.2s ease;
        }

        .st-key-create_new_ad button:hover {
            border-color: #79b79c;
            background: #f4fbf7;
            color: #0f8a5f;
            transform: translateY(-1px);
        }

        .st-key-create_new_ad button:active {
            transform: translateY(0);
        }
        </style>
        """
    )

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if image_path:
            image_url = f"{BACKEND_URL}/{image_path}"

            try:
                image_bytes = download_generated_image(image_path)

                st.download_button(
                    "↓ 결과물 다운로드",
                    data=image_bytes,
                    file_name=(
                        f"admaker_draft_{draft_id}"
                        f"_v{draft_version}.png"
                    ),
                    mime="image/png",
                    key="download_final_ad",
                    use_container_width=True,
                )

            except APIError:
                st.button(
                    "↓ 결과물 다운로드",
                    key="download_final_ad_disabled",
                    use_container_width=True,
                    disabled=True,
                )
        else:
            st.button(
                "↓ 결과물 다운로드",
                key="download_final_ad_disabled",
                use_container_width=True,
                disabled=True,
            )

    with action_col2:
        new_ad_clicked = st.button(
            "＋ 새 광고 만들기",
            key="create_new_ad",
            use_container_width=True,
        )
    
    if new_ad_clicked:
        keys_to_clear = [
            # 상품 입력
            "product_name",
            "product_price",
            "product_description",
            "product_industry",
            "product_image",
            "product_image_path",
            "product_id",

            # 상품 입력 위젯
            "product_name_input",
            "product_price_input",
            "product_description_input",

            # 프로젝트
            "project_id",

            # 전략 선택
            "strategy_mode",
            "reuse_previous_tone",
            "selected_platform",
            "poster_size",
            "selected_goal",
            "selected_style",
            "strategy_data",
            "recommendation",
            "selected_slogan",

            # 광고 생성
            "generation_status",
            "generated_drafts",
            "drafts",
            "selected_draft",
            "regeneration_request",
            "regenerating_draft",
            "regeneration_completed",

            # 최종 결과
            "final_ad_result",
        ]

        for key in keys_to_clear:
            st.session_state.pop(key, None)
    
        dynamic_keys = [
            key
            for key in list(st.session_state.keys())
            if (
                key.startswith("draft_feedback_")
                or key.startswith("industry_")
            )
        ]

        for key in dynamic_keys:
            st.session_state.pop(key, None)

        st.query_params["page"] = "product_input"
        st.rerun()
    