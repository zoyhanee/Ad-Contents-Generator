import streamlit as st

from utils.state import (
    clear_auth_state,
    is_authenticated,
)


def go_to_page(page: str) -> None:
    st.query_params["page"] = page
    st.rerun()


def render_header() -> None:
    authenticated = is_authenticated()

    user = st.session_state.get("user", {})

    user_name = (
        user.get("name")
        or user.get("email")
        or "사용자"
    )

    st.html(
        """
        <style>
        .header-brand {
            height: 44px;
            display: flex;
            align-items: center;
            font-size: 28px;
            font-weight: 800;
            color: #0f7a4a;
            white-space: nowrap;
        }

        .header-brand span {
            color: #ff4f3e;
        }

        .header-user {
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            color: #17211c;
            font-size: 14px;
            font-weight: 700;
            white-space: nowrap;
        }

        div[data-testid="stHorizontalBlock"]:has(
            .header-brand
        ) {
            min-height: 84px;
            align-items: center;
            border-bottom: 1px solid #e5e7eb;
            margin-bottom: 56px;
        }

        .st-key-header_new_ad button,
        .st-key-header_history button {
            height: 44px;
            border: none;
            background: transparent;
            color: #17211c;
            font-size: 15px;
            font-weight: 700;
            white-space: nowrap;
        }

        .st-key-header_new_ad button:hover,
        .st-key-header_history button:hover {
            border: none;
            background: #f4fbf7;
            color: #0f8a5f;
        }

        .st-key-header_logout button {
            height: 44px;
            border: 1px solid #0f7a4a;
            border-radius: 8px;
            background: #ffffff;
            color: #0f7a4a;
            font-size: 14px;
            font-weight: 800;
            white-space: nowrap;
        }

        .st-key-header_logout button:hover {
            border-color: #0f7a4a;
            background: #f4fbf7;
            color: #0f7a4a;
        }
        </style>
        """
    )

    if authenticated:
        (
            logo_col,
            spacer_left,
            new_ad_col,
            history_col,
            spacer_right,
            user_col,
            logout_col,
        ) = st.columns(
            [1.6, 1.2, 1.2, 0.9, 1.2, 1.5, 0.9],
            vertical_alignment="center",
        )

        with logo_col:
            st.html(
                """
                <div class="header-brand">
                    AdMaker&nbsp;<span>AI</span>
                </div>
                """
            )

        with new_ad_col:
            if st.button(
                "새 광고 만들기",
                key="header_new_ad",
                width="stretch",
            ):
                go_to_page("product_input")

        with history_col:
            if st.button(
                "히스토리",
                key="header_history",
                width="stretch",
            ):
                st.session_state.pop(
                    "selected_history_project_id",
                    None,
                )
                st.session_state.pop(
                    "selected_history_version",
                    None,
                )
                st.session_state.pop(
                    "history_editing",
                    None,
                )

                go_to_page("history")

        with user_col:
            st.html(
                f"""
                <div class="header-user">
                    {user_name}
                </div>
                """
            )

        with logout_col:
            if st.button(
                "로그아웃",
                key="header_logout",
                width="stretch",
            ):
                clear_auth_state()
                go_to_page("landing")

        return

    st.html(
        """
        <div class="header">
            <a
                class="logo"
                href="?page=landing"
                target="_self"
            >
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
                <a
                    class="nav-btn"
                    href="?page=login"
                    target="_self"
                >
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