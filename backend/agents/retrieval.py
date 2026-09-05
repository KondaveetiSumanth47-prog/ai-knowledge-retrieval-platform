from typing import List, Dict, Any
from ingestion.vector_store import VectorStoreManager

class RetrievalAgent:
    """
    2. Retrieval Agent:
    - Formulates similarity query
    - Queries ChromaDB vector store
    - Performs score filtering and re-ranking
    """
    def __init__(self, vector_store: VectorStoreManager = None):
        self.vector_store = vector_store or VectorStoreManager()

    def process(self, query_understanding: Dict[str, Any], top_k: int = 5) -> Dict[str, Any]:
        query_text = query_understanding['cleaned_query']
        domain_filter = query_understanding.get('target_domain', 'all')

        raw_results = self.vector_store.similarity_search(
            query_text=query_text,
            top_k=top_k,
            domain_filter=domain_filter
        )

        # Score filtering & re-ranking
        # Re-rank based on keyword match overlap and similarity score
        re_ranked = []
        keywords = set(k.lower() for k in query_understanding.get('keywords', []))

        for item in raw_results:
            content_lower = item['content'].lower()
            overlap_count = sum(1 for kw in keywords if kw in content_lower)
            boost = min(0.15, overlap_count * 0.03)
            final_score = round(min(1.0, item['score'] + boost), 4)

            item_copy = dict(item)
            item_copy['score'] = final_score
            re_ranked.append(item_copy)

        re_ranked.sort(key=lambda x: x['score'], reverse=True)

        avg_top_score = (sum(r['score'] for r in re_ranked[:3]) / min(3, len(re_ranked))) if re_ranked else 0.0

        return {
            "retrieved_chunks": re_ranked,
            "total_retrieved": len(re_ranked),
            "top_score": re_ranked[0]['score'] if re_ranked else 0.0,
            "avg_top_score": round(avg_top_score, 4),
            "sufficient_context": len(re_ranked) > 0 and re_ranked[0]['score'] >= 0.35
        }
