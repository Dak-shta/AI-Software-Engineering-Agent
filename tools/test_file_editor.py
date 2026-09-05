from pathlib import Path

from tools.file_editor import write_file


REPO = "sample_repo"
TEST_FILE = "sample_repo/_test_file.txt"


Path(TEST_FILE).write_text(
    "original content",
    encoding="utf-8"
)

result = write_file(
    REPO,
    TEST_FILE,
    "updated content"
)

print(result)

content = Path(TEST_FILE).read_text(
    encoding="utf-8"
)

print("Content:", content)

Path(TEST_FILE).unlink()


# Security test
try:
    write_file(
        REPO,
        "../.env",
        "GROQ_API_KEY=bad"
    )
except PermissionError as e:
    print("Security check:", e)