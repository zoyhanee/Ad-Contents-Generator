import streamlit as st


def is_authenticated() -> bool:
    return (
        st.session_state.get("is_authenticated", False)
        and "access_token" in st.session_state
    )
    
    
def clear_auth_state():
    keys = [
        "access_token",
        "user",
        "is_authenticated",
        "login_email",
        "login_password",
    ]

    for key in keys:
        st.session_state.pop(key, None)
        
        
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