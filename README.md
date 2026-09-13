# AI Software Engineering Agent

An AI-powered software engineering agent for **repository-level code understanding, debugging, automated repair, verification, Git-aware analysis, pull-request analysis, and controlled refactoring evaluation**.

The system combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), semantic code retrieval, ReAct-style reasoning, tool calling, targeted patching, Git-aware analysis, and automated testing** to investigate software engineering tasks over an existing codebase.

---

## Research Goal

This project investigates how LLM-based agents can move beyond isolated code generation toward **repository-level software engineering**.

Instead of generating code without repository context, the agent is designed to:

* Understand an existing repository
* Inspect repository structure and source files
* Retrieve relevant code context
* Identify software defects
* Select and execute development tools
* Generate targeted code modifications
* Apply patches to source files
* Run automated tests
* Verify whether a repair succeeds
* Inspect Git status and repository changes
* Analyze existing changes in a pull-request-style workflow
* Evaluate controlled software refactoring while preserving tested behavior

The project investigates both the **capabilities and limitations of LLM-based software engineering agents** through controlled, reproducible experiments.

---

# System Architecture

```text
                       User Request
                            │
                            ▼
                    ┌───────────────┐
                    │   LLM Agent   │
                    │  ReAct Loop   │
                    └───────┬───────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Tool Selection  │
                   └────────┬────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
    Repository         Retrieval          Testing
    Inspection          / RAG             / Pytest
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Bug Diagnosis │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Targeted Patch│
                    └───────┬───────┘
                            │
                            ▼
                        Run Tests
                            │
                      ┌─────┴─────┐
                      │           │
                   Failed       Passed
                      │           │
                      ▼           ▼
                   Iterate    Verified
```

For Git-aware and pull-request-style tasks, the workflow can additionally inspect:

```text
Git Status → Git Diff → Changed Files → Relevant Tests → Structured Analysis
```

---

# Key Components

## Repository Understanding

The agent can inspect repository structure and read relevant source files before modifying code.

This enables software-engineering tasks to be performed with awareness of the surrounding repository rather than treating individual code snippets in isolation.

## Semantic Retrieval

Repository code is chunked and embedded using:

```text
all-MiniLM-L6-v2
```

The embeddings are stored and queried using **ChromaDB**.

## Retrieval-Augmented Generation

Retrieved repository context can be supplied to the language model to support repository-aware reasoning about software engineering tasks.

The project evaluates multiple retrieval strategies rather than assuming that semantic retrieval is always optimal.

## ReAct Agent

The agent follows an iterative tool-use workflow:

```text
Observe → Select Tool → Execute → Observe → Reason → Act
```

The agent operates under a bounded execution budget to prevent uncontrolled tool execution.

The current configured maximum is:

```text
MAX_STEPS = 8
```

## Tool Calling

The agent can use tools for:

* Repository inspection
* File listing
* File reading
* Repository search
* Semantic retrieval
* Code modification
* Targeted patch application
* Test execution
* Git status inspection
* Git diff inspection
* Pull-request-style context analysis

## Targeted Code Modification

The system supports patch-based modification for targeted changes rather than relying exclusively on unrestricted file replacement.

The patch workflow uses explicit old/new code regions to reduce unintended modifications.

## Automated Verification

After modification, the agent executes tests and uses the resulting test status as an external verification signal.

The system does not treat an LLM-generated claim of success as sufficient evidence of a successful repair.

---

# Research Evaluations

The project currently contains four major evaluation areas:

1. **Retrieval Evaluation**
2. **Autonomous Repository Repair Evaluation**
3. **Git-Aware and Pull-Request Analysis**
4. **Controlled Software Refactoring Evaluation**

---

# 1. Retrieval Evaluation

Three repository retrieval strategies were compared using **15 natural-language queries**.

| Method   | Top-1 Accuracy | Top-3 Accuracy |
| -------- | -------------: | -------------: |
| Keyword  |         33.33% |     **80.00%** |
| Semantic |     **46.67%** |         73.33% |
| Hybrid   |         40.00% |         60.00% |

