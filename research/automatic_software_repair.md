# Automatic Software Repair

## Objective

The objective of this experiment was to extend the AI Software Engineering Agent from repository inspection and test execution to autonomous software repair.

The agent was given a known software issue and was required to diagnose the failure, identify the relevant source code, modify the repository, and verify the repair using automated tests.

## Experimental Setup

The sample repository contained:

* `app.py`
* `models.py`
* `test_models.py`

The `User` model accepted an optional email parameter, but the implementation incorrectly discarded the parameter.

The buggy implementation was:

```python
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = None
```

The test expected the supplied email to be stored.

## Initial Test Result

Before repair, the test suite produced:

```text
1 failed, 1 passed
```

The failing assertion was caused by:

```text
Expected: "alice@example.com"
Actual: None
```

## Agent Workflow

The agent used a bounded ReAct-style workflow.

```text
User Issue
    |
    v
list_files
    |
    v
run_tests
    |
    v
Test Failure
    |
    v
read_file
    |
    v
Diagnose Bug
    |
    v
apply_change
    |
    v
run_tests
    |
    v
Tests Pass
```

## Agent Execution

### Step 1 — Repository Discovery

The agent selected:

```text
list_files
```

and discovered:

```text
app.py
models.py
test_models.py
```

### Step 2 — Failure Detection

The agent selected:

```text
run_tests
```

The result was:

```text
1 failed, 1 passed
```

The failing test was:

```text
test_user_email
```

### Step 3 — Source Inspection

The agent selected:

```text
read_file
```

and retrieved:

```python
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = None
```

The agent correctly identified that the constructor ignored the supplied `email` argument.

### Step 4 — Repair

The agent selected:

```text
apply_change
```

and generated the corrected implementation:

```python
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email
```

The repository was modified using the safe file editor.

### Step 5 — Verification

The agent selected:

```text
run_tests
```

again.

The final result was:

```text
2 passed
```

The agent therefore concluded:

```text
The issue was repaired and all tests pass.
```

## Result

The experiment successfully demonstrated autonomous software repair.

The agent independently:

1. Discovered repository files.
2. Executed the test suite.
3. Interpreted a test failure.
4. Inspected the relevant source file.
5. Diagnosed the implementation error.
6. Generated a corrective code change.
7. Applied the change.
8. Re-executed the tests.
9. Verified that the repair succeeded.

## Significance

This experiment demonstrates a transition from passive code assistance to an agentic software engineering workflow.

The LLM was responsible for deciding which operation should be performed next, while deterministic Python tools performed repository operations and testing.

This separation provides a useful architecture:

```text
LLM = reasoning and action selection

Tools = deterministic execution
```

The test suite acts as an external verification mechanism rather than relying solely on the language model's claim that a generated fix is correct.

## Limitations

This experiment was performed on a small synthetic repository containing a single controlled bug.

The experiment therefore does not establish that the approach generalizes to large real-world repositories.

Additional limitations include:

* whole-file replacement rather than patch-based modification;
* limited repair iterations;
* no rollback mechanism;
* limited benchmark size;
* prompt-based rather than native function calling;
* no evaluation across diverse repositories.

## Next Step

The next stage is to replace prompt-based tool selection with native function/tool calling and introduce a safer patch-based modification mechanism.

The resulting system will then be evaluated on multiple software repair tasks using quantitative metrics such as repair success rate, test pass rate, tool calls, and repair iterations.
