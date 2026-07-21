from pathlib import Path
from urllib.parse import quote

import streamlit as st

from api.auth import AuthAPIError, get_me
from components.header import render_header
from utils.state import clear_auth_state, is_authenticated
from pages.login import render_login
from pages.signup import render_signup
from pages.product_input import render_product_input
from pages.strategy import render_strategy_selection
from pages.ad_generation import render_ad_generation
from pages.result import render_result
from pages.history import render_history


st.set_page_config(
    page_title="AdMaker AI",
    page_icon="📣",
    layout="wide",
)


BASE_DIR = Path(__file__).parent

PAGES = {
    "landing": "landing.html",
    "login": "login.html",
    "signup": "signup.html",
    "logout": None,
    "oauth_callback": None,
    "product_input": "product_input.html",
    "strategy_selection": "strategy_selection.html",
    "ad_generation": "ad_generation.html",
    "result": None,
    "history": None,
}

    
PROTECTED_PAGES = {
    "product_input",
    "strategy_selection",
    "ad_generation",
    "result",
    "history",
}

def get_current_page():
    page = st.query_params.get("page", "landing")

    if isinstance(page, list):
        page = page[0]

    return page if page in PAGES else "landing"


def load_html(page_name):
    css = (BASE_DIR / "styles.css").read_text(encoding="utf-8")
    body = (BASE_DIR / PAGES[page_name]).read_text(encoding="utf-8")

    return f"<style>{css}</style>{body}"


def load_landing_body():
    body = (BASE_DIR / "landing.html").read_text(encoding="utf-8")
    hero_start = body.find('<div class="hero-wrap">')

    if hero_start == -1:
        return body

    body = body[hero_start:]
    access_token = st.session_state.get("access_token")

    if is_authenticated() and access_token:
        body = body.replace(
            'href="?page=product_input"',
            (
                'href="?page=product_input'
                f'&access_token={quote(access_token, safe="")}"'
            ),
        )

    return body


def load_common_css():
    css = (BASE_DIR / "styles.css").read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


current_page = get_current_page()

access_token = st.query_params.get("access_token")

if isinstance(access_token, list):
    access_token = access_token[0]

if (
    access_token
    and current_page != "oauth_callback"
    and not is_authenticated()
):
    st.session_state["access_token"] = access_token

    try:
        user = get_me()

    except AuthAPIError:
        clear_auth_state()
        st.error("로그인 정보를 다시 불러오지 못했습니다.")
        st.query_params["page"] = "login"
        st.rerun()

    st.session_state["user"] = user
    st.session_state["is_authenticated"] = True

    st.query_params.clear()
    st.query_params["page"] = current_page
    st.rerun()

if current_page == "logout":
    clear_auth_state()

    st.query_params["page"] = "landing"
    st.rerun()

if current_page == "oauth_callback":
    access_token = st.query_params.get("access_token")

    if isinstance(access_token, list):
        access_token = access_token[0]

    if not access_token:
        st.error("Google 로그인 토큰을 확인할 수 없습니다.")
        st.query_params["page"] = "login"
        st.rerun()

    st.session_state["access_token"] = access_token

    try:
        user = get_me()

    except AuthAPIError:
        clear_auth_state()
        st.error("Google 로그인 정보를 불러오지 못했습니다.")
        st.query_params["page"] = "login"
        st.rerun()

    st.session_state["user"] = user
    st.session_state["is_authenticated"] = True

    st.query_params.clear()
    st.query_params["page"] = "product_input"
    st.rerun()
    
if (
    current_page in {"login", "signup"}
    and is_authenticated()
):
    st.query_params["page"] = "product_input"
    st.rerun()
    
if (
    current_page in PROTECTED_PAGES
    and not is_authenticated()
):
    st.warning("로그인이 필요한 서비스입니다.")

    st.query_params["page"] = "login"
    st.rerun()

if current_page == "login":
    load_common_css()
    render_login()
    
elif current_page == "signup":
    load_common_css()
    render_signup()

elif current_page == "product_input":
    load_common_css()
    render_product_input()
    
elif current_page == "strategy_selection":
    load_common_css()
    render_strategy_selection()

elif current_page == "ad_generation":
    load_common_css()
    render_ad_generation()

elif current_page == "result":
    load_common_css()
    render_result()
    
elif current_page == "history":
    load_common_css()
    render_history()

else:
    load_common_css()
    render_header()
    st.html(load_landing_body())
