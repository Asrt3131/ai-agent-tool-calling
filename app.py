import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agent_logic import app as agent_app

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

# ---------- 4. State Management ----------
if "messages" not in st.session_state:
    st.session_state.messages = []       # History for display
if "lc_history" not in st.session_state:
    st.session_state.lc_history = []     # Actual LangChain history for context

# ---------- 5. Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")

    show_tools = st.toggle("Show tool details", value=True)
    rtl_mode = st.toggle("Right-to-left (RTL) mode", value=True)

    st.divider()

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_history = []
        st.rerun()

    st.divider()
    st.caption(f"📊 Message count: **{len(st.session_state.messages)}**")
    st.caption("💡 Tip: the agent can call multiple tools in sequence.")

# If the user turned off RTL
if not rtl_mode:
    st.markdown(
        "<style>.stMarkdown,.stChatMessage{ direction: ltr; text-align: left; }</style>",
        unsafe_allow_html=True,
    )

# ---------- 6. Display History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])
        if msg.get("timestamp"):
            st.caption(f"🕒 {msg['timestamp']}")

# ---------- 7. User Input ----------
prompt = st.chat_input(
    "Example: What's Bitcoin's price today? Multiply it by 2 and save it to a file."
)

if prompt:
    # Record user message
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "timestamp": now}
    )
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕒 {now}")

    # Run Agent
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("⏳ **Processing...**")

        try:
            # LangChain history + new message
            lc_inputs = st.session_state.lc_history + [HumanMessage(content=prompt)]
            result = agent_app.invoke({"messages": lc_inputs})
            all_msgs = result["messages"]

            # Find the final message (last AIMessage without tool_calls)
            final_message = None
            for m in reversed(all_msgs):
                if isinstance(m, AIMessage) and not getattr(m, "tool_calls", None):
                    final_message = m
                    break
            if final_message is None:
                final_message = all_msgs[-1]

            final_text = final_message.content or "⚠️ No response received from the model."

            # Collect tool calls
            tool_calls = []
            for m in all_msgs:
                if isinstance(m, AIMessage) and getattr(m, "tool_calls", None):
                    for tc in m.tool_calls:
                        tool_calls.append(tc)

            # Collect tool results
            tool_results = {}
            for m in all_msgs:
                if isinstance(m, ToolMessage):
                    tool_results[m.tool_call_id] = m.content

            # Clear placeholder and show response
            placeholder.empty()

            if show_tools and tool_calls:
                with st.expander(f"🔧 Tools used ({len(tool_calls)})", expanded=False):
                    for i, tc in enumerate(tool_calls, 1):
                        st.markdown(f"**{i}. `{tc['name']}`**")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption("📥 Input:")
                            st.code(str(tc["args"]), language="python")
                        with col2:
                            st.caption("📤 Output:")
                            output = tool_results.get(tc["id"], "(no result)")
                            st.code(str(output)[:800], language="text")
                        if i < len(tool_calls):
                            st.divider()

            st.markdown(final_text)

            # Save to display history
            now2 = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": final_text,
                    "timestamp": now2,
                }
            )

            # Save to LangChain history for next context
            # Only keep Human and final AIMessage to avoid cluttering the context
            st.session_state.lc_history.append(HumanMessage(content=prompt))
            st.session_state.lc_history.append(AIMessage(content=final_text))

        except Exception as e:
            placeholder.empty()
            err_msg = f"❌ **Error running the agent:**\n\n```\n{type(e).__name__}: {e}\n```"
            st.error(err_msg)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": err_msg,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                }
            )

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