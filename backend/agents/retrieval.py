from typing import List, Dict, Any
from ingestion.vector_store import VectorStoreManager

class RetrievalAgent:
    """
    2. Retrieval Agent (Milestone 2):
    - Performs ChromaDB semantic vector search.
    - Hybrid Relevance Ranking: Cosine vector score (70%) + Keyword density match (30%).
    - Filters out low-confidence results (< 0.35 threshold).
    """
    def __init__(self, vector_store: VectorStoreManager = None, min_threshold: float = 0.35):
        self.vector_store = vector_store or VectorStoreManager()
        self.min_threshold = min_threshold

    def process(self, query_understanding: Dict[str, Any], top_k: int = 5) -> Dict[str, Any]:
        query_text = query_understanding['cleaned_query']
        domain_filter = query_understanding.get('target_domain', 'all')
        keywords = [k.lower() for k in query_understanding.get('keywords', [])]

        raw_results = self.vector_store.similarity_search(
            query_text=query_text,
            top_k=top_k * 2,  # Search wider window then rank & filter
            domain_filter=domain_filter
        )

        ranked_chunks = []
        filtered_out_count = 0

        for item in raw_results:
            content_lower = item['content'].lower()
            
            # Keyword density calculation
            kw_matches = sum(1 for kw in keywords if kw in content_lower)
            kw_density = (kw_matches / max(1, len(keywords))) if keywords else 0.0
            
            # Hybrid Score calculation
            vector_score = item['score']
            hybrid_score = round(min(1.0, (vector_score * 0.70) + (kw_density * 0.30)), 4)

            # Filtering low-confidence results
            if hybrid_score < self.min_threshold:
                filtered_out_count += 1
                continue

            item_copy = dict(item)
            item_copy['score'] = hybrid_score
            item_copy['vector_score'] = vector_score
            item_copy['kw_density'] = round(kw_density, 2)
            ranked_chunks.append(item_copy)

        # Sort by hybrid relevance score descending
        ranked_chunks.sort(key=lambda x: x['score'], reverse=True)
        top_chunks = ranked_chunks[:top_k]

        top_score = top_chunks[0]['score'] if top_chunks else 0.0
        avg_top_score = (sum(r['score'] for r in top_chunks[:3]) / min(3, len(top_chunks))) if top_chunks else 0.0

        return {
            "retrieved_chunks": top_chunks,
            "total_retrieved": len(top_chunks),
            "filtered_out_count": filtered_out_count,
            "top_score": top_score,
            "avg_top_score": round(avg_top_score, 4),
            "sufficient_context": len(top_chunks) > 0 and top_score >= self.min_threshold
        }
