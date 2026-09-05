import sys
import json
from agents.orchestrator import MultiAgentOrchestrator
from eval.evaluate import RAGEvaluator
from ingestion.vector_store import VectorStoreManager
from database import get_all_documents

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("================================================================================")
print("             RAG KNOWLEDGE RETRIEVAL PLATFORM - SYSTEM DEMONSTRATION")
print("================================================================================\n")

# Step 1: Knowledge Base Documents Status
docs = get_all_documents()
print("1. INGESTED KNOWLEDGE BASE DOCUMENTS (PDF, DOCX, TXT, CSV):")
print("--------------------------------------------------------------------------------")
for d in docs:
    print(f" • File: {d['filename']:<35} | Type: {d['file_type'].upper():<4} | Domain: {d['domain']:<32} | Chunks: {d['chunk_count']}")

vector_store = VectorStoreManager()
orchestrator = MultiAgentOrchestrator(vector_store=vector_store)

# Step 2: Factual Query Demonstration
print("\n\n2. DEMO: FACTUAL QUERY RESOLUTION PATH")
print("--------------------------------------------------------------------------------")
q1 = "What is the token expiration time in OAuth2 authentication?"
print(f"User Query: \"{q1}\"\n")
r1 = orchestrator.process_query(q1, domain_filter="all")

print(f"Classification     : {r1['intent']} Query")
print(f"Resolution Path    : {r1['resolution_path']}")
print(f"Confidence Level   : {r1['confidence_level']} ({int(r1['confidence_score']*100)}%)")
print(f"Pipeline Latency   : {r1['total_latency_ms']} ms")
print(f"Noise Chunks Filter: {r1['filtered_out_count']} low-confidence chunks removed\n")
print(f"Answer Output:\n{r1['answer']}\n")
print("Source Citations:")
for c in r1['citations']:
    print(f" - [{c['filename']}] Score: {int(c['score']*100)}% | Domain: {c['domain']}")


# Step 3: Procedural Workflow Query Demonstration
print("\n\n3. DEMO: PROCEDURAL WORKFLOW RESOLUTION PATH")
print("--------------------------------------------------------------------------------")
q2 = "What are the automated rollback triggers during production deployment?"
print(f"User Query: \"{q2}\"\n")
r2 = orchestrator.process_query(q2, domain_filter="all")

print(f"Classification     : {r2['intent']} Query")
print(f"Resolution Path    : {r2['resolution_path']}")
print(f"Confidence Level   : {r2['confidence_level']} ({int(r2['confidence_score']*100)}%)")
print(f"Pipeline Latency   : {r2['total_latency_ms']} ms\n")
print(f"Workflow Answer Output:\n{r2['answer']}\n")


# Step 4: Comparative Matrix Query Demonstration
print("\n\n4. DEMO: COMPARATIVE ANALYSIS RESOLUTION PATH")
print("--------------------------------------------------------------------------------")
q3 = "Compare AWS EC2 compute cost versus GCP GKE compute cost."
print(f"User Query: \"{q3}\"\n")
r3 = orchestrator.process_query(q3, domain_filter="all")

print(f"Classification     : {r3['intent']} Query")
print(f"Resolution Path    : {r3['resolution_path']}")
print(f"Confidence Level   : {r3['confidence_level']} ({int(r3['confidence_score']*100)}%)\n")
print(f"Comparative Matrix Output:\n{r3['answer']}\n")

# Step 5: Accuracy Benchmark Summary
print("\n5. RETRIEVAL ACCURACY BENCHMARK SUMMARY")
print("--------------------------------------------------------------------------------")
evaluator = RAGEvaluator(vector_store=vector_store)
eval_res = evaluator.run_benchmark()
print(f"Evaluated Benchmark Queries : {eval_res['total_queries']}")
print(f"Top-1 Retrieval Accuracy    : {eval_res['top_1_accuracy']}%")
print(f"Top-3 Retrieval Accuracy    : {eval_res['top_3_accuracy']}%")
print(f"Top-5 Retrieval Accuracy    : {eval_res['top_5_accuracy']}%")
print("================================================================================\n")
