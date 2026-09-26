from chunking import split_text

text = """
Artificial Intelligence is a branch of computer science.
Machine Learning allows computers to learn from data.
RAG stands for Retrieval Augmented Generation.
RAG retrieves relevant information before generating an answer.
"""

chunks = split_text(text, chunk_size=100, chunk_overlap=20)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\nChunk", i + 1)
    print(chunk)