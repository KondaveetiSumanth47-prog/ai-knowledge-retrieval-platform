import os
import werkzeug
from flask import Flask, request, jsonify
try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

from config import UPLOADS_DIR, SAMPLE_DOCS_DIR
from database import (
    init_db, get_all_documents, get_document_by_id, 
    get_chunks_for_document, delete_document, get_latest_eval_logs
)
from ingestion.pipeline import IngestionPipeline
from ingestion.vector_store import VectorStoreManager
from agents.orchestrator import MultiAgentOrchestrator
from eval.evaluate import RAGEvaluator

app = Flask(__name__)
if HAS_CORS:
    CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Initialize Database
init_db()

# Initialize core services
ingestion_pipeline = IngestionPipeline()
vector_store = VectorStoreManager()
orchestrator = MultiAgentOrchestrator(vector_store=vector_store)
evaluator = RAGEvaluator(vector_store=vector_store)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "RAG Multi-Agent Backend Server"})

@app.route('/api/ingest', methods=['POST'])
def ingest_document():
    """
    Ingests uploaded PDF, DOCX, TXT, or CSV document.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded in request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    domain = request.form.get('domain', 'General')
    chunk_size = request.form.get('chunk_size', type=int)
    chunk_overlap = request.form.get('chunk_overlap', type=int)

    filename = werkzeug.utils.secure_filename(file.filename)
    file_path = os.path.join(UPLOADS_DIR, filename)
    file.save(file_path)

    try:
        res = ingestion_pipeline.process_file(
            file_path=file_path,
            filename=file.filename,
            domain=domain,
            custom_chunk_size=chunk_size,
            custom_chunk_overlap=chunk_overlap
        )
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": f"Ingestion failed: {str(e)}"}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """Returns all ingested documents from SQLite metadata DB."""
    docs = get_all_documents()
    return jsonify({"documents": docs, "total": len(docs)})

@app.route('/api/documents/<doc_id>', methods=['GET'])
def get_document(doc_id):
    doc = get_document_by_id(doc_id)
    if not doc:
        return jsonify({"error": "Document not found."}), 404
    chunks = get_chunks_for_document(doc_id)
    return jsonify({"document": doc, "chunks": chunks})

@app.route('/api/documents/<doc_id>', methods=['DELETE'])
def remove_document(doc_id):
    doc = get_document_by_id(doc_id)
    if not doc:
        return jsonify({"error": "Document not found."}), 404

    # Delete from ChromaDB vector store
    vector_store.delete_document_chunks(doc_id)
    # Delete from SQLite
    delete_document(doc_id)

    if os.path.exists(doc.get('filepath', '')):
        try:
            os.remove(doc['filepath'])
        except Exception:
            pass

    return jsonify({"message": f"Document {doc_id} successfully deleted."}), 200

@app.route('/api/query', methods=['POST'])
def query_rag():
    """
    Executes query resolution via Multi-Agent Orchestrator.
    """
    data = request.get_json() or {}
    query_text = data.get('query', '').strip()
    domain_filter = data.get('domain', 'all')
    session_id = data.get('session_id')

    if not query_text:
        return jsonify({"error": "Query text is required."}), 400

    result = orchestrator.process_query(
        query_text=query_text,
        domain_filter=domain_filter,
        session_id=session_id
    )

    return jsonify(result), 200

@app.route('/api/eval/run', methods=['POST'])
def run_evaluation():
    """Executes retrieval accuracy benchmark across domains."""
    try:
        eval_summary = evaluator.run_benchmark()
        return jsonify(eval_summary), 200
    except Exception as e:
        return jsonify({"error": f"Evaluation benchmark failed: {str(e)}"}), 500

@app.route('/api/eval/results', methods=['GET'])
def get_eval_results():
    """Returns recent evaluation logs."""
    logs = get_latest_eval_logs()
    return jsonify({"eval_logs": logs})

@app.route('/api/seed_sample_docs', methods=['POST'])
def seed_sample_docs():
    """
    Automatically ingests the 8 pre-packaged sample documents across Domain 1 (IT Cloud) & Domain 2 (Healthcare).
    """
    sample_files = [
        # Domain 1: Cloud & DevOps
        (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "cloud_architecture_guide.pdf"), "cloud_architecture_guide.pdf", "Cloud Infrastructure & DevOps"),
        (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "devops_deployment_handbook.docx"), "devops_deployment_handbook.docx", "Cloud Infrastructure & DevOps"),
        (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "api_security_spec.txt"), "api_security_spec.txt", "Cloud Infrastructure & DevOps"),
        (os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "infrastructure_cost_analysis.csv"), "infrastructure_cost_analysis.csv", "Cloud Infrastructure & DevOps"),
        
        # Domain 2: Healthcare & Medical
        (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "patient_triage_protocol.pdf"), "patient_triage_protocol.pdf", "Healthcare & Medical Protocols"),
        (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "clinical_trial_guidelines.docx"), "clinical_trial_guidelines.docx", "Healthcare & Medical Protocols"),
        (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "hospital_discharge_policy.txt"), "hospital_discharge_policy.txt", "Healthcare & Medical Protocols"),
        (os.path.join(SAMPLE_DOCS_DIR, "domain2_healthcare", "drug_inventory_registry.csv"), "drug_inventory_registry.csv", "Healthcare & Medical Protocols"),
    ]

    results = []
    for path, name, domain in sample_files:
        if os.path.exists(path):
            try:
                res = ingestion_pipeline.process_file(file_path=path, filename=name, domain=domain)
                results.append({"filename": name, "domain": domain, "chunks": res['chunks_count']})
            except Exception as e:
                results.append({"filename": name, "error": str(e)})

    return jsonify({
        "message": f"Successfully ingested {len(results)} sample documents.",
        "details": results
    }), 200

@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Returns active sub-agents status and telemetry."""
    return jsonify({
        "agents": [
            {"id": "query_understanding", "name": "1. Query Understanding Agent", "status": "active", "role": "Classifies intent (Factual, Procedural, Comparative, Ambiguous) & routes resolution path"},
            {"id": "retrieval", "name": "2. Retrieval Agent", "status": "active", "role": "Semantic ChromaDB search, hybrid relevance ranking & low-confidence filtering"},
            {"id": "clarification", "name": "3. Clarification Agent", "status": "active", "role": "Evaluates confidence thresholds & prompts follow-up questions"},
            {"id": "memory", "name": "4. Conversation Memory Agent", "status": "active", "role": "Stores & retrieves multi-turn dialogue history state"},
            {"id": "response_generator", "name": "5. Response Generation Agent", "status": "active", "role": "Synthesizes grounded answers with citations & confidence indicators"}
        ],
        "orchestrator_status": "operational"
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting RAG Multi-Agent Flask Server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
