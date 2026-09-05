from agent.tool_selector import select_tool


request = "Run the tests for the User model."

result = select_tool(request)

print("Selected tool:", result["tool"])
print("Arguments:", result["arguments"])