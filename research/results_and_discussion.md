# Results and Discussion

## 1. Overview

The AI Software Engineering Agent was evaluated at two complementary levels.

The first experiment evaluated **repository retrieval**, measuring how effectively different retrieval strategies identified relevant source files from natural-language software engineering queries.

The second experiment evaluated **end-to-end autonomous software repair**, measuring whether the agent could inspect a repository, diagnose defects, modify source code, and verify the resulting repair through automated tests.

Together, these experiments evaluate both an important supporting component of the system and the overall agent behavior.

---

## 2. Retrieval Results

Three retrieval strategies were evaluated on 15 manually constructed repository-level queries:

* Keyword retrieval
* Semantic retrieval
* Hybrid retrieval

The results were:

| Retrieval Method | Top-1 Accuracy | Top-3 Accuracy |
| ---------------- | -------------: | -------------: |
| Keyword          |         33.33% |     **80.00%** |
| Semantic         |     **46.67%** |         73.33% |
| Hybrid           |         40.00% |         60.00% |

Semantic retrieval achieved the highest Top-1 accuracy at **46.67%**.

This indicates that semantic representations were more effective than lexical matching at identifying the single most relevant file for the evaluated queries.

However, keyword retrieval achieved the highest Top-3 accuracy at **80.00%**. This suggests that lexical matching can still be useful when multiple candidate files are considered.

The hybrid approach did not outperform the individual approaches. It achieved **40.00% Top-1** and **60.00% Top-3** accuracy.

This result demonstrates that combining retrieval signals does not automatically improve retrieval quality. The effectiveness of a hybrid strategy depends on factors such as score normalization, repository structure, chunking strategy, and query characteristics.

---

## 3. Autonomous Repair Results

The complete agent was evaluated on a controlled benchmark containing six injected software defects.

The benchmark covered several repair categories:

* Incorrect state assignment
* Incorrect return values
* Incorrect conditional logic
* Runtime/edge-case failures
* Incorrect function calls
* Dependency-related incorrect values

The results were:

| Metric                |      Result |
| --------------------- | ----------: |
| Benchmark cases       |       **6** |
| Successful repairs    |     **6/6** |
| Repair success rate   | **100.00%** |
| Final test-pass rate  | **100.00%** |
| Targeted patch usage  | **100.00%** |
| Average agent steps   |    **5.83** |
| Agent completion rate |  **83.33%** |

The agent successfully repaired every benchmark case.

Every successful repair used the targeted `apply_patch` mechanism, indicating that the agent consistently performed constrained modifications rather than replacing complete source files.

The final test-pass rate of 100% also demonstrates that the benchmark evaluator verified the repaired repository state independently through automated testing.

---

## 4. End-to-End Agent Behavior

The observed repair process followed a consistent pattern:

```text
Natural-Language Request
          ↓
Repository Inspection
          ↓
Test Execution
          ↓
Relevant Source Inspection
          ↓
Bug Diagnosis
          ↓
Targeted Patch
          ↓
Test Execution
          ↓
Repair Verification
```

This workflow demonstrates the integration of several components developed throughout the project.

The retrieval system provides repository context, while the ReAct-based agent determines which tools to use.

The test runner provides executable feedback, allowing the agent to observe failures and verify proposed changes.

The patch system constrains modifications to targeted source changes.

Finally, automated tests provide an external verification signal rather than relying solely on the language model's textual claim that a repair was successful.

---

## 5. Retrieval vs. End-to-End Repair

An important finding is the difference between retrieval accuracy and end-to-end repair performance.

Semantic retrieval achieved only **46.67% Top-1 accuracy** on the 15-query retrieval evaluation.

Nevertheless, the complete repair agent achieved **100% repair success** on the six controlled repair cases.

This does not mean that retrieval quality is unimportant.

Instead, the results suggest that an autonomous software engineering agent can compensate for imperfect initial retrieval through additional tool interactions.

For example, the agent can:

* inspect the repository structure,
* execute tests,
* read additional source files,
* observe test failures,
* refine its diagnosis,
* and verify the resulting modification.

