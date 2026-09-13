
import json


from agent.trace_logger import TraceLogger
from dotenv import load_dotenv
from groq import Groq

from agent.tools import execute_tool, TOOL_SCHEMAS


load_dotenv()

client = Groq()

MAX_STEPS = 8


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
14. When the task involves refactoring, existing changes, commits, or pull-request-style analysis, inspect pr_context first.
15. For pull-request analysis, prioritize changed files and their associated tests.
16. Do not inspect the implementation of repository tools unless necessary to understand the changed code.
17. For analysis-only requests, do not modify files.
18. After gathering sufficient information, provide the requested structured review instead of continuing unnecessary repository exploration.
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

        # ---------------------------------
# NO TOOL CALL
# ---------------------------------

        if not message.tool_calls:
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
                if tool_name == "pr_context":
                    arguments["repo_path"] = repo_path
                elif "repo_path" in arguments:
                    arguments["repo_path"] = repo_path

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

                observation = execute_tool(tool_name, **arguments)

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

def run_pr_review(user_request: str, repo_path: str, task_id: str = "pr_review"):
    """
    Run a read-only pull-request review.

    The reviewer can inspect repository context, changed files,
    and tests, but cannot modify files.
    """

    PR_REVIEW_PROMPT = """
You are a read-only pull-request reviewer.

Your task is to analyze the current repository changes.

Rules:
1. Start with pr_context.
2. Identify the relevant changed source files and associated tests.
3. Read the relevant changed source file.
4. Read its associated test file.
5. Do not modify any files.
6. Do not use apply_change or apply_patch.
7. Do not create missing files or fix repository configuration.
8. Ignore unrelated implementation details unless they directly affect the reviewed changes.
9. Do not inspect the implementation of repository tools unless necessary.
10. After gathering sufficient information, stop exploring.
11. Produce a structured review containing:
   - Change Summary
   - Tests
   - Potential Issues
   - Recommendations
"""

    messages = [
        {
            "role": "system",
            "content": PR_REVIEW_PROMPT
        },
        {
            "role": "user",
            "content": user_request
        }
    ]

    # ---------------------------------
    # READ-ONLY TOOLS
    # ---------------------------------

    read_only_tools = [
        tool
        for tool in TOOL_SCHEMAS
        if tool["function"]["name"] in [
            "pr_context",
            "read_file",
            "list_files",
            "git_status",
            "git_diff",
            "run_tests"
        ]
    ]

    trace_logger = TraceLogger(task_id)

    tools_used = []
    steps_completed = 0

    # ---------------------------------
    # REVIEW LOOP
    # ---------------------------------

    for step in range(1, 7):

        steps_completed = step

        print(
            f"\n========== PR REVIEW STEP {step} =========="
        )

        try:

            # ---------------------------------
            # LLM CALL
            # ---------------------------------

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=read_only_tools,
                tool_choice="auto",
                temperature=0,
                max_tokens=500,
            )

            message = response.choices[0].message

            print(
                "Assistant:",
                message.content
            )

            # ---------------------------------
            # FINAL REVIEW
            # ---------------------------------

            if not message.tool_calls:

                review = message.content or ""

                # If LLM returned an empty response,
                # explicitly ask for the final review.
                if not review.strip():

                    messages.append(
                        {
                            "role": "user",
                            "content": (
                                "You have enough information from the "
                                "repository context. Now provide the "
                                "final PR review. Do not call another "
                                "tool. Use exactly these sections:\n"
                                "1. Change Summary\n"
                                "2. Tests\n"
                                "3. Potential Issues\n"
                                "4. Recommendations"
                            )
                        }
                    )

                    continue

                print("\nFinal PR Review:")
                print(review)

                trace_file = trace_logger.save(
                    final_success=True,
                    total_steps=steps_completed,
                    tools_used=tools_used
                )

                return {
                    "steps": steps_completed,
                    "tools_used": tools_used,
                    "agent_completed": True,
                    "review": review,
                    "trace_file": str(trace_file)
                }

            # ---------------------------------
            # SAVE ASSISTANT TOOL CALL MESSAGE
            # ---------------------------------

            messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments
                            }
                        }
                        for call in message.tool_calls
                    ]
                }
            )

            # ---------------------------------
            # TOOL CALLS
            # ---------------------------------

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name

                if tool_name not in tools_used:
                    tools_used.append(tool_name)

                # ---------------------------------
                # PARSE ARGUMENTS
                # ---------------------------------

                try:

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    # Always force the actual repository path.
                    arguments["repo_path"] = repo_path

                except json.JSONDecodeError as e:

                    observation = {
                        "error": f"Invalid tool arguments: {e}"
                    }

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(observation)
                        }
                    )

                    continue

                print(
                    "Tool:",
                    tool_name
                )

                print(
                    "Arguments:",
                    arguments
                )

                # ---------------------------------
                # EXECUTE READ-ONLY TOOL
                # ---------------------------------

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

                print(
                    "Observation:",
                    observation
                )

                # ---------------------------------
                # TRACE
                # ---------------------------------

                trace_logger.log_step(
                    step_number=step,
                    tool_name=tool_name,
                    arguments=arguments,
                    observation=observation,
                    success=tool_success
                )

                # ---------------------------------
                # RETURN TOOL RESULT TO LLM
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
        # ERROR HANDLING
        # ---------------------------------

        except Exception as e:

            print(
                "PR REVIEW ERROR:",
                e
            )

            trace_file = trace_logger.save(
                final_success=False,
                total_steps=steps_completed,
                tools_used=tools_used
            )

            return {
                "steps": steps_completed,
                "tools_used": tools_used,
                "agent_completed": False,
                "failure_reason": "llm_api_or_tool_call_error",
                "error": str(e),
                "trace_file": str(trace_file)
            }

    # ---------------------------------
    # STEP BUDGET EXHAUSTED
    # ---------------------------------

    trace_file = trace_logger.save(
        final_success=False,
        total_steps=steps_completed,
        tools_used=tools_used
    )

    return {
        "steps": steps_completed,
        "tools_used": tools_used,
        "agent_completed": False,
        "failure_reason": "step_budget_exhausted",
        "trace_file": str(trace_file)
    }