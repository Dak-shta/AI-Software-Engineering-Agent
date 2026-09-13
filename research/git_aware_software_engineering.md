# Git-Aware Software Engineering Agent

## Objective

The software engineering agent was extended with Git-diff awareness to enable repository-level reasoning about existing code changes.

The motivation is to move beyond isolated bug repair and allow the agent to inspect the current state of a repository before performing refactoring, debugging, or pull-request-style analysis.

## Motivation

Software engineering tasks frequently involve understanding changes that have already been introduced into a repository.

A repository-level agent should therefore be able to:

- identify modified files
- inspect the exact code changes
- reason about the impact of those changes
- use the changes as context before proposing further modifications
- verify modifications using automated tests

The `git_diff` tool provides the agent with read-only access to the current uncommitted Git changes.

## Implementation

A new tool was implemented:

```text
tools/git_tools.py
The tool executes:

git diff

inside the supplied repository and returns:

success status
return code
diff output
error output

The tool was registered in:

agent/tools.py

and exposed to the LLM through the agent's tool schema.

The system prompt was also extended with a rule requiring the agent to inspect git_diff when a task involves:

refactoring
existing changes
commits
pull-request-style analysis
Experimental Verification

The tool was tested independently before being integrated into the agent workflow.

A controlled repository modification was introduced and inspected using git_diff.

The tool successfully returned the corresponding Git diff, demonstrating that the agent can access the exact textual representation of repository changes.

The tool was also tested through:

execute_tool("git_diff", repo_path=...)

and returned:

success: True
returncode: 0

with the detected repository changes in the diff output.

Research Significance

Git awareness extends the agent from basic repository-level repair toward broader software engineering tasks.

The capability provides a foundation for future experiments involving:

automated pull-request analysis
change-impact analysis
LLM-based refactoring
repository quality assessment
automated review comments
change-aware test selection

This extension is particularly relevant to research on AI-assisted software development and autonomous software engineering agents.

Limitations

The current implementation only provides the raw uncommitted Git diff.

It does not yet:

understand the semantic meaning of a change
analyze commit history
inspect pull requests
generate review comments
automatically determine whether a change is correct
perform change-impact analysis

These capabilities are reserved for future extensions.

Future Work

The next stage is to build a change-analysis layer on top of git_diff.

The agent could analyze a Git diff and generate a structured report containing:

changed files
changed functions
potential defects
affected tests
code-quality concerns
suggested improvements
recommended additional tests

This would transform Git-diff retrieval into an actual Git-aware software engineering capability.


### Step 8 — Add it to Git

Run:

```powershell
git add research\git_aware_software_engineering.md

Then:

git commit -m "Document Git-aware software engineering extension"

Then:

git push origin main
'''