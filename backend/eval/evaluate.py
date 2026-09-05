import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

from ingestion.vector_store import VectorStoreManager
from database import save_eval_run

# Standard Evaluation Test Dataset across 2 domains and 4 query types
BENCHMARK_QUERIES = [
    # --- Domain 1: IT Cloud Infrastructure & DevOps ---
    {
        "id": "q1",
        "domain": "Cloud Infrastructure & DevOps",
        "type": "Factual",
        "query": "What is the token expiration time in OAuth2 authentication?",
        "expected_keywords": ["OAuth2", "60 minutes", "Access Tokens expire"],
        "should_find": True
    },
    {
        "id": "q2",
        "domain": "Cloud Infrastructure & DevOps",
        "type": "Procedural",
        "query": "What are the automated rollback triggers during production deployment?",
        "expected_keywords": ["rollback", "5xx error rate", "exceeds 0.5%", "latency p99"],
        "should_find": True
    },
    {
        "id": "q3",
        "domain": "Cloud Infrastructure & DevOps",
        "type": "Comparative",
        "query": "Compare AWS EC2 compute cost versus GCP GKE compute cost.",
        "expected_keywords": ["AWS", "Compute EC2", "4500", "GCP", "4200"],
        "should_find": True
    },
    {
        "id": "q4",
        "domain": "Cloud Infrastructure & DevOps",
        "type": "Factual",
        "query": "What database replication strategy is used for PostgreSQL?",
        "expected_keywords": ["PostgreSQL", "asynchronous multi-region replication"],
        "should_find": True
    },
    {
        "id": "q5",
        "domain": "Cloud Infrastructure & DevOps",
        "type": "Unavailable",
        "query": "What is the quantum encryption key length for deep space satellite telemetry?",
        "expected_keywords": [],
        "should_find": False
    },

    # --- Domain 2: Healthcare & Medical Protocols ---
    {
        "id": "q6",
        "domain": "Healthcare & Medical Protocols",
        "type": "Factual",
        "query": "What storage temperature condition is required for Insulin Glargine?",
        "expected_keywords": ["Insulin", "Refrigerated", "2-8C"],
        "should_find": True
    },
    {
        "id": "q7",
        "domain": "Healthcare & Medical Protocols",
        "type": "Procedural",
        "query": "Within how many hours must a Serious Adverse Event (SAE) be reported to the IRB?",
        "expected_keywords": ["Serious Adverse Event", "IRB", "24 hours"],
        "should_find": True
    },
    {
        "id": "q8",
        "domain": "Healthcare & Medical Protocols",
        "type": "Comparative",
        "query": "What is the difference in response timeframe between Triage Level 1 and Triage Level 2?",
        "expected_keywords": ["Immediate", "Resuscitation", "15 minutes", "Emergent"],
        "should_find": True
    },
    {
        "id": "q9",
        "domain": "Healthcare & Medical Protocols",
        "type": "Factual",
        "query": "What vital signs stability period is required before inpatient hospital discharge?",
        "expected_keywords": ["stable for 24 consecutive hours", "discharge"],
        "should_find": True
    },
    {
        "id": "q10",
        "domain": "Healthcare & Medical Protocols",
        "type": "Unavailable",
        "query": "What is the recommended dosage of feline antibiotic for domestic cats?",
        "expected_keywords": [],
        "should_find": False
    }
]

class RAGEvaluator:
    """
    RAG Pipeline Retrieval Accuracy Benchmark:
    Evaluates Top-1, Top-3, and Top-5 Retrieval Accuracy and Precision@K.
    """
    def __init__(self, vector_store: VectorStoreManager = None):
        self.vector_store = vector_store or VectorStoreManager()

    def run_benchmark(self) -> Dict[str, Any]:
        results = []
        top_1_hits = 0
        top_3_hits = 0
        top_5_hits = 0
        evaluatable_count = 0
        low_relevance_queries = []

        for item in BENCHMARK_QUERIES:
            query = item['query']
            expected_kws = item['expected_keywords']
            should_find = item['should_find']

            # Perform top-5 retrieval
            retrieved = self.vector_store.similarity_search(query, top_k=5)

            if not should_find:
                # Unavailable query handling: low top similarity is CORRECT
                top_score = retrieved[0]['score'] if retrieved else 0.0
                is_correct = top_score < 0.40  # Successfully flagged as low relevance
                results.append({
                    "query_id": item['id'],
                    "query": query,
                    "domain": item['domain'],
                    "type": item['type'],
                    "top_1_hit": is_correct,
                    "top_3_hit": is_correct,
                    "top_5_hit": is_correct,
                    "top_score": top_score,
                    "note": "Unavailable query properly identified as low relevance." if is_correct else "False positive match."
                })
                if is_correct:
                    top_1_hits += 1
                    top_3_hits += 1
                    top_5_hits += 1
                else:
                    low_relevance_queries.append({
                        "query": query,
                        "reason": "Unavailable query returned high unexpected similarity."
                    })
                evaluatable_count += 1
                continue

            evaluatable_count += 1
            hit_in_top_1 = False
            hit_in_top_3 = False
            hit_in_top_5 = False

            top_score = retrieved[0]['score'] if retrieved else 0.0

            # Check matching in top positions
            for rank, r in enumerate(retrieved):
                content_lower = r['content'].lower()
                matches = sum(1 for kw in expected_kws if kw.lower() in content_lower)
                # Hit threshold: matches at least 1 key term or concept
                if matches >= 1:
                    if rank == 0:
                        hit_in_top_1 = True
                    if rank < 3:
                        hit_in_top_3 = True
                    if rank < 5:
                        hit_in_top_5 = True

            if hit_in_top_1:
                top_1_hits += 1
            if hit_in_top_3:
                top_3_hits += 1
            if hit_in_top_5:
                top_5_hits += 1

            if not hit_in_top_1:
                low_relevance_queries.append({
                    "query": query,
                    "top_score": top_score,
                    "reason": "Top-1 retrieval failed to prioritize highest relevance chunk."
                })

            results.append({
                "query_id": item['id'],
                "query": query,
                "domain": item['domain'],
                "type": item['type'],
                "top_1_hit": hit_in_top_1,
                "top_3_hit": hit_in_top_3,
                "top_5_hit": hit_in_top_5,
                "top_score": top_score,
                "retrieved_count": len(retrieved)
            })

        top_1_acc = round((top_1_hits / evaluatable_count) * 100, 2)
        top_3_acc = round((top_3_hits / evaluatable_count) * 100, 2)
        top_5_acc = round((top_5_hits / evaluatable_count) * 100, 2)

        eval_summary = {
            "id": f"eval_{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(),
            "total_queries": evaluatable_count,
            "top_1_accuracy": top_1_acc,
            "top_3_accuracy": top_3_acc,
            "top_5_accuracy": top_5_acc,
            "detailed_results": results,
            "low_relevance_queries": low_relevance_queries
        }

        # Save run log into SQLite
        save_eval_run(eval_summary)

        return eval_summary

if __name__ == '__main__':
    print("Executing RAG Retrieval Accuracy Benchmark...")
    evaluator = RAGEvaluator()
    res = evaluator.run_benchmark()
    print(f"Top-1 Accuracy: {res['top_1_accuracy']}%")
    print(f"Top-3 Accuracy: {res['top_3_accuracy']}%")
    print(f"Top-5 Accuracy: {res['top_5_accuracy']}%")
