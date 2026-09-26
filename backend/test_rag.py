from rag_pipeline import retrieve_information

question = "What is RAG?"

results = retrieve_information(question, top_k=3)

print("Question:", question)
print("\nRetrieved Information:")

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print(result)