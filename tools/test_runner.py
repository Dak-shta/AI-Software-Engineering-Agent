import subprocess
import sys


def run_tests(
    repo_path: str,
    test_path: str | None = None
):
    command = [
        sys.executable,
        "-m",
        "pytest"
    ]

    if test_path:
        command.append(test_path)

    result = subprocess.run(
        command,
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }