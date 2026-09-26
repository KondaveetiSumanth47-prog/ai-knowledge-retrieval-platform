from embeddings import create_embeddings

chunks = [
    "Artificial Intelligence is a branch of computer science.",
    "Machine Learning allows computers to learn from data.",
    "RAG retrieves relevant information before generating an answer."
]

embeddings = create_embeddings(chunks)

print("Number of chunks:", len(embeddings))
print("Embedding size:", len(embeddings[0]))
print("First embedding:", embeddings[0])