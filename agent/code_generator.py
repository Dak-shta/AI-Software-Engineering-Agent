from agent.llm import ask_llm
from agent.prompts import code_generation_prompt
from tools.vector_store import search_repository


def generate_code_change(query: str, top_k: int = 3):
    results = search_repository(
        query,
        top_k=top_k
    )

    if not results:
        return "No relevant repository code found."

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

    prompt = code_generation_prompt(
        context,
        query
    )

    return ask_llm(prompt)