## Findings

* Semantic retrieval achieved the strongest **Top-1 accuracy (46.67%)**.
* Keyword retrieval achieved the strongest **Top-3 accuracy (80.00%)**.
* The hybrid approach did not outperform the individual retrieval strategies on this evaluation set.

This demonstrates that combining retrieval signals does not automatically improve retrieval quality and motivates further investigation into:

* Code-aware chunking
* Retrieval reranking
* Function-level retrieval
* Class-level retrieval
* Improved hybrid strategies

---

# 2. Autonomous Repository Repair Evaluation

A controlled benchmark containing **six injected software defects** was used to evaluate end-to-end repository-level repair.

The benchmark includes different defect categories:

* Incorrect state assignment
* Incorrect return values
* Incorrect conditional logic
* Runtime/edge-case failure
* Incorrect function call
* Incorrect dependency-related value

## Results

| Metric              |    Result |
| ------------------- | --------: |
| Benchmark cases     |     **6** |
| Successful repairs  |   **5/6** |
| Repair success rate | **83.3%** |
| Failed repairs      |   **1/6** |
| Maximum agent steps |     **8** |

The repair success rate is calculated from the final automated test results after each repair.

```text
Repair Success Rate = Successful Repairs / Total Cases × 100
                     = 5 / 6 × 100
                     = 83.3%
```

The benchmark results are stored in:

```text
evaluation/benchmark_results.json
```

Detailed execution traces are stored in:

```text
evaluation/traces/
```

## Failure Analysis

### BUG-001

BUG-001 was the only unsuccessful benchmark case.

The agent began repository inspection and identified the relevant fixture, but did not complete the repair within the bounded interaction budget.

The failure illustrates an important research observation:

> Repository-level repair performance depends not only on code-generation capability, but also on efficient tool selection, tool-interface reliability, and effective management of the agent's interaction budget.

The failed case therefore provides useful evidence about limitations in agentic software-engineering workflows rather than simply representing an unsuccessful test.

---

# 3. Git-Aware Software Engineering

The project was extended beyond isolated repair tasks to include **Git-aware repository analysis**.

The agent can inspect:

* Current Git status
* Working-tree changes
* Repository diffs
* Changed source files
* Relevant tests

The Git-aware workflow provides repository context for tasks involving existing modifications, refactoring, and pull-request-style analysis.

The relevant tools include:

```text
git_status
git_diff
pr_context
```

This extension allows the agent to reason about **what has changed in a repository**, rather than only analyzing the repository's current source files.

---

# 4. Pull-Request Analysis

A read-only pull-request-style analysis workflow was evaluated using a controlled repository change.

The workflow included:

1. Inspecting the current repository context
2. Identifying changed files
3. Reading the modified source code
4. Inspecting the associated tests
5. Analyzing the change
6. Producing a structured review

The analysis was intentionally **read-only** and did not modify the repository.

This extends the project from autonomous repair toward broader **AI-assisted software engineering workflows**, including code review and change analysis.

---

# 5. Controlled Software Refactoring Evaluation

A separate controlled experiment evaluates whether software structure can be improved while preserving tested behavior.

## Objective

The experiment focuses on removing duplicated order-total calculation logic from a small repository-level example.

The original implementation contained duplicated logic in:

```text
calculate_order_total()
calculate_order_total_with_discount()
```

Both functions independently calculated item totals.

## Refactoring

The duplicated calculation logic was extracted into a shared helper:

```python
_calculate_items_total(items)
```

The two public functions were then simplified to reuse this helper.

The external behavior of the public functions was preserved.

## Behavioral Verification

Four tests were used:

1. Normal order-total calculation
2. Zero-quantity handling
3. Discount calculation
4. Zero-discount behavior

Result:

```text
4 passed in 0.70s
```

Therefore:

```text
Behavioral tests passed: 4/4
```

The experiment provides evidence that the tested behavior was preserved after the structural refactoring.

