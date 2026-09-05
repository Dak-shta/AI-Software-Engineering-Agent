from tools.change_parser import parse_code_change
from tools.file_editor import write_file


def apply_code_change(
    repo_path: str,
    generated_response: str
):
    change = parse_code_change(generated_response)

    result = write_file(
        repo_path,
        change["file"],
        change["code"]
    )

    return result