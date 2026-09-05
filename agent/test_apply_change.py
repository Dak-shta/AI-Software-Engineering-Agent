from agent.tools import execute_tool

result = execute_tool(
    "apply_change",
    repo_path="sample_repo",
    file_path="models.py",
    code="""class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email
"""
)

print(result)