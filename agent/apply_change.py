from pathlib import Path
from tools.file_editor import write_file


def apply_code_change(
    repo_path: str,
    file_path: str,
    code: str
):
    repo = Path(repo_path).resolve()
    target = (repo / file_path).resolve()

    return write_file(
        repo_path,
        str(target),
        code
    )