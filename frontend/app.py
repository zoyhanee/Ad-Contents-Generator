from pathlib import Path

import streamlit as st

from pages.product_input import render_product_input
from pages.strategy import render_strategy_selection
from pages.ad_generation import render_ad_generation
from pages.result import render_result


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
    "product_input": "product_input.html",
    "strategy_selection": "strategy_selection.html",
    "ad_generation": "ad_generation.html",
    "result": None,
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


def load_common_css():
    css = (BASE_DIR / "styles.css").read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


current_page = get_current_page()

if current_page == "product_input":
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

else:
    st.html(load_html(current_page))