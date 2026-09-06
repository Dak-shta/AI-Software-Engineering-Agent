from pathlib import Path


def apply_patch(
    repo_path: str,
    file_path: str,
    old_text: str,
    new_text: str
):
    repo = Path(repo_path).resolve()
    target = (repo / file_path).resolve()

    # Security: file must stay inside repository
    try:
        target.relative_to(repo)
    except ValueError:
        raise PermissionError(
            "File modification is allowed only inside the repository."
        )

    if target.name == ".env":
        raise PermissionError(
            "Modification of .env is not allowed."
        )

    if not target.exists():
        raise FileNotFoundError(
            f"File does not exist: {file_path}"
        )

    if not target.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    content = target.read_text(encoding="utf-8")

    # Safety: exact old code must exist
    occurrences = content.count(old_text)

    if occurrences == 0:
        raise ValueError(
            "Patch failed: old_text was not found in the file."
        )

    if occurrences > 1:
        raise ValueError(
            "Patch failed: old_text occurs multiple times."
        )

    updated_content = content.replace(
        old_text,
        new_text,
        1
    )

    target.write_text(
        updated_content,
        encoding="utf-8"
    )

    return {
        "success": True,
        "file": str(target),
        "message": "Patch applied successfully."
    }