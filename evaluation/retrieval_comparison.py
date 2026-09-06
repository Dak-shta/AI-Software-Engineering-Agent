from pathlib import Path

from tools.vector_store import collection, model
from tools.retriever import keyword_scores


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

    # Bug files
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


def get_file_name(path):
    return Path(path).name


def semantic_search(query, repo_path="sample_repo", top_k=3):

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where={
            "repo_path": str(repo_path)
        }
    )

    files = []

    for metadata in results["metadatas"][0]:
        files.append(
            get_file_name(metadata["file"])
        )

    return files


def keyword_search(query, repo_path="sample_repo", top_k=3):

    scores = keyword_scores(
        repo_path,
        query
    )

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        get_file_name(file)
        for file, score in ranked[:top_k]
    ]


def hybrid_search(query, repo_path="sample_repo", top_k=3):

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k * 3,
        where={
            "repo_path": str(repo_path)
        }
    )

    keywords = keyword_scores(
        repo_path,
        query
    )

    # Normalize keyword scores to 0-1.
    max_keyword_score = max(
        keywords.values(),
        default=0
    )

    if max_keyword_score > 0:
        normalized_keywords = {
            file: score / max_keyword_score
            for file, score in keywords.items()
        }
    else:
        normalized_keywords = {
            file: 0
            for file in keywords
        }

    # Aggregate semantic results at file level.
    file_scores = {}

    for i in range(len(results["documents"][0])):

        file = results["metadatas"][0][i]["file"]

        semantic_score = 1 / (
            1 + results["distances"][0][i]
        )

        keyword_score = normalized_keywords.get(
            file,
            0
        )

        final_score = (
            0.7 * semantic_score
            + 0.3 * keyword_score
        )

        # Keep the strongest chunk score for each file.
        if (
            file not in file_scores
            or final_score > file_scores[file]
        ):
            file_scores[file] = final_score

    ranked_files = sorted(
        file_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        get_file_name(file)
        for file, score in ranked_files[:top_k]
    ]

def evaluate_method(method_name, search_function):

    top1_correct = 0
    top3_correct = 0

    print("\n")
    print("=" * 60)
    print(method_name)
    print("=" * 60)

    for test in TEST_CASES:

        retrieved = search_function(
            test["query"],
            top_k=3
        )

        expected = test["expected_file"]

        top1_pass = (
            len(retrieved) >= 1
            and retrieved[0] == expected
        )

        top3_pass = (
            expected in retrieved
        )

        if top1_pass:
            top1_correct += 1

        if top3_pass:
            top3_correct += 1

        print(
            f"\nQuery: {test['query']}"
        )
        print(
            f"Expected: {expected}"
        )
        print(
            f"Retrieved: {retrieved}"
        )
        print(
            f"Top-1: {'PASS' if top1_pass else 'FAIL'} | "
            f"Top-3: {'PASS' if top3_pass else 'FAIL'}"
        )

    total = len(TEST_CASES)

    top1_accuracy = top1_correct / total
    top3_accuracy = top3_correct / total

    print("\n------------------------------")
    print(
        f"Top-1 Accuracy: {top1_accuracy:.2%}"
    )
    print(
        f"Top-3 Accuracy: {top3_accuracy:.2%}"
    )
    print("------------------------------")

    return {
        "top1": top1_accuracy,
        "top3": top3_accuracy
    }


def main():

    keyword_results = evaluate_method(
        "KEYWORD RETRIEVAL",
        keyword_search
    )

    semantic_results = evaluate_method(
        "SEMANTIC RETRIEVAL",
        semantic_search
    )

    hybrid_results = evaluate_method(
        "HYBRID RETRIEVAL",
        hybrid_search
    )

    print("\n")
    print("=" * 60)
    print("FINAL RETRIEVAL COMPARISON")
    print("=" * 60)

    print(
        f"\nKeyword   → "
        f"Top-1: {keyword_results['top1']:.2%}, "
        f"Top-3: {keyword_results['top3']:.2%}"
    )

    print(
        f"Semantic  → "
        f"Top-1: {semantic_results['top1']:.2%}, "
        f"Top-3: {semantic_results['top3']:.2%}"
    )

    print(
        f"Hybrid    → "
        f"Top-1: {hybrid_results['top1']:.2%}, "
        f"Top-3: {hybrid_results['top3']:.2%}"
    )


if __name__ == "__main__":
    main()