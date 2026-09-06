from pathlib import Path


BENCHMARK_CASES = [
    {
        "bug_id": "BUG-001",
        "file": "patch_fixture.py",
        "test_file": "test_patch_fixture.py",
        "description": "User email value was not stored correctly.",
        "expected_result": "success",
    },
    {
        "bug_id": "BUG-002",
        "file": "bug_return.py",
        "test_file": "test_bug_return.py",
        "description": "Function returned price instead of price multiplied by quantity.",
        "expected_result": "success",
    },
    {
        "bug_id": "BUG-003",
        "file": "bug_discount.py",
        "test_file": "test_bug_discount.py",
        "description": "Member discount was not applied correctly.",
        "expected_result": "success",
    },
    {
        "bug_id": "BUG-004",
        "file": "bug_failure.py",
        "test_file": "test_bug_failure.py",
        "description": "Division by zero is not handled.",
        "expected_result": "success",
    },
    {
        "bug_id": "BUG-005",
        "file": "bug_function_call.py",
        "test_file": "test_bug_function_call.py",
        "description": "Area calculation calls an undefined function instead of calculating length multiplied by width.",
        "expected_result": "success",
    },
    {
        "bug_id": "BUG-006",
        "file": "bug_dependency.py",
        "test_file": "test_bug_dependency.py",
        "description": "Function returns the user's name instead of the user's email.",
        "expected_result": "success",
    },
]


def get_benchmark():
    return BENCHMARK_CASES


def get_benchmark():
    return BENCHMARK_CASES


if __name__ == "__main__":
    cases = get_benchmark()

    print("========== BENCHMARK ==========")

    for case in cases:
        print(
            f"{case['bug_id']}: "
            f"{case['description']} "
            f"-> expected {case['expected_result']}"
        )

    print(f"\nTotal cases: {len(cases)}")