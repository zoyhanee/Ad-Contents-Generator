import streamlit as st
import requests

from components.header import render_header
from api.auth import AuthAPIError, signup
from utils.state import clear_signup_state


@st.dialog("회원가입 완료 🎉", dismissible=False)
def show_signup_success_dialog():
    st.write("회원가입이 완료되었습니다.")
    st.write("로그인 페이지로 이동해주세요.")

    if st.button(
        "로그인하러 가기",
        key="signup_success_confirm",
        use_container_width=True,
    ):
        clear_signup_state()

        st.query_params["page"] = "login"
        st.rerun()


def render_signup():
    # 1. 회원가입 상태 초기화

    # 2. 공통 헤더
    render_header()
    
    left_col, right_col = st.columns(
        [1, 1],
        gap="large",
    )
    
    with left_col:
        st.html(
            """
            <div class="signup-info">
                <div class="signup-visual">Ad</div>

                <div class="signup-info-item">
                    <div class="signup-info-icon">○</div>
                    <div>
                        <h3>이메일 인증 없이 간편 가입</h3>
                        <p>
                            복잡한 절차 없이 빠르게 서비스를
                            시작할 수 있어요.
                        </p>
                    </div>
                </div>

                <div class="signup-info-item">
                    <div class="signup-info-icon">□</div>
                    <div>
                        <h3>생성 결과 저장</h3>
                        <p>
                            생성한 광고 콘텐츠를 안전하게 저장합니다.
                        </p>
                    </div>
                </div>

                <div class="signup-info-item">
                    <div class="signup-info-icon">↺</div>
                    <div>
                        <h3>과거 작업물 불러오기</h3>
                        <p>
                            이전 작업물을 쉽게 불러와
                            계속 작업할 수 있어요.
                        </p>
                    </div>
                </div>
            </div>
            """
        )
        
    with right_col:
        st.html(
            """
            <style>

            .st-key-signup_email_input [data-baseweb="input"],
            .st-key-signup_password_input [data-baseweb="input"],
            .st-key-signup_password_confirm_input [data-baseweb="input"],
            .st-key-signup_store_name_input [data-baseweb="input"] {
                background: #ffffff !important;
                border-radius: 10px !important;
            }

            .st-key-signup_email_input label,
            .st-key-signup_password_input label,
            .st-key-signup_password_confirm_input label,
            .st-key-signup_store_name_input label {
                color: #17211c;
                font-size: 14px;
                font-weight: 700;
            }

            .st-key-signup_email_input input,
            .st-key-signup_password_input input,
            .st-key-signup_password_confirm_input input,
            .st-key-signup_store_name_input input {
                border: 1.5px solid #d9e1dc;
                border-radius: 10px;
                background: #ffffff !important;
                color: #17211c !important;
            }

            .st-key-signup_email_input input::placeholder,
            .st-key-signup_password_input input::placeholder,
            .st-key-signup_password_confirm_input input::placeholder,
            .st-key-signup_store_name_input input::placeholder {
                color: #a0aaa5;
                opacity: 1;
            }
            
            .st-key-signup_password_input [data-baseweb="input"] > div,
            .st-key-signup_password_confirm_input [data-baseweb="input"] > div {
                background: #ffffff !important;
            }

            .st-key-signup_password_input button,
            .st-key-signup_password_confirm_input button {
                background: #ffffff !important;
                border: none !important;
                color: #6b756f !important;
                box-shadow: none !important;
            }

            .st-key-signup_password_input button:hover,
            .st-key-signup_password_confirm_input button:hover {
                background: #ffffff !important;
                color: #0f8a5f !important;
            }
            
            .st-key-signup_submit button {
                min-height: 48px;
                margin-top: 8px;
                border: none;
                border-radius: 10px;
                background: #0f8a5f;
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
            }

            .st-key-signup_submit button:hover {
                border: none;
                background: #0b7651;
                color: #ffffff;
            }

            .st-key-signup_submit button:focus {
                border: none;
                color: #ffffff;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.15);
            }
            
            .st-key-signup_feedback [data-testid="stAlert"] {
                border-radius: 10px;
            }

            .st-key-signup_feedback [data-testid="stAlert"] p {
                color: #7a5d00 !important;
                font-weight: 600;
            }
            
            .signup-login-link {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 8px;
                margin-top: 22px;
                color: #6b756f;
                font-size: 14px;
            }

            .signup-login-link a {
                color: #0f8a5f;
                font-weight: 700;
                text-decoration: none;
            }

            .signup-login-link a:hover {
                color: #0b7651;
                text-decoration: underline;
            }
            
            </style>
            """
        )
        st.markdown("## 회원가입")
        st.caption(
            "이메일 계정으로 광고 콘텐츠 생성을 시작하세요."
        )
        email = st.text_input(
            "이메일",
            placeholder="example@email.com",
            key="signup_email_input",
        )

        password = st.text_input(
            "비밀번호",
            type="password",
            placeholder="비밀번호를 입력하세요",
            key="signup_password_input",
        )

        password_confirm = st.text_input(
            "비밀번호 재확인",
            type="password",
            placeholder="비밀번호를 다시 입력하세요",
            key="signup_password_confirm_input",
        )

        store_name = st.text_input(
            "가게명",
            placeholder="예: 행복한 문구점",
            key="signup_store_name_input",
        )
        
        signup_clicked = st.button(
            "가입하기",
            key="signup_submit",
            use_container_width=True,
        )
        
        with st.container(key="signup_feedback"):
            if signup_clicked:
                if (
                    not email.strip()
                    or not password.strip()
                    or not password_confirm.strip()
                    or not store_name.strip()
                ):
                    st.warning("모든 항목을 입력해주세요.")

                elif password != password_confirm:
                    st.warning("비밀번호가 일치하지 않습니다.")

                else:
                    try:
                        signup(
                            email=email,
                            password=password,
                            store_name=store_name,
                        )
                        
                        show_signup_success_dialog()

                    except AuthAPIError as e:
                        st.error(str(e))

                    except requests.exceptions.ConnectionError:
                        st.error("백엔드 서버에 연결할 수 없습니다.")

                    except Exception as e:
                        st.error(f"회원가입 중 오류가 발생했습니다.\n{e}")
        
        st.html(
            """
            <div class="signup-login-link">
                <span>이미 계정이 있으신가요?</span>
                <a href="?page=login" target="_self">
                    로그인
                </a>
            </div>
            """
        )