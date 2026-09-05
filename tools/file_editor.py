from pathlib import Path


def write_file(
    repo_path: str,
    file_path: str,
    content: str
):
    repo = Path(repo_path).resolve()
    target = Path(file_path).resolve()

    # Prevent modifying files outside the repository
    try:
        target.relative_to(repo)
    except ValueError:
        raise PermissionError(
            "File modification is allowed only inside the repository."
        )

    # Prevent modifying files that don't exist
    if not target.exists():
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    # Prevent accidental modification of sensitive files
    if target.name == ".env":
        raise PermissionError(
            "Modification of .env is not allowed."
        )

    target.write_text(
        content,
        encoding="utf-8"
    )

    return f"Updated {target}"