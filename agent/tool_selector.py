import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def select_tool(user_request: str):
    client = Groq()

    prompt = f"""
You are a software engineering agent.

Choose the best tool for the user's request.

Available tools:
1. run_tests
   - Runs pytest tests in the repository.

Return ONLY valid JSON.

Format:
{{
    "tool": "run_tests",
    "arguments": {{
        "repo_path": "sample_repo",
        "test_path": "test_models.py"
    }}
}}

User request:
{user_request}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)