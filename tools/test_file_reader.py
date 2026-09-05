from tools.file_reader import read_repository_file


content = read_repository_file(
    "sample_repo",
    "models.py"
)

print(content)