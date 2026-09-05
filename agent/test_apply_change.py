from pathlib import Path

from agent.apply_change import apply_code_change


TEST_FILE = "sample_repo/_test_model.py"


Path(TEST_FILE).write_text(
    "class Test:\n    pass\n",
    encoding="utf-8"
)


response = """
FILE: sample_repo/_test_model.py

CHANGE: Add a value attribute.

PROPOSED CODE:
```python
class Test:
    def __init__(self):
        self.value = 10

REASON:
Adds a value attribute.
"""

result = apply_code_change(
"sample_repo",
response
)

print(result)

print(
Path(TEST_FILE).read_text(
encoding="utf-8"
)
)

Path(TEST_FILE).unlink()