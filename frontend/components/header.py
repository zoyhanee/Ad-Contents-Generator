import html

import streamlit as st

from utils.state import is_authenticated


def render_header():
    authenticated = is_authenticated()

    user = st.session_state.get("user", {})

    if authenticated:
        user_name = html.escape(
            user.get("name")
            or user.get("email")
            or "사용자"
        )

        auth_html = f"""
        <div class="auth">
            <span class="user-name">
                {user_name}
            </span>
            <a
                class="nav-btn"
                href="?page=logout"
                target="_self"
            >
                로그아웃
            </a>
        </div>
        """
    else:
        auth_html = """
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
        """

    st.html(
        f"""
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

            {auth_html}
        </div>
        """
    )