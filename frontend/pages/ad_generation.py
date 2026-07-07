import html
import time

import requests
import streamlit as st

from utils.state import clear_after_strategy


BACKEND_URL = "http://127.0.0.1:8000"


def render_ad_generation():
    # 1. 생성 페이지 상태 초기화
    if "selected_draft" not in st.session_state:
        st.session_state.selected_draft = None

    if "drafts" not in st.session_state:
        st.session_state.drafts = []

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
                <div class="step-badge">3</div>

                <div>
                    <h1>광고 시안 생성</h1>
                    <p>
                        선택한 전략을 바탕으로
                        AI가 다양한 광고 시안을 생성해드려요.
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

                <div class="step-item active">
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
    st.html(
        """
        <style>
        .st-key-edit_strategy {
            margin-top: 10px;
            margin-bottom: 24px;
        }

        .st-key-edit_strategy button {
            height: 42px;
            border: 1.5px solid #d9e1dc;
            border-radius: 10px;
            background: #ffffff;
            color: #0f8a5f;
            font-size: 14px;
            font-weight: 700;
        }

        .st-key-edit_strategy button:hover {
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
            "전략 수정",
            key="edit_strategy",
            use_container_width=True,
        ):
            clear_after_strategy()
            
            st.query_params["page"] = "strategy_selection"
            st.rerun()
    
    # 4. 전략 데이터 불러오기
    final_strategy_data = st.session_state.get("final_strategy_data")

    if final_strategy_data is None:
        st.warning(
            "선택된 광고 전략 정보가 없습니다. "
            "광고 전략을 먼저 선택해주세요."
        )

        if st.button(
            "광고 전략 선택으로 돌아가기",
            key="back_to_strategy",
        ):
            st.query_params["page"] = "strategy_selection"
            st.rerun()

        return
    
    product_data = final_strategy_data.get("product")
    if not product_data:
        st.warning(
            "상품 정보가 없습니다. "
            "먼저 상품 정보를 입력해주세요."
        )

        if st.button(
            "상품 정보 입력으로 이동",
            key="back_to_product",
        ):
            st.query_params["page"] = "product_input"
            st.rerun()

        return
    product_name = html.escape(product_data["name"])
    product_price = html.escape(product_data["price"])

    # 5. 전략 데이터 표시용 변환
    platform_labels = {
        "instagram": "Instagram",
        "baemin": "배달의민족",
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


    platform = final_strategy_data.get("platform")

    platform_text = platform_labels.get(
        platform,
        platform,
    ) if platform else ""

    goal = final_strategy_data.get("goal")
    style = final_strategy_data.get("style")
    selected_slogan = final_strategy_data.get("selected_slogan")

    mode_labels = {
        "faster": "빠른 추천",
        "manual": "직접 설정",
    }

    mode = final_strategy_data.get("mode")
    poster_size = final_strategy_data.get("poster_size")

    summary_items = []

    # 전략 모드
    if mode:
        summary_items.append(
            f"<span><strong>전략 모드</strong> "
            f"{mode_labels.get(mode, mode)}</span>"
        )

    # 플랫폼
    if platform_text:
        summary_items.append(
            f"<span><strong>플랫폼</strong> "
            f"{platform_text}</span>"
        )

    # 광고 목표
    if goal:
        summary_items.append(
            f"<span><strong>광고 목표</strong> "
            f"{goal_labels.get(goal, goal)}</span>"
        )

    # 시각적 스타일
    if style:
        summary_items.append(
            f"<span><strong>스타일</strong> "
            f"{style_labels.get(style, style)}</span>"
        )

    # 포스터 규격
    if poster_size:
        summary_items.append(
            f"<span><strong>포스터 규격</strong> "
            f"{poster_size.upper()}</span>"
        )

    summary_html = "".join(summary_items)
    
    # 6. 선택 전략 요약
    st.html(
        f"""
        <div class="strategy-content">
            <div class="strategy-container">
                <section class="generation-strategy-card">
                    <div class="generation-strategy-head">
                        <div>
                            <span class="generation-strategy-label">
                                {product_name} · {product_price}
                            </span>
                            <h3>{selected_slogan or "선택한 전략으로 광고를 생성합니다"}</h3>
                        </div>
                    </div>

                    <div class="generation-strategy-items">
                        {summary_html}
                    </div>
                </section>
            </div>
        </div>
        """
    )

    # 7. 광고 시안 생성 상태 초기화
    if "generation_status" not in st.session_state:
        st.session_state.generation_status = "ready"

    if "generated_drafts" not in st.session_state:
        st.session_state.generated_drafts = []
    
    st.html(
        """
        <style>
        .st-key-start_generation {
            margin-top: 24px;
            margin-bottom: 48px;
        }

        .st-key-start_generation button {
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

        .st-key-start_generation button:hover {
            border: none;
            background: #0b7651;
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(15, 138, 95, 0.22);
        }

        .st-key-start_generation button:active {
            transform: translateY(0);
        }
        </style>
        """
    )
    # 8. 광고 시안 생성 시작
    if st.session_state.generation_status == "ready":
        st.html(
            """
            <div class="generation-ready">
                <div class="generation-ready-icon">✨</div>
                <h3>광고 시안을 생성할 준비가 되었어요</h3>
                <p>
                    선택한 상품 정보와 광고 전략을 바탕으로
                    AI가 다양한 광고 시안을 생성합니다.
                </p>
            </div>
            """
        )

        if st.button(
            "✨ AI 광고 시안 생성하기",
            key="start_generation",
            use_container_width=True,
        ):
            st.session_state.generation_status = "generating"
            st.rerun()
            
    # 9. 광고 시안 생성 중
    elif st.session_state.generation_status == "generating":
        st.html(
            """
            <div class="generation-loading">
                <div class="generation-loading-icon">✨</div>
                <h3>AI가 광고 시안을 만들고 있어요</h3>
                <p>
                    상품과 전략을 분석해 서로 다른 광고 방향을 생성하고 있습니다.
                </p>
            </div>
            """
        )

        progress_bar = st.progress(0)
        status_text = st.empty()
        generation_steps = [
            (20, "상품 정보를 분석하고 있어요..."),
            (45, "광고 전략을 적용하고 있어요..."),
            (70, "시각적 콘셉트를 구성하고 있어요..."),
            (90, "광고 시안을 마무리하고 있어요..."),
            (100, "생성이 완료되었습니다."),
        ]

        for progress, message in generation_steps:
            progress_bar.progress(progress)
            status_text.caption(message)
            time.sleep(0.5)

        payload = {
            "project_id": final_strategy_data["project_id"],
            "selected_slogan": selected_slogan,
        }

        try:
            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()

            st.session_state.generated_drafts = result["drafts"]
            st.session_state.generation_status = "completed"
            st.rerun()

        except requests.exceptions.ConnectionError:
            st.session_state.generation_status = "ready"
            st.error(
                "백엔드 서버에 연결할 수 없습니다. "
                "FastAPI 서버가 실행 중인지 확인해주세요."
            )

        except requests.exceptions.RequestException as e:
            st.session_state.generation_status = "ready"
            st.error(f"광고 시안 생성 요청 중 오류가 발생했습니다: {e}")
        
    # 10. 광고 시안 생성 완료
    elif st.session_state.generation_status == "completed":
        st.subheader("생성된 광고 시안")

        st.caption(
            "마음에 드는 시안을 선택해주세요. "
            "선택 후 수정하거나 다음 단계로 진행할 수 있어요."
        )

        selected_draft = st.session_state.selected_draft

        draft_css = """
        <style>
        .draft-preview-card {
            overflow: hidden;
            border: 1.5px solid #d9e1dc;
            border-radius: 16px;
            background: #ffffff;
        }

        .draft-preview-placeholder {
            aspect-ratio: 4 / 5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background:
                linear-gradient(
                    145deg,
                    #f4fbf7,
                    #edf3ef
                );
            color: #17211c;
        }

        .draft-preview-placeholder span {
            font-size: 26px;
            font-weight: 800;
        }

        .draft-preview-placeholder p {
            margin: 8px 0 0;
            color: #718078;
            font-size: 14px;
        }

        .st-key-select_draft_A button,
        .st-key-select_draft_B button,
        .st-key-select_draft_C button {
            height: 52px;
            margin-top: 10px;
            border: 1.5px solid #d9e1dc;
            border-radius: 10px;
            background: #ffffff;
            color: #17211c;
            font-weight: 700;
        }

        .st-key-select_draft_A button:hover,
        .st-key-select_draft_B button:hover,
        .st-key-select_draft_C button:hover {
            border-color: #79b79c;
            background: #ffffff;
            color: #17211c;
        }
        .st-key-draft_feedback_A textarea,
        .st-key-draft_feedback_B textarea,
        .st-key-draft_feedback_C textarea {
            min-height: 120px;
            border: 1.5px solid #d9e1dc;
            border-radius: 12px;
            background: #ffffff;
            color: #17211c;
        }

        .st-key-draft_feedback_A textarea:focus,
        .st-key-draft_feedback_B textarea:focus,
        .st-key-draft_feedback_C textarea:focus {
            border-color: #0f8a5f;
            box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
        }

        .st-key-draft_feedback_A textarea::placeholder,
        .st-key-draft_feedback_B textarea::placeholder,
        .st-key-draft_feedback_C textarea::placeholder {
            color: #a0aaa5;
        }
        .st-key-draft_feedback_A label,
        .st-key-draft_feedback_B label,
        .st-key-draft_feedback_C label {
            color: #17211c;
            font-size: 14px;
            font-weight: 700;
        }
        """

        if selected_draft is not None:
            draft_css += f"""
            .st-key-select_draft_{selected_draft} button {{
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
                box-shadow:
                    0 0 0 2px rgba(15, 138, 95, 0.1);
            }}

            .st-key-select_draft_{selected_draft} button:hover {{
                background: #f4fbf7;
                color: #0f8a5f;
            }}
            """

        draft_css += "</style>"

        st.html(draft_css)

        draft_cols = st.columns(3)

        for col, draft in zip(
            draft_cols,
            st.session_state.generated_drafts,
        ):
            draft_id = draft["id"]
            is_selected = (
                st.session_state.selected_draft == draft_id
            )

            with col:
                st.html(
                    f"""
                    <div class="draft-preview-card">
                        <div class="draft-preview-placeholder">
                            <span>시안 {draft_id}</span>
                            <p>AI 생성 이미지 영역</p>
                            <small>Version {draft["version"]}</small>
                        </div>
                    </div>
                    """
                )

                if st.button(
                    f"시안 {draft_id} 선택",
                    key=f"select_draft_{draft_id}",
                    use_container_width=True,
                ):
                    st.session_state.selected_draft = draft_id
                    st.rerun()
        st.html(
            """
            <style>
            .st-key-regenerate_selected_draft button {
                height: 48px;
                border: 1.5px solid #0f8a5f;
                border-radius: 10px;
                background: #ffffff;
                color: #0f8a5f;
                font-weight: 800;
            }

            .st-key-regenerate_selected_draft button:hover {
                border-color: #0f8a5f;
                background: #f4fbf7;
                color: #0f8a5f;
            }

            .st-key-regenerate_selected_draft button:disabled {
                border-color: #d9e1dc;
                background: #f4f6f5;
                color: #a0aaa5;
                opacity: 1;
            }
            </style>
            """
        )
        # 11. 선택 시안 피드백 및 재생성
        selected_draft = st.session_state.selected_draft

        if selected_draft is not None:
            st.divider()

            st.subheader(f"시안 {selected_draft} 수정하기")

            feedback = st.text_area(
                "수정하고 싶은 내용을 입력해주세요",
                placeholder=(
                    "예: 배경을 더 밝게 해주세요. "
                    "상품이 더 크게 보이게 해주세요."
                ),
                key=f"draft_feedback_{selected_draft}",
                height=120,
            )

            feedback_col, regenerate_col = st.columns([3, 1])

            with feedback_col:
                st.caption(
                    f"현재 선택된 시안: 시안 {selected_draft}"
                )

            with regenerate_col:
                regenerate_clicked = st.button(
                    "선택 시안 재생성",
                    key="regenerate_selected_draft",
                    use_container_width=True,
                    disabled=not feedback.strip(),
                )

            if regenerate_clicked:
                st.session_state.regeneration_request = {
                    "draft_id": selected_draft,
                    "feedback": feedback.strip(),
                }

                st.session_state.regenerating_draft = selected_draft
                st.rerun()

        # 12. 선택 시안 재생성 처리
        regenerating_draft = st.session_state.get("regenerating_draft")

        if regenerating_draft is not None:
            with st.spinner(
                f"시안 {regenerating_draft}을 다시 생성하고 있어요..."
            ):
                time.sleep(1.5)

            for draft in st.session_state.generated_drafts:
                if draft["id"] == regenerating_draft:
                    draft["version"] += 1
                    break

            st.session_state.regenerating_draft = None
            st.session_state.regeneration_completed = regenerating_draft

            st.rerun()
            
        regenerated_draft = st.session_state.pop(
            "regeneration_completed",
            None,
        )

        if regenerated_draft is not None:
            st.success(
                f"시안 {regenerated_draft}이 새 버전으로 재생성되었습니다."
            )
            
        # 13. 하단 액션 버튼
        st.divider()
        
        st.html(
            """
            <style>
            .st-key-regenerate_all_drafts button {
                height: 56px;
                border: 1.5px solid #d9e1dc;
                border-radius: 12px;
                background: #ffffff;
                color: #17211c;
                font-size: 15px;
                font-weight: 800;
            }

            .st-key-regenerate_all_drafts button:hover {
                border-color: #79b79c;
                background: #f8fbf9;
                color: #17211c;
            }

            .st-key-proceed_selected_draft button {
                height: 56px;
                border: none;
                border-radius: 12px;
                background: #0f8a5f;
                color: #ffffff;
                font-size: 15px;
                font-weight: 800;
                box-shadow: 0 8px 20px rgba(15, 138, 95, 0.16);
            }

            .st-key-proceed_selected_draft button:hover {
                border: none;
                background: #0b7651;
                color: #ffffff;
            }

            .st-key-proceed_selected_draft button:disabled {
                border: none;
                background: #dce3df;
                color: #98a39d;
                box-shadow: none;
                opacity: 1;
            }
            </style>
            """
        )

        action_col1, action_col2 = st.columns(2)

        with action_col1:
            regenerate_all_clicked = st.button(
                "↻ 전체 시안 다시 생성",
                key="regenerate_all_drafts",
                use_container_width=True,
            )

        with action_col2:
            proceed_clicked = st.button(
                "선택한 시안으로 진행 →",
                key="proceed_selected_draft",
                use_container_width=True,
                disabled=st.session_state.selected_draft is None,
            )
            
        if regenerate_all_clicked:
            st.session_state.generation_status = "generating"
            st.session_state.generated_drafts = []
            st.session_state.selected_draft = None

            st.session_state.pop("regeneration_request", None)
            st.session_state.pop("regenerating_draft", None)
            st.session_state.pop("regeneration_completed", None)

            st.rerun()

        if proceed_clicked:
            selected_draft_id = st.session_state.selected_draft

            selected_draft_data = next(
                (
                    draft
                    for draft in st.session_state.generated_drafts
                    if draft["id"] == selected_draft_id
                ),
                None,
            )

            st.session_state.final_ad_result = {
                "strategy": st.session_state.final_strategy_data,
                "selected_draft": selected_draft_data,
            }

            st.query_params["page"] = "result"
            st.rerun()