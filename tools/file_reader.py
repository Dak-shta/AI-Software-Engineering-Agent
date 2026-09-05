from pathlib import Path


def read_repository_file(repo_path: str, file_path: str):
    repo = Path(repo_path).resolve()
    target = (repo / file_path).resolve()

    try:
        target.relative_to(repo)
    except ValueError:
        raise PermissionError(
            "File reading is allowed only inside the repository."
        )

    if not target.exists():
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    if not target.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    return target.read_text(encoding="utf-8")