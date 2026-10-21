from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.reviewer import CodeReviewer
from backend.github_client import GitHubClient

app = FastAPI(
    title="Local Code Review Agent",
    description="AI‑powered code reviewer running 100 % locally (Qwen2.5‑Coder via Ollama)",
    version="1.0.0",
)

reviewer = CodeReviewer()
github = GitHubClient()


# ------------------------------------------------------------------
# Request models
# ------------------------------------------------------------------
class CodeReviewRequest(BaseModel):
    code: str
    filename: str = ""


class PRReviewRequest(BaseModel):
    repo_name: str  # e.g. "owner/repo"
    pr_number: int
    post_comment: bool = True
    add_labels: bool = True


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Local Code Review Agent is running 🤖",
        "model": "Qwen2.5‑Coder:7b",
        "status": "active",
    }


@app.post("/review/code")
def review_code(req: CodeReviewRequest):
    try:
        result = reviewer.review_snippet(req.code, req.filename)
        result["comment"] = reviewer.format_comment(result)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/review/pr")
def review_pr(req: PRReviewRequest):
    try:
        diff = github.get_pr_diff(req.repo_name, req.pr_number)
        review = reviewer.review_pr_diff(diff)
        comment = reviewer.format_comment(review)

        if req.post_comment:
            github.post_comment(req.repo_name, req.pr_number, comment)

        if req.add_labels and review.get("labels"):
            github.add_labels(req.repo_name, req.pr_number, review["labels"])

        return {
            "review": review,
            "comment_posted": req.post_comment,
            "labels_added": review.get("labels", []),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/prs/{owner}/{repo}")
def list_prs(owner: str, repo: str):
    try:
        prs = github.list_open_prs(f"{owner}/{repo}")
        return {"open_prs": prs, "count": len(prs)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# To run locally:  uvicorn backend.main:app --reload
