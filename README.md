# AI Software Engineering Agent

An AI-powered software engineering agent for **repository-level code understanding, debugging, automated repair, and verification**.

The system combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), semantic code retrieval, ReAct-style reasoning, tool calling, targeted patching, and automated testing** to perform software engineering tasks over an existing codebase.

---

## Research Goal

The project explores how LLM-based agents can move beyond simple code generation toward **autonomous repository-level software engineering**.

Instead of generating code in isolation, the agent must:

* Understand an existing repository.
* Locate relevant source code.
* Retrieve useful repository context.
* Inspect dependencies and files.
* Diagnose software defects.
* Select and execute development tools.
* Generate targeted code modifications.
* Run tests after modification.
* Verify whether the repair actually succeeds.

The project also investigates the **limitations of retrieval strategies and bounded agent reasoning** through controlled experiments.

---

## System Architecture

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
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
       Repository      Retrieval      Testing
       Inspection       / RAG         / Pytest
             │            │             │
             └────────────┼─────────────┘
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
                 Iterate     Verified
```

---

## Key Components

### Repository Understanding

The agent can inspect repository structure and read relevant source files before making modifications.

### Semantic Retrieval

Repository code is chunked and embedded using:

```text
all-MiniLM-L6-v2
```

Embeddings are stored and queried using **ChromaDB**.

### Retrieval-Augmented Generation

Retrieved repository context can be used to provide the language model with relevant code before reasoning about a software engineering task.

### ReAct Agent

The agent follows an iterative reasoning and tool-use loop:

```text
Observe → Select Tool → Execute → Observe → Reason → Act
```

A bounded execution budget is used to prevent uncontrolled tool execution.

### Tool Calling

The agent can select tools for:

* Repository inspection
* File listing
* File reading
* Code modification
* Patch application
* Test execution

### Safe Code Modification

Targeted modifications are performed using a patch-based workflow rather than unrestricted file replacement.

### Automated Verification

The agent executes tests after modifications and uses test results as an external verification signal.

---

# Research Experiments

The project includes two primary evaluations.

## 1. Retrieval Evaluation

Three repository retrieval strategies were compared using **15 natural-language queries**.

| Method   | Top-1 Accuracy | Top-3 Accuracy |
| -------- | -------------: | -------------: |
| Keyword  |         33.33% |     **80.00%** |
| Semantic |     **46.67%** |         73.33% |
| Hybrid   |         40.00% |         60.00% |

### Observation

Semantic retrieval achieved the strongest Top-1 accuracy.

Keyword retrieval achieved the strongest Top-3 accuracy.

The hybrid approach did not outperform the individual retrieval methods on this evaluation set.

This demonstrates that combining retrieval signals does not automatically improve retrieval quality and motivates future investigation into better code-aware chunking and reranking strategies.

---

## 2. Autonomous Repair Evaluation

A controlled benchmark containing **six injected software defects** was used to evaluate end-to-end autonomous repair.

The benchmark included:

* Incorrect state assignment
* Incorrect return values
* Incorrect conditional logic
* Runtime/edge-case failure
* Incorrect function call
* Dependency-related incorrect value

### Results

| Metric                |     Result |
| --------------------- | ---------: |
| Benchmark cases       |      **6** |
| Successful repairs    |    **6/6** |
| Repair success rate   |   **100%** |
| Final test-pass rate  |   **100%** |
| Targeted patch usage  |   **100%** |
| Average agent steps   |   **5.83** |
| Agent completion rate | **83.33%** |

Every benchmark case was successfully repaired and every successful repair used the targeted patch mechanism.

### Important Observation

One successful repair reached the configured maximum of six ReAct steps before the agent produced a final completion response.

Therefore:

```text
Repair success       = 100%
Agent completion     = 83.33%
```

This demonstrates that successful repository modification and conversational agent completion are separate properties that should be evaluated independently.

---

# Research Findings

The experiments produced several important observations.

### Semantic retrieval provides the strongest Top-1 baseline

Semantic retrieval achieved 46.67% Top-1 accuracy, outperforming keyword and hybrid retrieval.

### More retrieval signals do not guarantee better retrieval

The hybrid approach performed below semantic retrieval, demonstrating the importance of empirical evaluation of retrieval strategies.

### Agentic interaction can compensate for imperfect retrieval

Although retrieval accuracy was imperfect, the complete repair agent successfully repaired all six controlled defects.

This suggests that repository-level agents can obtain additional context through:

* File inspection
* Test execution
* Tool interaction
* Iterative reasoning
* Post-repair verification

### Executable verification is valuable

The system does not rely solely on the LLM's claim that a repair is correct.

Instead, the modified repository is tested after the repair, providing an external signal for evaluating success.

---

# Limitations

The current results should be interpreted as a controlled proof-of-concept.

### Small Evaluation Sets

The retrieval evaluation contains 15 queries and the repair benchmark contains six bugs.

### Controlled Defects

The benchmark bugs are manually constructed and simpler than many real-world software engineering issues.

### Limited Repository Scale

The experiments currently use small Python repositories rather than large production codebases.

### Fixed Agent Step Budget

The current agent uses:

```text
MAX_STEPS = 6
```

One successful repair reached this limit.

### No Large-Scale Real-World Evaluation

The current system has not yet been evaluated on a large-scale real-world benchmark such as the complete SWE-bench dataset.

---

# Future Work

Potential research directions include:

* AST-aware code chunking
* Function-level and class-level retrieval
* BM25 and hybrid retrieval improvements
* Retrieval reranking
* Adaptive ReAct step budgets
* Improved tool selection
* Multi-file software repair
* Regression bug evaluation
* Larger open-source repositories
* Real GitHub issue evaluation
* Larger SWE-bench-style experiments

---

# Repository Structure

```text
ai-software-engineering-agent/
│
├── agent/
│   ├── llm.py
│   ├── rag.py
│   ├── prompts.py
│   ├── code_generator.py
│   ├── apply_change.py
│   ├── tools.py
│   ├── tool_selector.py
│   ├── test_tools.py
│   ├── react_agent.py
│   └── ...
│
├── tools/
│   ├── repository.py
│   ├── retriever.py
│   ├── semantic_retriever.py
│   ├── chunker.py
│   ├── vector_store.py
│   ├── file_editor.py
│   ├── file_reader.py
│   ├── change_parser.py
│   ├── patch_editor.py
│   └── test_runner.py
│
├── sample_repo/
│   ├── app.py
│   ├── models.py
│   ├── test_models.py
│   └── ...
│
├── evaluation/
│   ├── benchmark.py
│   ├── benchmark_runner.py
│   ├── benchmark_results.json
│   ├── repair_metrics.py
│   ├── retrieval_comparison.py
│   └── ...
│
├── research/
│   ├── retrieval_evaluation.md
│   ├── prompt_engineering.md
│   ├── code_generation_and_verification.md
│   ├── agentic_tool_use.md
│   ├── automatic_software_repair.md
│   ├── repair_evaluation.md
│   └── results_and_discussion.md
│
├── tests/
├── vectorstore/
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

The `research/` directory contains technical notes and experimental analysis covering:

* Transformer and LLM foundations
* Retrieval evaluation
* Prompt engineering
* Code generation and verification
* Agentic tool use
* Automatic software repair
* Repair evaluation
* Combined experimental results and discussion

---

# Project Status

**Research Prototype — Evaluation Complete**

The core agent architecture and controlled evaluation pipeline are implemented.

Current work focuses on:

* Research documentation
* Reproducibility
* Repository cleanup
* Demonstration
* Architecture visualization
* Future evaluation on larger software engineering benchmarks

---

# Disclaimer

The reported 100% repair success rate is based on a small, controlled benchmark of six manually constructed defects.

It should not be interpreted as a general measure of autonomous software engineering capability.

The purpose of this project is to investigate the architecture, behavior, strengths, and limitations of LLM-based software engineering agents.
