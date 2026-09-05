import json

from dotenv import load_dotenv
from groq import Groq

from agent.tools import execute_tool

load_dotenv()

client = Groq()

MAX_STEPS = 5


def run_repair_agent(user_request: str):
    history = []

    for step in range(MAX_STEPS):
        print(f"\n========== STEP {step + 1} ==========")

        prompt = f"""
You are an AI software engineering repair agent.

Your goal is to solve the user's software issue by using repository tools.

Available tools:

1. list_files
Arguments:
{{
    "repo_path": "sample_repo"
}}

2. search_repository
Arguments:
{{
    "query": "search query",
    "repo_path": "sample_repo",
    "top_k": 3
}}

3. read_file
Arguments:
{{
    "repo_path": "sample_repo",
    "file_path": "models.py"
}}

4. run_tests
Arguments:
{{
    "repo_path": "sample_repo",
    "test_path": "test_models.py"
}}

5. apply_change
Arguments:
{{
    "repo_path": "sample_repo",
    "file_path": "models.py",
    "code": "complete replacement file contents"
}}

Rules:
- Use run_tests to verify the current state.
- If tests fail, inspect the failure and relevant source code.
- Use read_file before modifying a file.
- Use apply_change only when you have identified the bug.
- After applying a change, run the tests again.
- Never claim success unless tests actually pass.
- Do not invent files.
- Choose exactly ONE tool.
- Return ONLY valid JSON.

JSON format:

{{
    "thought": "brief reasoning",
    "action": "tool_name",
    "arguments": {{}}
}}

User request:
{user_request}

Previous observations:
{history}
"""

        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=300,
            response_format={"type": "json_object"},
        )

        decision = json.loads(
            response.choices[0].message.content
        )

        print("Thought:", decision["thought"])
        print("Action:", decision["action"])
        print("Arguments:", decision["arguments"])

        try:
            observation = execute_tool(
                decision["action"],
                **decision["arguments"]
            )
        except Exception as e:
            observation = {
                "error": str(e)
            }

        print("Observation:", observation)

        history.append({
            "action": decision["action"],
            "arguments": decision["arguments"],
            "observation": observation
        })

        if (
            decision["action"] == "run_tests"
            and isinstance(observation, dict)
            and observation.get("success")
        ):
            print("\nFinal Answer: The issue was repaired and all tests pass.")
            return

    print("\nFinal Answer: Repair attempt reached the maximum step limit.")


if __name__ == "__main__":
    run_repair_agent(
        "The User email is not being stored correctly. "
        "Find and repair the bug, then verify the fix with tests."
    )