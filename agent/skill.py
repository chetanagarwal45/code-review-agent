import httpx
import json
from typing import Dict, Any

API_BASE = "http://localhost:8000"  # FastAPI server


class CodeReviewSkill:
    """Agent Skill: Code Review (Open Standard)"""

    def __init__(self, api_base: str = API_BASE):
        self.api_base = api_base
        self.client = httpx.Client(timeout=120.0)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expected input:
        {
            "code": "<source code>",          # optional
            "pr_url": "https://github.com/owner/repo/pull/12", # optional
            "language": "python"              # optional, defaults to python
        }
        """
        if "pr_url" in input_data:
            return self._review_pr(input_data)
        elif "code" in input_data:
            return self._review_code(input_data)
        else:
            return {"error": "Provide either 'code' or 'pr_url'"}

    def _review_code(self, data: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.post(
            f"{self.api_base}/review/code",
            json={
                "code": data["code"],
                "filename": data.get("filename", ""),
            },
        )
        return resp.json()

    def _review_pr(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Parse PR URL → owner/repo + PR number
        parts = data["pr_url"].rstrip("/").split("/")
        repo_name = f"{parts[-4]}/{parts[-3]}"
        pr_number = int(parts[-1])

        resp = self.client.post(
            f"{self.api_base}/review/pr",
            json={
                "repo_name": repo_name,
                "pr_number": pr_number,
                "post_comment": data.get("post_comment", True),
                "add_labels": data.get("add_labels", True),
            },
        )
        return resp.json()

    def get_manifest(self) -> Dict[str, Any]:
        with open("agent/skill.json") as f:
            return json.load(f)
