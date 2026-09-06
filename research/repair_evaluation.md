# Repair Evaluation

## Objective

The repair evaluation measures whether the AI Software Engineering Agent can autonomously diagnose and repair software defects in a repository.

The evaluation focuses on the agent's ability to:

1. Inspect repository files.
2. Execute tests to identify failures.
3. Locate relevant source code.
4. Diagnose the underlying defect.
5. Apply a targeted patch.
6. Re-run tests to verify the repair.

---

## Experimental Setup

A controlled miniature benchmark containing six injected software bugs was created.

Each benchmark case contains:

* A repository fixture.
* A buggy implementation.
* One or more tests defining the expected behavior.
* A natural-language description of the defect.

The benchmark contains several repair categories:

| Bug     | Repair Type                                  |
| ------- | -------------------------------------------- |
| BUG-001 | Incorrect state assignment                   |
| BUG-002 | Incorrect return value                       |
| BUG-003 | Incorrect conditional/business logic         |
| BUG-004 | Runtime failure / edge-case handling         |
| BUG-005 | Incorrect function call                      |
| BUG-006 | Incorrect value returned across a dependency |

Each fixture was restored to its original broken state before evaluation.

The agent was then executed independently on each benchmark case.

The evaluator recorded the test state before and after the repair.

---

## Evaluation Metrics

### Repair Success

A repair is considered successful when the final benchmark tests pass without failures.

### Final Test-Pass Rate

The percentage of benchmark cases for which all tests pass after the agent's repair.

### Targeted Patch Usage

The percentage of benchmark cases in which the agent used the `apply_patch` tool.

### Agent Steps

The number of ReAct iterations performed by the agent.

The configured maximum was:

```text
MAX_STEPS = 6
```

### Agent Completion Rate

The percentage of benchmark cases for which the agent returned a final completion response before reaching the step limit.

This metric is reported separately from repair success because a repair can succeed even if the agent reaches the configured step limit.

---

## Results

| Bug     |        Tests Before |         Tests After | Steps | Patch Used | Repair  |
| ------- | ------------------: | ------------------: | ----: | ---------- | ------- |
| BUG-001 | 0 passed / 1 failed | 1 passed / 0 failed |     5 | Yes        | Success |
| BUG-002 | 0 passed / 1 failed | 1 passed / 0 failed |     6 | Yes        | Success |
| BUG-003 | 1 passed / 1 failed | 2 passed / 0 failed |     6 | Yes        | Success |
| BUG-004 | 1 passed / 1 failed | 2 passed / 0 failed |     6 | Yes        | Success |
| BUG-005 | 0 passed / 1 failed | 1 passed / 0 failed |     6 | Yes        | Success |
| BUG-006 | 0 passed / 1 failed | 1 passed / 0 failed |     6 | Yes        | Success |

---

## Aggregate Results

The benchmark produced the following results:

| Metric                |      Result |
| --------------------- | ----------: |
| Benchmark cases       |       **6** |
| Successful repairs    |     **6/6** |
| Repair success rate   | **100.00%** |
| Final test-pass rate  | **100.00%** |
| Targeted patch usage  | **100.00%** |
| Average agent steps   |    **5.83** |
| Agent completion rate |  **83.33%** |

The agent therefore successfully repaired every benchmark case while consistently using targeted patches.

---

## Observed Repair Workflow

The typical repair trajectory followed:

```text
Repository Inspection
        ↓
Test Execution
        ↓
Source Inspection
        ↓
Bug Diagnosis
        ↓
Targeted Patch
        ↓
Test Verification
```

The agent used repository tools to inspect files and execute tests before modifying code.

After identifying the defect, the agent generally used `apply_patch` to make a targeted modification rather than replacing an entire file.

The modified repository was then tested again to verify the repair.

---

## Step-Limit Observation

An important observation was identified in BUG-003.

The agent successfully repaired the bug and the final test suite passed:

