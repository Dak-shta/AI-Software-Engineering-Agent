from pathlib import Path


IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
}


def get_repository_files(repo_path: str):
    repo = Path(repo_path)

    files = []

    for path in repo.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        files.append(path)

    return files


def read_file(file_path: Path):
    try:
        return file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def build_repository_context(repo_path: str):
    files = get_repository_files(repo_path)

    context = []

    for file in files:
        content = read_file(file)

        if content is None:
            continue

        context.append(
            f"""
--- FILE: {file} ---

{content}
"""
        )

    return "\n".join(context)