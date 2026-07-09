import json

import streamlit.components.v1 as components


def render_copy_button(
    text: str,
    *,
    label: str = "게시글 문구 복사",
):
    text_json = json.dumps(text)
    label_json = json.dumps(label)

    components.html(
        f"""
        <button
            id="copy-button"
            onclick="copyPostText()"
        >
            <span id="copy-icon">⧉</span>
            <span id="copy-label"></span>
        </button>

        <script>
        const copyText = {text_json};
        const defaultLabel = {label_json};

        document.getElementById("copy-label").textContent =
            defaultLabel;

        async function copyPostText() {{
            const button =
                document.getElementById("copy-button");
            const label =
                document.getElementById("copy-label");

            try {{
                await navigator.clipboard.writeText(copyText);

                label.textContent = "복사 완료 ✓";
                button.classList.add("copied");

                setTimeout(() => {{
                    label.textContent = defaultLabel;
                    button.classList.remove("copied");
                }}, 1800);
            }} catch (error) {{
                label.textContent = "복사에 실패했어요";
            }}
        }}
        </script>

        <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }}

        #copy-button {{
            width: 100%;
            height: 50px;
            border: 1.5px solid #cfe7da;
            border-top: none;
            border-radius: 0 0 16px 16px;
            background: #f4fbf7;
            color: #0f8a5f;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;

            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;

            transition:
                background 0.2s ease,
                color 0.2s ease;
        }}

        #copy-button:hover {{
            background: #f4fbf7;
        }}

        #copy-button:active {{
            background: #dff4e9;
        }}

        #copy-button.copied {{
            background: #0f8a5f;
            color: #ffffff;
        }}
        </style>
        """,
        height=56,
    )