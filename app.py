import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# ✅ Import the full module (not just app) to avoid a crash if the key is missing
import agent_logic

# ---------- 1. Page Configuration ----------
st.set_page_config(
    page_title="AI Agent Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 2. Custom Styling (RTL + Modern Look) ----------
st.markdown(
    """
    <style>
    /* Font and right-to-left alignment for Persian content */
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
    }
    .stMarkdown, .stChatMessage, .stChatInput {
        direction: rtl;
        text-align: right;
    }
    /* Message cards */
    .stChatMessage {
        border-radius: 16px;
        padding: 8px 4px;
    }
    /* Header */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 22px 26px;
        border-radius: 18px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
    }
    .app-header h1 { margin: 0; font-size: 1.7rem; }
    .app-header p  { margin: 6px 0 0 0; opacity: 0.9; font-size: 0.95rem; }
    /* Footer */
    .footer {
        text-align: center;
        padding: 18px 0 8px 0;
        color: #888;
        font-size: 0.9rem;
        border-top: 1px solid rgba(128,128,128,0.2);
        margin-top: 40px;
        direction: ltr;
    }
    .footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    .footer a:hover { text-decoration: underline; }
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    /* Expander */
    .streamlit-expanderHeader { font-weight: 600; }
    /* Code */
    code { direction: ltr; display: inline-block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 3. Beautiful Header ----------
st.markdown(
    """
    <div class="app-header">
        <h1>🤖 AI Agent with Tool-Calling</h1>
        <p>Search · Wikipedia · Calculator · File Saver — powered by LangGraph & GPT-4o-mini</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- 4. Check that keys exist and the app is ready ----------
if agent_logic.agent_app is None:
    st.warning(f"⚠️ **The app is not ready yet!**\n\n{agent_logic.config_error}")
    st.info(
        """
        **To get started, you need to configure your API keys:**
        
        1. Open the **Manage app** panel in Streamlit Cloud (or use a `.env` file on your local machine).
        2. Go to **Settings > Secrets**.
        3. Add your keys in the following format:
        ```toml
        OPENAI_API_KEY = "sk-..."
        SERPER_API_KEY = "..."
        ```
        """
    )
else:
    # اگر ایجنت آماده بود، می‌توانید منطق چت و نمایش پیام‌ها را اینجا قرار دهید
    st.success("✅ ایجنت با موفقیت بارگذاری شد و آماده به کار است!")

# ---------- 8. Footer ----------
st.markdown(
    """
    <div class="footer">
        Built with ❤️ by <b>A_srt343</b> — Instagram:
        <a href="https://instagram.com/project_srt343" target="_blank">@project_srt343</a>
    </div>
    """,
    unsafe_allow_html=True,
)
