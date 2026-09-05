import json

from dotenv import load_dotenv
from groq import Groq

from agent.tools import execute_tool

load_dotenv()

client = Groq()

MAX_STEPS = 4


def run_react_agent(user_request: str):
    history = []

    for step in range(MAX_STEPS):
        print(f"\n========== STEP {step + 1} ==========")

        prompt = f"""
You are an AI software engineering agent.

Your job is to solve the user's request by using repository tools.

Available tools:

1. list_files
   Purpose: List all files inside the repository.
   Arguments:
   {{
       "repo_path": "sample_repo"
   }}

2. search_repository
   Purpose: Semantically search repository code.
   Arguments:
   {{
       "query": "search query",
       "repo_path": "sample_repo",
       "top_k": 3
   }}

3. read_file
   Purpose: Read a specific repository file.
   Arguments:
   {{
       "repo_path": "sample_repo",
       "file_path": "test_models.py"
   }}

4. run_tests
   Purpose: Run pytest tests.
   Arguments:
   {{
       "repo_path": "sample_repo",
       "test_path": "test_models.py"
   }}

Rules:
- Use list_files when you need to discover filenames.
- Use search_repository when you need to find relevant code.
- Use read_file when you need the contents of a known file.
- Use run_tests when the user asks for verification.
- Do not invent filenames.
- Do not claim tests passed unless run_tests actually succeeded.
- Choose exactly ONE tool per step.
- Return ONLY valid JSON.

Format:

{{
    "thought": "brief reasoning",
    "action": "tool_name",
    "arguments": {{
        "repo_path": "sample_repo"
    }}
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

        thought = decision["thought"]
        action = decision["action"]
        arguments = decision["arguments"]

        print("Thought:", thought)
        print("Action:", action)
        print("Arguments:", arguments)

        try:
            observation = execute_tool(
                action,
                **arguments
            )
        except Exception as e:
            observation = {
                "error": str(e)
            }

        print("Observation:", observation)

        history.append({
            "action": action,
            "arguments": arguments,
            "observation": observation
        })

        # If tests succeeded, we can finish without another
        # expensive Groq call.
        if (
            action == "run_tests"
            and isinstance(observation, dict)
            and observation.get("success")
        ):
            print("\nFinal Answer: Repository tests passed successfully.")
            return

    print("\nFinal Answer: The agent reached its maximum number of steps.")


if __name__ == "__main__":
    run_react_agent(
        "Check whether the User model tests pass."
    )