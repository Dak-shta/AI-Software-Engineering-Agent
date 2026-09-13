# AI Software Engineering Agent

An AI-powered software engineering agent for **repository-level code understanding, debugging, automated repair, and verification**.

The system combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), semantic code retrieval, ReAct-style reasoning, tool calling, targeted patching, and automated testing** to perform software engineering tasks over an existing codebase.

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
* Run automated tests
* Verify whether the repair actually succeeds

The project also investigates the **effectiveness of different code retrieval strategies and the limitations of bounded agentic reasoning** through controlled experiments.

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
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        Repository      Retrieval      Testing
        Inspection       / RAG        / Pytest
              │             │             │
              └─────────────┼─────────────┘
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
                   Failed      Passed
                      │           │
                      ▼           ▼
                   Iterate    Verified
```

---

# Key Components

## Repository Understanding

The agent can inspect repository structure and read relevant source files before modifying code.

## Semantic Retrieval

Repository code is chunked and embedded using:

```text
all-MiniLM-L6-v2
```

The embeddings are stored and queried using **ChromaDB**.

## Retrieval-Augmented Generation

Retrieved repository context can be supplied to the language model to support repository-aware reasoning about software engineering tasks.

## ReAct Agent

The agent follows an iterative tool-use workflow:

```text
Observe → Select Tool → Execute → Observe → Reason → Act
```

The agent uses a bounded execution budget to prevent uncontrolled tool execution.

## Tool Calling

The agent can use tools for:

* Repository inspection
* File listing
* File reading
* Repository search
* Code modification
* Patch application
* Test execution

## Targeted Code Modification

The system uses patch-based modification for targeted changes rather than relying exclusively on unrestricted file replacement.

## Automated Verification

After modification, the agent executes tests and uses the resulting test status as an external verification signal.

---

# Research Experiments

The project currently contains two primary evaluations:

1. **Retrieval Evaluation**
2. **Autonomous Repository Repair Evaluation**

---

# 1. Retrieval Evaluation

Three repository retrieval strategies were compared using **15 natural-language queries**.

| Method   | Top-1 Accuracy | Top-3 Accuracy |
| -------- | -------------: | -------------: |
| Keyword  |         33.33% |     **80.00%** |
| Semantic |     **46.67%** |         73.33% |
| Hybrid   |         40.00% |         60.00% |

### Findings

* Semantic retrieval achieved the strongest **Top-1 accuracy (46.67%)**.
* Keyword retrieval achieved the strongest **Top-3 accuracy (80.00%)**.
* The hybrid approach did not outperform the individual retrieval strategies on this evaluation set.

This demonstrates that combining retrieval signals does not automatically improve retrieval quality and motivates future investigation into **code-aware chunking, reranking, and retrieval strategies**.

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
| Maximum agent steps |     **6** |

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

---

# Successful Repair Examples

### BUG-002 — Incorrect Calculation

The original implementation returned the price without accounting for quantity.

The agent:

1. Inspected the repository.
2. Executed the tests.
3. Read the relevant source file.
4. Identified the incorrect return expression.
5. Applied a targeted patch.
6. Re-ran the tests.

The repaired implementation correctly calculates:

```text
Total = Price × Quantity
```

The tests passed after the modification.

### BUG-003 — Incorrect Discount Logic

The original implementation did not correctly apply the expected member discount.

The agent identified the incorrect conditional behavior and modified the member branch.

The complete benchmark test suite passed after the repair.

### BUG-004 — Division Failure

The original implementation raised an exception for a zero denominator, while the benchmark expected the defined safe behavior.

The agent identified the relevant conditional branch and modified the implementation accordingly.

Both tests passed after the repair.

### BUG-005 — Undefined Function Call

The implementation attempted to call an undefined rectangle-area function.

The agent replaced the incorrect function call with the appropriate calculation:

```text
Area = Length × Width
```

The test passed after the repair.

### BUG-006 — Incorrect Return Value

The implementation returned a user's name when the required behavior was to return the user's email.

The agent inspected the source and modified the returned attribute.

The test passed after the repair.

---

# Failure Analysis

## BUG-001

BUG-001 was the only unsuccessful benchmark case.

The agent began repository inspection and identified the relevant fixture, but did not complete the repair within the configured six-step interaction budget.

During execution, the agent repeatedly inspected the same file and also attempted to use unsupported arguments with the file-reading tool.

As a result, the agent exhausted its bounded interaction budget before producing a verified repair.

This highlights an important research observation:

> Repository-level repair performance depends not only on code-generation capability, but also on efficient tool selection, tool-interface reliability, and effective management of the agent's interaction budget.

The failure therefore provides a concrete direction for improving the agent rather than simply measuring successful repairs.

---

# Agent Execution Traces

The benchmark generates structured execution traces for each task.

Each trace records:

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

## 3. Repository inspection can complement imperfect retrieval

The retrieval experiment produced imperfect results, while the repair agent was still able to successfully repair most benchmark cases.

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

The six-step execution limit makes the experiment reproducible and prevents uncontrolled tool execution.

However, BUG-001 demonstrates that an insufficiently efficient tool-use strategy can cause the agent to fail even when the underlying software defect may be repairable.

This motivates future work on **adaptive execution budgets and improved tool selection**.

---

# Limitations

The current results should be interpreted as a **controlled research prototype evaluation** rather than a general measure of autonomous software engineering capability.

### Small Evaluation Sets

The retrieval evaluation contains 15 queries and the repair benchmark contains six defects.

### Controlled Defects

The benchmark defects are manually constructed and are smaller than many real-world software engineering issues.

### Limited Repository Scale

The current experiments primarily use small Python repositories rather than large production-scale codebases.

### Fixed Agent Step Budget

The current agent uses:

```text
MAX_STEPS = 6
```

The failure of BUG-001 demonstrates that this constraint can affect repair performance.

### No Large-Scale Real-World Evaluation

The current system has not yet been evaluated on a large-scale benchmark such as the full SWE-bench dataset.

---

# Future Work

Potential research directions include:

* AST-aware code chunking
* Function-level and class-level retrieval
* BM25-based retrieval
* Improved hybrid retrieval
* Retrieval reranking
* Adaptive ReAct step budgets
* Improved tool selection
* Tool argument validation
* Multi-file software repair
* Regression bug evaluation
* Larger open-source repositories
* Real GitHub issue evaluation
* Larger SWE-bench-style experiments

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
│   ├── traces/
│   └── ...
│
├── research/
│   ├── retrieval_evaluation.md
│   ├── prompt_engineering.md
│   ├── code_generation_and_verification.md
│   ├── agentic_tool_use.md
│   └── repository_repair_benchmark.md
│
├── sample_repo/
│
├── tests/
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
* **Git / GitHub**

---

# Research Documentation

The `research/` directory contains technical documentation and experimental analysis covering:

* Retrieval evaluation
* Prompt engineering
* Code generation and verification
* Agentic tool use
* Repository-level software repair
* Repair benchmarking
* Experimental results and discussion

Key research artifact:

```text
research/repository_repair_benchmark.md
```

---

# Reproducibility

The project maintains reproducible benchmark fixtures and automated evaluation scripts.

The repair benchmark can be executed through the evaluation pipeline, which:

1. Restores each buggy fixture.
2. Runs baseline tests.
3. Executes the repair agent.
4. Runs post-repair tests.
5. Records the outcome.
6. Saves benchmark results and execution traces.

This enables the repair results to be inspected rather than relying only on qualitative demonstrations.

---

# Project Status

**Research Prototype — Controlled Evaluation Complete**

The core repository-level agent architecture and controlled evaluation pipeline are implemented.

Current research artifacts include:

* Retrieval comparison experiment
* Autonomous repair benchmark
* Automated test-based verification
* Agent execution traces
* Research documentation
* Reproducible benchmark fixtures

Future work focuses on improving tool selection, retrieval quality, adaptive reasoning budgets, and evaluation on larger real-world software engineering benchmarks.

---

# Disclaimer

The reported **83.3% repair success rate** is based on a small, controlled benchmark containing six manually constructed software defects.

It should **not** be interpreted as a general measure of autonomous software engineering capability.

The purpose of this project is to investigate the architecture, behavior, strengths, limitations, and evaluation of LLM-based software engineering agents.
