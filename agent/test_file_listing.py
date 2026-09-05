from agent.tools import execute_tool


files = execute_tool(
    "list_files",
    repo_path="sample_repo"
)

print("Repository files:")

for file in files:
    print(file)