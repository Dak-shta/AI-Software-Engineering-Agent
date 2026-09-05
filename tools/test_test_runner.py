from tools.test_runner import run_tests


result = run_tests(
    "sample_repo",
    "test_models.py"
)

print("Success:", result["success"])
print("Return code:", result["returncode"])

print("\nOutput:")
print(result["stdout"])

if result["stderr"]:
    print("\nErrors:")
    print(result["stderr"])