```text
2 passed / 0 failed
```

However, the agent reached the configured maximum of six ReAct steps before returning a final completion response.

Therefore:

```text
Repair success = True
Agent completion = False
```

This demonstrates that **repair success and agent completion are not equivalent metrics**.

The benchmark evaluator therefore determines repair success from the final repository test state rather than relying exclusively on the agent's textual completion signal.

This is an important limitation of the current bounded-agent configuration.

---

## Interpretation

The results demonstrate that the implemented ReAct-based architecture can perform autonomous repair across several classes of controlled software defects.

The combination of:

* repository inspection,
* test-driven diagnosis,
* tool-based interaction,
* targeted patching,
* and post-repair verification

enabled successful repair of all six benchmark cases.

The **100% repair success rate** demonstrates the feasibility of the implemented architecture on this controlled benchmark.

However, this result should **not** be interpreted as evidence of general software-repair performance.

The benchmark is intentionally small and consists of manually constructed defects that are substantially simpler than real-world repository-level issues.

---

## Relationship to Retrieval Evaluation

The retrieval experiment and repair benchmark evaluate different stages of the system.

The retrieval experiment measures whether relevant repository files are ranked highly for natural-language queries.

The repair benchmark measures the complete agent's ability to use repository information, execute tests, modify code, and verify the resulting implementation.

The retrieval experiment produced:

| Method   |      Top-1 |  Top-3 |
| -------- | ---------: | -----: |
| Keyword  |     33.33% | 80.00% |
| Semantic | **46.67%** | 73.33% |
| Hybrid   |     40.00% | 60.00% |

Despite imperfect retrieval accuracy, the repair agent achieved 6/6 successful repairs.

One possible explanation is that end-to-end repair does not depend exclusively on the first retrieved result. The agent can inspect additional files, execute tests, and use multiple tool interactions to gather the context required for repair.

This highlights the difference between evaluating an individual retrieval component and evaluating complete agent behavior.

---

## Limitations

### 1. Small Benchmark

Only six bugs were evaluated.

The benchmark is therefore insufficient for estimating general software-repair performance.

### 2. Controlled Defects

The bugs were manually constructed and are simpler than many real-world software engineering issues.

### 3. Limited Repository Diversity

The evaluation uses small Python fixtures rather than large production repositories.

### 4. Limited Step Budget

The agent is currently restricted to six ReAct steps.

One successful repair reached this limit.

### 5. No Real-World Issue Benchmark

The current evaluation does not yet measure performance on a large real-world benchmark such as the complete SWE-bench dataset.

### 6. No Statistical Significance Analysis

The benchmark size is too small for meaningful statistical significance testing.

---

## Future Work

Future evaluation should investigate:

1. A larger number of repair instances.
2. Multi-file software defects.
3. Dependency and integration failures.
4. Regression bugs.
5. Larger open-source repositories.
6. Real-world GitHub issues.
7. SWE-bench-style evaluation at larger scale.
8. Different ReAct step budgets.
9. Retrieval ablation experiments.
10. Comparison with alternative agent configurations.

A particularly useful next experiment would be evaluating the relationship between **agent step budget and repair success**, since the current benchmark already identified a successful repair that reached the six-step limit.

---

## Conclusion

The controlled repair benchmark demonstrates that the AI Software Engineering Agent can autonomously perform repository inspection, test-driven diagnosis, targeted code modification, and post-repair verification.

The agent successfully repaired **6 out of 6 benchmark cases**, achieving:

* **100% repair success rate**
* **100% final test-pass rate**
* **100% targeted patch usage**
* **5.83 average agent steps**
* **83.33% agent completion rate**

The results provide an initial empirical validation of the agent architecture.

The benchmark remains intentionally limited, so the results should be interpreted as a controlled proof-of-concept rather than a claim of general software-repair capability.

Future work should evaluate the system on larger, more diverse, and more realistic software engineering tasks.
