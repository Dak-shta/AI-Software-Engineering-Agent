# Code Generation and Verification

## Objective

Evaluate whether the AI Software Engineering Agent can generate a code change from a natural-language request, apply the change to the repository, and verify that the modification does not break existing functionality.

---

## Task

The agent was given the following natural-language request:

> Add an email attribute to the User class.

The relevant repository contained a `User` class in:

```text
sample_repo/models.py
```

The original implementation was:

```python
class User:
    def __init__(self, name):
        self.name = name
```

---

## Code Generation

The agent used repository retrieval to identify the relevant code and generated the following proposed modification:

```python
class User:
    def __init__(self, name, email=None):
        self.name = name
        self.email = email
```

The generated change was designed to remain backward compatible because the new `email` parameter defaults to `None`.

---

## Change Application

The generated response was passed through the code-change parser, which extracted:

* Target file
* Proposed code

The file editor then applied the modification to:

```text
sample_repo/models.py
```

The editor also contains safety checks to prevent modification of files outside the repository and prevents modification of `.env`.

---

## Verification

### Baseline

Before introducing the new functionality, the existing test suite contained one test:

```text
1 passed
```

### After AI-generated modification

A new regression test was added to verify the email functionality:

```python
def test_user_email():
    user = User(
        "Alice",
        "alice@example.com"
    )

    assert user.email == "alice@example.com"
```

The complete test suite was then executed using:

```bash
python -m pytest sample_repo/test_models.py
```

Result:

```text
2 passed in 0.16s
```

---

## Results

| Stage                            |   Result |
| -------------------------------- | -------: |
| Baseline tests                   | 1 passed |
| Tests after AI modification      | 2 passed |
| Existing functionality preserved |      Yes |
| New email functionality verified |      Yes |

---

## Observation

The AI-generated modification successfully implemented the requested functionality while preserving the existing behavior of the `User` class.

The use of `email=None` allowed existing code such as:

```python
User("Alice")
```

to continue working without modification.

The additional test verified that:

```python
User("Alice", "alice@example.com")
```

correctly stores the email address.

This demonstrates that code generation alone is not sufficient for a software engineering agent. The generated modification should also be executed and verified through automated testing.

---

## Current Pipeline

The experiment establishes the following pipeline:

```text
Natural-language request
        ↓
Repository retrieval (RAG)
        ↓
LLM code generation
        ↓
Code-change parsing
        ↓
Safe file modification
        ↓
Automated test verification
```

---

## Limitations

The current prototype applies the generated code by replacing the relevant file content rather than generating and applying a precise patch or unified diff.

This approach is acceptable for the prototype but could become unsafe for larger repositories because unrelated changes in a file could potentially be overwritten.

Another limitation is that the verification step is currently triggered manually. The next version will allow the agent to invoke a test-running tool automatically.

---

## Next Step

The next stage is to implement a **Test Runner Tool** that allows the agent to execute repository tests programmatically and inspect:

* Exit status
* Standard output
* Error output
* Failed test names
* Tracebacks

This will enable the agent to move from:

```text
Generate → Apply → Manually Test
```

to:

```text
Generate → Apply → Automatically Test → Analyze Failure
```

which is an important step toward an autonomous software engineering agent.
