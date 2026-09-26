from chunking import split_text
from embeddings import create_embeddings
from vector_store import store_chunks, search_chunks

text = """
Artificial Intelligence is a branch of computer science.
Machine Learning allows computers to learn from data.
RAG stands for Retrieval Augmented Generation.
RAG retrieves relevant information before generating an answer.
ChromaDB is a vector database used for semantic search.
"""

chunks = split_text(text, chunk_size=100, chunk_overlap=20)

embeddings = create_embeddings(chunks)

store_chunks(chunks, embeddings)

query = "What is RAG?"

query_embedding = create_embeddings([query])[0]

results = search_chunks(query_embedding, top_k=3)

print("Question:", query)
print("\nRelevant Chunks:")

for result in results["documents"][0]:
    print("-", result)