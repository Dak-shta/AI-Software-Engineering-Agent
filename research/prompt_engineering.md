# Prompt Engineering Experiment

## Objective

Compare a basic prompt with a structured prompt for repository
question answering.

## Experimental Setup

The same repository, question, retrieved context, and LLM were
used. Only the prompt structure was changed.

### Question

> Where is the User object created?

---

## Prompt A — Basic

The basic prompt asks the model to answer the question using the
provided repository context.

### Result

The model correctly identified `sample_repo/app.py` and explained
that `User(name)` creates the object.

---

## Prompt B — Structured

The structured prompt specifies:

- The role of the model
- The task
- Restrictions against hallucination
- The need to identify relevant code
- A required answer format
- Instructions to state when context is insufficient

### Result

The model correctly identified `sample_repo/app.py` and explained
that `User(name)` invokes the constructor.

---

## Comparison

| Aspect | Basic Prompt | Structured Prompt |
|---|---|---|
| Correct file | PASS | PASS |
| Correct explanation | PASS | PASS |
| Hallucination | None observed | None observed |
| Structured output | No | Yes |
| Explicit constraints | No | Yes |

## Observation

Both prompts successfully answered the test question. The
structured prompt produced a more controlled response because it
explicitly specified constraints and an output format.

However, this single example is not sufficient to conclude that
structured prompting improves accuracy. A larger evaluation set
would be required.

## Conclusion

Structured prompting provides better control over the response
format and model behavior while maintaining correct answers on
the tested example.

Future experiments should evaluate multiple repository questions
and compare correctness, hallucination, and format adherence.