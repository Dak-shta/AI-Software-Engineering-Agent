# Retrieval Evaluation

## Objective

Evaluate the ability of different retrieval strategies to find
the correct repository code for natural-language questions.

## Evaluation Set

Three questions were tested against the sample repository.

| Question | Expected | Semantic | Hybrid |
|---|---|---|---|
| Where is the User class defined? | models.py | PASS | PASS |
| Where is the User object created? | app.py | PASS | PASS |
| How is the user's name stored? | models.py | FAIL | FAIL |

## Results

| Retrieval Method | Top-1 Accuracy |
|---|---:|
| Semantic Retrieval | 66.67% |
| Hybrid Retrieval | 66.67% |

## Observation

Hybrid retrieval did not improve Top-1 accuracy on this small
evaluation set.

The remaining failure occurs because both `app.py` and `models.py`
contain concepts related to `User` and `name`. Simple keyword
matching is not sufficient to distinguish object creation from
attribute storage.

## Conclusion

The experiment shows that combining semantic and keyword scores
does not automatically improve retrieval quality. A larger and
more diverse evaluation dataset would be required for a reliable
comparison.

## Next Step

Improve the retrieval strategy and evaluate it using a larger
set of repository questions.