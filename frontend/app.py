from pathlib import Path

import streamlit as st


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


st.html(load_html(get_current_page()))
