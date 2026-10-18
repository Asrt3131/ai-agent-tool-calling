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

# بارگذاری کلیدها از .env
load_dotenv()

# ---------- ۱. تعریف ابزارها ----------
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


# ابزارهای خارجی - نام صحیح GoogleSerperAPIWrapper است
search = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())
wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
)

tools = [search, wikipedia, calculator, save_file]
tools_by_name = {t.name: t for t in tools}

# ---------- ۲. مدل ----------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# ---------- ۳. State و Graph ----------
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

app = workflow.compile()