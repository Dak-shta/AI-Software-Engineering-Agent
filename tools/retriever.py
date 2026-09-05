from tools.repository import get_repository_files, read_file


def keyword_scores(repo_path: str, query: str):
    files = get_repository_files(repo_path)

    query_words = set(query.lower().split())
    scores = {}

    for file in files:
        content = read_file(file)

        if content is None:
            continue

        text = content.lower()

        score = sum(
            1 for word in query_words
            if word in text
        )

        scores[str(file)] = score

    return scores