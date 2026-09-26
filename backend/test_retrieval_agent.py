from retrieval_agent import RetrievalAgent


agent = RetrievalAgent(
    top_k=3,
    distance_threshold=0.60
)


test_queries = [
    {
        "query": "What is RAG?",
        "query_type": "factual"
    },
    {
    "query": "What is AI?",
    "query_type": "factual"
},
    {
        "query": "How does RAG work?",
        "query_type": "procedural"
    },
    {
        "query": "What is the difference between AI and Machine Learning?",
        "query_type": "comparative"
    },
    {
        "query": "What is quantum computing?",
        "query_type": "factual"
    }
]


for item in test_queries:

    classification = {
        "query_type": item["query_type"]
    }

    result = agent.retrieve(
        item["query"],
        classification
    )

    print("\n===================================")
    print("Query:", item["query"])
    print("Query Type:", result["query_type"])
    print("Status:", result["status"])
    print("Results Found:", result["result_count"])

    for index, retrieved in enumerate(result["results"], start=1):

        print("\nResult", index)
        print("Source:", retrieved["source"])
        print("Chunk Index:", retrieved["chunk_index"])
        print("Distance:", retrieved["distance"])
        print("Relevance Score:", retrieved["relevance_score"])
        print("Text:", retrieved["text"][:200])