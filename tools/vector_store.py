from tools.retriever import keyword_scores
import chromadb
from sentence_transformers import SentenceTransformer

from tools.repository import get_repository_files, read_file
from tools.chunker import chunk_code


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./vectorstore"
)

collection = client.get_or_create_collection(
    name="repository_code"
)


def index_repository(repo_path: str):
    files = get_repository_files(repo_path)

    chunks = []

    for file in files:
        content = read_file(file)

        if content is None:
            continue

        chunks.extend(
            chunk_code(file, content)
        )

    if not chunks:
        return 0

    embeddings = model.encode(
        [chunk["content"] for chunk in chunks]
    ).tolist()

    ids = [
    f"{repo_path}_{i}"
    for i in range(len(chunks))
]

    documents = [
        chunk["content"]
        for chunk in chunks
    ]

    metadatas = [
    {
        "file": chunk["file"],
        "start_line": chunk["start_line"],
        "end_line": chunk["end_line"],
        "repo_path": str(repo_path)
    }
    for chunk in chunks
]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


# ADD IT HERE 👇

def search_repository(
    query: str,
    repo_path: str = "sample_repo",
    top_k: int = 3
):
    query_embedding = model.encode(
        [query]
    ).tolist()

    results = collection.query(
    query_embeddings=query_embedding,
    n_results=top_k * 3,
    where={
        "repo_path": str(repo_path)
    }
)

    semantic_results = []

    for i in range(len(results["documents"][0])):
        semantic_results.append({
            "file": results["metadatas"][0][i]["file"],
            "start_line": results["metadatas"][0][i]["start_line"],
            "end_line": results["metadatas"][0][i]["end_line"],
            "content": results["documents"][0][i],
            "semantic_score": 1 / (
                1 + results["distances"][0][i]
            )
        })

    keywords = keyword_scores(repo_path, query)

    for result in semantic_results:
        file_score = keywords.get(result["file"], 0)

        result["keyword_score"] = file_score

        result["final_score"] = (
            0.7 * result["semantic_score"]
            + 0.3 * file_score
        )

    semantic_results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return semantic_results[:top_k]