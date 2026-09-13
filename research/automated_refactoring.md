# Automated Software Refactoring Evaluation

## Objective

This experiment evaluates whether the software-engineering workflow can preserve program behavior while improving internal code structure through refactoring.

The experiment focuses on removing duplicated order-total calculation logic from a small repository-level example.

## Baseline

The original implementation contained duplicated calculation logic in:

- `calculate_order_total()`
- `calculate_order_total_with_discount()`

Both functions independently iterated through the items, extracted price and quantity, calculated subtotals, and accumulated the total.

This duplication created an opportunity for structural refactoring without changing the externally observable behavior.

## Refactoring

The duplicated calculation logic was extracted into a shared helper:

```python
_calculate_items_total(items)
The two public functions were then simplified to reuse this helper.

The refactoring changed the internal structure while keeping the public functions and their expected behavior unchanged.

Behavioral Verification

Four tests were used to establish and verify expected behavior:

Normal order-total calculation
Handling of zero-quantity items
Discount calculation
Zero-discount behavior

After refactoring:

4/4 tests passed.

Observed result:

4 passed in 0.70s

This provides evidence that the refactoring preserved the tested behavior.

Full Repository Test Suite

The full repository test suite was also executed.

The suite encountered 13 test-collection errors caused by an existing Python import/package-name collision involving agent/tools.py and the tools/ package:

ModuleNotFoundError:
No module named 'tools.git_tools';
'tools' is not a package

The dedicated refactoring test file was not affected by this issue and passed independently.

Therefore, the full-suite collection issue is treated as a repository-level testing/infrastructure limitation rather than a failure of the refactoring itself.

Research Interpretation

The experiment demonstrates a controlled form of automated software-refactoring evaluation:

Duplicated implementation
        ↓
Structural refactoring
        ↓
Shared helper extraction
        ↓
Behavioral tests
        ↓
4/4 tests passed

The key evaluation criterion was behavioral preservation rather than simply reducing the number of lines of code.

Limitations

This experiment uses a small controlled example and a limited test suite. Passing the four tests does not prove complete semantic equivalence for all possible inputs.

The experiment therefore provides evidence of behavioral preservation for the tested cases rather than a formal proof of equivalence.

The repository also contains an existing Python import/package-name collision that prevents the complete test suite from being collected successfully.

Reproducibility

The experiment can be reproduced using:

$env:PYTHONPATH = "."
pytest tests\test_refactoring_example.py

Expected result:

4 passed
Relevance to AI for Software Engineering

Automated refactoring is an important software-engineering application of LLM-based agents.

This experiment extends the project's original focus on autonomous software repair toward a broader software-engineering workflow involving:

repository understanding
code modification
structural improvement
automated testing
behavioral verification

The experiment complements the project's existing repair, retrieval, Git-aware analysis, and pull-request analysis evaluations.


Save it.

---
