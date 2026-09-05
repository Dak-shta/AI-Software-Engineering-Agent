# Agentic Tool Use and ReAct Evaluation

## Objective

The goal of this experiment was to extend the AI Software Engineering Agent from a single-tool workflow into a bounded multi-step agent capable of selecting and executing different repository tools based on the current task.

The agent uses a ReAct-style loop in which the language model selects an action, observes the result, and then decides whether another tool is required.

## Available Tools

The agent currently has four repository tools:

* `list_files` — deterministically lists files in the repository.
* `search_repository` — performs semantic repository search.
* `read_file` — reads a specific repository file.
* `run_tests` — executes pytest tests.

The tools are executed locally by Python, while the Groq-hosted language model is used for action selection.

## Architecture

```text
User Request
     |
     v
LLM Decision
     |
     v
Tool Selection
     |
     v
Local Tool Execution
     |
     v
Observation
     |
     v
LLM Decision
     |
     +----> Another Tool
     |
     +----> Final Answer
```

The loop is bounded by a maximum number of steps to prevent uncontrolled tool execution and unnecessary API usage.

## Experiment

### User Request

> Check whether the User model tests pass.

### Agent Execution

The agent first selected:

```text
Action: list_files
Arguments:
{
    "repo_path": "sample_repo"
}
```

The repository returned:

```text
app.py
models.py
test_models.py
```

The agent then used the observation to identify the test file and selected:

```text
Action: run_tests
Arguments:
{
    "repo_path": "sample_repo",
    "test_path": "test_models.py"
}
```

The test runner returned:

```text
2 passed
```

The agent then terminated with:

```text
Final Answer: Repository tests passed successfully.
```

## Result

The experiment successfully demonstrated bounded multi-step tool use.

The agent was able to:

1. Interpret the user's software engineering request.
2. Determine that repository file discovery was necessary.
3. Select the deterministic `list_files` tool.
4. Use the resulting observation to identify the relevant test file.
5. Select the `run_tests` tool.
6. Execute the tests.
7. Base the final answer on the actual test result.

## Why Deterministic File Listing Was Added

The earlier experiment revealed a limitation of semantic retrieval.

When the agent was asked to discover test files using `search_repository`, semantic retrieval did not reliably identify filenames such as `test_models.py`.

This occurs because semantic retrieval is designed primarily to retrieve code based on meaning, rather than to answer deterministic filesystem questions.

For example:

```text
"What files exist in the repository?"
```

is fundamentally different from:

```text
"Where is code related to user creation?"
```

The first is better handled by deterministic filesystem traversal, while the second can benefit from semantic retrieval.

Therefore, repository navigation was separated into a dedicated deterministic tool.

## Observation

The successful execution demonstrated an important design principle:

> Not every repository operation should be delegated to semantic retrieval or an LLM.

Deterministic operations such as file listing and test execution can be performed locally and reliably.

The LLM should primarily decide **which operation is required**, while deterministic tools should perform the actual operation.

## API and Resource Considerations

The agent uses bounded reasoning steps and a limited output-token budget.

This is particularly important when using a free-tier hosted inference API.

Local operations such as:

* file listing,
* file reading,
* repository traversal,
* test execution

do not require additional model requests.

This allows the system to reserve model calls for tasks that actually require language-model reasoning.

## Limitations

This experiment has several limitations.

### 1. Limited Repository

The experiment was performed on a small sample repository containing only a few Python files.

The behavior may differ substantially on large real-world repositories.

### 2. Prompt-Based Tool Selection

The current implementation asks the model to return JSON describing the selected tool.

This works for the experiment, but native model function/tool calling would provide a more robust interface.

### 3. Limited Error Recovery

The current agent can observe tool errors, but it does not yet automatically diagnose and repair software failures.

### 4. No Code Modification

The current ReAct loop can inspect and test the repository, but it does not yet autonomously apply a code change and verify the result.

### 5. Retrieval Limitations

Semantic retrieval remains imperfect for exact repository navigation and filename discovery.

## Next Step

The next stage is to move from tool selection to autonomous software repair.

The agent should eventually be able to perform a workflow such as:

```text
Understand Task
      |
      v
Inspect Repository
      |
      v
Find Relevant Code
      |
      v
Run Tests
      |
      v
Analyze Failure
      |
      v
Generate Fix
      |
      v
Apply Change
      |
      v
Run Tests Again
      |
      +----> Passed → Finish
      |
      +----> Failed → Diagnose and Repair
```

This will move the project from a repository question-answering agent toward an autonomous software engineering agent.
