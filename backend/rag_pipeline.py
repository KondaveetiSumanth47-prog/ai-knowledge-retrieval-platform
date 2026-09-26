from embeddings import create_embeddings
from vector_store import get_collection, search_chunks

RELEVANCE_THRESHOLD = 0.60


def retrieve_information(question, top_k=3):
    if not isinstance(question, str) or not question.strip():
        return []

    if get_collection().count() == 0:
        return []

    try:
        query_embedding = create_embeddings([question.strip()])[0]
    except Exception:
        return []

    results = search_chunks(query_embedding, top_k=max(1, int(top_k or 3)))
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if distances:
        numeric_distances = []
        for value in distances:
            try:
                numeric_distances.append(float(value))
            except (TypeError, ValueError):
                continue
        if numeric_distances:
            best_distance = min(numeric_distances)
            if best_distance > RELEVANCE_THRESHOLD:
                return []

    retrieved_information = []
    for index, document in enumerate(documents):
        cleaned_text = (document or "").strip()
        if not cleaned_text:
            continue

        metadata = metadatas[index] if index < len(metadatas) and isinstance(metadatas[index], dict) else {}
        retrieved_information.append({
            "text": cleaned_text,
            "source": metadata.get("source", "Unknown"),
            "chunk_index": metadata.get("chunk_index", index),
            "file_type": metadata.get("file_type", "unknown"),
        })

    return retrieved_information