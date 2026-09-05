import os
import sys
import json
from ingestion.extractor import DocumentExtractor
from ingestion.cleaner import TextCleaner
from ingestion.chunker import DocumentChunker
from ingestion.embedder import EmbeddingGenerator
from ingestion.vector_store import VectorStoreManager
from agents.orchestrator import MultiAgentOrchestrator
from database import init_db, save_document, save_chunks, get_document_by_id
from config import SAMPLE_DOCS_DIR

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("================================================================================")
print("     STEP-BY-STEP LIVE FILE INGESTION & MULTI-AGENT RESOLUTION DEMO")
print("================================================================================\n")

init_db()

# Target system file to demonstrate
target_file_path = os.path.join(SAMPLE_DOCS_DIR, "domain1_it_cloud", "api_security_spec.txt")
filename = "api_security_spec.txt"
domain = "Cloud Infrastructure & DevOps"

print(f"TARGET SYSTEM FILE: {target_file_path}")
print(f"FILE FORMAT: TXT | DOMAIN: {domain}\n")

# ------------------------------------------------------------------------------
# STEP 1: Text Extraction
# ------------------------------------------------------------------------------
print("================================================================================")
print(" STEP 1: TEXT EXTRACTION (Multi-Format Document Parsing)")
print("================================================================================")
raw_text = DocumentExtractor.extract(target_file_path, file_type="txt")
print(f"[EXTRACTED RAW TEXT - {len(raw_text)} characters]:\n")
print(raw_text[:350] + "...\n")

# ------------------------------------------------------------------------------
# STEP 2: Text Cleaning & Normalization
# ------------------------------------------------------------------------------
print("================================================================================")
print(" STEP 2: TEXT CLEANING & NORMALIZATION")
print("================================================================================")
cleaned_text = TextCleaner.clean(raw_text)
print(f"[NORMALIZED CLEAN TEXT - {len(cleaned_text)} characters]:\n")
print(cleaned_text[:350] + "...\n")

# ------------------------------------------------------------------------------
# STEP 3: LangChain Text Chunking
# ------------------------------------------------------------------------------
print("================================================================================")
print(" STEP 3: LANGCHAIN TEXT CHUNKING (Size: 300 chars, Overlap: 30 chars)")
print("================================================================================")
doc_id = "demo_doc_api_spec"
chunker = DocumentChunker(chunk_size=300, chunk_overlap=30)
chunks = chunker.chunk_text(cleaned_text, document_id=doc_id)

print(f"Total Chunks Created: {len(chunks)}\n")
for idx, c in enumerate(chunks):
    print(f" • Chunk #{c['chunk_index'] + 1} [Chars {c['start_char']} - {c['end_char']}, ~{c['token_estimate']} tokens]:")
    print(f"   \"{c['content'].strip()}\"\n")

# ------------------------------------------------------------------------------
# STEP 4: Embedding Generation & ChromaDB Vector Store Indexing
# ------------------------------------------------------------------------------
print("================================================================================")
print(" STEP 4: EMBEDDING GENERATION & CHROMADB VECTOR STORE INDEXING")
print("================================================================================")
embedder = EmbeddingGenerator()
chunk_contents = [c['content'] for c in chunks]
embeddings = embedder.generate_embeddings(chunk_contents)

print(f"Generated {len(embeddings)} dense vector embeddings (384 dimensions each).")

vector_store = VectorStoreManager()
doc_metadata = {
    "id": doc_id,
    "filename": filename,
    "file_type": "txt",
    "domain": domain,
    "file_size": os.path.getsize(target_file_path),
    "chunk_count": len(chunks),
    "raw_char_count": len(cleaned_text),
    "upload_time": "2026-09-05T10:45:00",
    "filepath": target_file_path
}

save_document(doc_metadata)
save_chunks(chunks)
vector_store.add_chunks(chunks, embeddings, doc_metadata)
print(f"Indexed document metadata into SQLite database & vector vectors into ChromaDB.\n")

# ------------------------------------------------------------------------------
# STEP 5: Multi-Agent Query Resolution Pipeline Execution
# ------------------------------------------------------------------------------
print("================================================================================")
print(" STEP 5: MULTI-AGENT QUERY RESOLUTION ON INGESTED FILE")
print("================================================================================")
orchestrator = MultiAgentOrchestrator(vector_store=vector_store)
test_query = "What is the token expiration time in OAuth2 authentication?"
print(f"USER QUERY: \"{test_query}\"\n")

result = orchestrator.process_query(test_query, domain_filter="all")

print(">>> AGENT EXECUTION TRACE STREAM:")
for step in result['agent_trace']:
    print(f"  [{step['timestamp']}] {step['agent_name']} (Latency: {step['latency_ms']} ms)")
    print(f"     Action  : {step['action']}")
    print(f"     Details : {step['details']}\n")

print(f">>> GROUNDED ANSWER OUTPUT (Confidence: {result['confidence_level']} - {int(result['confidence_score']*100)}%):")
print(f"{result['answer']}\n")

print(">>> RETRIEVED SOURCE CITATIONS:")
for citation in result['citations']:
    print(f"  • Source: {citation['filename']} | Chunk #{citation['chunk_index']} | Hybrid Score: {int(citation['score']*100)}%")
print("\n================================================================================\n")
