from tools.git_tools import get_git_diff
from tools.git_status import get_git_status


def get_pr_context(repo_path: str):
    status_result = get_git_status(repo_path)
    diff_result = get_git_diff(repo_path)

    return {
        "success": (
            status_result["success"]
            and diff_result["success"]
        ),
        "status": status_result["status"],
        "diff": diff_result["diff"],
        "errors": {
            "status": status_result["stderr"],
            "diff": diff_result["stderr"]
        }
    }