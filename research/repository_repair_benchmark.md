# Repository-Level Software Repair Benchmark

## 1. Overview

This experiment evaluates the ability of the AI Software Engineering Agent to diagnose and repair software defects at the repository level.

The agent combines large language model reasoning, repository inspection, retrieval, tool use, code modification, and automated testing. Instead of evaluating code generation in isolation, the benchmark measures whether the agent can identify a defect, modify the appropriate source code, and produce a verified repair.

The experiment uses six deliberately seeded software defects representing different debugging scenarios.

---

## 2. Research Question

The primary research question is:

> How reliably can an LLM-based repository-level software engineering agent identify and repair realistic software defects using repository inspection, tool-based interaction, code modification, and automated test verification?

A secondary question is:

> What types of failures occur when the agent operates under a bounded tool-use and reasoning budget?

---

## 3. Experimental Setup

The benchmark consists of six buggy repository fixtures. Each fixture contains a specific defect together with tests designed to expose the defect.

For every benchmark case, the following procedure is used:

1. Restore the repository fixture to its reproducible buggy baseline.
2. Run the tests before agent execution.
3. Provide the software issue to the AI agent.
4. Allow the agent to inspect repository files using available tools.
5. Allow the agent to modify the defective source code.
6. Run the tests after the repair.
7. Determine repair success based on the final test results.
8. Record the agent's tool usage and execution trace.

The agent operates with a bounded maximum of six interaction steps. This prevents unlimited autonomous execution and makes the experiment reproducible.

---

## 4. Benchmark Cases

| ID      | Defect Type                         | Expected Repair                                                   |
| ------- | ----------------------------------- | ----------------------------------------------------------------- |
| BUG-001 | Email value not stored correctly    | Correct the user creation/storage logic                           |
| BUG-002 | Incorrect total calculation         | Multiply price by quantity                                        |
| BUG-003 | Incorrect member discount           | Apply the expected member discount                                |
| BUG-004 | Incorrect division-by-zero behavior | Return the expected safe result                                   |
| BUG-005 | Undefined function call             | Replace the incorrect function call with the required calculation |
| BUG-006 | Incorrect returned dependency       | Return the user's email instead of the name                       |

The benchmark therefore covers multiple classes of software defects rather than testing the agent on a single type of bug.

---

## 5. Evaluation Metrics

The primary metric is repair success rate.

A repair is considered successful when the test suite executed after the agent's modification passes without failures.

The repair success rate is calculated as:

$$
Repair\ Success\ Rate =
\frac{Successful\ Repairs}{Total\ Benchmark\ Cases}
\times 100
$$

The benchmark also records:

* Tests before repair
* Tests after repair
* Tools used
* Number of agent steps
* Agent completion status
* Execution traces
* Failure information

These additional measurements help distinguish successful repair from unsuccessful or incomplete agent behavior.

---

## 6. Results

The agent successfully repaired five of the six benchmark cases.

| ID      | Result                 | Repair Status |
| ------- | ---------------------- | ------------- |
| BUG-001 | Tests remained failing | Failed        |
| BUG-002 | Tests passed           | Successful    |
| BUG-003 | Tests passed           | Successful    |
| BUG-004 | Tests passed           | Successful    |
| BUG-005 | Tests passed           | Successful    |
| BUG-006 | Tests passed           | Successful    |

Overall:

**Successful repairs: 5/6**

**Repair success rate: 83.3%**

The result demonstrates that the agent was able to perform repository-level diagnosis and modification successfully in the majority of the evaluated cases.

---

## 7. Successful Repair Examples

### BUG-002 — Incorrect Calculation

The initial implementation returned the product price instead of accounting for the requested quantity.

The agent:

1. Inspected the repository.
2. Executed the tests.
3. Read the relevant source file.
4. Identified the incorrect return expression.
5. Applied a targeted patch.
6. Re-ran the tests.

The repaired implementation correctly calculated:

$$
Total = Price \times Quantity
$$

The tests passed after the modification.

---

### BUG-003 — Incorrect Discount Logic

The original implementation did not correctly apply the member discount.

The agent inspected the implementation and modified the member branch to apply the expected discount.

The complete benchmark test suite passed after the repair.

---

### BUG-004 — Division Failure

The original implementation raised an exception when the denominator was zero, while the benchmark expected the safe behavior defined by the test.

The agent identified the relevant conditional branch and modified the behavior accordingly.

Both benchmark tests passed after the repair.

This case demonstrates that the agent was able to modify not only simple arithmetic expressions but also conditional error-handling behavior.