### Important Research Scope

This is a **controlled refactoring evaluation**, not a claim that the LLM autonomously completed the refactoring.

The experiment is included to evaluate software-engineering workflow and behavioral preservation while keeping the evaluation reproducible and clearly scoped.

Detailed documentation is available at:

```text
research/automated_refactoring.md
```

---

# Agent Execution Traces

The repair benchmark generates structured execution traces for each task.

Each trace records information such as:

* Task ID
* Agent step number
* Tool used
* Tool arguments
* Tool observations
* Tool success status
* Total execution steps
* Tools used during execution

The traces provide additional evidence for analyzing how the agent behaves during successful and unsuccessful repairs.

Location:

```text
evaluation/traces/
```

---

# Research Findings

## 1. Semantic retrieval provides the strongest Top-1 baseline

Semantic retrieval achieved **46.67% Top-1 accuracy**, outperforming keyword and hybrid retrieval on the evaluated query set.

## 2. More retrieval signals do not guarantee better retrieval

The hybrid strategy performed below the individual semantic and keyword approaches in this experiment.

This demonstrates why retrieval strategies should be evaluated empirically rather than assuming that combining multiple signals will automatically improve performance.

## 3. Repository inspection complements imperfect retrieval

The retrieval experiment produced imperfect results, while the repair agent successfully repaired most benchmark cases.

This suggests that repository-level agents can obtain additional context through:

* File inspection
* Search
* Test execution
* Tool interaction
* Iterative reasoning
* Post-repair verification

## 4. Executable verification is important

The system does not rely solely on the language model's claim that a repair is correct.

Instead, the modified repository is tested after the repair.

This provides an external verification signal and makes the evaluation more reproducible.

## 5. Bounded reasoning introduces a measurable trade-off

A bounded execution budget improves reproducibility and prevents uncontrolled tool execution.

However, unsuccessful benchmark cases demonstrate that inefficient tool use can prevent an agent from completing a repair even when the underlying defect may be repairable.

This motivates future investigation into:

* Adaptive execution budgets
* Improved tool selection
* Tool argument validation
* More efficient repository exploration

## 6. Structural refactoring can be evaluated through behavioral preservation

The controlled refactoring experiment demonstrates a complementary evaluation principle:

```text
Existing Structure
       ↓
Structural Refactoring
       ↓
Behavioral Tests
       ↓
4/4 Tests Passed
```

The important criterion is not simply whether code becomes shorter, but whether the tested externally observable behavior remains correct.

---

# Limitations

The current results should be interpreted as a **controlled research prototype evaluation**, rather than a general measure of autonomous software engineering capability.

### Small Evaluation Sets

The retrieval evaluation contains 15 queries and the repair benchmark contains six defects.

### Controlled Defects

The benchmark defects are manually constructed and are smaller than many real-world software engineering issues.

### Limited Repository Scale

The current experiments primarily use small Python repositories rather than large production-scale codebases.

### Bounded Agent Execution

The current agent uses:

```text
MAX_STEPS = 8
```

The execution budget can affect whether the agent completes more complex tasks.

### Controlled Refactoring Experiment

The refactoring evaluation uses a small controlled example and a limited behavioral test suite.

Passing the tests does not constitute formal proof of semantic equivalence for every possible input.

### No Large-Scale Real-World Benchmark

The current system has not been evaluated on the full SWE-bench dataset or another large-scale production benchmark.

---

# Future Work

Potential research directions include:

* AST-aware code chunking
* Function-level and class-level retrieval
* BM25-based retrieval
* Improved hybrid retrieval
* Retrieval reranking
* Adaptive ReAct execution budgets
* Improved tool selection
* Tool argument validation
* Multi-file software repair
* Regression bug evaluation
* Larger open-source repositories
* Real GitHub issue evaluation
* Larger SWE-bench-style experiments
* Automated refactoring on larger repositories
* Behavioral and regression-based refactoring evaluation

---

# Repository Structure

