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
        "login_email_input",
        "login_password_input",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def clear_signup_state():
    keys = [
        "signup_email_input",
        "signup_password_input",
        "signup_password_confirm_input",
        "signup_store_name_input",
        "signup_success_confirm",
    ]

    for key in keys:
        st.session_state.pop(key, None)
       
        
def clear_after_product():
    keys = [
        # 전략 설정
        "strategy_mode",
        "selected_platform",
        "poster_size",
        "selected_goal",
        "selected_style",

        # 전략 추천 결과
        "project_id",
        "strategy_data",
        "recommendation",
        "selected_slogan",

        # 광고 생성 결과
        "generation_status",
        "generated_drafts",
        "selected_draft",
        "selected_post_copy",
        "regeneration_request",
        "regenerating_draft",
        "regeneration_completed",
        "final_ad_result",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def clear_recommendation_state():
    keys = [
        "project_id",
        "strategy_data",
        "recommendation",
        "selected_slogan",
    ]

    for key in keys:
        st.session_state.pop(key, None)
        
        
def clear_after_strategy():
    keys = [
        "generation_status",
        "generated_drafts",
        "selected_draft",
        "selected_post_copy",
        "regeneration_request",
        "regenerating_draft",
        "regeneration_completed",
        "final_ad_result",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def clear_after_draft():
    st.session_state.pop("final_ad_result", None)
    
