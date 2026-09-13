
import json

from agent.trace_logger import TraceLogger
from dotenv import load_dotenv
from groq import Groq

from agent.tools import execute_tool, TOOL_SCHEMAS


load_dotenv()

client = Groq()

MAX_STEPS = 6


SYSTEM_PROMPT = """
You are an AI software engineering repair agent.

Your job is to diagnose and repair software issues in a repository.

Rules:
1. Use tools to inspect the repository.
2. Always run tests to understand the current state.
3. If tests fail, inspect the relevant source file.
4. Read a file before modifying it.
5. Identify the exact buggy code before making changes.
6. Prefer apply_patch for targeted modifications.
7. Use apply_change only when replacing the entire file is genuinely necessary.
8. When using apply_patch, provide the exact old code and corrected new code.
9. After modifying code, run tests again.
10. Never claim success unless tests actually pass.
11. Do not invent files or repository information.
12. Work step-by-step and use the available tools.
13. Always use the repository path provided by the caller.
"""


def run_repair_agent(
    user_request: str,
    repo_path: str = "sample_repo",
    task_id: str = "unknown_task"
):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_request
        }
    ]

    tools_used = []
    steps_completed = 0
    final_success = False
    failure_reason = None

    trace_logger = TraceLogger(task_id)

    for step in range(MAX_STEPS):

        steps_completed = step + 1

        print(f"\n========== STEP {step + 1} ==========")

        # ---------------------------------
        # LLM CALL
        # ---------------------------------

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                temperature=0,
                max_tokens=500,
            )

        except Exception as e:
            failure_reason = "llm_api_or_tool_call_error"

            print("\nLLM/API ERROR:")
            print(str(e))

            trace_file = trace_logger.save(
                final_success=False,
                total_steps=steps_completed,
                tools_used=tools_used
            )

            return {
                "steps": steps_completed,
                "tools_used": tools_used,
                "agent_completed": False,
                "failure_reason": failure_reason,
                "error": str(e),
                "trace_file": str(trace_file)
            }

        message = response.choices[0].message

        print("Assistant:", message.content)

        # ---------------------------------
        # NO TOOL CALL
        # ---------------------------------

        if not message.tool_calls:

            print("\nFinal Answer:")
            print(message.content)

            final_success = True
            break

        messages.append(message)

        # ---------------------------------
        # TOOL CALLS
        # ---------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            if tool_name not in tools_used:
                tools_used.append(tool_name)

            tool_success = False

            # ---------------------------------
            # Parse tool arguments
            # ---------------------------------

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

                if arguments.get("repo_path") in {
                    "",
                    "/",
                    ".",
                    None
                }:
                    arguments["repo_path"] = repo_path

            except json.JSONDecodeError as e:

                observation = {
                    "error": f"Invalid tool arguments: {e}"
                }

                print("Tool argument error:", observation)

                trace_logger.log_step(
                    step_number=step + 1,
                    tool_name=tool_name,
                    arguments={},
                    observation=observation,
                    success=False
                )

                tool_output = json.dumps(
                    observation,
                    default=str
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output
                    }
                )

                continue

            # ---------------------------------
            # Execute tool
            # ---------------------------------

            print("Tool:", tool_name)
            print("Arguments:", arguments)

            try:

                observation = execute_tool(
                    tool_name,
                    **arguments
                )

                tool_success = True

            except Exception as e:

                observation = {
                    "error": str(e)
                }

                tool_success = False

            print("Observation:", observation)

            # ---------------------------------
            # Trace logging
            # ---------------------------------

            trace_logger.log_step(
                step_number=step + 1,
                tool_name=tool_name,
                arguments=arguments,
                observation=observation,
                success=tool_success
            )

            # ---------------------------------
            # Send tool result back to LLM
            # ---------------------------------

            if isinstance(observation, str):

                tool_output = observation

            else:

                tool_output = json.dumps(
                    observation,
                    default=str
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_output
                }
            )

    # ---------------------------------
    # Save trace
    # ---------------------------------

    if not final_success and failure_reason is None:
        failure_reason = "step_budget_exhausted"

    trace_file = trace_logger.save(
        final_success=final_success,
        total_steps=steps_completed,
        tools_used=tools_used
    )

    return {
        "steps": steps_completed,
        "tools_used": tools_used,
        "agent_completed": final_success,
        "failure_reason": failure_reason,
        "trace_file": str(trace_file)
    }

