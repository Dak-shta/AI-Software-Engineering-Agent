import json
from pathlib import Path


BENCHMARK_PATH = Path("evaluation/swebench_mini.json")
RESULTS_PATH = Path("evaluation/repair_results.json")


def load_json(path):
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def build_results():
    benchmark = load_json(BENCHMARK_PATH)
    repair_results = load_json(RESULTS_PATH)

    # Keep the latest result for each bug.
    results_by_bug = {
        result["bug_id"]: result
        for result in repair_results
    }

    evaluation = []

    for case in benchmark:
        result = results_by_bug.get(case["bug_id"])

        if result is None:
            status = "not_evaluated"
        elif result["success"]:
            status = "success"
        else:
            status = "failure"

        evaluation.append({
            "instance_id": case["instance_id"],
            "bug_id": case["bug_id"],
            "problem_statement": case["problem_statement"],
            "target_file": case["target_file"],
            "test_file": case["test_file"],
            "expected_behavior": case["expected_behavior"],
            "expected_result": case["expected_result"],
            "actual_result": status,
            "steps": result["steps"] if result else None,
            "tests_before": (
                result["tests_before"]
                if result else None
            ),
            "tests_after": (
                result["tests_after"]
                if result else None
            ),
            "tools_used": (
                result["tools_used"]
                if result else []
            ),
        })

    return evaluation


def save_results(evaluation):
    output_path = Path(
        "evaluation/swebench_mini_results.json"
    )

    output_path.write_text(
        json.dumps(
            evaluation,
            indent=2
        ),
        encoding="utf-8"
    )

    return output_path


if __name__ == "__main__":
    evaluation = build_results()
    output_path = save_results(evaluation)

    print("========== MINI SWE-BENCH EVALUATION ==========")

    for result in evaluation:
        print(
            f"{result['instance_id']}: "
            f"{result['actual_result']}"
        )

    print(
        f"\nResults saved to: {output_path}"
    )