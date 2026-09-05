from pathlib import Path
from tools.repository import get_repository_files


def list_repository_files(repo_path: str):
    repo = Path(repo_path).resolve()

    files = get_repository_files(repo_path)

    return [
        str(Path(file).resolve().relative_to(repo))
        for file in files
    ]