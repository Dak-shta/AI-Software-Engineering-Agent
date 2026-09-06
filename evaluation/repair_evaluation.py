import json
from datetime import datetime
from pathlib import Path


def create_repair_record(
    bug_id,
    description,
    tests_before,
    tests_after,
    tools_used,
    steps,
    success,
):
    return {
        "bug_id": bug_id,
        "description": description,
        "tests_before": tests_before,
        "tests_after": tests_after,
        "tools_used": tools_used,
        "steps": steps,
        "success": success,
        "timestamp": datetime.now().isoformat(),
    }


def save_repair_record(record, output_path="evaluation/repair_results.json"):
    path = Path(output_path)

    if path.exists():
        results = json.loads(path.read_text(encoding="utf-8"))
    else:
        results = []

    results.append(record)

    path.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":

    record = create_repair_record(
        bug_id="BUG-001",
        description="User email value was not stored correctly.",
        tests_before={
            "passed": 2,
            "failed": 1,
        },
        tests_after={
            "passed": 3,
            "failed": 0,
        },
        tools_used=[
            "list_files",
            "run_tests",
            "read_file",
            "apply_patch",
            "run_tests",
        ],
        steps=5,
        success=True,
    )

    save_repair_record(record)

    print("Repair evaluation record saved.")