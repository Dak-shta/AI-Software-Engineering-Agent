# Retrieval Evaluation

## Objective

The retrieval component of the AI Software Engineering Agent was evaluated to determine how effectively it identifies relevant repository files from natural-language software engineering queries.

Three retrieval strategies were compared:

1. Keyword Retrieval
2. Semantic Retrieval
3. Hybrid Retrieval

The experiment evaluates whether the expected source file appears within the Top-1 and Top-3 retrieved results.

---

## Evaluation Dataset

A set of 15 natural-language queries was created over the sample repository.

The queries cover three categories:

* User/model-related repository questions
* User object creation and initialization
* Function and bug-related code localization

Each query has a manually defined expected source file.

Example queries include:

* "Where is the User class defined?"
* "Where is the User object created?"
* "Where is the calculate_total function?"
* "Where is the area calculation function?"
* "Where is the user's email retrieved?"

---

## Retrieval Methods

### 1. Keyword Retrieval

Keyword retrieval assigns scores based on the occurrence of query terms within repository files.

This provides a simple lexical baseline.

### 2. Semantic Retrieval

Semantic retrieval represents repository code and the query using the `all-MiniLM-L6-v2` sentence-transformer model.

Cosine similarity is then used to rank repository chunks according to semantic relevance.

### 3. Hybrid Retrieval

Hybrid retrieval combines semantic similarity with normalized keyword scores.

The experiment also aggregates results at the file level and retains the strongest score for each file.

The hybrid score is calculated as:

```text
Hybrid Score =
0.7 × Semantic Score
+
0.3 × Normalized Keyword Score
```

---

## Experimental Results

The three approaches were evaluated on all 15 queries.

| Retrieval Method | Top-1 Accuracy | Top-3 Accuracy |
| ---------------- | -------------: | -------------: |
| Keyword          |         33.33% |     **80.00%** |
| Semantic         |     **46.67%** |         73.33% |
| Hybrid           |         40.00% |         60.00% |

---

## Analysis

### Top-1 Retrieval

Semantic retrieval achieved the highest Top-1 accuracy:

**46.67%**

This was higher than:

* Keyword retrieval: 33.33%
* Hybrid retrieval: 40.00%

This indicates that semantic similarity was more effective at identifying the single most relevant file for the evaluated queries.

---

### Top-3 Retrieval

Keyword retrieval achieved the highest Top-3 accuracy:

**80.00%**

Semantic retrieval achieved:

**73.33%**

Hybrid retrieval achieved:

**60.00%**

The relatively strong Keyword Top-3 result indicates that lexical matching can still identify relevant repository files when several candidates are returned.

---

## Hybrid Retrieval Observation

The hybrid approach did not outperform semantic retrieval.

Although the hybrid method combines two complementary signals, the current evaluation does not show an improvement in retrieval accuracy.

Possible reasons include:

1. The evaluation repository is small.
2. Query vocabulary overlaps strongly with multiple files.
3. The keyword signal may favor files containing common terms.
4. The repository contains several test files with terminology similar to the source files.
5. The current chunking strategy uses fixed-size chunks rather than syntax-aware code structures.

Therefore, simply combining semantic and lexical scores does not guarantee better retrieval performance.

---

## Important Research Observation

The experiment demonstrates that **retrieval quality depends on the evaluation metric and retrieval strategy**.

Semantic retrieval achieved the strongest Top-1 performance, while keyword retrieval achieved the strongest Top-3 performance.

This suggests that lexical and semantic retrieval capture different aspects of repository relevance.

For the current implementation, semantic retrieval is therefore retained as the primary retrieval baseline, while hybrid retrieval is treated as an experimental alternative rather than an automatic improvement.

---

## Relationship Between Retrieval and Software Repair

Retrieval quality and end-to-end repair success were evaluated separately.

The retrieval experiment measured whether the correct repository file was ranked highly for a natural-language query.

The repair benchmark, in contrast, evaluated whether the complete agent could diagnose and repair a software defect using repository inspection, testing, tool execution, and targeted code modification.

The retrieval experiment achieved:

* Semantic Top-1: **46.67%**
* Semantic Top-3: **73.33%**

Despite these imperfect retrieval results, the repair benchmark successfully repaired all six controlled bugs.

This suggests that end-to-end software repair does not depend exclusively on a single retrieval result. The agent can perform additional repository inspection, read files, execute tests, and gather information through tool interactions.

Therefore, retrieval accuracy and autonomous repair success should be considered separate but related evaluation dimensions.

---

## Limitations

### 1. Small Evaluation Set

Only 15 retrieval queries were evaluated.

A larger dataset would provide stronger evidence.

### 2. Small Repository

The evaluation uses a miniature Python repository rather than a large production-scale repository.

### 3. Fixed-Size Chunking

The current chunker uses fixed line-based chunks with overlap.

This does not explicitly preserve functions, classes, imports, or other syntactic structures.

### 4. Limited Query Diversity

The queries are manually constructed and may not represent the full variety of real-world software engineering requests.

### 5. No Large-Scale Benchmark

The retrieval evaluation has not yet been tested on large open-source repositories.

---

## Future Work

Future retrieval experiments could investigate:

1. AST-aware code chunking.
2. Function-level and class-level retrieval.
3. BM25-based lexical retrieval.
4. Reciprocal Rank Fusion.
5. Query expansion.
6. Repository-aware reranking.
7. Larger real-world repositories.
8. Retrieval evaluation using real software engineering issues.

---

## Conclusion

The retrieval experiment provides an empirical comparison of three repository retrieval strategies.

Semantic retrieval achieved the highest Top-1 accuracy at **46.67%**, while keyword retrieval achieved the highest Top-3 accuracy at **80.00%**.

The hybrid strategy achieved **40.00% Top-1** and **60.00% Top-3**, and therefore did not improve upon the individual retrieval approaches in this evaluation.

The results demonstrate that retrieval strategy selection should be empirically evaluated rather than assuming that combining multiple retrieval signals will automatically improve performance.

The experiment also establishes a baseline for future work involving larger repositories, syntax-aware code representations, and more sophisticated reranking methods.
