\# 🤖 AI Agent with Tool-Calling (LangGraph)



An intelligent agent built with \*\*LangGraph\*\* that autonomously decides when to use \*\*Google Search, Wikipedia, a Calculator, or a File Saver\*\* based on user queries.



\## 🎯 Features

\- \*\*Autonomous Tool Selection:\*\* The LLM picks the right tool(s) for each query.

\- \*\*Multi-Step Reasoning:\*\* Can chain multiple tool calls (Search → Calculate → Save).

\- \*\*Transparent UI:\*\* Streamlit interface shows which tools were used.



\## 🛠️ Tech Stack

\- \*\*Orchestration:\*\* LangGraph

\- \*\*LLM:\*\* OpenAI GPT-4o-mini

\- \*\*Tools:\*\* Serper (Google Search), Wikipedia, Python Calculator, File I/O

\- \*\*UI:\*\* Streamlit



\## 🚀 Run Locally

```bash

git clone https://github.com/YOUR\_USERNAME/ai-agent-tool-calling.git

cd ai-agent-tool-calling

python -m venv venv

source venv/bin/activate   # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

\# create .env with OPENAI\_API\_KEY and SERPER\_API\_KEY

streamlit run app.py

