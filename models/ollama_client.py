import httpx
import json

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5-coder:7b"

class OllamaClient:
    def __init__(self, model: str = MODEL_NAME, base_url: str = OLLAMA_URL):
        self.model = model
        self.base_url = base_url
        self.client = httpx.Client(timeout=120.0)

    def review(self, code: str, language: str = "python") -> dict:
        """
        Sends code to the locally‑running Ollama model and expects a JSON
        response with the fields defined in the Agent Skill spec.
        """
        prompt = self._build_prompt(code, language)

        r = self.client.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
        )
        r.raise_for_status()
        raw = r.json()["response"]
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback – wrap the raw text as a suggestion
            return {
                "bugs": [],
                "suggestions": [raw.strip()],
                "security_issues": [],
                "quality_score": 5,
                "summary": "Model returned non‑JSON; treat as suggestion",
                "labels": ["reviewed"],
                "severity": "low",
            }

    def _build_prompt(self, code: str, language: str) -> str:
        return f"""
You are an expert code reviewer. Review the following {language} code.

Return ONLY a JSON object with this exact structure:
{{
    "bugs": ["list of bugs found"],
    "suggestions": ["list of improvement suggestions"],
    "security_issues": ["list of security issues"],
    "quality_score": <integer 1‑10>,
    "summary": "one‑line summary",
    "labels": ["bug","enhancement","security","good-code"],
    "severity": "low|medium|high|critical"
}}

Code:
```{language}
{code}
