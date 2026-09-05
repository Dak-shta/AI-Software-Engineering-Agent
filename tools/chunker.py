from pathlib import Path


def chunk_code(
    file_path: Path,
    content: str,
    chunk_size: int = 40,
    overlap: int = 10
):
    lines = content.splitlines()

    chunks = []

    start = 0

    while start < len(lines):
        end = start + chunk_size

        chunk = "\n".join(lines[start:end])

        chunks.append({
            "file": str(file_path),
            "start_line": start + 1,
            "end_line": min(end, len(lines)),
            "content": chunk
        })

        start += chunk_size - overlap

    return chunks