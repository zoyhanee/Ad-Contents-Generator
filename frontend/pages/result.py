import streamlit as st


def render_result():
    # 최종 결과 데이터 확인
    final_ad_result = st.session_state.get("final_ad_result")

    if final_ad_result is None:
        st.warning(
            "선택된 최종 광고 시안이 없습니다. "
            "광고 시안을 먼저 선택해주세요."
        )

        if st.button(
            "광고 시안 선택으로 돌아가기",
            key="back_to_ad_generation",
        ):
            st.query_params["page"] = "ad_generation"
            st.rerun()

        return

    # 공통 헤더
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

                <a
                    class="nav-btn primary"
                    href="?page=signup"
                    target="_self"
                >
                    회원가입
                </a>
            </div>
        </div>
        """
    )

    # 선택된 최종 시안
    selected_draft = final_ad_result["selected_draft"]

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

    st.html(
        f"""
        <div class="result-content">
            <div class="result-container">
                <section class="final-result-card">
                    <div class="final-result-badge">
                        ✓ 최종 선택
                    </div>

                    <div class="final-result-preview">
                        <span>시안 {draft_id}</span>
                        <p>AI 생성 이미지 영역</p>
                        <small>Version {draft_version}</small>
                    </div>

                    <div class="final-result-info">
                        <div>
                            <span class="final-result-label">
                                최종 광고 시안
                            </span>
                            <h2>시안 {draft_id}</h2>
                        </div>

                        <a
                            class="strategy-edit-link"
                            href="?page=ad_generation"
                            target="_self"
                        >
                            다른 시안 선택
                        </a>
                    </div>
                </section>
            </div>
        </div>
        """
    )

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
    platforms = strategy.get("platforms", [])
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

    if platforms:
        platform_text = ", ".join(
            platform_labels.get(platform, platform)
            for platform in platforms
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

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if image_path:
            with open(image_path, "rb") as image_file:
                st.download_button(
                    "↓ 결과물 다운로드",
                    data=image_file,
                    file_name=(
                        f"admaker_draft_{draft_id}"
                        f"_v{draft_version}.png"
                    ),
                    mime="image/png",
                    key="download_final_ad",
                    use_container_width=True,
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
            "strategy_mode",
            "reuse_previous_tone",
            "selected_platforms",
            "poster_size",
            "selected_goal",
            "selected_style",
            "strategy_data",
            "recommendation",
            "selected_slogan",
            "final_strategy_data",
            "generation_status",
            "generated_drafts",
            "selected_draft",
            "regeneration_request",
            "regenerating_draft",
            "regeneration_completed",
            "final_ad_result",
        ]

        for key in keys_to_clear:
            st.session_state.pop(key, None)
    
        feedback_keys = [
            key
            for key in st.session_state.keys()
            if key.startswith("draft_feedback_")
        ]

        for key in feedback_keys:
            st.session_state.pop(key, None)

        st.query_params["page"] = "product_input"
        st.rerun()
    