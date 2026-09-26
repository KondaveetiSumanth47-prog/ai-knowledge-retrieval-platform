from retrieval_agent import RetrievalAgent
from response_generation_agent import ResponseGenerationAgent


retrieval_agent = RetrievalAgent(
    top_k=3,
    distance_threshold=0.60
)

response_agent = ResponseGenerationAgent()


query = "What is RAG?"


classification = {
    "query_type": "factual"
}


retrieval_result = retrieval_agent.retrieve(
    query,
    classification
)


response_result = response_agent.generate_response(
    query,
    retrieval_result["results"],
    retrieval_result["query_type"]
)


print("\n===================================")
print("QUERY")
print("===================================")
print(query)

print("\nQUERY TYPE")
print(response_result["query_type"])

print("\nANSWER")
print(response_result["answer"])

print("\nSOURCES")
for source in response_result["sources"]:
    print("-", source)

print("\nCONFIDENCE")
print("Label:", response_result["confidence"]["label"])
print("Score:", response_result["confidence"]["score"])

print("\nSTATUS")
print(response_result["status"])