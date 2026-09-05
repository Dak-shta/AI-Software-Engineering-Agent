from agent.tools import execute_tool


result = execute_tool(
    "search_repository",
    query="Where is the User class defined?",
    repo_path="sample_repo",
    top_k=2
)

print("Search results:")

for item in result:
    print("\nFile:", item["file"])
    print("Lines:", item["start_line"], "-", item["end_line"])
    print("Score:", item["final_score"])
    print("Code:")
    print(item["content"])