import os
from typing import Annotated, Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun, GoogleSerperRun
from langchain_community.utilities import WikipediaAPIWrapper, GoogleSerperAPIWrapper
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# Load keys from .env
load_dotenv()

# Try to read keys from Streamlit Secrets (for cloud environments)
try:
    import streamlit as st
    if not os.environ.get("SERPER_API_KEY") and "SERPER_API_KEY" in st.secrets:
        os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
    if not os.environ.get("OPENAI_API_KEY") and "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass  # If not in a Streamlit environment, don't raise an error

# ---------- 1. Define Tools ----------
@tool
def calculator(expression: str) -> str:
    """Useful for mathematical calculations. 
    Input should be a valid Python math expression like '2+2' or '1500*0.9'."""
    try:
        allowed = set("0123456789+-*/()., ")
        if not set(expression) <= allowed:
            return "Error: Invalid characters in expression."
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@tool
def save_file(content: str, filename: str = "output.txt") -> str:
    """Save text content to a local file. 
    Use this when the user asks to save or write something to a file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Content saved to '{filename}' ({len(content)} chars)."
    except Exception as e:
        return f"Error saving file: {e}"

# Global variables to hold the app
agent_app = None
config_error = None

# Function to build the app (Lazy Initialization)
def build_agent():
    global agent_app, config_error
    
    # Check for required keys
    if not os.environ.get("SERPER_API_KEY"):
        config_error = "Serper API key not found. Please set it in .env or Secrets."
        return None
    if not os.environ.get("OPENAI_API_KEY"):
        config_error = "OpenAI API key not found. Please set it in .env or Secrets."
        return None

    try:
        # External tools
        search = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper(serper_api_key=os.environ.get("SERPER_API_KEY")))
        wikipedia = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
        )

        tools = [search, wikipedia, calculator, save_file]
        tools_by_name = {t.name: t for t in tools}

        # Model
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        llm_with_tools = llm.bind_tools(tools)

        # State and Graph
        class AgentState(TypedDict):
            messages: Annotated[list, add_messages]

        def call_model(state: AgentState):
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        def call_tools(state: AgentState):
            last_message = state["messages"][-1]
            tool_messages = []
            for tool_call in last_message.tool_calls:
                tool_func = tools_by_name[tool_call["name"]]
                try:
                    observation = tool_func.invoke(tool_call["args"])
                except Exception as e:
                    observation = f"Tool error: {e}"
                tool_messages.append(
                    {
                        "role": "tool",
                        "content": str(observation),
                        "tool_call_id": tool_call["id"],
                    }
                )
            return {"messages": tool_messages}

        def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
            last_message = state["messages"][-1]
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            return "__end__"

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", call_model)
        workflow.add_node("tools", call_tools)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")

        agent_app = workflow.compile()
        config_error = None
        return agent_app
        
    except Exception as e:
        config_error = f"Error building the app: {str(e)}"
        return None

# Initial attempt to build the app
build_agent()
