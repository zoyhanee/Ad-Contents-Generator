from datetime import datetime
from html import escape

import streamlit as st

from api.client import APIError
from api.history import (
    get_history,
    get_history_detail,
    update_history,
)
from components.header import render_header
from config import BACKEND_URL


def format_saved_at(value: str | None) -> str:
    if not value:
        return "-"

    try:
        saved_at = datetime.fromisoformat(value)
        return saved_at.strftime("%Y.%m.%d %H:%M")
    except ValueError:
        return value


def normalize_history_image_path(
    image_path: str | None,
) -> str | None:
    if not image_path:
        return None

    return image_path.replace("\\", "/").lstrip("/")
    

@st.dialog("저장 완료")
def show_save_success_dialog():
    st.success(
        "수정된 광고가 새 버전으로 저장되었습니다."
    )

    if st.button(
        "확인",
        key="history_save_success_confirm",
        use_container_width=True,
    ):
        st.rerun()
    

def render_history_detail(
    project_id: int,
) -> None:
    st.html(
        """
        <style>
        .st-key-back_to_history button,
        .st-key-edit_history_ad button,
        .st-key-go_to_latest_history_version button,
        .st-key-save_history_edit button,
        .st-key-cancel_history_edit button {
            height: 48px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 800;
            opacity: 1;
        }

        .st-key-back_to_history button,
        .st-key-edit_history_ad button,
        .st-key-go_to_latest_history_version button,
        .st-key-cancel_history_edit button {
            border: none;
            background: #0f8a5f;
            color: #ffffff;
        }

        .st-key-back_to_history button:hover,
        .st-key-edit_history_ad button:hover,
        .st-key-go_to_latest_history_version button:hover,
        .st-key-cancel_history_edit button:hover {
            border: none;
            background: #0b7651;
            color: #ffffff;
        }

        .st-key-save_history_edit button {
            border: none;
            background: #0f8a5f;
            color: #ffffff;
        }

        .st-key-save_history_edit button:hover {
            border: none;
            background: #0b7651;
            color: #ffffff;
        }

        .st-key-back_to_history button:focus,
        .st-key-edit_history_ad button:focus,
        .st-key-go_to_latest_history_version button:focus,
        .st-key-save_history_edit button:focus,
        .st-key-cancel_history_edit button:focus,
        .st-key-back_to_history button:focus-visible,
        .st-key-edit_history_ad button:focus-visible,
        .st-key-go_to_latest_history_version button:focus-visible,
        .st-key-save_history_edit button:focus-visible,
        .st-key-cancel_history_edit button:focus-visible {
            outline: none !important;
            box-shadow: 0 0 0 3px rgba(15, 138, 95, 0.12);
        }
        </style>
        """
    )

    if st.button(
        "← 히스토리로 돌아가기",
        key="back_to_history",
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
        st.rerun()

    try:
        detail = get_history_detail(project_id)

    except APIError as exc:
        st.error(
            f"광고를 불러오지 못했습니다: {exc}"
        )
        return

    product_name = detail["product_name"]
    safe_product_name = escape(product_name)
    product_price = detail.get("product_price")
    product_description = detail.get(
        "product_description"
    )
    product_industry = detail.get(
        "product_industry"
    )

    latest_version = detail["latest_version"]
    versions = detail.get("versions", [])

    selected_version = st.session_state.get(
        "selected_history_version",
        latest_version,
    )

    selected_result = next(
        (
            item
            for item in versions
            if item["version"] == selected_version
        ),
        None,
    )

    if selected_result is None:
        selected_result = versions[0]
        selected_version = selected_result["version"]

    version = selected_result["version"]
    image_path = normalize_history_image_path(
        selected_result.get("image_path")
    )
    post_copy = selected_result.get("post_copy")
    saved_at = format_saved_at(
        selected_result.get("saved_at")
    )

    is_latest_version = (
        version == latest_version
    )

    st.html(
        f"""
        <div class="history-header">
            <h1 class="history-title">
                {safe_product_name}
            </h1>
            <div class="history-description">
                저장된 광고 결과를 확인할 수 있습니다.
            </div>
        </div>
        """
    )

    left_col, right_col = st.columns(
        [1.1, 0.9],
        gap="large",
    )

    with left_col:
        if image_path:
            image_url = (
                f"{BACKEND_URL}/"
                f"{image_path.lstrip('/')}"
            )

            st.image(
                image_url,
                use_container_width=True,
            )
        else:
            st.info("저장된 이미지가 없습니다.")

    with right_col:
        st.subheader("상품 정보")

        st.write(f"**상품명**  \n{product_name}")

        if product_price is not None:
            st.write(
                f"**가격**  \n{product_price:,}원"
            )

        if product_industry:
            st.write(
                f"**업종**  \n{product_industry}"
            )

        if product_description:
            st.write(
                f"**상품 설명**  \n"
                f"{product_description}"
            )

        if is_latest_version:
            st.caption(
                f"최신 버전 v{version} · {saved_at}"
            )
        else:
            st.caption(
                f"과거 버전 v{version} · {saved_at}"
            )

    st.divider()

    st.subheader("게시글 문구")

    is_editing = st.session_state.get(
        "history_editing",
        False,
    )

    if is_editing:
        edited_post_copy = st.text_area(
            "게시글 문구 수정",
            value=post_copy or "",
            height=220,
            key=f"history_post_copy_{project_id}_{version}",
            label_visibility="collapsed",
        )

        st.subheader("이미지 수정 요청")

        image_feedback = st.text_area(
            "이미지 수정 요청",
            placeholder=(
                "예: 배경을 따뜻한 저녁 분위기로 바꿔주세요.\n"
                "비워두면 기존 이미지를 그대로 유지합니다."
            ),
            height=120,
            key=f"history_image_feedback_{project_id}_{version}",
            label_visibility="collapsed",
        )

        st.caption(
            "이미지 수정 요청을 입력하면 AI가 현재 광고 이미지를 "
            "기준으로 새로운 이미지를 생성합니다."
        )

    else:
        if post_copy:
            st.text_area(
                "저장된 게시글 문구",
                value=post_copy,
                height=220,
                key=f"history_post_copy_view_{project_id}_{version}",
                disabled=True,
                label_visibility="collapsed",
            )
        else:
            st.info("저장된 게시글 문구가 없습니다.")

    st.divider()

    st.subheader("버전 기록")

    st.html(
        """
        <style>
        div[class*="st-key-history_version_"] button {
            height: 42px;
            border: 1.5px solid #d9e1dc;
            border-radius: 10px;
            background: #ffffff;
            color: #17211c !important;
            font-size: 14px;
            font-weight: 800;
            opacity: 1;
        }

        div[class*="st-key-history_version_"] button * {
            color: inherit !important;
            opacity: 1 !important;
        }

        div[class*="st-key-history_version_"] button:hover {
            border-color: #0f8a5f;
            background: #f4fbf7;
            color: #0f8a5f !important;
        }

        div[class*="st-key-history_version_"] button:disabled,
        div[class*="st-key-history_version_"] button:disabled:hover {
            border: 1.5px solid #0f8a5f;
            background: #0f8a5f;
            color: #ffffff !important;
            opacity: 1;
            cursor: default;
        }
        </style>
        """
    )

    for item in versions:
        item_version = item["version"]
        item_saved_at = format_saved_at(
            item.get("saved_at")
        )

        version_col, date_col = st.columns(
            [0.25, 0.75]
        )

        with version_col:
            version_clicked = st.button(
                f"v{item_version}",
                key=(
                    f"history_version_"
                    f"{project_id}_{item_version}"
                ),
                use_container_width=True,
                disabled=(
                    item_version == version
                ),
            )

        with date_col:
            if item_version == latest_version:
                st.write(
                    f"{item_saved_at} · 최신"
                )
            else:
                st.write(item_saved_at)

        if version_clicked:
            st.session_state[
                "selected_history_version"
            ] = item_version

            st.session_state.pop(
                "history_editing",
                None,
            )

            st.rerun()

    if is_editing:
        save_col, cancel_col = st.columns(2)

        with save_col:
            save_clicked = st.button(
                "✓ 수정본 저장",
                key="save_history_edit",
                use_container_width=True,
            )

        with cancel_col:
            cancel_clicked = st.button(
                "취소",
                key="cancel_history_edit",
                use_container_width=True,
            )

        if save_clicked:
            try:
                normalized_image_feedback = (
                    image_feedback.strip()
                )

                if normalized_image_feedback:
                    st.html(
                        """
                        <style>
                        .history-update-overlay {
                            position: fixed;
                            inset: 0;
                            z-index: 9999;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            padding: 24px;
                            background: rgba(15, 23, 42, 0.28);
                            backdrop-filter: blur(3px);
                        }

                        .history-update-popup {
                            width: min(520px, calc(100vw - 48px));
                            padding: 42px 44px;
                            border: 1px solid #d9e1dc;
                            border-radius: 22px;
                            background: #ffffff;
                            box-shadow: 0 24px 70px rgba(15, 23, 42, 0.22);
                            text-align: center;
                        }

                        .history-update-spinner {
                            width: 58px;
                            height: 58px;
                            margin: 0 auto 22px;
                            border: 5px solid #e4f2eb;
                            border-top-color: #0f8a5f;
                            border-radius: 999px;
                            animation: history-update-spin 1s linear infinite;
                        }

                        @keyframes history-update-spin {
                            to {
                                transform: rotate(360deg);
                            }
                        }

                        .history-update-popup h3 {
                            margin: 0 0 14px;
                            color: #08111f;
                            font-size: 24px;
                            font-weight: 900;
                        }

                        .history-update-popup p {
                            margin: 0;
                            color: #4b5b52;
                            font-size: 15px;
                            line-height: 1.8;
                        }

                        .history-update-time-guide {
                            margin-top: 18px;
                            padding: 14px 16px;
                            border-radius: 14px;
                            background: #f1f8f4;
                            color: #0f8a5f;
                            font-size: 15px;
                            font-weight: 800;
                        }

                        .history-update-warning {
                            margin-top: 18px;
                            color: #d94832;
                            font-size: 14px;
                            font-weight: 700;
                            line-height: 1.7;
                        }
                        </style>

                        <div class="history-update-overlay">
                            <div class="history-update-popup">
                                <div class="history-update-spinner"></div>

                                <h3>AI가 광고 이미지를 수정하고 있어요</h3>

                                <p>
                                    입력하신 이미지 수정 요청을 반영해<br>
                                    새로운 광고 이미지를 만들고 있습니다.
                                </p>

                                <div class="history-update-time-guide">
                                    이미지 수정에는 최대 5분 정도 소요될 수 있습니다.
                                </div>

                                <div class="history-update-warning">
                                    생성 중에는 새로고침하거나 창을 닫지 말아주세요.<br>
                                    완료되면 자동으로 수정본이 저장됩니다.
                                </div>
                            </div>
                        </div>
                        """
                    )
                else:
                    st.html(
                        """
                        <style>
                        .history-update-inline {
                            margin: 18px 0;
                            padding: 16px 18px;
                            border-radius: 12px;
                            background: #f1f8f4;
                            color: #0f8a5f;
                            font-size: 14px;
                            font-weight: 800;
                            text-align: center;
                        }
                        </style>

                        <div class="history-update-inline">
                            수정본을 저장하고 있습니다...
                        </div>
                        """
                    )

                update_history(
                    project_id=project_id,
                    post_copy=edited_post_copy,
                    image_feedback=(
                        normalized_image_feedback
                        or None
                    ),
                )

                st.session_state.history_editing = False

                show_save_success_dialog()

            except APIError as exc:
                st.error(
                    f"수정본을 저장하지 못했습니다: {exc}"
                )

        if cancel_clicked:
            st.session_state.history_editing = False
            st.rerun()

    else:
        if is_latest_version:
            edit_clicked = st.button(
                "광고 수정하기",
                key="edit_history_ad",
                use_container_width=True,
            )

            if edit_clicked:
                st.session_state.history_editing = True
                st.rerun()

        else:
            st.info(
                "과거 버전을 보고 있습니다. "
                "수정하려면 최신 버전을 선택해주세요."
            )

            if st.button(
                f"최신 버전 v{latest_version}으로 이동",
                key="go_to_latest_history_version",
                use_container_width=True,
            ):
                st.session_state[
                    "selected_history_version"
                ] = latest_version

                st.rerun()


def render_history():
    render_header()
    
    st.html(
        """
        <style>
        .history-header {
            margin-bottom: 28px;
        }

        .history-title {
            margin: 0;
            color: #17211c;
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .history-description {
            margin-top: 8px;
            color: #68756e;
            font-size: 15px;
            line-height: 1.6;
        }

        .history-card-info {
            padding-top: 6px;
            padding-bottom: 10px;
        }

        .history-product-name {
            margin-bottom: 6px;
            color: #17211c;
            font-size: 18px;
            font-weight: 800;
        }

        .history-meta {
            color: #7b8780;
            font-size: 13px;
            font-weight: 600;
        }

        div[data-testid="stImage"] img {
            border-radius: 14px;
        }

        div[class*="st-key-history_open_"] button {
            height: 46px;
            border: 1.5px solid #d9e1dc;
            border-radius: 10px;
            background: #ffffff;
            color: #17211c;
            font-size: 14px;
            font-weight: 800;
        }

        div[class*="st-key-history_open_"] button:hover {
            border-color: #0f8a5f;
            background: #f4fbf7;
            color: #0f8a5f;
        }
        </style>
        """
    )
    
    selected_project_id = st.session_state.get(
        "selected_history_project_id"
    )

    if selected_project_id is not None:
        render_history_detail(
            selected_project_id
        )
        return

    st.html(
        """
        <div class="history-header">
            <h1 class="history-title">
                광고 히스토리
            </h1>
            <div class="history-description">
                저장한 광고를 다시 확인하고
                필요한 내용을 수정할 수 있습니다.
            </div>
        </div>
        """
    )

    try:
        history_items = get_history()

    except APIError as exc:
        st.error(
            f"히스토리를 불러오지 못했습니다: {exc}"
        )
        return

    if not history_items:
        st.info(
            "아직 저장된 광고가 없습니다. "
            "광고를 만든 뒤 최종 결과를 저장해보세요."
        )
        return

    columns = st.columns(3)

    for index, item in enumerate(history_items):
        project_id = item["project_id"]
        product_name = item["product_name"]
        safe_product_name = escape(product_name)
        version = item["version"]
        image_path = normalize_history_image_path(
            item.get("image_path")
        )
        saved_at = format_saved_at(
            item.get("saved_at")
        )

        column = columns[index % 3]

        with column:
            if image_path:
                image_url = (
                    f"{BACKEND_URL}/"
                    f"{image_path.lstrip('/')}"
                )

                st.image(
                    image_url,
                    use_container_width=True,
                )
            else:
                st.info("저장된 이미지가 없습니다.")

            st.html(
                f"""
                <div class="history-card-info">
                    <div class="history-product-name">
                        {safe_product_name}
                    </div>

                    <div class="history-meta">
                        v{version} · {saved_at}
                    </div>
                </div>
                """
            )

            open_clicked = st.button(
                "광고 열기",
                key=f"history_open_{project_id}",
                use_container_width=True,
            )

            if open_clicked:
                st.session_state[
                    "selected_history_project_id"
                ] = project_id

                st.session_state.pop(
                    "selected_history_version",
                    None,
                )

                st.session_state.pop(
                    "history_editing",
                    None,
                )

                st.rerun()


if __name__ == "__main__":
    render_history()