```text
ai-sw-agent/
│
├── agent/
│   ├── llm.py
│   ├── rag.py
│   ├── prompts.py
│   ├── code_generator.py
│   ├── apply_change.py
│   ├── tools.py
│   ├── tool_selector.py
│   ├── react_agent.py
│   └── trace_logger.py
│
├── evaluation/
│   ├── benchmark.py
│   ├── benchmark_runner.py
│   ├── benchmark_results.json
│   └── traces/
│
├── research/
│   ├── retrieval_evaluation.md
│   ├── prompt_engineering.md
│   ├── code_generation_and_verification.md
│   ├── agentic_tool_use.md
│   ├── repository_repair_benchmark.md
│   ├── automatic_software_repair.md
│   ├── repair_evaluation.md
│   ├── results_and_discussion.md
│   ├── git_aware_software_engineering.md
│   ├── pr_analysis.md
│   └── automated_refactoring.md
│
├── sample_repo/
│   ├── refactoring_example.py
│   └── ...
│
├── tests/
│   ├── test_refactoring_example.py
│   └── ...
│
├── tools/
│   ├── git_tools.py
│   ├── git_status.py
│   ├── pr_context.py
│   ├── patch_editor.py
│   └── ...
│
├── vectorstore/
│
├── main.py
├── requirements.txt
└── .gitignore
```

---

# Technologies

* **Python**
* **Large Language Models**
* **Groq API**
* **Retrieval-Augmented Generation**
* **Sentence Transformers**
* **ChromaDB**
* **ReAct**
* **Tool Calling**
* **Pytest**
* **Git**
* **GitHub**

---

# Research Documentation

The `research/` directory contains technical documentation and experimental analysis covering:

* Retrieval evaluation
* Prompt engineering
* Code generation and verification
* Agentic tool use
* Repository-level software repair
* Automatic software repair
* Repair evaluation
* Experimental results and discussion
* Git-aware software engineering
* Pull-request analysis
* Controlled software refactoring

Important research artifacts include:

```text
research/repository_repair_benchmark.md
research/retrieval_evaluation.md
research/git_aware_software_engineering.md
research/pr_analysis.md
research/automated_refactoring.md
```

---

# Reproducibility

The project maintains reproducible benchmark fixtures, experiments, tests, and execution traces.

The repair benchmark pipeline:

1. Restores each buggy fixture
2. Runs baseline tests
3. Executes the repair agent
4. Runs post-repair tests
5. Records the outcome
6. Saves benchmark results and execution traces

The controlled refactoring evaluation can be reproduced using:

```powershell
$env:PYTHONPATH = "."
pytest tests\test_refactoring_example.py
```

Expected result:

```text
4 passed
```

The repository therefore contains both quantitative benchmark results and supporting execution artifacts rather than relying only on qualitative demonstrations.

---

# Project Status

**Research Prototype — Controlled Evaluation Complete**

The project currently includes:

* Repository-level LLM agent architecture
* Retrieval-Augmented Generation
* Keyword, semantic, and hybrid retrieval evaluation
* ReAct-style tool use
* Autonomous repository repair benchmark
* **83.3% repair success rate on the controlled six-case benchmark**
* Automated test-based verification
* Structured agent execution traces
* Git status and diff analysis
* Pull-request-style read-only analysis
* Controlled software refactoring evaluation
* **4/4 behavioral tests passing after refactoring**
* Research documentation
* Reproducible benchmark fixtures
* Research paper

The project is now considered **feature-complete for the current research scope**.

Future work is identified as research direction rather than part of the current implementation.

---

# Disclaimer

The reported **83.3% repair success rate** is based on a small, controlled benchmark containing six manually constructed software defects.

The **4/4 refactoring result** is based on a small controlled example and its associated behavioral tests.

Neither result should be interpreted as a general measure of autonomous software engineering capability.

The purpose of this project is to investigate the architecture, behavior, strengths, limitations, and evaluation of LLM-based software engineering agents through controlled and reproducible experiments.
