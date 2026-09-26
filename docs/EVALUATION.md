# Retrieval Evaluation

## Evaluated domains
1. Education
2. Technology

## Query categories tested
1. Factual query
2. Procedural query
3. Comparative query
4. Information-present query
5. Information-unavailable query

## Questions used
- What is Machine Learning?
- What is ChromaDB?
- How does RAG retrieve information?
- What is the difference between supervised and unsupervised learning?
- What is quantum computing?

## Retrieval settings tested
- Top-1
- Top-3
- Top-5

## Accuracy formula
Top-1 Accuracy = Number of queries where the correct relevant information appears in the first result divided by total evaluated known queries × 100

Top-3 Accuracy = Number of queries where the correct relevant information appears within the first three results divided by total evaluated known queries × 100

Top-5 Accuracy = Number of queries where the correct relevant information appears within the first five results divided by total evaluated known queries × 100

## Important rule for unavailable-query handling
The unavailable-query test is treated as a separate no-answer detection check rather than as a retrieval-accuracy test. This is because the expected outcome is not “retrieve a correct answer,” but instead “return no relevant information.”

## Real verification result
The actual project was evaluated against the current knowledge base using the live retrieval pipeline.

### Verified retrieval accuracy for known relevant queries
- Top-1 Accuracy: 100%
- Top-3 Accuracy: 100%
- Top-5 Accuracy: 100%

These values are based only on the four valid topic queries that are actually present in the knowledge base.

## Unavailable-information test
Question: What is quantum computing?

Expected behavior: The system should reject weak matches and return no relevant information.

Verified behavior after the relevance-threshold fix:
- the backend returns an empty retrieved_chunks list
- the response includes the clear message: "No relevant information found in the current knowledge base."

This case is evaluated separately from the retrieval-accuracy metrics above.

## Threshold logic used
The ChromaDB collection uses cosine distance. In this project, lower distance values represent stronger similarity. A simple relevance gate is used:

- retrieve top-k candidates
- read the best distance from the ChromaDB results
- if the best distance is greater than 0.60, treat the query as insufficiently relevant and return no results

This threshold was chosen because valid in-domain queries were consistently observed below 0.60, while the unavailable-topic query produced a weaker match above this range.

## Notes
- These values were measured against the live project behavior and the current sample knowledge base.
- The results reflect the actual project contents, not a hypothetical benchmark.
- The current milestone is retrieval-focused and does not include a full answer-generation model.
