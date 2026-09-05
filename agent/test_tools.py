from agent.tools import execute_tool


# This is the tool-selection result produced by the LLM.
tool_decision = {
    "tool": "run_tests",
    "arguments": {
        "repo_path": "sample_repo",
        "test_path": "test_models.py"
    }
}


result = execute_tool(
    tool_decision["tool"],
    **tool_decision["arguments"]
)


print("Selected tool:", tool_decision["tool"])
print("Arguments:", tool_decision["arguments"])

print("\nTool result:")
print("Success:", result["success"])
print("Return code:", result["returncode"])

print("\nOutput:")
print(result["stdout"])

if result["stderr"]:
    print("\nErrors:")
    print(result["stderr"])