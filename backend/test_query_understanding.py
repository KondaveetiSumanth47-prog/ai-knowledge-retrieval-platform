from query_understanding_agent import QueryUnderstandingAgent


agent = QueryUnderstandingAgent()

test_queries = [
    "What is RAG?",
    "How does RAG work?",
    "What is the difference between AI and Machine Learning?",
    "Tell me about it"
]

for query in test_queries:
    result = agent.classify_query(query)

    print("\nQuery:", query)
    print("Type:", result["query_type"])
    print("Confidence:", result["classification_confidence"])
    print("Routing:", result["routing"])