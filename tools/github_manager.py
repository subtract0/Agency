import os
import json
import base64
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv
import requests
from agency_swarm.tools import BaseTool
from pydantic import Field

# Load environment variables
load_dotenv()


class GitHubManager(BaseTool):
    """
    A tool to manage GitHub repositories via the REST API.
    Handles pull requests, branches, commits, and issues through direct API calls.
    """

    action: str = Field(
        ...,
        description="The action to perform: 'create_pr', 'get_pr', 'create_branch', 'list_prs', 'comment_pr', 'get_repo_info'"
    )

    repo: Optional[str] = Field(
        None,
        description="The GitHub repository in the format 'owner/repo'. If not provided, will be extracted from git remote."
    )

    title: Optional[str] = Field(
        None,
        description="Title for the pull request or issue"
    )

    body: Optional[str] = Field(
        None,
        description="Body content for the pull request, issue, or comment"
    )

    branch: Optional[str] = Field(
        None,
        description="Source branch name for pull request"
    )

    base: Optional[str] = Field(
        "main",
        description="Target/base branch for pull request (defaults to 'main')"
    )

    pr_number: Optional[int] = Field(
        None,
        description="Pull request number for getting or commenting on a specific PR"
    )

    files: Optional[Dict[str, str]] = Field(
        None,
        description="Dictionary of file paths and their content for creating commits"
    )

    commit_message: Optional[str] = Field(
        None,
        description="Commit message when creating commits"
    )

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from environment variables."""
        # Try multiple possible environment variable names
        token = os.environ.get("GH_TOKEN")
        if not token:
            token = os.environ.get("GITHUB_TOKEN")
        if not token:
            token = os.environ.get("GITHUB_ACCESS_TOKEN")
        return token

    def _get_repo_from_git(self) -> Optional[str]:
        """Extract repository info from git remote."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                # Parse GitHub URL formats
                if "github.com" in url:
                    if url.startswith("git@"):
                        # SSH format: git@github.com:owner/repo.git
                        parts = url.split(":")[-1]
                    elif url.startswith("https://"):
                        # HTTPS format: https://github.com/owner/repo.git
                        parts = url.split("github.com/")[-1]
                    else:
                        return None

                    # Remove .git suffix if present
                    if parts.endswith(".git"):
                        parts = parts[:-4]

                    return parts
        except Exception:
            pass
        return None

    def _get_headers(self, token: str) -> Dict[str, str]:
        """Get API headers with authentication."""
        return {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def _get_default_branch(self, repo: str, headers: Dict[str, str]) -> str:
        """Get the default branch of the repository."""
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["default_branch"]
        return "main"  # Fallback to main

    def create_pull_request(self, repo: str, headers: Dict[str, str]) -> str:
        """Create a pull request."""
        if not self.title or not self.branch:
            return "Error: Title and branch are required for creating a pull request"

        # Get default branch if base not specified
        if not self.base:
            self.base = self._get_default_branch(repo, headers)

        url = f"https://api.github.com/repos/{repo}/pulls"
        data = {
            "title": self.title,
            "body": self.body or "",
            "head": self.branch,
            "base": self.base,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            pr_data = response.json()
            return f"Pull request created successfully!\nURL: {pr_data['html_url']}\nNumber: #{pr_data['number']}"
        elif response.status_code == 422:
            error_data = response.json()
            if "errors" in error_data:
                errors = error_data["errors"]
                if any(e.get("message", "").startswith("A pull request already exists") for e in errors):
                    # Try to find the existing PR
                    search_url = f"https://api.github.com/repos/{repo}/pulls"
                    search_params = {"head": f"{repo.split('/')[0]}:{self.branch}", "state": "open"}
                    search_response = requests.get(search_url, headers=headers, params=search_params)
                    if search_response.status_code == 200 and search_response.json():
                        existing_pr = search_response.json()[0]
                        return f"A pull request already exists for this branch!\nURL: {existing_pr['html_url']}\nNumber: #{existing_pr['number']}"
                    return "A pull request already exists for this branch"
            return f"Validation error: {error_data.get('message', 'Unknown validation error')}"
        else:
            return f"Error creating pull request: {response.status_code} - {response.text}"

    def get_pull_request(self, repo: str, headers: Dict[str, str]) -> str:
        """Get information about a specific pull request."""
        if not self.pr_number:
            return "Error: PR number is required"

        url = f"https://api.github.com/repos/{repo}/pulls/{self.pr_number}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            pr = response.json()
            return (
                f"PR #{pr['number']}: {pr['title']}\n"
                f"State: {pr['state']}\n"
                f"Author: {pr['user']['login']}\n"
                f"Branch: {pr['head']['ref']} -> {pr['base']['ref']}\n"
                f"URL: {pr['html_url']}\n"
                f"Mergeable: {pr.get('mergeable', 'unknown')}\n"
                f"Description:\n{pr.get('body', 'No description')}"
            )
        else:
            return f"Error getting pull request: {response.status_code} - {response.text}"

    def list_pull_requests(self, repo: str, headers: Dict[str, str]) -> str:
        """List open pull requests."""
        url = f"https://api.github.com/repos/{repo}/pulls"
        params = {"state": "open", "per_page": 10}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            prs = response.json()
            if not prs:
                return "No open pull requests found"

            result = "Open Pull Requests:\n\n"
            for pr in prs:
                result += (
                    f"#{pr['number']}: {pr['title']}\n"
                    f"  Author: {pr['user']['login']}\n"
                    f"  Branch: {pr['head']['ref']} -> {pr['base']['ref']}\n"
                    f"  URL: {pr['html_url']}\n\n"
                )
            return result
        else:
            return f"Error listing pull requests: {response.status_code} - {response.text}"

    def comment_on_pr(self, repo: str, headers: Dict[str, str]) -> str:
        """Add a comment to a pull request."""
        if not self.pr_number or not self.body:
            return "Error: PR number and comment body are required"

        url = f"https://api.github.com/repos/{repo}/issues/{self.pr_number}/comments"
        data = {"body": self.body}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            comment = response.json()
            return f"Comment added successfully!\nURL: {comment['html_url']}"
        else:
            return f"Error adding comment: {response.status_code} - {response.text}"

    def create_branch(self, repo: str, headers: Dict[str, str]) -> str:
        """Create a new branch."""
        if not self.branch:
            return "Error: Branch name is required"

        # Get the default branch's latest commit SHA
        base_branch = self.base or self._get_default_branch(repo, headers)
        ref_url = f"https://api.github.com/repos/{repo}/git/ref/heads/{base_branch}"

        response = requests.get(ref_url, headers=headers)
        if response.status_code != 200:
            return f"Error getting base branch: {response.status_code} - {response.text}"

        latest_sha = response.json()["object"]["sha"]

        # Create the new branch
        create_url = f"https://api.github.com/repos/{repo}/git/refs"
        data = {
            "ref": f"refs/heads/{self.branch}",
            "sha": latest_sha
        }

        response = requests.post(create_url, headers=headers, json=data)

        if response.status_code == 201:
            return f"Branch '{self.branch}' created successfully from '{base_branch}'"
        elif response.status_code == 422:
            return f"Branch '{self.branch}' already exists"
        else:
            return f"Error creating branch: {response.status_code} - {response.text}"

    def get_repo_info(self, repo: str, headers: Dict[str, str]) -> str:
        """Get repository information."""
        url = f"https://api.github.com/repos/{repo}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            info = response.json()
            return (
                f"Repository: {info['full_name']}\n"
                f"Description: {info.get('description', 'No description')}\n"
                f"Default Branch: {info['default_branch']}\n"
                f"Private: {info['private']}\n"
                f"Stars: {info['stargazers_count']}\n"
                f"Forks: {info['forks_count']}\n"
                f"Open Issues: {info['open_issues_count']}\n"
                f"URL: {info['html_url']}"
            )
        else:
            return f"Error getting repository info: {response.status_code} - {response.text}"

    def run(self) -> str:
        """Execute the GitHub API action."""
        # Get authentication token
        token = self._get_github_token()
        if not token:
            return (
                "Error: No GitHub token found in environment variables.\n"
                "Please set one of: GH_TOKEN, GITHUB_TOKEN, or GITHUB_ACCESS_TOKEN"
            )

        # Get repository if not provided
        if not self.repo:
            self.repo = self._get_repo_from_git()
            if not self.repo:
                return (
                    "Error: Could not determine repository.\n"
                    "Please provide the 'repo' parameter in format 'owner/repo' or ensure you're in a git repository."
                )

        headers = self._get_headers(token)

        # Route to appropriate action
        try:
            if self.action == "create_pr":
                return self.create_pull_request(self.repo, headers)
            elif self.action == "get_pr":
                return self.get_pull_request(self.repo, headers)
            elif self.action == "list_prs":
                return self.list_pull_requests(self.repo, headers)
            elif self.action == "comment_pr":
                return self.comment_on_pr(self.repo, headers)
            elif self.action == "create_branch":
                return self.create_branch(self.repo, headers)
            elif self.action == "get_repo_info":
                return self.get_repo_info(self.repo, headers)
            else:
                return f"Error: Unknown action '{self.action}'. Valid actions: create_pr, get_pr, list_prs, comment_pr, create_branch, get_repo_info"
        except requests.exceptions.RequestException as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


# Create alias for Agency Swarm tool loading
github_manager = GitHubManager