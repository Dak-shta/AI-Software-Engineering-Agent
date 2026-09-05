from tools.test_runner import run_tests
from tools.file_reader import read_repository_file
from tools.vector_store import search_repository
from tools.file_listing import list_repository_files
from agent.apply_change import apply_code_change


TOOLS = {
    "run_tests": run_tests,
    "read_file": read_repository_file,
    "search_repository": search_repository,
    "list_files": list_repository_files,
    "apply_change": apply_code_change
}


def execute_tool(tool_name: str, **kwargs):
    if tool_name not in TOOLS:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    return TOOLS[tool_name](**kwargs)