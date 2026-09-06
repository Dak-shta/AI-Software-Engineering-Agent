import json
from pathlib import Path

RESULTS_PATH = Path("evaluation/benchmark_results.json")


def load_results():
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"Results file not found: {RESULTS_PATH}"
        )

    return json.loads(
        RESULTS_PATH.read_text(encoding="utf-8")
    )


def calculate_metrics(results):
    total_cases = len(results)

    successful_repairs = sum(
        1
        for result in results
        if result["success"]
    )

    patch_used = sum(
        1
        for result in results
        if "apply_patch" in result["tools_used"]
    )

    final_tests_passed = sum(
        1
        for result in results
        if result["tests_after"]["failed"] == 0
    )

    agent_completed = sum(
        1
        for result in results
        if result["agent_completed"]
    )

    average_steps = (
        sum(result["steps"] for result in results)
        / total_cases
        if total_cases
        else 0
    )

    repair_success_rate = (
        successful_repairs / total_cases * 100
        if total_cases
        else 0
    )

    final_test_pass_rate = (
        final_tests_passed / total_cases * 100
        if total_cases
        else 0
    )

    patch_usage_rate = (
        patch_used / total_cases * 100
        if total_cases
        else 0
    )

    completion_rate = (
        agent_completed / total_cases * 100
        if total_cases
        else 0
    )

    return {
        "benchmark_cases": total_cases,
        "successful_repairs": successful_repairs,
        "repair_success_rate": round(
            repair_success_rate, 2
        ),
        "final_test_pass_rate": round(
            final_test_pass_rate, 2
        ),
        "patch_usage_rate": round(
            patch_usage_rate, 2
        ),
        "average_steps": round(
            average_steps, 2
        ),
        "agent_completion_rate": round(
            completion_rate, 2
        ),
    }


if __name__ == "__main__":
    results = load_results()

    metrics = calculate_metrics(results)

    print("\n========== REPAIR EVALUATION ==========")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\n========================================")