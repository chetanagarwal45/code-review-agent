from models.ollama_client import OllamaClient


class CodeReviewer:
    def __init__(self):
        self.ollama = OllamaClient()

    # ------------------------------------------------------------------
    # Helper: detect language from filename or fallback to python
    # ------------------------------------------------------------------
    @staticmethod
    def _detect_language(filename: str) -> str:
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".go": "go",
            ".rs": "rust",
        }
        for ext, lang in ext_map.items():
            if filename.lower().endswith(ext):
                return lang
        return "python"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def review_snippet(self, code: str, filename: str = "") -> dict:
        lang = self._detect_language(filename)
        return self.ollama.review(code, lang)

    def review_pr_diff(self, diff: str) -> dict:
        """
        The diff already contains only the added lines (we strip the leading '+').
        """
        added = []
        for line in diff.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                added.append(line[1:])  # drop the '+'
        code = "\n".join(added)
        # Treat the whole diff as a Python‑like snippet; language detection is optional.
        return self.ollama.review(code, "python")

    # ------------------------------------------------------------------
    # Formatting helpers for GitHub comment
    # ------------------------------------------------------------------
    @staticmethod
    def format_comment(review: dict) -> str:
        score = review.get("quality_score", 0)
        emoji = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"

        comment = f"""## 🤖 AI Code Review Report

### {emoji} Quality Score: {score}/10
**Summary:** {review.get('summary', 'N/A')}
**Severity:** `{review.get('severity', 'low').upper()}`

---

### 🐛 Bugs Found ({len(review.get('bugs', []))})
"""
        for b in review.get("bugs", []):
            comment += f"- ❌ {b}\n"

        comment += f"""
### 💡 Suggestions ({len(review.get('suggestions', []))})
"""
        for s in review.get("suggestions", []):
            comment += f"- 💬 {s}\n"

        comment += f"""
### 🔒 Security Issues ({len(review.get('security_issues', []))})
"""
        for sec in review.get("security_issues", []):
            comment += f"- ⚠️ {sec}\n"

        comment += (
            "\n---\n*Reviewed by Local Code Review Agent 🤖 powered by Qwen2.5‑Coder*"
        )
        return comment
