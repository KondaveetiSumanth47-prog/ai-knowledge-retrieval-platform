from rag_pipeline import retrieve_information

queries = [
    {"category": "Factual query", "question": "What is Machine Learning?"},
    {"category": "Procedural query", "question": "What is RAG?"},
    {"category": "Comparative query", "question": "What is the difference between supervised and unsupervised learning?"},
    {"category": "Known answer in knowledge base", "question": "What is ChromaDB used for?"},
    {"category": "Unknown answer not in knowledge base", "question": "What is quantum computing?"},
]

for top_k in [1, 3, 5]:
    print(f"\n=== Top-{top_k} Retrieval Evaluation ===")
    for item in queries:
        question = item["question"]
        category = item["category"]
        results = retrieve_information(question, top_k=top_k)
        print(f"{category}: {question}")
        if not results:
            print("  No relevant chunks returned")
        else:
            first = results[0]
            print(f"  Source: {first.get('source', 'Unknown')} | Chunk: {first.get('chunk_index', 0)}")
            print(f"  Preview: {first.get('text', '')[:120]}...")