Therefore, repository retrieval should not necessarily be evaluated as an isolated predictor of end-to-end repair success.

The experiments suggest that **agentic interaction can provide additional context beyond a single retrieval result**.

---

## 6. Step Budget and Agent Completion

The repair benchmark also exposed a limitation of the current bounded ReAct architecture.

The agent is configured with:

```text
MAX_STEPS = 6
```

One benchmark case, BUG-003, successfully passed all tests but reached the maximum step budget before producing a final completion response.

Consequently:

* Repair success = **100%**
* Agent completion rate = **83.33%**

This distinction is important.

A system can successfully modify and verify a repository even when its conversational execution reaches the configured step limit.

The result suggests that future versions should investigate adaptive step budgets or more efficient tool-selection strategies.

---

## 7. Research Interpretation

The combined experiments provide three main findings.

### Finding 1 — Semantic retrieval provides the strongest Top-1 baseline

Semantic retrieval outperformed keyword and hybrid retrieval on Top-1 accuracy.

This supports the use of semantic representations as the primary retrieval baseline for the current agent.

### Finding 2 — Hybrid retrieval did not automatically improve performance

The hybrid approach performed below semantic retrieval on both reported metrics.

This demonstrates the importance of empirical evaluation when introducing retrieval combinations rather than assuming that additional signals will necessarily improve performance.

### Finding 3 — End-to-end agent behavior can exceed individual component performance

Despite imperfect retrieval accuracy, the complete repair agent successfully repaired all six controlled defects.

This suggests that repository-level software engineering agents should be evaluated not only through individual component metrics but also through end-to-end task completion and executable verification.

---

## 8. Limitations

The results should be interpreted within the scope of the current evaluation.

### Small Retrieval Dataset

Only 15 retrieval queries were evaluated.

### Small Repair Benchmark

Only six software defects were used for autonomous repair evaluation.

### Controlled Defects

The repair cases were manually constructed and are substantially simpler than real-world software engineering issues.

### Limited Repository Scale

The experiments use small Python repositories rather than large production repositories.

### Limited Agent Budget

The agent currently operates with a maximum of six ReAct steps.

### No Large-Scale Real-World Evaluation

The current system has not yet been evaluated across a large real-world benchmark such as the full SWE-bench dataset.

Therefore, the reported 100% repair success rate should be interpreted as a **controlled benchmark result**, not as a general estimate of software-repair capability.

---

## 9. Future Research Directions

The experimental results suggest several directions for future work.

### Retrieval

Future retrieval experiments could investigate:

* AST-aware code chunking
* Function-level retrieval
* Class-level retrieval
* BM25 retrieval
* Reciprocal Rank Fusion
* Query expansion
* Repository-aware reranking

### Agent Architecture

Future agent experiments could investigate:

* Adaptive ReAct step budgets
* More efficient tool selection
* Retrieval ablation
* Different prompting strategies
* Improved failure recovery
* Explicit planning before tool execution

### Software Repair

The repair evaluation could be expanded to:

* Multi-file bugs
* Dependency failures
* Regression bugs
* Larger repositories
* Real GitHub issues
* SWE-bench-style tasks

---

## 10. Overall Conclusion

The combined evaluation demonstrates the feasibility of an AI Software Engineering Agent that integrates repository retrieval, tool-based reasoning, targeted code modification, and automated verification.

The retrieval experiment established a baseline for repository-context selection, with semantic retrieval achieving the strongest Top-1 performance at **46.67%**.

The autonomous repair benchmark demonstrated successful end-to-end repair of **6/6 controlled software defects**, achieving a **100% repair success rate** and **100% final test-pass rate**.

The experiments also revealed meaningful limitations. Hybrid retrieval did not improve upon semantic retrieval, and one successful repair reached the configured agent step limit.

These findings demonstrate that the system is not simply a code-generation interface. It forms an agentic software engineering loop in which the model can inspect a repository, interact with development tools, modify source code, execute tests, and use executable feedback to validate its actions.

The current results provide a controlled baseline for future research on larger repositories, more realistic software defects, improved retrieval strategies, and stronger autonomous software engineering agents.
