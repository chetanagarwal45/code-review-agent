import os
from github import Github
from dotenv import load_dotenv


load_dotenv()  # pulls values from .env (not committed)

class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("GITHUB_TOKEN not set in environment")
        self.gh = Github(token)

    # ------------------------------------------------------------------
    # PR helpers
    # ------------------------------------------------------------------
    def get_pr_diff(self, repo_full_name: str, pr_number: int) -> str:
        repo = self.gh.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        diff = ""
        for file in pr.get_files():
            if file.patch:   # the unified diff for this file
                diff += f"\n### File: {file.filename}\n{file.patch}\n"
        return diff

    def post_comment(self, repo_full_name: str, pr_number: int, body: str) -> bool:
        try:
            repo = self.gh.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(body)
            return True
        except Exception as e:
            print(f"Error posting comment: {e}")
            return False

    def add_labels(self, repo_full_name: str, pr_number: int, labels: list) -> bool:
        try:
            repo = self.gh.get_repo(repo_full_name)
            issue = repo.get_issue(pr_number)

            # Ensure labels exist; create if missing
            existing = {l.name for l in repo.get_labels()}
            colour_map = {
                "bug": "d73a4a",
                "enhancement": "a2eeef",
                "security": "e4e669",
                "good-code": "0075ca",
                "needs-review": "e99695",
            }
            for lbl in labels:
                if lbl not in existing:
                    repo.create_label(lbl, colour_map.get(lbl, "ededed"))
                    existing.add(lbl)

            issue.add_to_labels(*labels)
            return True
        except Exception as e:
            print(f"Error adding labels: {e}")
            return False

    def list_open_prs(self, repo_full_name: str):
        repo = self.gh.get_repo(repo_full_name)
        return [
            {
                "number": pr.number,
                "title": pr.title,
                "author": pr.user.login,
                "url": pr.html_url,
            }
            for pr in repo.get_pulls(state="open")
        ]
