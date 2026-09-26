from embeddings import create_embeddings
from vector_store import search_chunks


class RetrievalAgent:

    def __init__(self, top_k=3, distance_threshold=0.60, min_relevance_score=0.44):
        self.top_k = top_k
        self.distance_threshold = distance_threshold
        self.min_relevance_score = min_relevance_score

    def retrieve(self, query, query_classification=None):

        query_embedding = create_embeddings([query])[0]

        results = search_chunks(
            query_embedding,
            top_k=self.top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved_results = []

        for i, document in enumerate(documents):

            distance = distances[i] if i < len(distances) else None

            relevance_score = (
                max(0, 1 - distance)
                if distance is not None
                else 0
            )

            if (
                distance is not None
                and (
                    distance > self.distance_threshold
                    or relevance_score < self.min_relevance_score
                )
            ):
                continue

            metadata = (
                metadatas[i]
                if i < len(metadatas) and metadatas[i]
                else {}
            )

            retrieved_results.append({
                "text": document,
                "source": metadata.get("source", "Unknown"),
                "chunk_id": metadata.get("chunk_id", "Unknown"),
                "chunk_index": metadata.get("chunk_index", i),
                "citation": metadata.get(
                    "citation",
                    metadata.get("source", "Unknown")
                ),
                "file_type": metadata.get("file_type", "Unknown"),
                "distance": distance,
                "relevance_score": round(relevance_score, 3)
            })

        return {
            "query": query,
            "query_type": (
                query_classification.get("query_type")
                if query_classification
                else "unknown"
            ),
            "top_k": self.top_k,
            "results": retrieved_results,
            "result_count": len(retrieved_results),
            "status": (
                "success"
                if retrieved_results
                else "no_relevant_information"
            )
        }