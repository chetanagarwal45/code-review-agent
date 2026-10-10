# 🚀 Local Code Review Agent  
*AI‑powered code reviewer that runs **100 % locally** on Qwen2.5‑Coder (Ollama)*  

---

## 📋 Table of Contents  

| 🔖 Section | 📄 Description |
|-----------|----------------|
| **About** | What the project does and why it matters |
| **Features** | Highlights of the agent |
| **Demo** | Quick look at the UI & API |
| **Repo Layout** | Folder‑by‑folder overview |
| **Getting Started** | Step‑by‑step setup guide |
| **Usage** | How to call the agent (UI / API / Skill) |
| **Agent Skill** | Open‑Standard manifest & implementation |
| **Testing & CI** | How we keep quality high |
| **Future Ideas** | Road‑map & enhancements |
| **Team** | Who built it |
| **License** | MIT – feel free to reuse |
| **Acknowledgements** | Shout‑outs to the tools we used |

---

## 📖 About  

> **💡 Idea:** Give developers an instant, private code reviewer that never leaves their machine.  
> **🎯 Goal:** Spot bugs, suggest improvements, and post ready‑to‑use GitHub comments – all powered by the open‑weight **Qwen2.5‑Coder** model served by **Ollama**.  

Because the model runs locally, you can review proprietary code without worrying about data leakage or API‑rate limits.  

---

## ⭐ Features  

| ✅ Feature | 📝 Details |
|-----------|------------|
| **Instant AI review** | Qwen2.5‑Coder:7B runs via Ollama – no external calls. |
| **GitHub PR integration** | Fetches diff, posts a formatted comment, can auto‑label (bug, enhancement, security). |
| **Agent‑Skill compliant** | Follows the *Agent Skill Open Standard* (`agent/skill.json`). |
| **Multi‑language support** | Auto‑detects Python, JS/TS, Java, Go, Rust, C++; falls back to Python. |
| **100 % local & private** | All processing stays on your laptop. |
| **Open‑source & MIT licensed** | Free to fork, modify, and redistribute. |
| **CI/CD pipeline** | Lint (`flake8`), format (`black`), unit tests run on every PR via GitHub Actions. |
| **Streamlit demo UI** | One‑click way to test the reviewer without touching the API. |

---

## 🎥 Demo  

| 🖥️ UI | 🔌 API |
|------|--------|
| ![Streamlit UI](https://i.imgur.com/8KZzV9L.png) | ![Swagger UI](https://i.imgur.com/5GkR9yT.png) |

*Replace the image URLs with your own screenshots or GIFs if you have them.*  

---

## 📂 Repository Layout  

```text
code-review-agent/
│
├── agent/                 # Agent Skill definition + entry point
│   ├── skill.json        # Open Standard manifest
│   └── skill.py          # Skill implementation
│
├── backend/               # FastAPI server & core logic
│   ├── main.py           # API endpoints
│   ├── reviewer.py       # Calls Ollama, builds review objects
│   └── github_client.py  # PyGithub wrapper (diff, comments, labels)
│
├── frontend/              # Streamlit demo UI
│   └── app.py
│
├── models/                # Thin wrapper around Ollama HTTP API
│   └── ollama_client.py
│
├── tests/                 # Pytest suite
│   └── test_reviewer.py
│
├── .github/
│   └── workflows/
│       └── ci.yml        # Lint + test on every PR
│
├── .env.example          # Template for GitHub token (never commit .env)
├── .gitignore
├── requirements.txt
└── README.md
