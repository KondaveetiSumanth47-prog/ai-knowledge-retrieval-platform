import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from chunking import split_text
from document_reader import read_document
from embeddings import create_embeddings
from orchestrator import Orchestrator
from vector_store import store_chunks

app = Flask(__name__)
CORS(app)

orchestrator = Orchestrator()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".csv"}


@app.route("/")
def home():
    return "AI Knowledge Retrieval Platform Backend is Working!"


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}

    question = (data.get("question") or "").strip()
    session_id = data.get("session_id") or data.get("conversation_id") or "default-session"
    original_query = (data.get("original_query") or "").strip()
    clarification_response = (data.get("clarification_response") or "").strip()

    raw_top_k = data.get("top_k", 3)
    try:
        selected_top_k = int(raw_top_k)
    except (TypeError, ValueError):
        selected_top_k = 3
    if selected_top_k not in {1, 3, 5}:
        selected_top_k = 3

    if not question and not original_query:
        return jsonify({"error": "Question is required."}), 400

    effective_question = question or original_query

    try:
        response = orchestrator.process_query(
            effective_question,
            session_id=session_id,
            original_query=original_query or None,
            clarification_response=clarification_response or None,
            top_k=selected_top_k,
        )
    except Exception:
        response = {
            "question": effective_question,
            "query": effective_question,
            "query_type": "ambiguous",
            "classification_confidence": 0.0,
            "answer": "I could not process your question because the request failed. Please try again.",
            "sources": [],
            "confidence": {"label": "Low", "score": 0.0},
            "retrieved_chunks": [],
            "status": "processing_error",
            "routing": "clarification",
        }

    status_code = 200
    if response.get("status") in {"invalid_query", "processing_error", "classification_failed"}:
        status_code = 400

    return jsonify(response), status_code


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if file is None or file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file format. Supported types: PDF, DOCX, TXT, CSV."}), 400

    safe_name = os.path.basename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
    file.save(file_path)

    try:
        text = read_document(file_path)
    except Exception:
        return jsonify({"error": "The uploaded file could not be read. Please verify the file is valid."}), 400

    if not text or not text.strip():
        return jsonify({"error": "The uploaded document is empty or contains no readable text."}), 400

    chunks = split_text(text, chunk_size=500, chunk_overlap=50)
    if not chunks:
        return jsonify({"error": "The document did not produce any valid text chunks for indexing."}), 400

    embeddings = create_embeddings(chunks)
    store_result = store_chunks(chunks, embeddings, source=safe_name, file_type=extension.lstrip("."))

    return jsonify({
        "message": "Document uploaded and stored successfully.",
        "filename": safe_name,
        "number_of_chunks": len(chunks),
        "stored": store_result.get("stored", 0),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)