import json
import re
import subprocess
from pathlib import Path

from evaluation.benchmark import get_benchmark
from agent.react_agent import run_repair_agent


FIXTURES_DIR = Path("evaluation/fixtures")
RESULTS_PATH = Path("evaluation/benchmark_results.json")


def reset_fixture(fixture):
    """Restore a benchmark fixture to its original Git state."""

    result = subprocess.run(
        [
            "git",
            "restore",
            "--source=HEAD",
            "--",
            str(fixture),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Failed to reset fixture {fixture}:\n"
            f"{result.stderr}"
        )


def run_tests(repo_path):
    """Run pytest and return exact test counts."""

    result = subprocess.run(
        [
            str(Path(".myenv/Scripts/python.exe")),
            "-m",
            "pytest",
            str(repo_path),
            "--tb=no",
            "-q",
        ],
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr

    passed_match = re.search(r"(\d+)\s+passed", output)
    failed_match = re.search(r"(\d+)\s+failed", output)

    passed = (
        int(passed_match.group(1))
        if passed_match
        else 0
    )

    failed = (
        int(failed_match.group(1))
        if failed_match
        else 0
    )

    return {
        "passed": passed,
        "failed": failed,
        "returncode": result.returncode,
    }


def save_results(results):
    """Save benchmark results to JSON."""

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    RESULTS_PATH.write_text(
        json.dumps(
            results,
            indent=2
        ),
        encoding="utf-8",
    )


def main():

    benchmark = get_benchmark()

    results = []

    print("\n")
    print("=" * 60)
    print("        AI SOFTWARE ENGINEERING AGENT BENCHMARK")
    print("=" * 60)

    for case in benchmark:

        bug_id = case["bug_id"]
        fixture = FIXTURES_DIR / bug_id

        print("\n")
        print("=" * 60)
        print(f"RUNNING {bug_id}")
        print("=" * 60)

        # ---------------------------------
        # Reset fixture
        # ---------------------------------

        print("\nResetting fixture...")
        reset_fixture(fixture)

        # ---------------------------------
        # Tests BEFORE repair
        # ---------------------------------

        tests_before = run_tests(fixture)

        print(
            f"\nTests before: "
            f"{tests_before['passed']} passed, "
            f"{tests_before['failed']} failed"
        )

        # ---------------------------------
        # Agent
        # ---------------------------------

        request = (
            f"Repair the bug described below in the repository "
            f"located at {fixture}. "
            f"Use this exact repository path for all tools: {fixture}. "
            f"Do not use sample_repo. "
            f"Do not modify files outside this repository. "
            f"First inspect the repository and run the tests. "
            f"Diagnose the failure, make the smallest safe fix, "
            f"and run the tests again.\n\n"
            f"Bug: {case['description']}"
        )

        agent_result = run_repair_agent(
            request,
            repo_path=str(fixture),
            task_id=bug_id
        )

        # ---------------------------------
        # Tests AFTER repair
        # ---------------------------------

        tests_after = run_tests(fixture)

        repair_success = (
            tests_after["failed"] == 0
            and tests_after["passed"] > 0
        )

        print(
            f"\nTests after: "
            f"{tests_after['passed']} passed, "
            f"{tests_after['failed']} failed"
        )

        print(
            f"Steps: "
            f"{agent_result['steps']}"
        )

        print(
            f"Tools: "
            f"{agent_result['tools_used']}"
        )

        print(
            f"Repair success: "
            f"{repair_success}"
        )

        # ---------------------------------
        # Save result
        # ---------------------------------

        results.append(
            {
                "bug_id": bug_id,
                "description": case["description"],
                "tests_before": tests_before,
                "tests_after": tests_after,
                "tools_used": agent_result["tools_used"],
                "steps": agent_result["steps"],
                "agent_completed": agent_result[
                    "agent_completed"
                ],
                "success": repair_success,
            }
        )

        save_results(results)

    print("\n")
    print("=" * 60)
    print("BENCHMARK COMPLETE")
    print("=" * 60)

    print(
        f"\nResults saved to: "
        f"{RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()