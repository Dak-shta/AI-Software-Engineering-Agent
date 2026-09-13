import subprocess


def get_git_status(repo_path: str):
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "status": result.stdout,
        "stderr": result.stderr
    }