---

### BUG-005 — Undefined Function

The implementation attempted to call an undefined rectangle-area function.

The agent identified the incorrect function call and replaced it with the appropriate calculation:

$$
Area = Length \times Width
$$

The test passed after the modification.

---

### BUG-006 — Incorrect Return Value

The implementation returned a user's name when the required behavior was to return the user's email.

The agent inspected the relevant source code and changed the returned attribute.

The test passed after the repair.

---

## 8. Failure Analysis

### BUG-001

BUG-001 was the only unsuccessful benchmark case.

The agent correctly began repository inspection and identified the relevant fixture, but it did not complete the repair within the six-step interaction budget.

During execution, the agent repeatedly inspected the same file and also attempted to use unsupported arguments with the file-reading tool.

This resulted in the agent exhausting its bounded interaction budget before producing a verified repair.

The failure therefore highlights an important limitation of the current system:

> Successful repository-level repair depends not only on code-generation capability, but also on efficient tool selection and effective use of the available interaction budget.

This failure is particularly useful for research because it identifies a concrete area for improvement rather than simply reporting successful cases.

---

## 9. Tool Usage

The benchmark demonstrates the use of multiple software engineering tools, including:

* `list_files`
* `read_file`
* `search`
* `apply_patch`
* `run_tests`

The successful cases generally followed a workflow similar to:

```text
Repository Inspection
        ↓
Test Execution
        ↓
Source Inspection
        ↓
Bug Identification
        ↓
Targeted Patch
        ↓
Test Execution
        ↓
Verified Repair
```

This workflow reflects the repository-level nature of the agent rather than isolated code completion.

---

## 10. Execution Traces

The benchmark generates structured execution traces for individual tasks.

Each trace records:

* Benchmark task ID
* Agent step number
* Tool used
* Tool arguments
* Tool observation
* Tool success status
* Total execution steps
* Tools used during execution

These traces provide additional evidence for analyzing agent behavior and identifying failure patterns.

The traces are stored in:

```text
evaluation/traces/
```

The benchmark results are stored in:

```text
evaluation/benchmark_results.json
```

---

## 11. Reliability Interpretation

An 83.3% repair success rate indicates that the current agent can successfully repair a majority of the evaluated defects under the defined experimental conditions.

However, the result should not be interpreted as general software engineering accuracy.

The benchmark is intentionally small and uses six controlled repository fixtures. The result is therefore best interpreted as an initial evaluation of the agent's repository-level repair capability.

The experiment also demonstrates why success rate alone is insufficient for evaluating autonomous software engineering systems. Execution traces and failure analysis provide additional information about how and why the agent succeeds or fails.

---

## 12. Limitations

Several limitations should be considered:

1. The benchmark contains only six defect cases.
2. The defects are controlled and relatively small.
3. The benchmark does not represent the full diversity of real-world software repositories.
4. The agent uses a bounded six-step interaction budget.
5. Model behavior may vary across different LLMs.
6. The evaluation does not yet include large-scale benchmarks such as SWE-bench.
7. Tool-interface errors can affect agent performance independently of its underlying debugging capability.

Therefore, the current results should be considered an initial controlled evaluation rather than a comprehensive measure of autonomous software engineering performance.

---

## 13. Future Work

Future experiments can improve the evaluation in several directions:

* Increase the number of repository-level bug cases.
* Add more complex multi-file defects.
* Improve tool argument validation.
* Improve tool-selection strategies.
* Introduce adaptive interaction budgets.
* Compare different retrieval strategies during repair.
* Compare multiple LLMs.
* Evaluate performance on larger public software engineering benchmarks.
* Analyze repair quality in addition to test-based correctness.
* Measure execution cost and number of tool calls.

A particularly important improvement is reducing unnecessary repeated tool calls so that the agent can use its bounded interaction budget more efficiently.

---

## 14. Conclusion

This benchmark provides an initial empirical evaluation of the AI Software Engineering Agent's repository-level repair capability.

Across six controlled software defects, the agent successfully repaired five cases, achieving an overall repair success rate of **83.3%**.

The experiment demonstrates that the combination of LLM reasoning, repository inspection, tool use, targeted code modification, and automated test verification can support effective software repair.

At the same time, the unsuccessful BUG-001 case demonstrates a key limitation: autonomous software engineering performance depends not only on the quality of generated code but also on efficient planning, tool selection, error handling, and interaction-budget management.

The benchmark and execution traces therefore provide a foundation for further research into reliable LLM-based software engineering agents.
