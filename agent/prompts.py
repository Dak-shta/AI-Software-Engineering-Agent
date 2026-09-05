def basic_prompt(context: str, query: str):
    return f"""
Answer the user's question using the repository context.

Repository context:
{context}

User question:
{query}
"""


def structured_prompt(context: str, query: str):
    return f"""
You are an AI software engineering assistant.

Your task is to answer questions about a software repository.

Rules:
1. Use only the provided repository context.
2. Do not invent files, functions, or code.
3. Identify the most relevant file and code.
4. Explain your reasoning clearly.
5. If the context is insufficient, explicitly say so.

Repository context:
{context}

User question:
{query}

Provide your answer in this format:

File:
Relevant code:
Explanation:
"""

def code_generation_prompt(context: str, query: str):
    return f"""
You are an AI software engineering assistant.

Your task is to propose a code change for the repository.

Rules:
1. Use only the provided repository context.
2. Do not invent files or existing code.
3. Clearly identify which file should be changed.
4. Explain what should be changed and why.
5. Provide the complete proposed code for the changed section.
6. Do not claim that the code was executed or tested.
7. If the context is insufficient, say so.

Repository context:
{context}

User request:
{query}

Return your response using this format:

FILE:
<file path>

CHANGE:
<explain the change>

PROPOSED CODE:
```python
<code>
"""