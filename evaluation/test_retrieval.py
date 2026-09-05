from tools.vector_store import search_repository


TEST_CASES = [
    {
        "query": "Where is the User class defined?",
        "expected_file": "models.py"
    },
    {
        "query": "Where is the User object created?",
        "expected_file": "app.py"
    },
    {
        "query": "How is the user's name stored?",
        "expected_file": "models.py"
    }
]


def evaluate_retrieval():
    correct = 0

    for test in TEST_CASES:
        results = search_repository(
            test["query"],
            top_k=1
        )

        retrieved_file = results[0]["file"]

        print(f"\nQuestion: {test['query']}")
        print(f"Expected: {test['expected_file']}")
        print(f"Retrieved: {retrieved_file}")

        if test["expected_file"] in retrieved_file:
            correct += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")

    accuracy = correct / len(TEST_CASES)

    print("\n--------------------")
    print(f"Top-1 Accuracy: {accuracy:.2%}")
    print("--------------------")


if __name__ == "__main__":
    evaluate_retrieval()