from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    if not chunks:
        return []

    texts = [str(chunk).strip() for chunk in chunks if str(chunk).strip()]
    if not texts:
        return []

    embeddings = model.encode(texts)
    return embeddings