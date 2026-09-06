from tools.vector_store import search_repository


TEST_CASES = [
    # models.py
    {
        "query": "Where is the User class defined?",
        "expected_file": "models.py"
    },
    {
        "query": "How is the user's name stored?",
        "expected_file": "models.py"
    },
    {
        "query": "Where is the user's email stored?",
        "expected_file": "models.py"
    },
    {
        "query": "What attributes does the User class contain?",
        "expected_file": "models.py"
    },
    {
        "query": "Where is the User model implemented?",
        "expected_file": "models.py"
    },

    # app.py
    {
        "query": "Where is the User object created?",
        "expected_file": "app.py"
    },
    {
        "query": "Where is a User instance initialized?",
        "expected_file": "app.py"
    },
    {
        "query": "Which file creates a user?",
        "expected_file": "app.py"
    },
    {
        "query": "Where is the User constructor called?",
        "expected_file": "app.py"
    },
    {
        "query": "Where is a user object instantiated?",
        "expected_file": "app.py"
    },

    # Other repository files
    {
        "query": "Where is the calculate_total function?",
        "expected_file": "bug_return.py"
    },
    {
        "query": "Where is the discount calculation implemented?",
        "expected_file": "bug_discount.py"
    },
    {
        "query": "Where is division performed?",
        "expected_file": "bug_failure.py"
    },
    {
        "query": "Where is the area calculation function?",
        "expected_file": "bug_function_call.py"
    },
    {
        "query": "Where is the user's email retrieved?",
        "expected_file": "bug_dependency.py"
    }
]


def evaluate_retrieval():

    top1_correct = 0
    top3_correct = 0

    for test in TEST_CASES:

        results = search_repository(
            test["query"],
            top_k=3
        )

        from pathlib import Path

        retrieved_files = [
    Path(result["file"]).name
    for result in results
]

        expected = test["expected_file"]

        top1_pass = expected in retrieved_files[:1]
        top3_pass = expected in retrieved_files[:3]

        if top1_pass:
            top1_correct += 1

        if top3_pass:
            top3_correct += 1

        print(f"\nQuestion: {test['query']}")
        print(f"Expected: {expected}")
        print(f"Retrieved: {retrieved_files}")

        print(
            f"Top-1: {'PASS' if top1_pass else 'FAIL'} | "
            f"Top-3: {'PASS' if top3_pass else 'FAIL'}"
        )

    top1_accuracy = top1_correct / len(TEST_CASES)
    top3_accuracy = top3_correct / len(TEST_CASES)

    print("\n==============================")
    print("Retrieval Evaluation Results")
    print("==============================")

    print(f"Test Cases: {len(TEST_CASES)}")
    print(f"Top-1 Accuracy: {top1_accuracy:.2%}")
    print(f"Top-3 Accuracy: {top3_accuracy:.2%}")

    print("==============================")


if __name__ == "__main__":
    evaluate_retrieval()