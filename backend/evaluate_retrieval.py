from embeddings import create_embeddings
from vector_store import search_chunks


test_cases = [
    {
        "type": "Factual",
        "question": "What is ChromaDB?",
        "expected": "ChromaDB"
    },
    {
        "type": "Factual",
        "question": "What is Machine Learning?",
        "expected": "Machine Learning"
    },
    {
        "type": "Procedural",
        "question": "How does RAG retrieve information?",
        "expected": "retrieves relevant information"
    },
    {
        "type": "Comparative",
        "question": "What is the difference between supervised and unsupervised learning?",
        "expected": "Supervised Learning"
    },
    {
        "type": "Unavailable",
        "question": "What is quantum computing?",
        "expected": "Quantum Computing"
    }
]


def evaluate_question(question, expected, top_k):
    query_embedding = create_embeddings([question])[0]

    results = search_chunks(
        query_embedding,
        top_k=top_k
    )

    retrieved_documents = results["documents"][0]

    for document in retrieved_documents:
        if expected.lower() in document.lower():
            return True

    return False


print("RAG Retrieval Evaluation")
print("=" * 60)

for top_k in [1, 3, 5]:

    correct = 0
    total = len(test_cases)

    print(f"\nTop-{top_k} Evaluation")
    print("-" * 40)

    for index, test in enumerate(test_cases, start=1):

        found = evaluate_question(
            test["question"],
            test["expected"],
            top_k
        )

        print(f"\nTest {index}")
        print("Type:", test["type"])
        print("Question:", test["question"])

        if test["type"] == "Unavailable":
            if found:
                print("Result: Information Found")
            else:
                print("Result: Information Not Found")
        else:
            if found:
                print("Result: PASS")
                correct += 1
            else:
                print("Result: FAIL")

    available_tests = total - 1
    accuracy = (correct / available_tests) * 100

    print(f"\nTop-{top_k} Accuracy: {accuracy:.2f}%")


print("\n" + "=" * 60)
print("Evaluation Completed")