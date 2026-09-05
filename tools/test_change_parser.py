from tools.change_parser import parse_code_change


response = """
FILE: sample_repo/models.py

CHANGE: Add an email attribute.

PROPOSED CODE:
```python
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email

REASON:
The User class should store the user's email.
"""

print("----- RAW RESPONSE -----")
print(repr(response))

print("\n----- FILE MATCH -----")

import re

file_match = re.search(
r"FILE:\s*(.+)",
response
)

print(file_match.group(1) if file_match else "NO FILE MATCH")

print("\n----- CODE MATCH -----")

code_match = re.search(
r"PROPOSED CODE:\s*(?:python)?\s*\n?(.*?)",
response,
re.DOTALL
)

print(code_match.group(1) if code_match else "NO CODE MATCH")

print("\n----- PARSER -----")

result = parse_code_change(response)

print("File:", result["file"])
print("Code:")
print(result["code"])