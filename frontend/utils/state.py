import streamlit as st


def clear_after_product():
    keys = [
        "project_id",
        "strategy_data",
        "recommendation",
        "selected_slogan",
        "generation_status",
        "generated_drafts",
        "selected_draft",
        "regeneration_request",
        "regenerating_draft",
        "regeneration_completed",
        "final_ad_result",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def clear_after_strategy():
    keys = [
        "generation_status",
        "generated_drafts",
        "selected_draft",
        "regeneration_request",
        "regenerating_draft",
        "regeneration_completed",
        "final_ad_result",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def clear_after_draft():
    st.session_state.pop("final_ad_result", None)