import sys
import json
from agents.orchestrator import MultiAgentOrchestrator
from eval.evaluate import RAGEvaluator
from ingestion.vector_store import VectorStoreManager

# Set stdout encoding for Windows console compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("================================================================================")
print("       AI-BASED KNOWLEDGE RETRIEVAL PLATFORM - MILESTONE 2 DEMONSTRATION")
print("================================================================ magic\n")

vector_store = VectorStoreManager()
orchestrator = MultiAgentOrchestrator(vector_store=vector_store)
evaluator = RAGEvaluator(vector_store=vector_store)

def print_separator(title):
    print(f"\n--------------------------------------------------------------------------------")
    print(f" DEMO CASE: {title}")
    print(f"--------------------------------------------------------------------------------")

# Demo 1: Factual Query
print_separator("Query Understanding Agent -> Factual Direct Resolution Path")
q1 = "What is the token expiration time in OAuth2 authentication?"
print(f"USER QUERY: \"{q1}\"\n")
res1 = orchestrator.process_query(q1, domain_filter="all")

print(">>> LIVE MULTI-AGENT EXECUTION TRACE & LATENCY TELEMETRY:")
for step in res1['agent_trace']:
    print(f"  [{step['timestamp']}] {step['agent_name']} (Latency: {step['latency_ms']} ms)")
    print(f"     Action  : {step['action']}")
    print(f"     Details : {step['details']}\n")

print(f">>> FINAL ANSWER (Confidence: {res1['confidence_level']} - {int(res1['confidence_score']*100)}%):")
print(f"{res1['answer']}\n")


# Demo 2: Procedural Workflow Query
print_separator("Query Understanding Agent -> Procedural Workflow Resolution Path")
q2 = "What are the automated rollback triggers during production deployment?"
print(f"USER QUERY: \"{q2}\"\n")
res2 = orchestrator.process_query(q2, domain_filter="all")

print(">>> LIVE MULTI-AGENT EXECUTION TRACE & LATENCY TELEMETRY:")
for step in res2['agent_trace']:
    print(f"  [{step['timestamp']}] {step['agent_name']} (Latency: {step['latency_ms']} ms)")
    print(f"     Action  : {step['action']}")
    print(f"     Details : {step['details']}\n")

print(f">>> FINAL WORKFLOW ANSWER (Confidence: {res2['confidence_level']} - {int(res2['confidence_score']*100)}%):")
print(f"{res2['answer']}\n")


# Demo 3: Comparative Analysis Query
print_separator("Query Understanding Agent -> Comparative Matrix Resolution Path")
q3 = "Compare AWS EC2 compute cost versus GCP GKE compute cost."
print(f"USER QUERY: \"{q3}\"\n")
res3 = orchestrator.process_query(q3, domain_filter="all")

print(f">>> CLASSIFICATION: {res3['intent']} | RESOLUTION PATH: {res3['resolution_path']}")
print(f">>> FINAL COMPARATIVE MATRIX (Confidence: {res3['confidence_level']} - {int(res3['confidence_score']*100)}%):")
print(f"{res3['answer']}\n")


# Demo 4: RAG Retrieval Accuracy Benchmark
print_separator("RAG Retrieval Accuracy Benchmark Suite")
print("Executing automated 10-query benchmark across Cloud Infrastructure & Healthcare...")
eval_res = evaluator.run_benchmark()

print("\n================ BENCHMARK RESULTS ================")
print(f"Total Benchmark Queries Evaluated : {eval_res['total_queries']}")
print(f"Top-1 Retrieval Accuracy          : {eval_res['top_1_accuracy']}%")
print(f"Top-3 Retrieval Accuracy          : {eval_res['top_3_accuracy']}%")
print(f"Top-5 Retrieval Accuracy          : {eval_res['top_5_accuracy']}%")
print("====================================================")
