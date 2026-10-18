# 🤖 AI Agent with Tool-Calling (LangGraph)

> An intelligent, autonomous AI agent built with **LangGraph** that dynamically selects and chains tools — **Google Search, Wikipedia, Calculator, and File I/O** — based on the user's query.

<p align="center">
  <a href="https://ai-agent-tool-calling-f6rdca8iuuhukcwe7lrnl5.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://github.com/Asrt3131/ai-agent-tool-calling.git">
    <img src="https://img.shields.io/badge/📂%20Source%20Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repo">
  </a>
</p>

---

## 📖 Overview

This project demonstrates a **tool-augmented LLM agent** powered by **LangGraph**. Instead of hard-coding which tool to call, the agent reasons autonomously about the user's intent, selects the appropriate tool(s), and can even **chain multiple tool calls** together in a single reasoning loop.

The result is a flexible, transparent assistant that can research, compute, and persist information — all from a single natural-language prompt.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **Autonomous Tool Selection** | The LLM decides the right tool(s) for each query — no manual routing. |
| 🔗 **Multi-Step Reasoning** | Supports chained workflows such as `Search → Calculate → Save`. |
| 👁️ **Transparent UI** | Streamlit interface displays which tools were invoked and why. |
| ⚡ **Streaming Responses** | Real-time feedback while the agent reasons and acts. |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Orchestration** | [LangGraph](https://github.com/langchain-ai/langgraph) |
| **LLM** | OpenAI GPT-4o-mini |
| **Tools** | Serper (Google Search), Wikipedia, Python Calculator, File I/O |
| **UI** | [Streamlit](https://streamlit.io/) |

---

## 🚀 Try It Live

👉 **[Launch the live app](https://ai-agent-tool-calling-f6rdca8iuuhukcwe7lrnl5.streamlit.app/)**

---

## 📂 Repository

👉 **[github.com/Asrt3131/ai-agent-tool-calling](https://github.com/Asrt3131/ai-agent-tool-calling.git)**

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Asrt3131/ai-agent-tool-calling.git
cd ai-agent-tool-calling
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 5. Launch the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🔑 Required API Keys

| Key | Purpose | Get it here |
|-----|---------|-------------|
| `OPENAI_API_KEY` | Powers the LLM (GPT-4o-mini) | [platform.openai.com](https://platform.openai.com/api-keys) |
| `SERPER_API_KEY` | Enables Google Search tool | [serper.dev](https://serper.dev/) |

---

## 🧩 How It Works

```
User Query
    │
    ▼
┌─────────────┐
│    LLM      │◄──────────────┐
│  (Reasoning)│               │
└──────┬──────┘               │
       │                      │
       ▼                      │
  Tool Call? ─── Yes ──► Execute Tool
       │                      │
       No                     │
       ▼                      │
   Final Answer ◄─────────────┘
```

1. The user submits a query.
2. The LLM analyzes the query and decides whether a tool is needed.
3. If yes, LangGraph routes to the appropriate tool, executes it, and feeds the result back to the LLM.
4. The loop repeats until the LLM produces a final answer — enabling multi-step reasoning.

---

## 📝 License

This project is open-source and available for educational and personal use.

---

## 🙌 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check the [issues page](https://github.com/Asrt3131/ai-agent-tool-calling/issues) or open a pull request.

---

<p align="center">
  Built with ❤️ using LangGraph & Streamlit
</p>
