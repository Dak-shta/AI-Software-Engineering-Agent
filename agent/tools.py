from tools.git_tools import get_git_diff
from tools.pr_context import get_pr_context
from tools.test_runner import run_tests
from tools.file_reader import read_repository_file
from tools.vector_store import search_repository
from tools.file_listing import list_repository_files
from agent.apply_change import apply_code_change
from tools.patch_editor import apply_patch
from tools.git_status import get_git_status


TOOLS = {
    "run_tests": run_tests,
    "git_status": get_git_status,
"pr_context": get_pr_context,
    "read_file": read_repository_file,
    "search_repository": search_repository,
    "list_files": list_repository_files,
    "apply_change": apply_code_change,
    "apply_patch": apply_patch,
    "git_diff": get_git_diff
}


def execute_tool(tool_name: str, **kwargs):
    if tool_name not in TOOLS:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    return TOOLS[tool_name](**kwargs)


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files inside the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string"
                    }
                },
                "required": ["repo_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_repository",
            "description": "Search repository code using semantic retrieval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "repo_path": {
                        "type": "string"
                    },
                    "top_k": {
                        "type": "integer"
                    }
                },
                "required": ["query", "repo_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a specific file inside the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string"
                    },
                    "file_path": {
                        "type": "string"
                    }
                },
                "required": ["repo_path", "file_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run pytest tests in the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string"
                    },
                    "test_path": {
                        "type": "string"
                    }
                },
                "required": ["repo_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "apply_change",
            "description": "Replace an existing repository file with corrected code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string"
                    },
                    "file_path": {
                        "type": "string"
                    },
                    "code": {
                        "type": "string"
                    }
                },
                "required": [
                    "repo_path",
                    "file_path",
                    "code"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "apply_patch",
            "description": (
                "Safely modify an existing repository file by replacing "
                "one exact piece of old code with new code. "
                "Use this instead of replacing the entire file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string"
                    },
                    "file_path": {
                        "type": "string"
                    },
                    "old_text": {
                        "type": "string"
                    },
                    "new_text": {
                        "type": "string"
                    }
                },
                "required": [
                    "repo_path",
                    "file_path",
                    "old_text",
                    "new_text"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "git_diff",
            "description": "Show the current uncommitted Git changes in the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Absolute path to the repository."
                    }
                },
                "required": ["repo_path"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "git_status",
        "description": "Show the current Git status of the repository, including modified, staged, and untracked files.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Absolute path to the repository."
                }
            },
            "required": ["repo_path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pr_context",
        "description": (
            "Collect Git status and Git diff information "
            "for pull-request-style analysis of repository changes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Absolute path to the repository."
                }
            },
            "required": ["repo_path"]
        }
    }
}
]