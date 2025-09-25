import os
import json
import requests
from typing import Dict, Optional, List
from shared.common_models import model_to_dict, dict_to_model,  BaseResponse, MetricsData, ConfigData, TaskResult, AnalysisResult

from agency_swarm.tools import BaseTool
from pydantic import Field


def _read_token_from_env_or_dotenv() -> Optional[str]:
    # Prefer environment variables first
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):  # common env names
        val = os.getenv(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    # Fallback: parse .env in repo root if present
    try:
        dotenv_path = os.path.join(os.getcwd(), ".env")
        if os.path.isfile(dotenv_path):
            with open(dotenv_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
                        return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


class GitHubManager(BaseTool):
    """
    Manage GitHub operations via REST API (no gh/git CLI required).

    Capabilities (current):
    - Create branch from default branch
    - Commit a set of files (path -> content) to that branch
    - Open a pull request

    Caveats:
    - This tool commits the provided file contents as-is. Ensure you pass the desired state.
    - Does not delete or rename files; additive/updates only.
    """

    repo: str = Field(..., description="GitHub repo 'owner/repo'")
    title: str = Field(..., description="Pull request title and commit message title")
    body: str = Field("", description="Pull request body")
    branch_name: str = Field(..., description="Branch to create/update for the PR")
    base_branch: Optional[str] = Field(None, description="Base branch for the PR (defaults to repo default)")
    file_changes: ConfigData = Field(
        default_factory=dict,
        description="Mapping of file paths to new content for commit",
    )
    token: Optional[str] = Field(default_factory=_read_token_from_env_or_dotenv, description="GitHub token")

    api_base: str = Field("https://api.github.com", description="GitHub API base URL")

    # -------------- Utility --------------

    def _headers(self) -> ConfigData:
        if not self.token:
            raise RuntimeError("GitHub token not available. Set GITHUB_TOKEN or GH_TOKEN, or add it to .env")
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }

    def _get_default_branch(self) -> str:
        url = f"{self.api_base}/repos/{self.repo}"
        r = requests.get(url, headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json().get("default_branch", "main")

    def _get_branch_head(self, branch: str) -> str:
        url = f"{self.api_base}/repos/{self.repo}/git/ref/heads/{branch}"
        r = requests.get(url, headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json()["object"]["sha"]

    def _get_commit_tree_sha(self, commit_sha: str) -> str:
        url = f"{self.api_base}/repos/{self.repo}/git/commits/{commit_sha}"
        r = requests.get(url, headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json()["tree"]["sha"]

    def _create_branch(self, new_branch: str, from_commit_sha: str) -> None:
        url = f"{self.api_base}/repos/{self.repo}/git/refs"
        data = {"ref": f"refs/heads/{new_branch}", "sha": from_commit_sha}
        r = requests.post(url, headers=self._headers(), data=json.dumps(data), timeout=20)
        # If branch exists, a 422 occurs. Treat as success if ref already exists.
        if r.status_code == 422 and "Reference already exists" in r.text:
            return
        r.raise_for_status()

    def _create_blob(self, content: str) -> str:
        url = f"{self.api_base}/repos/{self.repo}/git/blobs"
        data = {"content": content, "encoding": "utf-8"}
        r = requests.post(url, headers=self._headers(), data=json.dumps(data), timeout=20)
        r.raise_for_status()
        return r.json()["sha"]

    def _create_tree(self, base_tree_sha: str, blobs: ConfigData) -> str:
        url = f"{self.api_base}/repos/{self.repo}/git/trees"
        tree_entries: List[ConfigData] = []
        for path, blob_sha in blobs.items():
            tree_entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob_sha})
        data = {"base_tree": base_tree_sha, "tree": tree_entries}
        r = requests.post(url, headers=self._headers(), data=json.dumps(data), timeout=20)
        r.raise_for_status()
        return r.json()["sha"]

    def _create_commit(self, message: str, tree_sha: str, parent_commit_sha: str) -> str:
        url = f"{self.api_base}/repos/{self.repo}/git/commits"
        data = {"message": message, "parents": [parent_commit_sha], "tree": tree_sha}
        r = requests.post(url, headers=self._headers(), data=json.dumps(data), timeout=20)
        r.raise_for_status()
        return r.json()["sha"]

    def _update_branch_ref(self, branch: str, commit_sha: str) -> None:
        url = f"{self.api_base}/repos/{self.repo}/git/refs/heads/{branch}"
        data = {"sha": commit_sha, "force": False}
        r = requests.patch(url, headers=self._headers(), data=json.dumps(data), timeout=20)
        r.raise_for_status()

    def _create_pr(self, title: str, body: str, head: str, base: str) -> ConfigData:
        url = f"{self.api_base}/repos/{self.repo}/pulls"
        data = {"title": title, "body": body, "head": head, "base": base}
        r = requests.post(url, headers=self._headers(), data=json.dumps(data), timeout=20)
        r.raise_for_status()
        return r.json()

    # -------------- Tool entry point --------------

    def run(self) -> str:
        try:
            base = self.base_branch or self._get_default_branch()
            base_head_commit = self._get_branch_head(base)
            base_tree_sha = self._get_commit_tree_sha(base_head_commit)

            # Ensure branch exists (create if missing)
            self._create_branch(self.branch_name, base_head_commit)

            # Prepare blobs
            blobs: ConfigData = {}
            for path, content in (self.file_changes or {}).items():
                blob_sha = self._create_blob(content)
                blobs[path] = blob_sha

            if not blobs:
                # No changes to commit; proceed to PR creation
                pr = self._create_pr(self.title, self.body, self.branch_name, base)
                return pr.get("html_url", json.dumps(pr))

            # Create tree and commit
            new_tree_sha = self._create_tree(base_tree_sha, blobs)
            commit_sha = self._create_commit(self.title, new_tree_sha, base_head_commit)

            # Update branch
            self._update_branch_ref(self.branch_name, commit_sha)

            # Open PR
            pr = self._create_pr(self.title, self.body, self.branch_name, base)
            return pr.get("html_url", json.dumps(pr))
        except Exception as e:
            return f"Error creating PR: {e}"