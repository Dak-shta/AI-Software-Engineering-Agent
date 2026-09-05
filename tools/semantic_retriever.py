from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from tools.repository import get_repository_files, read_file
from tools.chunker import chunk_code


model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_semantic(repo_path: str, query: str, top_k: int = 3):
    files = get_repository_files(repo_path)

    chunks = []

    for file in files:
        content = read_file(file)

        if content is None:
            continue

        file_chunks = chunk_code(file, content)
        chunks.extend(file_chunks)

    if not chunks:
        return []

    query_embedding = model.encode([query])

    chunk_texts = [
        chunk["content"]
        for chunk in chunks
    ]

    chunk_embeddings = model.encode(chunk_texts)

    similarities = cosine_similarity(
        query_embedding,
        chunk_embeddings
    )[0]

    ranked = sorted(
        zip(similarities, chunks),
        reverse=True,
        key=lambda x: x[0]
    )

    return ranked[:top_k]