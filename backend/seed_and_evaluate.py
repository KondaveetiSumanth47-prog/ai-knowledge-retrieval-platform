import os
from database import init_db
from ingestion.pipeline import IngestionPipeline
from eval.evaluate import RAGEvaluator
from config import SAMPLE_DOCS_DIR

print("Initializing database...")
init_db()

pipeline = IngestionPipeline()

sample_files = [
    # Domain 1: Cloud Infrastructure & DevOps
    (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "cloud_architecture_guide.pdf"), "cloud_architecture_guide.pdf", "Cloud Infrastructure & DevOps"),
    (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "devops_deployment_handbook.docx"), "devops_deployment_handbook.docx", "Cloud Infrastructure & DevOps"),
    (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "api_security_spec.txt"), "api_security_spec.txt", "Cloud Infrastructure & DevOps"),
    (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "infrastructure_cost_analysis.csv"), "infrastructure_cost_analysis.csv", "Cloud Infrastructure & DevOps"),
    
    # Domain 2: Healthcare & Medical Protocols
    (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "patient_triage_protocol.pdf"), "patient_triage_protocol.pdf", "Healthcare & Medical Protocols"),
    (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "clinical_trial_guidelines.docx"), "clinical_trial_guidelines.docx", "Healthcare & Medical Protocols"),
    (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "hospital_discharge_policy.txt"), "hospital_discharge_policy.txt", "Healthcare & Medical Protocols"),
    (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "drug_inventory_registry.csv"), "drug_inventory_registry.csv", "Healthcare & Medical Protocols"),
]

print("\nIngesting sample documents across Domain 1 & Domain 2...")
for path, name, domain in sample_files:
    if os.path.exists(path):
        res = pipeline.process_file(file_path=path, filename=name, domain=domain)
        print(f" -> Ingested '{name}' [{domain}] - Chunks: {res['chunks_count']}")
    else:
        print(f" ERROR: Missing file {path}")

print("\nRunning RAG Retrieval Accuracy Benchmark Suite...")
evaluator = RAGEvaluator()
eval_res = evaluator.run_benchmark()

print("\n================ BENCHMARK RESULTS ================")
print(f"Total Evaluated Queries: {eval_res['total_queries']}")
print(f"Top-1 Retrieval Accuracy: {eval_res['top_1_accuracy']}%")
print(f"Top-3 Retrieval Accuracy: {eval_res['top_3_accuracy']}%")
print(f"Top-5 Retrieval Accuracy: {eval_res['top_5_accuracy']}%")
print("====================================================\n")
