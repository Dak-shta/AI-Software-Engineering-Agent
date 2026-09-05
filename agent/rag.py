from agent.llm import ask_llm
from agent.prompts import structured_prompt
from tools.vector_store import search_repository


def answer_question(query: str, top_k: int = 3):
    results = search_repository(
        query,
        top_k=top_k
    )

    if not results:
        return "No relevant code found."

    context_parts = []

    for result in results:
        context_parts.append(
            f"""
FILE: {result["file"]}
LINES: {result["start_line"]}-{result["end_line"]}

CODE:
{result["content"]}
"""
        )

    context = "\n".join(context_parts)

    prompt = structured_prompt(
    context,
    query
)

    return ask_llm(prompt)