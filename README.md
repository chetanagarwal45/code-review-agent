# 🚀 Local Code Review Agent  
*AI‑powered code reviewer that runs **100 % locally** on Qwen2.5‑Coder (Ollama)*  

---

## 📋 Table of Contents  

| 🔖 Section | 📄 Description |
|-----------|----------------|
| **About** | What the project does and why it matters |
| **Features** | Highlights of the agent |
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
```

*Every package contains an `__init__.py` so it can be imported as a module.*  

---

## 🛠️ Getting Started  

> **Prerequisites**  
> - Python 3.11+  
> - [Ollama](https://ollama.com) installed (`ollama serve` must be running)  
> - GitHub Personal Access Token (classic) with `repo` scope (for PR commenting)  

### 1️⃣ Clone the repo  

```bash
git clone https://github.com/chetanagarwal45/code-review-agent.git
cd code-review-agent
```

### 2️⃣ Set up a virtual environment  

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3️⃣ Install dependencies  

```bash
pip install -r requirements.txt
```

### 4️⃣ Pull the model (first time only)  

```bash
ollama pull qwen2.5-coder:7b
```

### 5️⃣ Configure your GitHub token  

```bash
cp .env.example .env   # then edit .env and add your token
```

`.env` should look like:  

```env
GITHUB_TOKEN=ghp_your_personal_access_token_here
# Optional – default repo if you like
GITHUB_REPO=chetanagarwal45/code-review-agent
```

> **Never** commit the real `.env` – it is listed in `.gitignore`.  

### 6️⃣ Start the services  

| Terminal | Command | What it runs |
|----------|---------|--------------|
| 1️⃣ | `ollama serve` | Keeps the Ollama model server alive |
| 2️⃣ | `uvicorn backend.main:app --reload` | FastAPI backend → `http://localhost:8000` |
| 3️⃣ | `streamlit run frontend/app.py` | Streamlit demo UI → `http://localhost:8501` |

Open the Swagger UI at `http://localhost:8000/docs` to test the API directly, or launch the Streamlit UI for a no‑code experience.  

---

## 🚀 Usage  

### Via the Streamlit UI  

1. Open `http://localhost:8501`.  
2. Choose **“Review a code snippet”** or **“Review a GitHub PR”**.  
3. Paste your code or PR URL, hit **Review**.  
4. See a quality score, summary, bug/suggestion/security lists, and a ready‑to‑post GitHub comment.  

### Via the API (cURL / Thunder Client)  

```bash
# Review a raw snippet
curl -X POST http://localhost:8000/review/code \
     -H "Content-Type: application/json" \
     -d '{"code":"def foo(x):\n    return x+1","filename":"example.py"}'

# Review a PR (replace OWNER/REPO and PR_NUMBER)
curl -X POST http://localhost:8000/review/pr \
     -H "Content-Type: application/json" \
     -d '{"repo_name":"OWNER/REPO","pr_number":42,"post_comment":true,"add_labels":true}'
```

The response JSON contains a `comment` field with markdown‑ready text you can post directly to GitHub.  

---

## 🧩 Agent Skill (Open Standard)  

The skill lives in the `agent/` folder.  

**skill.json** (excerpt)  

```json
{
  "schema_version": "1.0",
  "name": "code-review-agent",
  "display_name": "Local Code Review Agent",
  "description": "Reviews code and GitHub PRs using Qwen2.5‑Coder running locally via Ollama.",
  "version": "1.0.0",
  "license": "MIT",
  "author": "chetanagarwal45",
  "capabilities": [
    "code_review",
    "bug_detection",
    "security_analysis",
    "github_pr_review",
    "auto_labeling"
  ],
  "input": {
    "type": "object",
    "properties": {
      "code": {"type": "string"},
      "pr_url": {"type": "string"},
      "language": {"type": "string"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "bugs": {"type": "array"},
      "suggestions": {"type": "array"},
      "security_issues": {"type": "array"},
      "quality_score": {"type": "number"},
      "labels": {"type": "array"},
      "comment": {"type": "string"}
    }
  },
  "endpoints": {
    "review_code": "POST /review/code",
    "review_pr": "POST /review/pr",
    "list_prs": "GET /prs/{owner}/{repo}"
  },
  "model": {
    "name": "qwen2.5-coder",
    "size": "7b",
    "provider": "ollama",
    "local": true,
    "open_weight": true
  }
}
```

**skill.py** simply proxies the HTTP calls to the FastAPI backend and returns the parsed JSON, satisfying the Agent Skill Open Standard contract.  

---

## 🧪 Testing & CI  

* **Unit tests** – run `pytest -q` from the repo root. They cover language detection, comment formatting, and the Ollama client’s fallback behaviour.  
* **CI** – The workflow in `.github/workflows/ci.yml` runs on every push and pull request:  

  ```yaml
  name: CI Pipeline
  on:
    push:
      branches: [main]
    pull_request:
      branches: [main]
  jobs:
    lint-and-test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: '3.11'
        - run: pip install -r requirements.txt
        - run: flake8 . --max-line-length=100
        - run: black --check .
        - run: pytest tests/
  ```  

A passing build shows a green check‑mark on the repo’s main page.  

---

## 🔮 Future Ideas  

| 🚀 Idea | ⏱️ Priority | 📝 Note |
|--------|------------|---------|
| Inline review comments per file in a PR | High | Use `get_files()` and post review comments per file. |
| Confidence scores per suggestion (model logits) | Medium | Gives reviewers a sense of certainty. |
| GitHub Action that runs the agent on every push | Medium | No UI needed – just a workflow. |
| Custom rule packs (team‑specific linters) | Low | Allow org‑specific policies via a simple YAML config. |
| Ensemble of Qwen2.5‑Coder + CodeLlama for higher accuracy | Low | Fallback / voting mechanism. |

---

## 👥 Team  

| 👤 Name | 💼 Role | 🎓 College | 📧 Email | 📞 Phone |
|--------|--------|------------|----------|----------|
| Chetan Agarwal | Frontend / UI / GitHub agent / DevOps | Amity University Rajasthan | chetanagarwal4545@gmail.com | 7357691973 |
| Saurav | Backend / AI integration /Testing / Documentation | Amity University Rajasthan | saurav00752@outlook.com | 8386865521 |


*All members contributed equally; we tracked work with GitHub Issues, developed in feature branches, opened draft PRs early, and followed the checklist supplied by the competition organizers.*  

---

## 📜 License  

This project is licensed under the **MIT License** – see the `LICENSE` file for details.  

---

## 🙏 Acknowledgements  

- **Ollama** – for making it trivial to run LLMs locally.  
- **Qwen team** – for releasing the Qwen2.5‑Coder model under an open‑weight license.  
- **Streamlit, FastAPI, PyGithub** – excellent libraries that sped up development.  
- The Manipal University  competition organizers(Vansh Kapoor,Kintan Jain,Akshit Saini) – for the motivating challenge and clear guidelines.  
