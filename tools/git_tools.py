import subprocess


def get_git_diff(repo_path: str):
    result = subprocess.run(
        ["git", "diff"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "diff": result.stdout,
        "stderr": result.stderr
    }