from html import escape

import requests
import streamlit as st

from components.header import render_header
from api.auth import AuthAPIError, get_google_login_url, login


def render_login():
    # 1. 로그인 상태 초기화

    # 2. 공통 헤더
    render_header()
    
    left_col, right_col = st.columns(
        [1.2, 1],
        gap="large",
    )
    
    with left_col:
        st.html(
            """
            <div class="login-copy">
                <div class="badge">AI로 더 쉽고, 더 효과적인 광고 제작</div>

                <h1>
                    AI가 제안하는 전략으로<br>
                    <span class="green">광고 효과</span>를 높이세요
                </h1>

                <div class="benefit-list">
                    <div class="benefit">
                        <div class="benefit-icon">□</div>
                        <div>
                            <h3>내 작업물 저장</h3>
                            <p>생성한 광고 콘텐츠와 프로젝트를 안전하게 저장하고 관리하세요.</p>
                        </div>
                    </div>

                    <div class="benefit">
                        <div class="benefit-icon">↺</div>
                        <div>
                            <h3>광고 결과 다시 불러오기</h3>
                            <p>이전 광고 결과를 언제든지 확인하고 재활용할 수 있어요.</p>
                        </div>
                    </div>

                    <div class="benefit">
                        <div class="benefit-icon">▥</div>
                        <div>
                            <h3>생성 기록 관리</h3>
                            <p>광고 생성 기록을 한눈에 확인하고 성과를 분석해보세요.</p>
                        </div>
                    </div>
                </div>
            </div>
            """
        )
    
    with right_col:
        st.html(
            """
            <style>

            .st-key-login_email_input [data-baseweb="input"],
            .st-key-login_password_input [data-baseweb="input"] {
                background: #ffffff !important;
                border-radius: 10px !important;
            }
            
            .st-key-login_email_input label,
            .st-key-login_password_input label {
                color: #17211c;
                font-size: 14px;
                font-weight: 700;
            }

            .st-key-login_email_input input,
            .st-key-login_password_input input{
                border:1.5px solid #d9e1dc;
                border-radius:10px;
                background:#ffffff;
                color: #17211c;
            }
            
            .st-key-login_email_input input::placeholder,
            .st-key-login_password_input input::placeholder {
                color: #a0aaa5;
                opacity: 1;
            }
            
            .st-key-login_email_input input:focus,
            .st-key-login_password_input input:focus {
                border-color: #0f8a5f;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.1);
            }
            
            .st-key-login_submit button {
                min-height: 48px;
                margin-top: 8px;
                border: none;
                border-radius: 10px;
                background: #0f8a5f;
                color: #ffffff;
                font-size: 15px;
                font-weight: 700;
            }

            .st-key-login_submit button:hover {
                border: none;
                background: #0b7651;
                color: #ffffff;
            }

            .st-key-login_submit button:focus {
                border: none;
                color: #ffffff;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.15);
            }
            
            /* 눈 아이콘이 들어가는 오른쪽 영역 */
            .st-key-login_password_input [data-baseweb="input"] > div {
                background: #ffffff !important;
            }

            /* 눈 아이콘 버튼 */
            .st-key-login_password_input button {
                background: #ffffff !important;
                border: none !important;
                color: #6b756f !important;
                box-shadow: none !important;
            }

            .st-key-login_password_input button:hover,
            .st-key-login_password_input button:focus,
            .st-key-login_password_input button:active {
                background: #ffffff !important;
                color: #0f8a5f !important;
                box-shadow: none !important;
            }

            /* 눈 아이콘 */
            .st-key-login_password_input button svg {
                color: currentColor !important;
                fill: currentColor !important;
            }
            
            .login-signup-link {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 8px;
                margin-top: 22px;
                color: #6b756f;
                font-size: 14px;
            }

            .login-signup-link a {
                color: #0f8a5f;
                font-weight: 700;
                text-decoration: none;
            }

            .login-signup-link a:hover {
                color: #0b7651;
                text-decoration: underline;
            }

            .google-login-link {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                min-height: 48px;
                margin-top: 10px;
                border: 1.5px solid #d9e1dc;
                border-radius: 10px;
                background: #ffffff;
                font-size: 15px;
                font-weight: 700;
                text-decoration: none;
                color: #4b5563 !important;
                transition: background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
            }

            .google-login-link:hover,
            .google-login-link:focus {
                border-color: #b9c3bd;
                background: #f8faf9;
                color: #17211c !important;
                box-shadow: 0 0 0 2px rgba(15, 138, 95, 0.06);
                text-decoration: none;
            }

            .google-login-icon {
                width: 18px;
                height: 18px;
                flex: 0 0 18px;
            }

            .st-key-google_login_submit button {
                min-height: 48px;
                margin-top: 10px;
                border: 1.5px solid #d9e1dc;
                border-radius: 10px;
                background: #f1f3f5;
                color: #98a19b;
                font-size: 15px;
                font-weight: 700;
            }
            
            </style>
            """
        )
        st.markdown("## 로그인")
        st.caption("광고 콘텐츠 생성을 계속하려면 로그인해주세요.")

        email = st.text_input(
            "이메일",
            placeholder="example@email.com",
            key="login_email_input",
        )

        password = st.text_input(
            "비밀번호",
            type="password",
            placeholder="비밀번호를 입력하세요",
            key="login_password_input",
        )

        login_clicked = st.button(
            "로그인",
            key="login_submit",
            use_container_width=True,
        )

        try:
            google_login_url = get_google_login_url()

        except Exception:
            google_login_url = None

        if google_login_url:
            safe_google_login_url = escape(google_login_url, quote=True)

            st.html(
                f"""
                <a
                    class="google-login-link"
                    href="{safe_google_login_url}"
                    target="_self"
                    rel="noopener"
                >
                    <img
                        class="google-login-icon"
                        src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
                        alt=""
                    />
                    <span>Google 계정으로 로그인</span>
                </a>
                """
            )

        else:
            st.button(
                "Google로 로그인",
                key="google_login_submit",
                use_container_width=True,
                disabled=True,
            )
    
    if login_clicked:
        if not email.strip() or not password.strip():
            st.warning("이메일과 비밀번호를 모두 입력해주세요.")

        else:
            try:
                result = login(
                    email=email,
                    password=password,
                )

                st.session_state["access_token"] = result["access_token"]
                st.session_state["user"] = result["user"]
                st.session_state["is_authenticated"] = True

                st.success("로그인되었습니다.")

                st.query_params["page"] = "product_input"
                st.rerun()

            except AuthAPIError as e:
                st.error(str(e))

            except requests.exceptions.ConnectionError:
                st.error("백엔드 서버에 연결할 수 없습니다.")

            except Exception:
                st.error("로그인 중 오류가 발생했습니다.")

            
    st.html(
        """
        <div class="login-signup-link">
            <span>아직 계정이 없으신가요?</span>
            <a href="?page=signup" target="_self">
                회원가입
            </a>
        </div>
        """
    )
    
    
