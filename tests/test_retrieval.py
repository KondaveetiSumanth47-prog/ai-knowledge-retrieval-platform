import json
from rag_pipeline import retrieve_information

# Retrieval accuracy is measured on known relevant questions only.
# The unavailable-query test is evaluated separately as a no-answer detection check.
valid_queries = [
    {"domain": "Education", "category": "Factual query", "question": "What is Machine Learning?", "expected": ["Machine Learning", "machine learning"]},
    {"domain": "Technology", "category": "Factual query", "question": "What is ChromaDB?", "expected": ["ChromaDB"]},
    {"domain": "Technology", "category": "Procedural query", "question": "How does RAG retrieve information?", "expected": ["retrieves relevant information", "RAG", "retrieval"]},
    {"domain": "Education", "category": "Comparative query", "question": "What is the difference between supervised and unsupervised learning?", "expected": ["Supervised Learning", "Unsupervised Learning", "supervised", "unsupervised"]},
]

unavailable_query = {
    "question": "What is quantum computing?",
    "expected": "No relevant information found in the current knowledge base."
}


def evaluate_query(question, expected_terms, top_k):
    results = retrieve_information(question, top_k=top_k)
    joined_text = " ".join(item.get("text", "") for item in results).lower()

    normalized_expected = [term.lower() for term in expected_terms]
    return any(term in joined_text for term in normalized_expected)


def run_evaluation():
    results = {}
    for top_k in [1, 3, 5]:
        passed = 0
        rows = []
        for item in valid_queries:
            question = item["question"]
            category = item["category"]
            domain = item["domain"]
            expected = item["expected"]

            is_correct = evaluate_query(question, expected, top_k)
            if is_correct:
                passed += 1

            rows.append({
                "domain": domain,
                "category": category,
                "question": question,
                "top_k": top_k,
                "passed": is_correct,
            })

        accuracy = (passed / len(valid_queries)) * 100
        results[f"top_{top_k}"] = {
            "accuracy": round(accuracy, 2),
            "passed": passed,
            "total": len(valid_queries),
            "rows": rows,
        }

    no_answer_result = retrieve_information(unavailable_query["question"], top_k=5)
    results["unavailable_query_no_answer"] = {
        "question": unavailable_query["question"],
        "passed": len(no_answer_result) == 0,
        "retrieved_count": len(no_answer_result),
    }

    return results


if __name__ == "__main__":
    evaluation = run_evaluation()
    print(json.dumps(evaluation, indent=2))
